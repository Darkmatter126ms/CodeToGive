import os
import stripe
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client
from database_helpers import (
    create_donation_with_updates, 
    create_subscription_with_updates,
    update_campaign_progress,
    update_donor_subscription_status,
    get_campaign_progress,
    get_donor_summary,
    update_subscription_status
)

# Load environment variables
load_dotenv()

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Set up Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create Flask app and blueprint
app = Flask(__name__)
CORS(app)
payment_blueprint = Blueprint("payment", __name__)

# Subscription plans configuration
SUBSCRIPTION_PLANS = {
    "supporter": {
        "name": "Supporter",
        "price": 6000,  # $60.00 in cents
        "currency": "usd",
        "interval": "month"
    },
    "advocate": {
        "name": "Advocate", 
        "price": 12000,  # $120.00 in cents
        "currency": "usd",
        "interval": "month"
    },
    "champion": {
        "name": "Champion",
        "price": 50000,  # $500.00 in cents
        "currency": "usd", 
        "interval": "month"
    }
}

# Health Check
@payment_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "payment service alive"}), 200

# Create payment intent (one-time donation)
@payment_blueprint.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    amount = data.get('amount')  # Amount in cents
    currency = data.get('currency', 'usd')
    donor_email = data.get('email')
    donor_name = data.get('name', '')
    campaign_id = data.get('campaign_id')
    
    # Create or get donor
    donor = None
    if donor_email:
        # Check if donor exists
        existing_donor = supabase.table("Donors").select("*").eq("email", donor_email).execute()
        if existing_donor.data:
            donor = existing_donor.data[0]
        else:
            # Create new donor
            new_donor = supabase.table("Donors").insert({
                "name": donor_name,
                "email": donor_email
            }).execute()
            donor = new_donor.data[0] if new_donor.data else None
    
    # Create payment intent
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        metadata={
            'type': 'one_time_donation',
            'donor_email': donor_email,
            'donor_id': str(donor['donor_id']) if donor else '',
            'campaign_id': str(campaign_id) if campaign_id else ''
        }
    )
    
    # Save pending donation (will be confirmed by webhook)
    if donor and campaign_id:
        donation_data = {
            "donor_id": donor['donor_id'],
            "campaign_id": campaign_id,
            "amount": amount / 100,  # Convert cents to dollars
            "stripe_payment_intent_id": intent['id'],
            "payment_type": "one_time",
            "payment": "pending"  # Will be updated to "completed" by webhook
        }
        create_donation_with_updates(donation_data)
    
    return jsonify({
        'client_secret': intent['client_secret'],
        'payment_intent_id': intent['id'],
        'donor_id': donor['donor_id'] if donor else None
    }), 200

# Create subscription
@payment_blueprint.route('/create-subscription', methods=['POST'])
def create_subscription():
    data = request.json
    plan_id = data.get('plan_id')  # supporter, advocate, champion
    customer_email = data.get('email')
    customer_name = data.get('name', '')
    
    if plan_id not in SUBSCRIPTION_PLANS:
        return jsonify({'error': 'Invalid plan'}), 400
        
    plan = SUBSCRIPTION_PLANS[plan_id]
    
    # Create or get Stripe customer (no donor table involvement)
    customers = stripe.Customer.list(email=customer_email, limit=1)
    if customers.data:
        customer = customers.data[0]
    else:
        customer = stripe.Customer.create(
            email=customer_email,
            name=customer_name
        )
    
    # Create price object (if doesn't exist)
    price = stripe.Price.create(
        unit_amount=plan['price'],
        currency=plan['currency'],
        recurring={'interval': plan['interval']},
        product_data={
            'name': f"REACH {plan['name']} Subscription"
        }
    )
    
    # Create subscription
    # Option 1: Incomplete subscription (requires frontend payment confirmation)
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{'price': price.id}],
        payment_behavior='default_incomplete',  # Customer will provide payment method later
        expand=['latest_invoice.payment_intent'],
        metadata={
            'plan_id': plan_id,
            'plan_name': plan['name'],
            'customer_email': customer_email,
            'customer_name': customer_name
        }
    )
    
    # Alternative Option 2: If you want immediate subscription without client_secret
    # (Uncomment this and comment above if you don't want payment confirmation step)
    # subscription = stripe.Subscription.create(
    #     customer=customer.id,
    #     items=[{'price': price.id}],
    #     payment_behavior='allow_incomplete',  # Creates active subscription immediately
    #     metadata={
    #         'plan_id': plan_id,
    #         'plan_name': plan['name'],
    #         'customer_email': customer_email,
    #         'customer_name': customer_name
    #     }
    # )
    
    # Save subscription to database (without donor relationship)
    subscription_data = {
        "plan_id": plan_id,
        "stripe_subscription_id": subscription.id,
        "status": subscription.status,
        "current_period_start": subscription.get('current_period_start'),
        "current_period_end": subscription.get('current_period_end'),
        "customer_email": customer_email,
        "customer_name": customer_name
    }
    
    try:
        supabase.table("DonorSubscriptions").insert(subscription_data).execute()
    except Exception as e:
        print(f"Warning: Could not save subscription to database: {e}")
    
    # Safely get client_secret if available
    client_secret = None
    if hasattr(subscription, 'latest_invoice') and subscription.latest_invoice:
        if hasattr(subscription.latest_invoice, 'payment_intent') and subscription.latest_invoice.payment_intent:
            client_secret = subscription.latest_invoice.payment_intent.client_secret
    
    return jsonify({
        'subscription_id': subscription.id,
        'client_secret': client_secret,
        'customer_id': customer.id,
        'customer_email': customer_email,
        'status': subscription.status
    }), 200

