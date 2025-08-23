# Backend Setup Guide

This guide will help you set up and start the backend for the CodeToGive project.

## 1. Create and Activate a Virtual Environment (Recommended)
```
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## 2. Install Dependencies
```
pip install -r requirements.txt
```

## 3. Environment Configuration

### 3.1 Create Environment File
Create a `.env` file in the `backend/` directory:
```bash
touch .env
```

### 3.2 Configure Stripe API Keys
Add your Stripe configuration to `.env`:

```bash
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Application Configuration
SECRET=your_app_secret_key_here
FRONTEND_URL=http://localhost:5173
```

### 3.3 How to Get Stripe API Keys

1. **Create Stripe Account**: Go to https://stripe.com and sign up
2. **Access Dashboard**: Navigate to your Stripe dashboard
3. **Get API Keys**: 
   - Go to `Developers` → `API keys` in the left sidebar
   - Copy your `Publishable key` (starts with `pk_test_...`)
   - Copy your `Secret key` (starts with `sk_test_...`)
4. **Replace Values**: Update the `.env` file with your actual keys

**⚠️ Important**: Never commit your `.env` file to version control. The file is already in `.gitignore`.

## 4. Run the Backend Services

### 4.1 Main Tutorial Service
```
cd tutorial
python flask.py
python hello.py
```
The backend should now be running!
Try `http://localhost:8082/test` to see if it works!
### Test Card Numbers (Stripe Test Mode)
- **Successful payment**: 4242 4242 4242 4242
- **Requires verification**: 4000 0027 6000 3184  
- **Failed payment**: 4000 0000 0000 0002

## 6. API Endpoints
- `/test` - Sample endpoint to check if the service is alive

## Troubleshooting
- Ensure all dependencies are installed
- Check your `.env` file for correct values
- Verify Stripe keys are valid (test mode keys start with `sk_test_` and `pk_test_`)
- Ensure services are running on different ports
- Check Supabase connection if database operations fail

---

Feel free to contribute and improve the backend!
