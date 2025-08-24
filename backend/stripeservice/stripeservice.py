import os
import stripe
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

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

payment_blueprint = Blueprint("stripeservice", __name__)

# Health Check
@payment_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "payment service alive"}), 200

# Get Stripe Charge
@payment_blueprint.route('/charges', methods=['POST'])
def charge():
    try:
        data = request.get_json()

        # Create the charge using Stripe API
        charge = stripe.Charge.create(
            amount=data["amount"],
            currency=data["currency"],
            description=data["description"],
            source=data["source"]
        )

        print("✅ Charge created:", charge["id"])
        return jsonify({
            "success": True,
            "message": "Charge successful", 
            "charge": charge
        }), 200

    except stripe.error.CardError as e:
        return jsonify({"error": f"Card error: {e.user_message}"}), 402

    except stripe.error.RateLimitError as e:
        return jsonify({"error": "Too many requests to Stripe API"}), 429

    except stripe.error.InvalidRequestError as e:
        return jsonify({"error": f"Invalid request: {e.user_message}"}), 400

    except stripe.error.AuthenticationError as e:
        return jsonify({"error": "Authentication with Stripe API failed"}), 401

    except stripe.error.APIConnectionError as e:
        return jsonify({"error": "Network communication with Stripe failed"}), 503

    except stripe.error.StripeError as e:
        return jsonify({"error": "Something went wrong with Stripe"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Register blueprint
app.register_blueprint(payment_blueprint, url_prefix='/stripeservice')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
