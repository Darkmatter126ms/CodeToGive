
from datetime import datetime
import os
from flask import Blueprint, Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get SECRET from env
secret = os.getenv("SECRET")

# Create Blueprint for test routes
test_blueprint = Blueprint("test", __name__)

# Create and configure Flask app
app = Flask(__name__)
CORS(app)

@test_blueprint.route('', methods=["GET"])
def test():
    return jsonify({"Hello": secret}), 200

# Register the guest Blueprint with the app
app.register_blueprint(test_blueprint, url_prefix="/test")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
