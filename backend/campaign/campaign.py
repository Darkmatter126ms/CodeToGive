import os
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client
import mimetypes, re

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

def sanitize_filename(name):
    return re.sub(r'\s+', '_', name)

# Health Check
@campaign_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"}), 200

# Create Campaign
@campaign_blueprint.route('/', methods=['POST'])
def create_campaign():
    # Accept form data and file
    name = request.form.get("name")
    description = request.form.get("description")
    status = request.form.get("status")
    goal_amount = request.form.get("goal_amount")
    end_date = request.form.get("end_date")
    file = request.files.get("file")

    file_url = None
    if file:
        # Upload file to Supabase Storage
        bucket = "photos/logos"
        safe_filename = sanitize_filename(file.filename)
        file_path = f"{safe_filename}"
        file_data = file.read()
        content_type, _ = mimetypes.guess_type(file.filename)
        if not content_type:
            content_type = "application/octet-stream"
        upload_response = supabase.storage.from_(bucket).upload(
            file_path, file_data, {"content-type": content_type}
        )
        # Get public URL
        file_url = supabase.storage.from_(bucket).get_public_url(file_path)

    # Create Campaign in Supabase
    campaign_data = {
        "name": name,
        "description": description,
        "status": status,
        "goal_amount": goal_amount,
        "end_date": end_date,
        "school_logo": file_url,
    }
    response = supabase.table("Campaigns").insert(campaign_data).execute()

    if response.data:
        return jsonify({"status": "success", "data": response.data, "school_logo": file_url}), 201
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
    # Accept form data and file
    name = request.form.get("name")
    description = request.form.get("description")
    status = request.form.get("status")
    goal_amount = request.form.get("goal_amount")
    end_date = request.form.get("end_date")
    file = request.files.get("file")

    file_url = None
    if file:
        bucket = "photos/logos"
        safe_filename = sanitize_filename(file.filename)
        file_path = f"{safe_filename}"
        file_data = file.read()
        content_type, _ = mimetypes.guess_type(file.filename)
        if not content_type:
            content_type = "application/octet-stream"
        upload_response = supabase.storage.from_(bucket).upload(
            file_path, file_data, {"content-type": content_type}
        )
        file_url = supabase.storage.from_(bucket).get_public_url(file_path)

    update_data = {
        "name": name,
        "description": description,
        "status": status,
        "goal_amount": goal_amount,
        "end_date": end_date,
    }
    if file_url:
        update_data["school_logo"] = file_url

    response = supabase.table("Campaigns").update(update_data).eq("campaign_id", campaign_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data, "school_logo": file_url}), 200
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

@campaign_blueprint.route('generate-badge/<int:campaign_id>', methods=['PUT'])
def create_badge(campaign_id):
    badge = request.files.get("badge")

    badge_url = None
    if badge:
        bucket = "photos/badges"  # Change to your bucket name
        safe_filename = sanitize_filename(badge.filename)
        file_path = f"{safe_filename}"
        file_data = badge.read()
        content_type, _ = mimetypes.guess_type(badge.filename)
        if not content_type:
            content_type = "application/octet-stream"
        upload_response = supabase.storage.from_(bucket).upload(
            file_path, file_data, {"content-type": content_type}
        )
        badge_url = supabase.storage.from_(bucket).get_public_url(file_path)

    response = supabase.table("Campaigns").update({"badge": badge_url}).eq("campaign_id", campaign_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data, "badge": badge_url}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to create badge"}), 400

# Register the campaign Blueprint with the app
app.register_blueprint(campaign_blueprint, url_prefix="/campaign")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
