import os
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create Blueprint for AI routes
ai_blueprint = Blueprint("ai", __name__)

# Create and configure Flask app
app = Flask(__name__)
CORS(app)

@ai_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"}), 200

@ai_blueprint.route('/generate', methods=['POST'])
def generate():
    data = request.json
    # Get information from json

    # Prompt goes here!

    # Return Image
    
    return jsonify({"status": "success", "data": data}), 200
