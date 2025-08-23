# Payment API Endpoints Documentation

This document describes all available endpoints in the updated payment system with database integration.

## Base URL
```
http://localhost:8084/payment
```

## 🔐 Authentication & Setup Endpoints

### Health Check
```
GET /health
```
**Response:** Service status
```json
{"status": "payment service alive"}
```

### Get Subscription Plans
```
GET /plans
```
**Response:** Available subscription tiers
```json
{
  "supporter": {"name": "Supporter", "price": 6000, "currency": "usd", "interval": "month"},
  "advocate": {"name": "Advocate", "price": 12000, "currency": "usd", "interval": "month"},
  "champion": {"name": "Champion", "price": 50000, "currency": "usd", "interval": "month"}
}
```

---

## 💳 Payment Processing Endpoints

### Create Payment Intent (One-time Donation)
```
POST /create-payment-intent
```
**Request Body:**
```json
{
  "amount": 5000,           // Amount in cents ($50.00)
  "currency": "usd",        // Optional, defaults to "usd"
  "email": "user@example.com",
  "name": "John Doe",       // Optional
  "campaign_id": 1          // Optional, for campaign donations
}
```
**Response:**
```json
{
  "client_secret": "pi_xxx_secret_xxx",
  "payment_intent_id": "pi_xxxxxxxxxxxxx",
  "donor_id": 123
}
```
**Database Actions:**
- Creates or finds donor by email
- Saves pending donation to Donations table
- Links donation to campaign if provided

### Create Subscription
```
POST /create-subscription
```
**Request Body:**
```json
{
  "plan_id": "supporter",    // "supporter", "advocate", or "champion"
  "email": "user@example.com",
  "name": "John Doe"
}
```
**Response:**
```json
{
  "subscription_id": "sub_xxxxxxxxxxxxx",
  "client_secret": "pi_xxx_secret_xxx",
  "customer_id": "cus_xxxxxxxxxxxxx",
  "donor_id": 123
}
```
**Database Actions:**
- Creates or finds donor by email
- Links donor to Stripe customer
- Saves subscription to donor_subscriptions table
- Updates donor subscription_status

### Get Subscription Status
```
GET /subscription-status/<subscription_id>
```
**Response:**
```json
{
  "status": "active",
  "current_period_end": 1234567890,
  "plan_id": "supporter",
  "amount": 6000
}
```

### Cancel Subscription
```
POST /cancel-subscription/<subscription_id>
```
**Response:**
```json
{
  "status": "cancelled",
  "cancel_at_period_end": true,
  "current_period_end": 1234567890
}
```

### Stripe Webhook Handler
```
POST /webhook
```
**Purpose:** Handles Stripe events and updates database
**Handled Events:**
- `payment_intent.succeeded` - Confirms donations
- `invoice.payment_succeeded` - Records subscription payments
- `customer.subscription.updated` - Updates subscription status
- `customer.subscription.deleted` - Handles cancellations

---

## 📊 Data Retrieval Endpoints

### Campaign Information

#### Get Single Campaign
```
GET /campaign/<campaign_id>
```
**Response:**
```json
{
  "status": "success",
  "data": {
    "campaign_id": 1,
    "name": "Emergency School Meals",
    "current_amount": 5000.00,
    "goal_amount": 25000.00,
    "progress_percentage": 20.0,
    "status": "active"
  }
}
```

#### Get All Campaigns
```
GET /campaigns
```
**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "campaign_id": 1,
      "name": "Emergency School Meals",
      "current_amount": 5000.00,
      "goal_amount": 25000.00,
      "progress_percentage": 20.0,
      "status": "active"
    }
  ]
}
```

#### Get Campaign Donations
```
GET /campaign/<campaign_id>/donations
```
**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "donation_id": 1,
      "amount": 100.00,
      "donated_at": "2024-01-15T10:30:00Z",
      "Donors": {"name": "John Doe", "email": "john@example.com"}
    }
  ],
  "total_donations": 15,
  "total_amount": 5000.00
}
```

### Donor Information

#### Get Single Donor
```
GET /donor/<donor_id>
```
**Response:**
```json
{
  "status": "success",
  "data": {
    "donor_id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "total_donated": 150.00,
    "subscription_status": "active",
    "stripe_customer_id": "cus_xxxxxxxxxxxxx",
    "active_subscription": {
      "plan_id": "supporter",
      "status": "active"
    },
    "donation_count": 3
  }
}
```

#### Get Donor by Email
```
GET /donor/email/<email>
```
**Response:** Same as Get Single Donor

#### Get Donor Donations
```
GET /donor/<donor_id>/donations
```
**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "donation_id": 1,
      "amount": 50.00,
      "payment_type": "one_time",
      "Campaigns": {"name": "Emergency School Meals"}
    }
  ],
  "total_donations": 3,
  "total_amount": 150.00
}
```

#### Get Donor Subscriptions
```
GET /donor/<donor_id>/subscriptions
```
**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "subscription_id": 1,
      "status": "active",
      "current_period_start": "2024-01-01T00:00:00Z",
      "current_period_end": "2024-02-01T00:00:00Z",
      "subscription_plans": {
        "name": "Supporter",
        "price_cents": 6000,
        "features": {"reports": "monthly", "badges": "basic"}
      }
    }
  ]
}
```

### Subscription Management

#### Get Active Subscriptions
```
GET /subscriptions/active
```
**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "subscription_id": 1,
      "status": "active",
      "Donors": {"name": "John Doe", "email": "john@example.com"},
      "subscription_plans": {"name": "Supporter", "price_cents": 6000}
    }
  ],
  "total_active_subscriptions": 5
}
```

### Analytics

#### Get Payment Statistics
```
GET /stats
```
**Response:**
```json
{
  "status": "success",
  "data": {
    "total_donations_amount": 15000.00,
    "total_donations_count": 45,
    "monthly_recurring_revenue": 1200.00,
    "active_subscriptions": 8,
    "total_donors": 25,
    "total_campaigns": 3
  }
}
```

---

## 🗄️ Database Integration

### Tables Used

**Existing Tables (Enhanced):**
- `Campaigns` - Campaign data with auto-updated current_amount
- `Donors` - Donor profiles with Stripe customer IDs and subscription status
- `Donations` - All payments (one-time and subscription) with Stripe IDs

**New Tables:**
- `subscription_plans` - Subscription tier definitions
- `donor_subscriptions` - Active subscription tracking
- `donor_badges` - Badge rewards (optional)

### Automatic Updates

The system automatically:
- ✅ Updates campaign progress when donations are made
- ✅ Updates donor subscription status when subscriptions change
- ✅ Creates donation records for subscription payments
- ✅ Links all payments to Stripe for reconciliation

---

## 🧪 Testing

Run the test script to verify all endpoints:
```bash
python payment/test_payment_api.py
```

The test script will:
1. Test health check and plans
2. Test database-integrated payment creation
3. Test data retrieval endpoints
4. Verify database saves are working

---

## 🔗 Integration Notes

**Frontend Integration:**
- Use `/create-payment-intent` for one-time donations
- Use `/create-subscription` for monthly subscriptions
- Use data endpoints to display campaign progress and user dashboards

**Database Requirements:**
- Run `subscription_tables.sql` to create required tables
- Ensure Supabase connection is configured in `.env`

**Stripe Configuration:**
- Set up webhook endpoint pointing to `/webhook`
- Configure webhook to send payment events
