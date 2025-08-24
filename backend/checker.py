from multiprocessing import context
import os
import schedule
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client
import logging
from zoneinfo import ZoneInfo
import requests

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('campaign_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set up Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_open_campaigns():
    """
    Query the database for campaigns that are currently open
    """
    try:
        logger.info("🔍 Starting daily campaign check...")
        
        # Get current date
        current_date = datetime.now().isoformat()
        
        # Query for open campaigns
        # Assuming campaigns have 'status', 'start_date', 'end_date' fields
        response = supabase.table('Campaigns').select('*').filter('status', 'eq', 'open').execute()
        
        if response.data:
            open_campaigns = response.data
            logger.info(f"✅ Found {len(open_campaigns)} open campaigns")
            
            # Process each open campaign
            for campaign in open_campaigns:
                process_campaign(campaign)
                
        else:
            logger.info("📭 No open campaigns found")
            
    except Exception as e:
        logger.error(f"❌ Error checking campaigns: {str(e)}")

def process_campaign(campaign):
    """
    Process an individual campaign - check if it needs updates
    """
    try:
        campaign_id = campaign.get('campaign_id')
        title = campaign.get('name', 'Untitled Campaign')
        end_date = campaign.get('end_date')
        current_amount = campaign.get('current_amount', 0)
        goal_amount = campaign.get('goal_amount', 0)
        
        logger.info(f"🎯 Processing campaign: {title} (ID: {campaign_id})")
        
        # Check if campaign should be closed due to end date
        if end_date:
            try:
                # Handle different datetime formats from database
                if end_date.endswith('Z'):
                    end_date_str = end_date[:-1] + '+00:00'
                elif '+' not in end_date and 'T' in end_date:
                    end_date_str = end_date + '+00:00'
                else:
                    end_date_str = end_date
                
                end_date_obj = datetime.fromisoformat(end_date_str)
                
                # Get current time with same timezone
                current_time = datetime.now(end_date_obj.tzinfo) if end_date_obj.tzinfo else datetime.now()
                
                if current_time >= end_date_obj:
                    close_expired_campaign(campaign_id, title)
                    send_email(campaign)
                    return
                    
            except (ValueError, TypeError) as date_error:
                logger.error(f"❌ Error parsing end_date '{end_date}' for campaign {campaign_id}: {date_error}")
        
        # Check if campaign has reached its goal
        if goal_amount > 0 and current_amount >= goal_amount:
            close_completed_campaign(campaign_id, title)
            send_email(campaign)
            return
        
        # Log campaign status
        progress = (current_amount / goal_amount * 100) if goal_amount > 0 else 0
        logger.info(f"  📊 Progress: ${current_amount:.2f} / ${goal_amount:.2f} ({progress:.1f}%)")
        
    except Exception as e:
        logger.error(f"❌ Error processing campaign {campaign.get('campaign_id', 'unknown')}: {str(e)}")
        logger.error(f"Campaign data: {campaign}")  # Debug info

def close_expired_campaign(campaign_id, title):
    """
    Close a campaign that has passed its end date
    """
    try:
        # Update campaign status to finished
        response = supabase.table('Campaigns').update({
            'status': 'finished'
        }).eq('campaign_id', campaign_id).execute()
        
        if response.data:
            logger.info(f"⏰ Closed expired campaign: {title}")
            # Send badge emails to all donors
            campaign_data = response.data[0]  # Get the updated campaign data
            send_email(campaign_data)
        else:
            logger.error(f"❌ Failed to close expired campaign: {title}")
            
    except Exception as e:
        logger.error(f"❌ Error closing expired campaign {campaign_id}: {str(e)}")

def close_completed_campaign(campaign_id, title):
    """
    Close a campaign that has reached its goal
    """
    try:
        # Update campaign status to finished
        response = supabase.table('Campaigns').update({
            'status': 'finished'
        }).eq('campaign_id', campaign_id).execute()
        
        if response.data:
            logger.info(f"🎉 Closed finished campaign: {title}")
            # Send badge emails to all donors
            campaign_data = response.data[0]  # Get the updated campaign data
            send_email(campaign_data)
            # You could trigger celebration notifications here
        else:
            logger.error(f"❌ Failed to close finished campaign: {title}")

    except Exception as e:
        logger.error(f"❌ Error closing finished campaign {campaign_id}: {str(e)}")

def get_campaign_statistics():
    """
    Get overall campaign statistics for daily reporting
    """
    try:
        # Count campaigns by status
        total_campaigns = supabase.table('Campaigns').select('campaign_id').execute()
        open_campaigns = supabase.table('Campaigns').select('campaign_id').filter('status', 'eq', 'open').execute()
        closed_campaigns = supabase.table('Campaigns').select('campaign_id').filter('status', 'eq', 'closed').execute()
        finished_campaigns = supabase.table('Campaigns').select('campaign_id').filter('status', 'eq', 'finished').execute()

        total_count = len(total_campaigns.data) if total_campaigns.data else 0
        open_count = len(open_campaigns.data) if open_campaigns.data else 0
        finished_count = len(finished_campaigns.data) if finished_campaigns.data else 0
        closed_count = len(closed_campaigns.data) if closed_campaigns.data else 0
        
        logger.info(f"📈 Campaign Statistics:")
        logger.info(f"  📊 Total: {total_count}")
        logger.info(f"  🟢 Open: {open_count}")
        logger.info(f"  ⛔ Closed: {closed_count}")
        logger.info(f"  ✅ Finished: {finished_count}")
        
    except Exception as e:
        logger.error(f"❌ Error getting statistics: {str(e)}")

def daily_check():
    """
    Main daily check function
    """
    logger.info("🌅 Starting daily campaign check routine")
    check_open_campaigns()
    get_campaign_statistics()
    logger.info("🌙 Daily campaign check completed\n" + "="*50)

def run_scheduler():
    """
    Set up and run the daily scheduler
    """
    logger.info("🚀 Campaign Checker started")
    logger.info("⏰ Scheduled to run daily at 9:00 AM")
    
    # Schedule daily check at 9:00 AM
    # schedule.every().day.at("23:18").do(daily_check)
    
    # Optional: Run immediately on startup for testing
    daily_check()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def send_email(campaign):

    email_type = "badge"

    # Get All Donors
    donors = supabase.table("Donations").select("donor_id").filter("campaign_id", "eq", campaign.get('campaign_id')).execute()

    for donor in donors.data:
        donor_id = donor['donor_id']  
        donor_response = requests.get(f"http://127.0.0.1:8081/donor/{donor_id}").json() 
        donor_data = donor_response.get("data", [{}])[0] if donor_response.get("data") else {}
        
        context = {
            "donor_name": donor_data.get("name", "Valued Donor"),
            "badge_earned": campaign.get("badge"),
            "campaign_name": campaign.get("name"),
        }
        
        # Send email to this donor
        try:
            email_payload = {
                "to_email": donor_data.get("email"),
                "email_type": email_type,
                "context": context
            }
            
            email_response = requests.post("http://127.0.0.1:8087/email/send-email", json=email_payload)
            if email_response.status_code == 200:
                logger.info(f"✅ Badge email sent to {donor_data.get('name', 'Unknown')} ({donor_data.get('email')})")
            else:
                logger.error(f"❌ Failed to send badge email to {donor_data.get('email')}: {email_response.text}")
                
        except Exception as email_error:
            logger.error(f"❌ Error sending email to donor {donor_id}: {str(email_error)}")


if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("👋 Campaign Checker stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")