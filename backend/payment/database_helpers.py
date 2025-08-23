"""
Database Helper Functions for Payment System
These functions handle data updates that were previously done by database triggers.
Call these functions after database operations to keep data synchronized.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Set up Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def update_campaign_progress(campaign_id):
    """
    Update the current_amount for a campaign based on all donations.
    Call this function after creating, updating, or deleting donations.
    
    Args:
        campaign_id (int): ID of the campaign to update
    
    Returns:
        dict: Updated campaign data or None if error
    """
    # Calculate total donations for this campaign
    donations_response = supabase.table("Donations").select("amount").eq("campaign_id", campaign_id).execute()
    
    if donations_response.data:
        total_amount = sum(donation['amount'] for donation in donations_response.data)
    else:
        total_amount = 0
    
    # Update campaign current_amount
    campaign_response = supabase.table("Campaigns").update({
        "current_amount": total_amount
    }).eq("campaign_id", campaign_id).execute()
    
    print(f"Campaign {campaign_id} updated: current_amount = ${total_amount}")
    return campaign_response.data[0] if campaign_response.data else None

def update_donor_subscription_status(donor_id):
    """
    Update donor's subscription_status based on their active subscriptions.
    Call this function after creating, updating, or canceling subscriptions.
    
    Args:
        donor_id (int): ID of the donor to update
    
    Returns:
        dict: Updated donor data or None if error
    """
    # Check for active subscriptions
    active_subs = supabase.table("donor_subscriptions").select("status").eq("donor_id", donor_id).eq("status", "active").execute()
    
    past_due_subs = supabase.table("donor_subscriptions").select("status").eq("donor_id", donor_id).in_("status", ["past_due", "trialing"]).execute()
    
    # Determine status
    if active_subs.data:
        new_status = "active"
    elif past_due_subs.data:
        new_status = "past_due"
    else:
        new_status = "none"
    
    # Update donor subscription_status
    donor_response = supabase.table("Donors").update({
        "subscription_status": new_status
    }).eq("donor_id", donor_id).execute()
    
    print(f"Donor {donor_id} subscription status updated: {new_status}")
    return donor_response.data[0] if donor_response.data else None

def create_donation_with_updates(donation_data):
    """
    Create a donation and automatically update campaign progress.
    Use this instead of directly inserting into Donations table.
    
    Args:
        donation_data (dict): Donation data to insert
    
    Returns:
        dict: Created donation data
    """
    # Insert donation
    donation_response = supabase.table("Donations").insert(donation_data).execute()
    
    if donation_response.data:
        donation = donation_response.data[0]
        
        # Update campaign progress if this donation has a campaign_id
        if donation.get('campaign_id'):
            update_campaign_progress(donation['campaign_id'])
        
        print(f"Donation created: ${donation.get('amount')} for campaign {donation.get('campaign_id')}")
        return donation
    
    return None

def create_subscription_with_updates(subscription_data):
    """
    Create a subscription and automatically update donor status.
    Use this instead of directly inserting into donor_subscriptions table.
    
    Args:
        subscription_data (dict): Subscription data to insert
    
    Returns:
        dict: Created subscription data
    """
    # Insert subscription
    subscription_response = supabase.table("donor_subscriptions").insert(subscription_data).execute()
    
    if subscription_response.data:
        subscription = subscription_response.data[0]
        
        # Update donor subscription status
        update_donor_subscription_status(subscription['donor_id'])
        
        print(f"Subscription created: {subscription.get('plan_id')} for donor {subscription.get('donor_id')}")
        return subscription
    
    return None

def update_subscription_status(subscription_id, new_status):
    """
    Update subscription status and automatically update donor status.
    Use this for handling Stripe webhook events.
    
    Args:
        subscription_id (int): ID of the subscription to update
        new_status (str): New status ('active', 'canceled', 'past_due', etc.)
    
    Returns:
        dict: Updated subscription data
    """
    # Update subscription status
    subscription_response = supabase.table("donor_subscriptions").update({
        "status": new_status
    }).eq("subscription_id", subscription_id).execute()
    
    if subscription_response.data:
        subscription = subscription_response.data[0]
        
        # Update donor subscription status
        update_donor_subscription_status(subscription['donor_id'])
        
        print(f"Subscription {subscription_id} status updated: {new_status}")
        return subscription
    
    return None

def get_campaign_progress(campaign_id):
    """
    Get campaign progress information.
    
    Args:
        campaign_id (int): ID of the campaign
    
    Returns:
        dict: Campaign progress data
    """
    campaign_response = supabase.table("Campaigns").select("*").eq("campaign_id", campaign_id).execute()
    
    if campaign_response.data:
        campaign = campaign_response.data[0]
        
        # Calculate progress percentage
        current_amount = campaign.get('current_amount', 0)
        goal_amount = campaign.get('goal_amount', 1)  # Avoid division by zero
        progress_percentage = (current_amount / goal_amount) * 100 if goal_amount > 0 else 0
        
        return {
            'campaign_id': campaign_id,
            'name': campaign.get('name'),
            'current_amount': current_amount,
            'goal_amount': goal_amount,
            'progress_percentage': round(progress_percentage, 2),
            'status': campaign.get('status')
        }
    
    return None

def get_donor_summary(donor_id):
    """
    Get comprehensive donor information including subscription status.
    
    Args:
        donor_id (int): ID of the donor
    
    Returns:
        dict: Donor summary data
    """
    # Get donor basic info
    donor_response = supabase.table("Donors").select("*").eq("donor_id", donor_id).execute()
    
    if not donor_response.data:
        return None
    
    donor = donor_response.data[0]
    
    # Get total donations
    donations_response = supabase.table("Donations").select("amount").eq("donor_id", donor_id).execute()
    total_donated = sum(donation['amount'] for donation in donations_response.data) if donations_response.data else 0
    
    # Get active subscription
    subscription_response = supabase.table("donor_subscriptions").select("*").eq("donor_id", donor_id).eq("status", "active").execute()
    active_subscription = subscription_response.data[0] if subscription_response.data else None
    
    return {
        'donor_id': donor_id,
        'name': donor.get('name'),
        'email': donor.get('email'),
        'total_donated': total_donated,
        'subscription_status': donor.get('subscription_status', 'none'),
        'stripe_customer_id': donor.get('stripe_customer_id'),
        'active_subscription': active_subscription,
        'donation_count': len(donations_response.data) if donations_response.data else 0
    }
