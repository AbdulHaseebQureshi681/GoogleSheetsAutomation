"""
Advanced Mailtrap API Diagnostic
Checks token, domain, and API setup
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def advanced_diagnostics():
    """Run advanced diagnostics on Mailtrap API setup"""
    
    print("🔍 Advanced Mailtrap API Diagnostic")
    print("="*70)
    
    api_token = os.getenv('MAILTRAP_API_TOKEN')
    email_from = os.getenv('EMAIL_FROM', 'test@example.com')
    
    print(f"✅ API Token: {api_token[:15]}...{api_token[-10:]}")
    print(f"✅ From Email: {email_from}")
    print()
    
    # Extract domain from email
    domain = email_from.split('@')[1] if '@' in email_from else 'unknown'
    print(f"📧 Sending Domain: {domain}")
    print()
    
    # Test 1: Check API with your actual email
    print("="*70)
    print("📍 Test 1: Sending test email with your FROM address")
    print("="*70)
    
    url = "https://send.api.mailtrap.io/api/send"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": {
            "email": email_from,
            "name": os.getenv('EMAIL_FROM_NAME', 'Test Sender')
        },
        "to": [{"email": email_from}],  # Send to yourself
        "subject": "Mailtrap API Test",
        "text": "Testing Mailtrap API",
        "html": "<p>Testing Mailtrap API</p>"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        print()
        
        if response.status_code == 200:
            print("✅✅✅ SUCCESS! Email sent!")
            print("Check your inbox (or spam folder)")
            return True
        elif response.status_code == 401:
            print("❌ UNAUTHORIZED - Token is invalid")
            print()
            print("🔍 Debugging steps:")
            print("1. Are you logged into the CORRECT Mailtrap account?")
            print("2. Did you copy the ENTIRE token (no spaces)?")
            print("3. Is the token from 'Sending' section?")
            print()
            print("🔄 Try this:")
            print("1. Go to: https://mailtrap.io/home")
            print("2. Make sure you're in the right workspace")
            print("3. Click 'Sending' in sidebar")
            print("4. Click 'Sending Domains'")
            print("5. Click on your domain")
            print("6. Look for 'API Integration' or 'API Tokens'")
            print("7. Generate a NEW token")
            print("8. Copy the ENTIRE token carefully")
            
        elif response.status_code == 403:
            print("❌ FORBIDDEN - Domain or permission issue")
            print()
            print("🔧 Solutions:")
            print(f"1. Verify domain '{domain}' in Mailtrap")
            print("2. Check DNS records are correct")
            print("3. Wait for domain verification (can take up to 48 hours)")
            
        elif response.status_code == 422:
            print("❌ VALIDATION ERROR")
            print()
            print("Response details:", response.json())
            
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    # Test 2: Try with mailtrap.io domain
    print()
    print("="*70)
    print("📍 Test 2: Trying with Mailtrap's verified domain")
    print("="*70)
    
    # Mailtrap provides a default sending address
    payload2 = {
        "from": {
            "email": "hello@demomailtrap.com",  # Mailtrap's verified domain
            "name": "Test Sender"
        },
        "to": [{"email": email_from}],
        "subject": "Mailtrap API Test (Demo Domain)",
        "text": "Testing with demo domain",
        "html": "<p>Testing with demo domain</p>"
    }
    
    try:
        response2 = requests.post(url, json=payload2, headers=headers)
        print(f"Status Code: {response2.status_code}")
        print(f"Response: {response2.text}")
        print()
        
        if response2.status_code == 200:
            print("✅ SUCCESS with demo domain!")
            print("This means your token IS valid!")
            print()
            print("⚠️  The issue is with YOUR sending domain")
            print(f"   Domain '{domain}' needs to be verified")
            print()
            print("🔧 Fix:")
            print(f"1. Go to: https://mailtrap.io/sending/domains")
            print(f"2. Verify domain: {domain}")
            print(f"3. Add required DNS records")
            print(f"4. Wait for verification")
            print()
            print("OR")
            print()
            print("🔧 Quick workaround:")
            print("   Use 'hello@demomailtrap.com' as your FROM address")
            print("   Update .env: EMAIL_FROM=hello@demomailtrap.com")
            return True
        elif response2.status_code == 401:
            print("❌ Still unauthorized - Token is definitely invalid")
            print()
            print("🚨 ACTION REQUIRED:")
            print("Your API token is NOT working. You need to:")
            print("1. Delete current token in Mailtrap")
            print("2. Create a BRAND NEW token")
            print("3. Make sure you're in 'Sending' (not 'Testing')")
            print("4. Copy the entire token")
            print("5. Replace in .env file")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()
    print("="*70)
    print("📚 Key Points:")
    print("="*70)
    print("• Mailtrap has TWO separate APIs:")
    print("  - Testing API (for Email Testing inbox)")
    print("  - Sending API (for real email sending)")
    print()
    print("• You need a token from the SENDING API")
    print("• Location: Sending → Sending Domains → Your Domain → API")
    print()
    print("• If still not working, try:")
    print("  - Use a different email service (SendGrid, Mailgun)")
    print("  - Or use SMTP method (email_sender.py)")
    print("="*70)
    
    return False


if __name__ == "__main__":
    success = advanced_diagnostics()
    
    if not success:
        print()
        print("💡 QUICK FIX: Use SMTP instead")
        print("   Your SMTP credentials are already working")
        print("   Run: python email_sender.py")
