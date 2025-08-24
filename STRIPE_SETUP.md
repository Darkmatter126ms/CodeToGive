# Stripe Payment System Setup Guide

## 1. Environment Configuration

Create a `.env` file in the `backend/` directory:

```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Application Configuration
SECRET=your_app_secret
FRONTEND_URL=http://localhost:5173
```

## 2. Stripe Account Setup Steps

1. **Register Stripe Account**
   - Visit https://stripe.com
   - Create developer account
   - Verify email address

2. **Get API Keys**
   - Go to Dashboard > Developers > API keys
   - Copy test environment keys:
     - `Publishable key` → STRIPE_PUBLISHABLE_KEY
     - `Secret key` → STRIPE_SECRET_KEY

3. **Setup Products and Pricing**
   - Go to Dashboard > Products
   - Create subscription products:
     - Supporter ($60/month)
     - Advocate ($120/month) 
     - Champion ($500/month)

## 3. Test Card Numbers

Use these test card numbers during development:

```
Successful payment: 4242 4242 4242 4242
Requires verification: 4000 0027 6000 3184
Failed payment: 4000 0000 0000 0002
```

## 4. Development Phase Planning

### Phase 1: Backend API (2-3 days)
- [ ] Install Stripe Python library
- [ ] Create Payment Intent API
- [ ] Create subscription management API
- [ ] Setup Webhook handling

### Phase 2: Frontend UI (2-3 days)
- [ ] Install Stripe.js
- [ ] Create payment form components
- [ ] Integrate Stripe Elements
- [ ] Implement payment flow

### Phase 3: Integration Testing (1 day)
- [ ] End-to-end testing
- [ ] Error handling verification
- [ ] Subscription flow testing
