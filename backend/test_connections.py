#!/usr/bin/env python3
"""
Test script to verify Stripe and Supabase API connections
Run this to make sure your .env file is configured correctly
"""

import os
from dotenv import load_dotenv
import stripe
from supabase import create_client

# Load environment variables
load_dotenv()

def test_env_variables():
    """Check if all required environment variables are set"""
    print("🔧 Testing Environment Variables...")
    
    required_vars = [
        'STRIPE_SECRET_KEY',
        'STRIPE_PUBLISHABLE_KEY', 
        'SUPABASE_URL',
        'SUPABASE_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f"your_{var.lower()}_here":
            missing_vars.append(var)
            print(f"❌ {var}: NOT SET")
        else:
            print(f"✅ {var}: {'*' * 20}")  # Mask the actual value
    
    if missing_vars:
        print(f"\n⚠️  Please set these variables in your .env file: {', '.join(missing_vars)}")
        return False
    
    print("✅ All environment variables are set!\n")
    return True

def test_stripe_connection():
    """Test Stripe API connection"""
    print("💳 Testing Stripe Connection...")
    
    try:
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        # Test with a simple API call
        account = stripe.Account.retrieve()
        print(f"✅ Stripe Connected Successfully!")
        print(f"   Account ID: {account.id}")
        print(f"   Country: {account.country}")
        print(f"   Currency: {account.default_currency}")
        return True
        
    except Exception as e:
        if 'stripe' in locals():
            if hasattr(e, '__class__') and 'AuthenticationError' in str(e.__class__):
                print(f"❌ Stripe Authentication Failed: {e}")
            else:
                print(f"❌ Stripe Connection Error: {e}")
        else:
            print(f"❌ Stripe Import Error: {e}")
        return False

def test_supabase_connection():
    """Test Supabase API connection"""
    print("\n🗄️  Testing Supabase Connection...")
    
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Test with a simple query (this will fail if connection is bad)
        # We'll try to list tables or do a simple query
        response = supabase.table("Campaigns").select("count", count="exact").execute()
        print(f"✅ Supabase Connected Successfully!")
        print(f"   URL: {supabase_url}")
        print(f"   Campaigns table accessible: Yes")
        return True
        
    except Exception as e:
        print(f"❌ Supabase Connection Error: {e}")
        print("   Make sure your SUPABASE_URL and SUPABASE_KEY are correct")
        print("   and that the Campaigns table exists in your database")
        return False

def main():
    print("🚀 API Connection Test\n")
    
    # Test 1: Environment Variables
    if not test_env_variables():
        return
    
    # Test 2: Stripe Connection  
    stripe_ok = test_stripe_connection()
    
    # Test 3: Supabase Connection
    supabase_ok = test_supabase_connection()
    
    # Summary
    print("\n" + "="*50)
    print("📊 CONNECTION TEST SUMMARY")
    print("="*50)
    print(f"Stripe API:    {'✅ CONNECTED' if stripe_ok else '❌ FAILED'}")
    print(f"Supabase API:  {'✅ CONNECTED' if supabase_ok else '❌ FAILED'}")
    
    if stripe_ok and supabase_ok:
        print("\n🎉 All connections successful! You're ready to test payments.")
    else:
        print("\n⚠️  Please fix the failed connections before proceeding.")

if __name__ == "__main__":
    main()
