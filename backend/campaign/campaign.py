
from datetime import datetime
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

# Create Blueprint for campaign routes
campaign_blueprint = Blueprint("campaign", __name__)

# Create and configure Flask app
app = Flask(__name__)
CORS(app)

# Health Check
@campaign_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"}), 200

# Create Campaign
@campaign_blueprint.route('/', methods=['POST'])
def create_campaign():
    # Get Data from Request Body
    data = request.json

    # Create Campaign in Supabase
    response = supabase.table("Campaigns").insert({
        "name": data.get("name"),
        "description": data.get("description"),
        "status": data.get("status"),
        "goal_amount": data.get("goal_amount"),
        "badge": data.get("badge"),
        "end_date": data.get("end_date"),
    }).execute()

    # Check if Campaign was Created Successfully
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 201
    else:
        return jsonify({"status": "error", "message": "Failed to create campaign"}), 400

# View All Campaigns
@campaign_blueprint.route('/', methods=['GET'])
def view_all_campaigns():
    response = supabase.table("Campaigns").select("*").execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "No campaigns found"}), 404

# View Campaign
@campaign_blueprint.route('/<int:campaign_id>', methods=['GET'])
def view_campaign(campaign_id):
    response = supabase.table("Campaigns").select("*").eq("campaign_id", campaign_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Campaign not found"}), 404

# Update Campaign
@campaign_blueprint.route('/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    data = request.json
    response = supabase.table("Campaigns").update({
        "name": data.get("name"),
        "description": data.get("description"),
        "status": data.get("status"),
        "goal_amount": data.get("goal_amount"),
        "badge": data.get("badge"),
        "end_date": data.get("end_date"),
    }).eq("campaign_id", campaign_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to update campaign"}), 400

# Delete Campaign
@campaign_blueprint.route('/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    response = supabase.table("Campaigns").delete().eq("campaign_id", campaign_id).execute()
    if response.data:
        return jsonify({"status": "success", "message": "Campaign deleted successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to delete campaign"}), 400

# Register the campaign Blueprint with the app
app.register_blueprint(campaign_blueprint, url_prefix="/campaign")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
