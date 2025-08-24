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
        # Create unique filename to avoid duplicates
        import time
        timestamp = str(int(time.time()))
        safe_filename = f"{timestamp}_{sanitize_filename(file.filename)}"
        file_path = f"{safe_filename}"
        file_data = file.read()
        content_type, _ = mimetypes.guess_type(file.filename)
        if not content_type:
            content_type = "application/octet-stream"
        
        try:
            upload_response = supabase.storage.from_(bucket).upload(
                file_path, file_data, {"content-type": content_type}
            )
            # Get public URL
            file_url = supabase.storage.from_(bucket).get_public_url(file_path)
        except Exception as e:
            print(f"Upload error: {e}")
            # If upload fails due to duplicate, try to get existing file URL
            try:
                file_url = supabase.storage.from_(bucket).get_public_url(file_path)
            except:
                return jsonify({"status": "error", "message": f"Failed to upload file: {str(e)}"}), 400

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
        # Create unique filename to avoid duplicates
        import time
        timestamp = str(int(time.time()))
        safe_filename = f"{timestamp}_{sanitize_filename(file.filename)}"
        file_path = f"{safe_filename}"
        file_data = file.read()
        content_type, _ = mimetypes.guess_type(file.filename)
        if not content_type:
            content_type = "application/octet-stream"
        
        try:
            upload_response = supabase.storage.from_(bucket).upload(
                file_path, file_data, {"content-type": content_type}
            )
            file_url = supabase.storage.from_(bucket).get_public_url(file_path)
        except Exception as e:
            print(f"Upload error: {e}")
            # If upload fails due to duplicate, try to get existing file URL
            try:
                file_url = supabase.storage.from_(bucket).get_public_url(file_path)
            except:
                return jsonify({"status": "error", "message": f"Failed to upload file: {str(e)}"}), 400

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
    # Step 1: Get theme from request body
    data = request.get_json() or {}
    theme = data.get('theme', 'prestigious')  # Default to prestigious if no theme provided
    
    # Step 2: Fetch campaign from Supabase to get description
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
    
    # Step 3: Define theme-specific styling
    theme_styles = {
        'cute': {
            'colors': 'soft pastel pink (#FFB6C1), bright pink (#FF69B4), and golden yellow (#FFD700)',
            'style': 'playful and friendly with rounded corners, heart shapes, and cheerful decorative elements',
            'mood': 'warm, inviting, and joyful with cute illustrations'
        },
        'prestigious': {
            'colors': 'deep navy blue (#000080), rich gold (#FFD700), and crisp white',
            'style': 'formal and elegant with sharp geometric borders, classical laurel wreaths, and premium typography',
            'mood': 'authoritative, distinguished, and professional like an academic award'
        },
        'pretty': {
            'colors': 'lavender (#E6E6FA), plum (#DDA0DD), and hot pink (#FF1493)',
            'style': 'elegant and feminine with floral patterns, delicate swirls, and graceful curves',
            'mood': 'sophisticated, beautiful, and refined with artistic flourishes'
        },
        'nature': {
            'colors': 'forest green (#228B22), lime green (#32CD32), and light green (#90EE90)',
            'style': 'organic and natural with leaf patterns, tree motifs, and earth-inspired elements',
            'mood': 'fresh, sustainable, and environmentally conscious'
        },
        'modern': {
            'colors': 'dark slate (#2C3E50), bright blue (#3498DB), and light gray (#ECF0F1)',
            'style': 'clean and minimalist with geometric shapes, sharp lines, and contemporary design',
            'mood': 'innovative, tech-forward, and sleek'
        }
    }
    
    # Get theme styling or default to prestigious
    theme_info = theme_styles.get(theme, theme_styles['prestigious'])

    # Step 4: Construct the AI prompt with theme-specific elements
    prompt = (
        f"Create a {theme} themed sponsor appreciation badge for '{name}' campaign. "
        f"Design requirements: "
        f"- Clean, elegant circular or shield-shaped badge on pure white background "
        f"- Bold, readable text '{name}' as the main title in premium serif or sans-serif font "
        f"- Subtitle text 'Sponsor Appreciation' or 'Thank You Sponsor' below the main title "
        f"- Color scheme: {theme_info['colors']} "
        f"- Style: {theme_info['style']} "
        f"- Mood: {theme_info['mood']} "
        f"- Professional border with decorative elements appropriate for {theme} theme "
        f"- High contrast for text readability "
        f"- Corporate/institutional aesthetic suitable for formal recognition "
        f"- Campaign focus: {description} "
        f"- Overall appearance: Premium certificate design, award-quality appearance "
        f"- No complex backgrounds, maintain focus on text and elegant design elements "
        f"- Theme consistency: Ensure all elements reflect the {theme} aesthetic"
    )

    # Debug: Print the values we're about to use
    print(f"DEBUG - Campaign: {name}")
    print(f"DEBUG - Description: {description}")
    print(f"DEBUG - Selected Theme: {theme}")
    print(f"DEBUG - Base image URL: {base_image}")
    print(f"DEBUG - Base image type: {type(base_image)}")
    formatted_name = sanitize_filename(name)

    try:
        image_path = generate_badge(
            prompt, base_image_url=base_image, output_filename=f"{formatted_name}_{theme}_badge.png"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    # Step 5: Upload to Supabase
    bucket = "photos/badges"
    # Create unique filename to avoid duplicates
    import time
    timestamp = str(int(time.time()))
    original_filename = os.path.basename(image_path)
    safe_filename = f"{timestamp}_{original_filename}"
    
    with open(image_path, "rb") as f:
        file_data = f.read()
    content_type, _ = mimetypes.guess_type(image_path)
    if not content_type:
        content_type = "application/octet-stream"

    try:
        supabase.storage.from_(bucket).upload(
            safe_filename, file_data, {"content-type": content_type}
        )
        badge_url = supabase.storage.from_(bucket).get_public_url(safe_filename)
    except Exception as e:
        print(f"Badge upload error: {e}")
        # If upload fails due to duplicate, try to get existing file URL
        try:
            badge_url = supabase.storage.from_(bucket).get_public_url(safe_filename)
        except:
            return jsonify({"status": "error", "message": f"Failed to upload badge: {str(e)}"}), 500

    # Step 6: Update DB with badge URL
    response = (
        supabase.table("Campaigns")
        .update({"badge": badge_url})
        .eq("campaign_id", campaign_id)
        .execute()
    )

    if response.data:
        return (
            jsonify({"status": "success", "data": response.data, "badge": badge_url, "theme": theme}),
            200,
        )
    else:
        return jsonify({"status": "error", "message": "Failed to create badge"}), 400

# Register the campaign Blueprint with the app
app.register_blueprint(campaign_blueprint, url_prefix="/campaign")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
