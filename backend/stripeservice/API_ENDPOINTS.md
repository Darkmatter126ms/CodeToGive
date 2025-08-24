# Payment API - Postman Collection

**Base URL:** `http://localhost:8084/payment`

## 🚀 Quick Setup for Postman

1. Create a new Collection named "Payment API"
2. Set Collection Variables:
   - `base_url`: `http://localhost:8084/payment`
   - `donor_email`: `test@example.com` 
   - `donor_name`: `Test User`

---

## 📋 API Endpoints

### 1. Health Check
```
Method: GET
URL: {{base_url}}/health
Headers: None required

Expected Response (200):
{
  "status": "payment service alive"
}
```

### 2. Get Subscription Plans
```
Method: GET
URL: {{base_url}}/plans
Headers: None required

Expected Response (200):
{
  "supporter": {
    "name": "Supporter",
    "price": 6000,
    "currency": "usd", 
    "interval": "month"
  },
  "advocate": {
    "name": "Advocate",
    "price": 12000,
    "currency": "usd",
    "interval": "month"
  },
  "champion": {
    "name": "Champion", 
    "price": 50000,
    "currency": "usd",
    "interval": "month"
  }
}
```

### 3. Create Payment Intent (One-time Donation)
```
Method: POST
URL: {{base_url}}/create-payment-intent
Headers:
  Content-Type: application/json

Request Body (raw JSON):
{
  "amount": 5000,
  "currency": "usd",
  "email": "{{donor_email}}",
  "name": "{{donor_name}}",
  "campaign_id": 1
}

Expected Response (200):
{
  "client_secret": "pi_xxx_secret_xxx",
  "payment_intent_id": "pi_xxxxxxxxxxxxx", 
  "donor_id": 123
}
```

### 4. Create Subscription
```
Method: POST
URL: {{base_url}}/create-subscription
Headers:
  Content-Type: application/json

Request Body (raw JSON):
{
  "plan_id": "supporter",
  "email": "{{donor_email}}",
  "name": "{{donor_name}}"
}

Expected Response (200):
{
  "subscription_id": "sub_xxxxxxxxxxxxx",
  "client_secret": "pi_xxx_secret_xxx", 
  "customer_id": "cus_xxxxxxxxxxxxx",
  "customer_email": "test@example.com",
  "status": "incomplete"
}
```

### 5. Get Subscription Status
```
Method: GET
URL: {{base_url}}/subscription-status/sub_xxxxxxxxxxxxx
Headers: None required

Expected Response (200):
{
  "status": "active",
  "current_period_end": 1234567890,
  "current_period_start": 1234567890,
  "plan_id": "supporter",
  "amount": 6000,
  "cancel_at_period_end": false
}
```

### 6. Cancel Subscription
```
Method: POST
URL: {{base_url}}/cancel-subscription/sub_xxxxxxxxxxxxx
Headers: None required

Expected Response (200):
{
  "status": "cancelled",
  "cancel_at_period_end": true,
  "current_period_end": 1234567890
}
```

### 7. Get Campaign Donations
```
Method: GET
URL: {{base_url}}/campaign/1/donations
Headers: None required

Expected Response (200):
{
  "status": "success",
  "data": [
    {
      "donation_id": 1,
      "amount": 100.00,
      "donated_at": "2024-01-15T10:30:00Z",
      "Donors": {
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
  ],
  "total_donations": 15,
  "total_amount": 5000.00
}
```

### 8. Get Donor Donations
```
Method: GET
URL: {{base_url}}/donor/123/donations
Headers: None required

Expected Response (200):
{
  "status": "success",
  "data": [
    {
      "donation_id": 1,
      "amount": 50.00,
      "payment_type": "one_time",
      "Campaigns": {
        "name": "Emergency School Meals"
      }
    }
  ],
  "total_donations": 3,
  "total_amount": 150.00
}
```

### 9. Get Active Subscriptions
```
Method: GET
URL: {{base_url}}/subscriptions/active
Headers: None required

Expected Response (200):
{
  "status": "success",
  "data": [
    {
      "subscription_id": 1,
      "status": "active",
      "customer_email": "john@example.com",
      "customer_name": "John Doe",
      "SubscriptionPlans": {
        "name": "Supporter",
        "price_cents": 6000
      }
    }
  ],
  "total_active_subscriptions": 5
}
```

### 10. Get Subscriptions by Email
```
Method: GET
URL: {{base_url}}/subscriptions/email/test@example.com
Headers: None required

Expected Response (200):
{
  "status": "success",
  "data": [
    {
      "subscription_id": 1,
      "status": "active",
      "current_period_start": "2024-01-01T00:00:00Z",
      "current_period_end": "2024-02-01T00:00:00Z",
      "SubscriptionPlans": {
        "name": "Supporter",
        "price_cents": 6000,
        "features": {
          "description": "Monthly impact reports and basic badge collection"
        }
      }
    }
  ]
}
```

### 11. Get Payment Statistics
```
Method: GET
URL: {{base_url}}/stats
Headers: None required

Expected Response (200):
{
  "status": "success",
  "data": {
    "total_donations_amount": 15000.00,
    "total_donations_count": 45,
    "monthly_recurring_revenue": 1200.00,
    "active_subscriptions": 8,
    "total_subscribers": 25,
    "total_campaigns": 3
  }
}
```

### 12. Test Complete Payment (Development Only)
```
Method: POST
URL: {{base_url}}/test-complete-payment/pi_xxxxxxxxxxxxx
Headers: None required

Expected Response (200):
{
  "status": "success",
  "message": "Payment pi_xxxxxxxxxxxxx marked as completed",
  "donation_id": 1,
  "amount": 50.00
}
```

### 13. Stripe Webhook Handler
```
Method: POST
URL: {{base_url}}/webhook
Headers:
  Content-Type: application/json
  Stripe-Signature: whsec_xxxxxxxxxxxxx

Request Body (raw):
[Stripe webhook payload - handled automatically by Stripe]

Expected Response (200):
{
  "status": "success"
}

Note: This endpoint is for Stripe webhooks only. 
      Do not test manually unless you have valid Stripe signatures.
```

---

## 🧪 Testing Sequence

**Recommended testing order:**

1. **Health Check** → Verify service is running
2. **Get Plans** → Check available subscription tiers
3. **Create Payment Intent** → Test donation creation
4. **Test Complete Payment** → Simulate successful payment (dev only)
5. **Get Campaign Donations** → Verify donation was recorded
6. **Create Subscription** → Test subscription creation
7. **Get Subscription Status** → Check subscription details
8. **Get Active Subscriptions** → List all active subscriptions
9. **Get Payment Stats** → View aggregated data
10. **Cancel Subscription** → Test subscription cancellation

---

## 📝 Notes for Testing

- **Replace placeholder values** like `sub_xxxxxxxxxxxxx` with actual IDs from responses
- **Use consistent email** across tests to see related data
- **Check database** after each operation to verify data persistence
- **Test error cases** by using invalid IDs or malformed requests
- **Monitor logs** in the Flask console for debugging

---

## 🔧 Environment Variables Required

Ensure your `.env` file contains:
```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
```

---

## 🚨 Important

- **Amounts** are in cents (5000 = $50.00)
- **Timestamps** are Unix timestamps  
- **Test cards** use Stripe test card numbers (4242424242424242)
- **Webhooks** require ngrok or similar for local testing