# Get subscription status
@payment_blueprint.route('/subscription-status/<subscription_id>', methods=['GET'])
def get_subscription_status(subscription_id):
    subscription = stripe.Subscription.retrieve(subscription_id)
    # Safely get amount from subscription items
    amount = None
    if hasattr(subscription, 'items') and subscription.items:
        # subscription.items is a StripeList object, access the data properly
        try:
            items_data = subscription.items.data if hasattr(subscription.items, 'data') else list(subscription.items)
            if items_data and len(items_data) > 0:
                first_item = items_data[0]
                if hasattr(first_item, 'price') and hasattr(first_item.price, 'unit_amount'):
                    amount = first_item.price.unit_amount
        except (AttributeError, TypeError):
            # Fallback: try to iterate directly
            try:
                for item in subscription.items:
                    if hasattr(item, 'price') and hasattr(item.price, 'unit_amount'):
                        amount = item.price.unit_amount
                        break
            except (AttributeError, TypeError):
                amount = None
    
    return jsonify({
        'status': subscription.status,
        'current_period_end': subscription.get('current_period_end'),
        'current_period_start': subscription.get('current_period_start'),
        'plan_id': subscription.metadata.get('plan_id'),
        'amount': amount,
        'cancel_at_period_end': subscription.get('cancel_at_period_end', False)
    }), 200

# Cancel subscription
@payment_blueprint.route('/cancel-subscription/<subscription_id>', methods=['POST'])
def cancel_subscription(subscription_id):
    # Cancel subscription in Stripe
    subscription = stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True
    )
    
    # Update subscription in database (no donor involvement)
    try:
        subscription_update = supabase.table("DonorSubscriptions").update({
            "cancel_at_period_end": True,
            "status": "cancelled" if subscription.status == "canceled" else subscription.status
        }).eq("stripe_subscription_id", subscription_id).execute()
    except Exception as e:
        print(f"Warning: Could not update subscription in database: {e}")
    
    return jsonify({
        'status': 'cancelled',
        'cancel_at_period_end': subscription.get('cancel_at_period_end', False),
        'current_period_end': subscription.get('current_period_end')
    }), 200

# Webhook handling
@payment_blueprint.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
    
    # Handle different event types
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print(f"Payment for {payment_intent['amount']} succeeded!")
        
        # Update donation status from pending to completed
        donation_update = supabase.table("Donations").update({
            "payment": "completed"
        }).eq("stripe_payment_intent_id", payment_intent['id']).execute()
        
        # Update campaign progress if donation exists
        if donation_update.data:
            donation = donation_update.data[0]
            if donation.get('campaign_id'):
                update_campaign_progress(donation['campaign_id'])
        
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        subscription_id = invoice['subscription']
        print(f"Subscription {subscription_id} payment succeeded!")
        
        # Just log the successful payment - no donor/donation record needed
        print(f"Payment amount: ${invoice['amount_paid']/100}")
        
    elif event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        print(f"Subscription {subscription['id']} created!")
        # Subscription is already saved during creation, no additional action needed
        
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        print(f"Subscription {subscription['id']} updated!")
        
        # Update subscription status in database (no donor involvement)
        try:
            subscription_update = supabase.table("DonorSubscriptions").update({
                "status": subscription['status'],
                "current_period_start": subscription.get('current_period_start'),
                "current_period_end": subscription.get('current_period_end'),
                "cancel_at_period_end": subscription.get('cancel_at_period_end', False)
            }).eq("stripe_subscription_id", subscription['id']).execute()
        except Exception as e:
            print(f"Warning: Could not update subscription: {e}")
            
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        print(f"Subscription {subscription['id']} cancelled!")
        
        # Update subscription status to cancelled (no donor involvement)
        try:
            subscription_update = supabase.table("DonorSubscriptions").update({
                "status": "cancelled"
            }).eq("stripe_subscription_id", subscription['id']).execute()
        except Exception as e:
            print(f"Warning: Could not update cancelled subscription: {e}")
        
    return jsonify({'status': 'success'}), 200

# Get all subscription plans
@payment_blueprint.route('/plans', methods=['GET'])
def get_plans():
    return jsonify(SUBSCRIPTION_PLANS), 200

