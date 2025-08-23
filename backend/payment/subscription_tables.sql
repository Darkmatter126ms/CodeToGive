-- Subscription System Database Schema
-- This file adds subscription functionality to your existing Campaigns, Donors, and Donations tables

-- ============================================================================
-- EXTEND EXISTING TABLES (Add columns to your current tables)
-- ============================================================================

-- Extend Donors table for Stripe integration
ALTER TABLE Donors 
ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(100),
ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(50) DEFAULT 'none'; -- 'none', 'active', 'canceled', 'past_due'

-- Extend Donations table for subscription tracking
ALTER TABLE Donations
ADD COLUMN IF NOT EXISTS subscription_id INTEGER,
ADD COLUMN IF NOT EXISTS stripe_payment_intent_id VARCHAR(100),
ADD COLUMN IF NOT EXISTS payment_type VARCHAR(50) DEFAULT 'one_time'; -- 'one_time', 'subscription'

-- ============================================================================
-- NEW TABLES (Required for subscription functionality)
-- ============================================================================

-- 1. Subscription Plans Table (stores the 3 tiers: $60/$120/$500)
CREATE TABLE IF NOT EXISTS subscription_plans (
    plan_id VARCHAR(50) PRIMARY KEY,        -- 'supporter', 'advocate', 'champion'
    name VARCHAR(100) NOT NULL,             -- 'Supporter', 'Advocate', 'Champion'
    price_cents INTEGER NOT NULL,           -- 6000, 12000, 50000 (price in cents)
    currency VARCHAR(3) DEFAULT 'usd',      -- 'usd'
    interval_type VARCHAR(20) DEFAULT 'month', -- 'month', 'year'
    features JSONB,                         -- Plan features (reports, badges, etc.)
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Donor Subscriptions Table (tracks active subscriptions)
CREATE TABLE IF NOT EXISTS donor_subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    donor_id INTEGER NOT NULL,              -- Links to Donors table
    plan_id VARCHAR(50) NOT NULL,           -- Links to subscription_plans
    stripe_subscription_id VARCHAR(100) UNIQUE, -- Stripe subscription ID
    status VARCHAR(50) NOT NULL,            -- 'active', 'canceled', 'past_due', 'trialing'
    current_period_start TIMESTAMP,         -- Current billing period start
    current_period_end TIMESTAMP,           -- Current billing period end  
    cancel_at_period_end BOOLEAN DEFAULT false, -- Will cancel when period ends
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. Donor Badges Table (optional - for reward system)
CREATE TABLE IF NOT EXISTS donor_badges (
    badge_id SERIAL PRIMARY KEY,
    donor_id INTEGER NOT NULL,              -- Links to Donors table
    badge_type VARCHAR(100) NOT NULL,       -- 'milestone_100', 'loyal_supporter', 'champion_level'
    badge_name VARCHAR(100) NOT NULL,       -- Human readable name
    earned_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB                          -- Badge details (image URL, description, etc.)
);

-- ============================================================================
-- ADD FOREIGN KEY CONSTRAINTS (Links between tables)
-- ============================================================================

-- Link donor_subscriptions to existing tables
ALTER TABLE donor_subscriptions
ADD CONSTRAINT IF NOT EXISTS fk_donor_subscriptions_donor_id 
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id) ON DELETE CASCADE,
ADD CONSTRAINT IF NOT EXISTS fk_donor_subscriptions_plan_id 
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(plan_id);

-- Link donations to subscriptions
ALTER TABLE Donations
ADD CONSTRAINT IF NOT EXISTS fk_donations_subscription_id 
    FOREIGN KEY (subscription_id) REFERENCES donor_subscriptions(subscription_id);

-- Link badges to donors
ALTER TABLE donor_badges
ADD CONSTRAINT IF NOT EXISTS fk_donor_badges_donor_id 
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id) ON DELETE CASCADE;

-- ============================================================================
-- INSERT DEFAULT SUBSCRIPTION PLANS
-- ============================================================================

INSERT INTO subscription_plans (plan_id, name, price_cents, features) VALUES
('supporter', 'Supporter', 6000, '{
    "reports": "monthly", 
    "badges": "basic", 
    "leaderboard": true,
    "description": "Monthly impact reports and basic badge collection"
}'),
('advocate', 'Advocate', 12000, '{
    "reports": "weekly", 
    "badges": "advanced", 
    "leaderboard": true, 
    "exclusive_campaigns": true,
    "description": "Weekly reports, advanced badges, and exclusive campaign access"
}'),
('champion', 'Champion', 50000, '{
    "reports": "real_time", 
    "badges": "premium", 
    "leaderboard": true, 
    "vip_access": true, 
    "personal_reports": true,
    "description": "Real-time tracking, premium badges, VIP access, and personalized reports"
}')
ON CONFLICT (plan_id) DO NOTHING;

-- ============================================================================
-- CREATE INDEXES (For better query performance)
-- ============================================================================

-- Indexes on new columns
CREATE INDEX IF NOT EXISTS idx_donors_stripe_customer ON Donors(stripe_customer_id);
CREATE INDEX IF NOT EXISTS idx_donors_subscription_status ON Donors(subscription_status);
CREATE INDEX IF NOT EXISTS idx_donations_subscription_id ON Donations(subscription_id);
CREATE INDEX IF NOT EXISTS idx_donations_stripe_intent ON Donations(stripe_payment_intent_id);
CREATE INDEX IF NOT EXISTS idx_donations_payment_type ON Donations(payment_type);

-- Indexes on new tables
CREATE INDEX IF NOT EXISTS idx_donor_subscriptions_donor_id ON donor_subscriptions(donor_id);
CREATE INDEX IF NOT EXISTS idx_donor_subscriptions_stripe_id ON donor_subscriptions(stripe_subscription_id);
CREATE INDEX IF NOT EXISTS idx_donor_subscriptions_status ON donor_subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_donor_badges_donor_id ON donor_badges(donor_id);
CREATE INDEX IF NOT EXISTS idx_donor_badges_type ON donor_badges(badge_type);

-- ============================================================================
-- HELPER FUNCTIONS (Call these from your backend code)
-- ============================================================================

-- Note: Instead of triggers, call these functions from your Python backend code
-- This gives you more control and easier debugging during development

-- Example usage in Python:
-- After creating a donation, call: update_campaign_progress(campaign_id)
-- After updating subscription, call: update_donor_subscription_status(donor_id)

-- ============================================================================
-- SUMMARY
-- ============================================================================

-- This script adds:
-- 1. 2 new columns to Donors table (stripe_customer_id, subscription_status)
-- 2. 3 new columns to Donations table (subscription_id, stripe_payment_intent_id, payment_type)
-- 3. 3 new tables (subscription_plans, donor_subscriptions, donor_badges)
-- 4. Foreign key constraints to link everything together
-- 5. Indexes for performance
-- 6. Default subscription plans ($60/$120/$500)

-- Your existing Campaigns, Donors, and Donations tables remain fully functional!
-- One-time donations continue to work exactly as before.
-- Subscription functionality is added on top of your existing structure.

-- Data updates (like campaign progress) should be handled in your Python backend code
-- for better control and easier debugging during development.
