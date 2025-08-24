#!/usr/bin/env python3
"""
Test script to verify database schema for payment system
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

def test_database_tables():
    """Check if all required tables exist"""
    print("🗄️ Testing Database Schema...")
    
    try:
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        
        required_tables = [
            "Campaigns",
            "Donors", 
            "Donations",
            "SubscriptionPlans",
            "DonorSubscriptions"
        ]
        
        print("Checking for required tables:")
        
        for table in required_tables:
            try:
                # Try to query the table (with limit 0 to avoid getting data)
                response = supabase.table(table).select("*").limit(0).execute()
                print(f"  ✅ {table}: EXISTS")
            except Exception as e:
                print(f"  ❌ {table}: NOT FOUND - {e}")
                return False
                
        print("\n🔍 Checking subscription plans data:")
        plans = supabase.table("SubscriptionPlans").select("plan_id, name, price_cents").execute()
        if plans.data:
            for plan in plans.data:
                print(f"  ✅ {plan['plan_id']}: {plan['name']} - ${plan['price_cents']/100:.2f}/month")
        else:
            print("  ⚠️  No subscription plans found - check your database setup")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_sample_campaign():
    """Create a test campaign for payment testing"""
    print("\n🎯 Creating Test Campaign...")
    
    try:
        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        
        # Check if test campaign already exists
        existing = supabase.table("Campaigns").select("*").eq("name", "Test Payment Campaign").execute()
        
        if existing.data:
            campaign = existing.data[0]
            print(f"  ✅ Test campaign already exists (ID: {campaign['campaign_id']})")
        else:
            # Create test campaign
            campaign_data = {
                "name": "Test Payment Campaign",
                "description": "Campaign for testing payment functionality", 
                "status": "active",
                "goal_amount": 1000.00,
                "end_date": "2024-12-31"
            }
            
            result = supabase.table("Campaigns").insert(campaign_data).execute()
            if result.data:
                campaign = result.data[0]
                print(f"  ✅ Created test campaign (ID: {campaign['campaign_id']})")
            else:
                print("  ❌ Failed to create test campaign")
                return None
                
        return campaign
        
    except Exception as e:
        print(f"❌ Error creating test campaign: {e}")
        return None

def main():
    print("🚀 Database Schema Test\n")
    
    # Test database tables
    tables_ok = test_database_tables()
    
    if tables_ok:
        # Create test campaign
        test_campaign = test_sample_campaign()
        
        if test_campaign:
            print(f"\n🎉 Database is ready for payment testing!")
            print(f"   Test Campaign ID: {test_campaign['campaign_id']}")
            print(f"   Test Campaign Goal: ${test_campaign['goal_amount']}")
        else:
            print(f"\n⚠️  Database tables exist but couldn't create test campaign")
    else:
        print(f"\n❌ Database schema is incomplete. Please:")
        print(f"   1. Check your database tables exist")
        print(f"   2. Verify subscription plans are properly configured")

if __name__ == "__main__":
    main()