# TEST ENDPOINT - Simulate completed payment (for testing only)
@payment_blueprint.route('/test-complete-payment/<payment_intent_id>', methods=['POST'])
def test_complete_payment(payment_intent_id):
    """Test endpoint to simulate payment completion"""
    try:
        # For now, just update database without touching Stripe
        # In production, Stripe webhooks handle this automatically
        donation_update = supabase.table("Donations").update({
            "payment": "completed"
        }).eq("stripe_payment_intent_id", payment_intent_id).execute()
        
        if donation_update.data:
            donation = donation_update.data[0]
            # Update campaign progress if donation exists
            if donation.get('campaign_id'):
                update_campaign_progress(donation['campaign_id'])
            
            return jsonify({
                'status': 'success',
                'message': f'Payment {payment_intent_id} marked as completed in database',
                'donation_id': donation['donation_id'],
                'amount': donation['amount'],
                'note': 'Stripe status remains incomplete (normal for test setup)'
            }), 200
        else:
            return jsonify({'error': 'Payment intent not found in database'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PAYMENT-SPECIFIC DATA ENDPOINTS
# ============================================================================
# Note: Basic campaign/donor CRUD should use campaign.py and donor.py services
# These endpoints provide payment-specific aggregated data only

# Get all donations for a campaign
@payment_blueprint.route('/campaign/<int:campaign_id>/donations', methods=['GET'])
def get_campaign_donations(campaign_id):
    donations_response = supabase.table("Donations").select("*, Donors(name, email)").eq("campaign_id", campaign_id).execute()
    if donations_response.data:
        return jsonify({
            'status': 'success',
            'data': donations_response.data,
            'total_donations': len(donations_response.data),
            'total_amount': sum(d['amount'] for d in donations_response.data)
        }), 200
    else:
        return jsonify({
            'status': 'success',
            'data': [],
            'total_donations': 0,
            'total_amount': 0
        }), 200

# Get all donations for a donor
@payment_blueprint.route('/donor/<int:donor_id>/donations', methods=['GET'])
def get_donor_donations(donor_id):
    donations_response = supabase.table("Donations").select("*, Campaigns(name)").eq("donor_id", donor_id).execute()
    if donations_response.data:
        return jsonify({
            'status': 'success',
            'data': donations_response.data,
            'total_donations': len(donations_response.data),
            'total_amount': sum(d['amount'] for d in donations_response.data)
        }), 200
    else:
        return jsonify({
            'status': 'success',
            'data': [],
            'total_donations': 0,
            'total_amount': 0
        }), 200

# Get all active subscriptions
@payment_blueprint.route('/subscriptions/active', methods=['GET'])
def get_active_subscriptions():
    subscriptions_response = supabase.table("DonorSubscriptions").select("*, SubscriptionPlans(name, price_cents)").eq("status", "active").execute()
    if subscriptions_response.data:
        return jsonify({
            'status': 'success',
            'data': subscriptions_response.data,
            'total_active_subscriptions': len(subscriptions_response.data)
        }), 200
    else:
        return jsonify({
            'status': 'success',
            'data': [],
            'total_active_subscriptions': 0
        }), 200

# Get subscription details by email
@payment_blueprint.route('/subscriptions/email/<email>', methods=['GET'])
def get_subscriptions_by_email(email):
    subscriptions_response = supabase.table("DonorSubscriptions").select("*, SubscriptionPlans(name, price_cents, features)").eq("customer_email", email).execute()
    if subscriptions_response.data:
        return jsonify({
            'status': 'success',
            'data': subscriptions_response.data
        }), 200
    else:
        return jsonify({
            'status': 'success',
            'data': []
        }), 200

# Get payment statistics
@payment_blueprint.route('/stats', methods=['GET'])
def get_payment_stats():
    # Get total donations
    total_donations_response = supabase.table("Donations").select("amount").execute()
    total_amount = sum(d['amount'] for d in total_donations_response.data) if total_donations_response.data else 0
    total_donations_count = len(total_donations_response.data) if total_donations_response.data else 0
    
    # Get active subscriptions
    active_subs_response = supabase.table("DonorSubscriptions").select("*, SubscriptionPlans(price_cents)").eq("status", "active").execute()
    monthly_recurring = sum(s['SubscriptionPlans']['price_cents'] / 100 for s in active_subs_response.data) if active_subs_response.data else 0
    
    # Get total unique subscription customers
    total_subscribers = len(active_subs_response.data) if active_subs_response.data else 0
    
    # Get total campaigns
    total_campaigns_response = supabase.table("Campaigns").select("campaign_id").execute()
    total_campaigns = len(total_campaigns_response.data) if total_campaigns_response.data else 0
    
    return jsonify({
        'status': 'success',
        'data': {
            'total_donations_amount': total_amount,
            'total_donations_count': total_donations_count,
            'monthly_recurring_revenue': monthly_recurring,
            'active_subscriptions': len(active_subs_response.data) if active_subs_response.data else 0,
            'total_subscribers': total_subscribers,
            'total_campaigns': total_campaigns
        }
    }), 200

# Register blueprint
app.register_blueprint(payment_blueprint, url_prefix='/payment')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, debug=True)
