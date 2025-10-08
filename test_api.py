"""
Mailtrap API Diagnostic Tool
Tests your API token and connection
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_mailtrap_api():
    """Test Mailtrap API connection and token"""
    
    print("🔍 Mailtrap API Diagnostic Tool")
    print("="*60)
    
    # Get token
    api_token = os.getenv('MAILTRAP_API_TOKEN')
    
    if not api_token:
        print("❌ No API token found in .env file")
        return
    
    print(f"✅ API Token found: {api_token[:10]}...{api_token[-10:]}")
    print()
    
    # Test 1: Check API endpoint
    print("📍 Test 1: Testing API endpoint...")
    url = "https://send.api.mailtrap.io/api/send"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Simple test payload
    payload = {
        "from": {
            "email": "test@example.com",
            "name": "Test Sender"
        },
        "to": [
            {
                "email": "test@example.com"
            }
        ],
        "subject": "Test Email",
        "text": "This is a test",
        "html": "<p>This is a test</p>"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS! API is working correctly")
            print("🎉 You can now send emails with email_sender_api.py")
        elif response.status_code == 401:
            print("❌ UNAUTHORIZED ERROR")
            print()
            print("Possible causes:")
            print("1. Invalid API token")
            print("2. Token doesn't have 'Sending' permission")
            print("3. Using Testing API token instead of Sending API token")
            print()
            print("🔧 Solutions:")
            print("1. Go to: https://mailtrap.io/api-tokens")
            print("2. Make sure you're in 'Sending' section (not 'Testing')")
            print("3. Create a new API token with 'Send Email' permission")
            print("4. Copy the NEW token to your .env file")
        elif response.status_code == 422:
            print("❌ VALIDATION ERROR")
            print()
            print("This usually means:")
            print("1. Email format is incorrect")
            print("2. Sending domain not verified")
            print()
            print("🔧 Solutions:")
            print("1. Verify your sending domain in Mailtrap")
            print("2. Go to: https://mailtrap.io/sending/domains")
            print("3. Add and verify your domain")
        else:
            print(f"❌ UNEXPECTED ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    # Test 2: Check if using sandbox token
    print()
    print("📍 Test 2: Checking token type...")
    
    # Try sandbox endpoint
    sandbox_url = "https://sandbox.api.mailtrap.io/api/send"
    
    try:
        sandbox_response = requests.post(sandbox_url, json=payload, headers=headers)
        
        if sandbox_response.status_code != 404:
            print("⚠️  WARNING: Your token might be for Testing/Sandbox")
            print("   You need a SENDING API token, not a Testing token")
            print()
            print("🔧 How to get the right token:")
            print("   1. Go to: https://mailtrap.io")
            print("   2. Click 'Sending' in sidebar (NOT 'Testing')")
            print("   3. Go to 'Sending Domains' or 'API Tokens'")
            print("   4. Create new token for SENDING")
        else:
            print("✅ Token type looks correct (for Sending API)")
            
    except Exception as e:
        print(f"Info: {e}")
    
    print()
    print("="*60)
    print("📚 Additional Resources:")
    print("- Mailtrap Sending API Docs: https://api-docs.mailtrap.io/docs/mailtrap-api-docs/")
    print("- Get API Tokens: https://mailtrap.io/api-tokens")
    print("- Verify Domains: https://mailtrap.io/sending/domains")
    print("="*60)


if __name__ == "__main__":
    test_mailtrap_api()
