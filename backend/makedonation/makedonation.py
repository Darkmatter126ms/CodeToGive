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

donor_URL = "http://127.0.0.1:8081/donor"
campaign_URL = "http://127.0.0.1:8080/campaign"
donation_URL = "http://127.0.0.1:8084/donation"
stripe_URL = "http://127.0.0.1:8085/stripeservice"
email_URL = "http://127.0.0.1:8087/email"

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
    try:
        payment = requests.post(
            f"{stripe_URL}/charges",
            json=charge,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Stripe service status code: {payment.status_code}")
        print(f"Stripe service raw response: {payment.text}")
        
        if payment.status_code != 200:
            return jsonify({
                "success": False,
                "error": f"Stripe service returned status {payment.status_code}: {payment.text}"
            }), payment.status_code

        try:
            payment_data = payment.json()
            print("Stripe response:", payment_data)
        except ValueError as e:
            print(f"Failed to parse Stripe response as JSON: {e}")
            return jsonify({
                "success": False,
                "error": f"Invalid JSON response from Stripe service: {payment.text}"
            }), 500
        
        if payment_data.get("success"):
            current_amount = requests.get(f"{campaign_URL}/{campaign_id}").json().get("data", [{}])[0].get("current_amount")
            current_amount += amount
            requests.patch(f"{campaign_URL}/{campaign_id}", json={"current_amount": current_amount})

            # Payment succeeded, proceed to create or get donor
            donor_id = None  # Initialize donor_id
            
            try:
                print(f"Looking up donor with email: {email}")
                donor_response = requests.get(f"{donor_URL}/{email}")
                print(f"Donor lookup response: {donor_response.status_code}")
                print(f"Donor lookup response body: {donor_response.text}")
                
                if donor_response.status_code == 200:
                    donor_json = donor_response.json()
                    print(f"Donor lookup JSON: {donor_json}")
                    
                    if donor_json.get("data"):
                        donor_data = donor_json["data"]
                        if isinstance(donor_data, list) and len(donor_data) > 0:
                            donor_id = donor_data[0].get("donor_id")
                        else:
                            donor_id = donor_data.get("donor_id")
                        print(f"Found existing donor with ID: {donor_id}")
                        
                if not donor_id:
                    # Create new donor if not found
                    print(f"Creating new donor for email: {email}, name: {name}")
                    donor = {
                        "email": email,
                        "name": name,
                    }
                    donor_response = requests.post(donor_URL, json=donor)
                    print(f"Create donor response: {donor_response.status_code}")
                    print(f"Create donor response body: {donor_response.text}")
                    
                    if donor_response.status_code == 201:
                        donor_json = donor_response.json()
                        print(f"Create donor JSON: {donor_json}")
                        
                        # Try different ways to extract donor_id
                        if isinstance(donor_json, dict):
                            data = donor_json.get("data")
                            if isinstance(data, list) and len(data) > 0:
                                donor_id = data[0].get("donor_id")
                            elif isinstance(data, dict):  # in case API returns a single dict in future
                                donor_id = data.get("donor_id")
                            elif "donor_id" in donor_json:
                                donor_id = donor_json.get("donor_id")

                        print(f"Extracted donor ID: {donor_id}")
                        
                        if not donor_id:
                            return jsonify({
                                "success": False,
                                "error": f"Failed to extract donor ID from response: {donor_json}"
                            }), 500
                    else:
                        return jsonify({
                            "success": False,
                            "error": f"Failed to create donor: {donor_response.text}"
                        }), donor_response.status_code
                        
            except requests.exceptions.ConnectionError:
                return jsonify({
                    "success": False,
                    "error": "Donor service is not available. Please start the donor service."
                }), 503
                
            # Verify we have a donor_id before proceeding
            if not donor_id:
                return jsonify({
                    "success": False,
                    "error": "Failed to obtain donor ID"
                }), 500
                
            print(f"Final donor_id before creating donation: {donor_id}")
                
            # Create the donation record
            donation = {
                "campaign_id": campaign_id,
                "donor_id": donor_id,
                "amount": amount,
            }
            
            print(f"Creating donation with data: {donation}")

            try:
                donation_response = requests.post(donation_URL, json=donation)
                print(f"Donation response: {donation_response.status_code}")
                print(f"Donation response body: {donation_response.text}")
                
                if donation_response.status_code == 201:

                    campaign_name = requests.get(f"{campaign_URL}/{campaign_id}").json().get("data", [{}])[0].get("name")
                    email_context = {
                        "email_type": "thanks",
                        "to_email": email,
                        "context": {
                            "donor_name": name,
                            "donation_amount": amount,
                            "campaign_name": campaign_name
                        }
                    }
                    requests.post(f"{email_URL}/send-email", json=email_context)

                    return jsonify({"success": True, "data": donation_response.json()}), 201
                else:
                    return jsonify({
                        "success": False,
                        "error": f"Failed to create donation: {donation_response.text}"
                    }), donation_response.status_code
                
            except requests.exceptions.ConnectionError:
                return jsonify({
                    "success": False,
                    "error": "Donation service is not available. Please start the donation service."
                }), 503


        else:
            return jsonify({
                "success": False,
                "error": payment_data.get("error", "Payment failed")
            }), 400
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "error": "Stripe service is not available. Please start the Stripe service on port 8085."
        }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500

app.register_blueprint(makedonation_blueprint, url_prefix="/makedonation")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)