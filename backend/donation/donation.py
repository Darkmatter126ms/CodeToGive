import os
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

# Create Blueprint for donation routes
donation_blueprint = Blueprint("donation", __name__)

# Health Check
@donation_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"}), 200

# Create Donations
@donation_blueprint.route('/', methods=['POST'])
def create_donation():
    # Accept form data
    donor_id = request.form.get("donor_id")
    campaign_id = request.form.get("campaign_id")
    amount = request.form.get("amount")

    # Create Donation in Supabase
    donation_data = {
        "campaign_id": campaign_id,
        "donor_id": donor_id,
        "amount": amount,
    }
    response = supabase.table("Donations").insert(donation_data).execute()

    if response.data:
        return jsonify({"status": "success", "data": response.data}), 201
    else:
        return jsonify({"status": "error", "message": "Failed to create donation"}), 400
    
# View All Donations
@donation_blueprint.route('/', methods=['GET'])
def view_donations():
    response = supabase.table("Donations").select("*").execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to retrieve donations"}), 400
    
# View Donations
@donation_blueprint.route('/<int:donation_id>', methods=['GET'])
def view_donor_donations(donation_id):
    response = supabase.table("Donations").select("*").eq("donation_id", donation_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to retrieve donations"}), 400

# Update Donation
@donation_blueprint.route('/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
    data = request.json
    response = supabase.table("Donations").update({
        "campaign_id": data.get("campaign_id"),
        "donor_id": data.get("donor_id"),
        "amount": data.get("amount"),
    }).eq("donation_id", donation_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to update donation"}), 400
    
# Delete Donations
@donation_blueprint.route('/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    response = supabase.table("Donations").delete().eq("donation_id", donation_id).execute()
    if response.data:
        return jsonify({"status": "success", "message": "Donation deleted successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to delete donation"}), 400
    
app.register_blueprint(donation_blueprint, url_prefix='/donation')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)