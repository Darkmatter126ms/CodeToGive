# TODO: Implement email sending functionality with endpoints for
# - Badge + Social Media Sharing
# - Post Event Email

import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS

# Load environment variables from .env
load_dotenv()

# Create and configure Flask app
app = Flask(__name__)
CORS(app)

# Create Blueprint for email routes
email_blueprint = Blueprint("email", __name__)

# ---------- Configuration ----------
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_NAME = "Project Reach Team"
FROM_EMAIL = SMTP_USER
TEMPLATE_DIR = "templates"
SUBJECT = "Welcome to Project Reach 👋"

def send_email(message: EmailMessage):
    use_ssl = (SMTP_PORT == 465)
    if use_ssl:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(message)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(message)

# Health Check
@email_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Send Email
@email_blueprint.route('/send-email', methods=['POST'])
def send_email_template_endpoint():
    data = request.json
    email_type = data.get('email_type', 'default')
    to_emails = data.get('to_emails', [])
    context = data.get('context', {})

    # Select template based on email_type
    if email_type == "badge":
        template_file = "badge_social.html"
    elif email_type == "post_event":
        template_file = "post_event.html"
    else:
        template_file = "welcome.html"

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template(template_file)
    html_body = template.render(**context)

    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = formataddr((FROM_NAME, FROM_EMAIL))
    msg["To"] = ", ".join(to_emails)
    msg.set_content("This is a fallback plain text message.")
    msg.add_alternative(html_body, subtype="html")

    try:
        send_email(msg)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

app.register_blueprint(email_blueprint, url_prefix="/email")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)