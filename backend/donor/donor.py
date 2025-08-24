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

# Create Blueprint for donor routes
donor_blueprint = Blueprint("donor", __name__)

# Health Check
@donor_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"}), 200

# Create Donor
@donor_blueprint.route('/', methods=['POST'])
def create_donor():
    data = request.json
    response = supabase.table("Donors").insert({
        "name": data.get("name"),
        "email": data.get("email"),
    }).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 201
    else:
        return jsonify({"status": "error", "message": "Failed to create donor"}), 400

# View All Donors
@donor_blueprint.route('/', methods=['GET'])
def get_donors():
    response = supabase.table("Donors").select("*").execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "No donors found"}), 404

# View Donor
@donor_blueprint.route('/<int:donor_id>', methods=['GET'])
def get_donor(donor_id):
    response = supabase.table("Donors").select("*").eq("donor_id", donor_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Donor not found"}), 404

# Update Donor
@donor_blueprint.route('/<int:donor_id>', methods=['PUT'])
def update_donor(donor_id):
    data = request.json
    response = supabase.table("Donors").update({
        "name": data.get("name"),
        "email": data.get("email"),
    }).eq("donor_id", donor_id).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to update donor"}), 400

# Delete Donor
@donor_blueprint.route('/<int:donor_id>', methods=['DELETE'])
def delete_donor(donor_id):
    response = supabase.table("Donors").delete().eq("donor_id", donor_id).execute()
    if response.data:
        return jsonify({"status": "success", "message": "Donor deleted successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to delete donor"}), 400

@donor_blueprint.route('/<string:email>', methods=['GET'])
def get_donor_by_email(email):
    response = supabase.table("Donors").select("*").eq("email", email).execute()
    if response.data:
        return jsonify({"status": "success", "data": response.data}), 200
    else:
        return jsonify({"status": "error", "message": "Donor not found"}), 404

app.register_blueprint(donor_blueprint, url_prefix='/donor')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
