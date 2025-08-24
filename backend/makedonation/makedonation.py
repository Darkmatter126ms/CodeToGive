import os
import requests
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env
load_dotenv()

# Set up Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create and configure Flask app
app = Flask(__name__)
CORS(app)

campaign_URL = "http://127.0.0.1:8082/campaign"
donor_URL = "http://127.0.0.1:8083/donor"
donation_URL = "http://127.0.0.1:8084/donation"
stripe_URL = "http://127.0.0.1:8085/stripeservice"

# Create Blueprint for donation routes
makedonation_blueprint = Blueprint("makedonation", __name__)

# Health Check
@makedonation_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


@makedonation_blueprint.route("/donate", methods=["POST"])
def donate():
    data = request.json
    print("Received donation request:", data)
    
    # Campaign ID
    campaign_id = data.get("campaign_id")
    name = data.get("name")
    # Email to get Donor ID or Create New One
    email = data.get("email")
    # Amount Donated
    amount = data.get("amount")
    # For Stripe (this should contain the properly formatted charge data)
    charge = data.get("charge")

    print("Forwarding to Stripe service:", charge)
    
    # Forward the charge data to stripe service
    payment = requests.post(
        f"{stripe_URL}/charges",
        json=charge,  # Send the charge object directly (contains amount, currency, description, source)
        headers={'Content-Type': 'application/json'}
    )

    try:
        payment_data = payment.json()
        print("Stripe response:", payment_data)
        
        if payment.status_code == 200 and payment_data.get("success"):
            # Payment succeeded, proceed to create or get donor
            donor_response = requests.get(f"{donor_URL}/{email}")   
            if donor_response.status_code == 200 and donor_response.json().get("data"):
                donor_id = donor_response.json()["data"][0].get("id")
            else:
                # Create new donor if not found
                donor = {
                    "email": email,
                    "name": name,
                }
                donor_response = requests.post(donor_URL, json=donor)
                if donor_response.status_code == 201:
                    donor_id = donor_response.json().get("id")
                else:
                    return jsonify({
                        "success": False,
                        "error": donor_response.json().get("error", "Failed to create donor")
                    }), donor_response.status_code
                
            # Create the donation record
            donation = {
                "campaign_id": campaign_id,
                "donor_id": donor_id,
                "amount": amount,
            }

            donation_response = requests.post(donation_URL, json=donation)
            if donation_response.status_code == 201:
                return jsonify({"success": True, "data": donation_response.json()}), 201
            else:
                return jsonify({
                    "success": False,
                    "error": donation_response.json().get("error", "Failed to create donation")
                }), donation_response.status_code

        else:
            return jsonify({
                "success": False,
                "error": payment_data.get("error", "Payment failed")
            }), payment.status_code
            
    except ValueError:
        payment_data = {"error": "Stripe service did not return valid JSON", "raw": payment.text}
        return jsonify({
            "success": False,
            "error": "Invalid response from payment service"
        }), 500

app.register_blueprint(makedonation_blueprint, url_prefix="/makedonation")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)