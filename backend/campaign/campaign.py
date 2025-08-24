import mimetypes
import os
import re

from badge import generate_badge
from dotenv import load_dotenv
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from supabase import Client, create_client

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
    return re.sub(r"\s+", "_", name)

# Health Check
@campaign_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "alive"}), 200

# Create Campaign
@campaign_blueprint.route("/", methods=["POST"])
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
        return (
            jsonify(
                {"status": "success", "data": response.data, "school_logo": file_url}
            ),
            201,
        )
    else:
        return jsonify({"status": "error", "message": "Failed to create campaign"}), 400

# View All Campaigns
@campaign_blueprint.route("/", methods=["GET"])
def view_all_campaigns():
    response = supabase.table("Campaigns").select("*").execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "No campaigns found"}), 404

# View Campaign
@campaign_blueprint.route("/<int:campaign_id>", methods=["GET"])
def view_campaign(campaign_id):
    response = (
        supabase.table("Campaigns").select("*").eq("campaign_id", campaign_id).execute()
    )
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Campaign not found"}), 404

# Update Campaign
@campaign_blueprint.route("/<int:campaign_id>", methods=["PUT"])
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

    response = (
        supabase.table("Campaigns")
        .update(update_data)
        .eq("campaign_id", campaign_id)
        .execute()
    )
    if response.data:
        return (
            jsonify(
                {"status": "success", "data": response.data, "school_logo": file_url}
            ),
            200,
        )
    else:
        return jsonify({"status": "error", "message": "Failed to update campaign"}), 400

# Delete Campaign
@campaign_blueprint.route("/<int:campaign_id>", methods=["DELETE"])
def delete_campaign(campaign_id):
    response = (
        supabase.table("Campaigns").delete().eq("campaign_id", campaign_id).execute()
    )
    if response.data:
        return (
            jsonify({"status": "success", "message": "Campaign deleted successfully"}),
            200,
        )
    else:
        return jsonify({"status": "error", "message": "Failed to delete campaign"}), 400

import mimetypes
import os

@campaign_blueprint.route("/generate-badge/<int:campaign_id>", methods=["PUT"])
def create_badge(campaign_id):
    # Step 1: Fetch campaign from Supabase to get description
    campaign = (
        supabase.table("Campaigns")
        .select("description, name, school_logo")
        .eq("campaign_id", campaign_id)
        .single()
        .execute()
    )

    if not campaign.data:
        return jsonify({"status": "error", "message": "Campaign not found"}), 404

    description = campaign.data.get("description")
    name = campaign.data.get("name")
    base_image = campaign.data.get("school_logo") 

    # Step 2: Construct the AI prompt
    prompt = (
        f"Create a professional sponsor appreciation badge for '{name}' campaign. "
        f"Design requirements: "
        f"- Clean, elegant circular or shield-shaped badge on pure white background "
        f"- Bold, readable text '{name}' as the main title in premium serif or sans-serif font "
        f"- Subtitle text 'Sponsor Appreciation' or 'Thank You Sponsor' below the main title "
        f"- Rich color scheme with gold, blue, or deep green accents "
        f"- Subtle gradient or metallic finish effect "
        f"- Professional border with decorative elements like laurel leaves, stars, or geometric patterns "
        f"- High contrast for text readability "
        f"- Corporate/institutional aesthetic suitable for formal recognition "
        f"- Campaign focus: {description} "
        f"- Style: Premium certificate design, award-quality appearance, modern typography "
        f"- No complex backgrounds, maintain focus on text and elegant design elements"
    )

    # Debug: Print the values we're about to use
    print(f"DEBUG - Campaign: {name}")
    print(f"DEBUG - Description: {description}")
    print(f"DEBUG - Base image URL: {base_image}")
    print(f"DEBUG - Base image type: {type(base_image)}")
    formatted_name = sanitize_filename(name)

    try:
        image_path = generate_badge(
            prompt, base_image_url=base_image, output_filename=f"{formatted_name}_badge.png"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    # Step 3: Upload to Supabase
    bucket = "photos/badges"
    safe_filename = os.path.basename(image_path)
    with open(image_path, "rb") as f:
        file_data = f.read()
    content_type, _ = mimetypes.guess_type(image_path)
    if not content_type:
        content_type = "application/octet-stream"

    supabase.storage.from_(bucket).upload(
        safe_filename, file_data, {"content-type": content_type}
    )
    badge_url = supabase.storage.from_(bucket).get_public_url(safe_filename)

    # Step 4: Update DB with badge URL
    response = (
        supabase.table("Campaigns")
        .update({"badge": badge_url})
        .eq("campaign_id", campaign_id)
        .execute()
    )

    if response.data:
        return (
            jsonify({"status": "success", "data": response.data, "badge": badge_url}),
            200,
        )
    else:
        return jsonify({"status": "error", "message": "Failed to create badge"}), 400

# Register the campaign Blueprint with the app
app.register_blueprint(campaign_blueprint, url_prefix="/campaign")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
