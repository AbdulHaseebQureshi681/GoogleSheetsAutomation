"""
Mailtrap Sending Setup Diagnostic
Helps you set up real email sending with Mailtrap
"""

import os
from dotenv import load_dotenv

load_dotenv()

def check_mailtrap_sending_setup():
    """Check if Mailtrap is properly configured for real sending"""
    
    print("🔍 Mailtrap Sending Setup Diagnostic")
    print("="*70)
    print()
    
    # Check environment variables
    api_token = os.getenv('MAILTRAP_API_TOKEN')
    email_from = os.getenv('EMAIL_FROM')
    
    print("📋 Current Configuration:")
    print(f"  API Token: {api_token[:15]}...{api_token[-10:] if api_token else 'NOT SET'}")
    print(f"  From Email: {email_from}")
    
    if email_from:
        domain = email_from.split('@')[1]
        print(f"  Domain: {domain}")
    else:
        domain = None
    
    print()
    print("="*70)
    print("✅ CHECKLIST: What You Need for Real Email Sending")
    print("="*70)
    print()
    
    # Checklist
    checklist = [
        {
            "step": "1. Switch to 'Sending' Section",
            "details": [
                "Go to: https://mailtrap.io",
                "Click 'Sending' in left sidebar (NOT 'Testing')",
                "This is where real email sending is configured"
            ],
            "status": "❓"
        },
        {
            "step": "2. Add Sending Domain",
            "details": [
                "In 'Sending' section, click 'Sending Domains'",
                "Click 'Add Domain'",
                f"Enter your domain: {domain if domain else 'your-domain.com'}",
                "Mailtrap will show DNS records to add"
            ],
            "status": "❓"
        },
        {
            "step": "3. Add DNS Records",
            "details": [
                "Go to your domain registrar (GoDaddy, Namecheap, etc.)",
                "Add the DNS records Mailtrap provides:",
                "  - SPF record (TXT)",
                "  - DKIM record (TXT)",
                "  - DMARC record (TXT)",
                "Save and wait 24-48 hours for propagation"
            ],
            "status": "❓"
        },
        {
            "step": "4. Verify Domain",
            "details": [
                "Go back to Mailtrap → Sending → Sending Domains",
                "Your domain should show 'Verified' status",
                "If not verified, wait longer or check DNS records"
            ],
            "status": "❓"
        },
        {
            "step": "5. Get Sending API Token",
            "details": [
                "In Sending Domains, click on your VERIFIED domain",
                "Look for 'API Integration' or 'API Tokens' section",
                "Create a NEW token (not from Testing section!)",
                "Copy the entire token"
            ],
            "status": "❓"
        },
        {
            "step": "6. Update .env File",
            "details": [
                "Open your .env file",
                "Replace MAILTRAP_API_TOKEN with the new token",
                "Make sure it's from the Sending section"
            ],
            "status": "✅" if api_token else "❌"
        }
    ]
    
    for item in checklist:
        print(f"{item['status']} {item['step']}")
        for detail in item['details']:
            print(f"     {detail}")
        print()
    
    print("="*70)
    print("⚠️  IMPORTANT NOTES:")
    print("="*70)
    print()
    print("• Mailtrap 'Testing' ≠ Mailtrap 'Sending'")
    print("  - Testing: Emails go to your inbox only (sandbox)")
    print("  - Sending: Emails go to real recipients (production)")
    print()
    print("• Domain verification takes 24-48 hours")
    print("  - You cannot send real emails until domain is verified")
    print("  - Check DNS propagation: https://dnschecker.org")
    print()
    print("• Token from 'Testing' will NOT work for 'Sending'")
    print("  - You need a separate token from the Sending section")
    print("  - Current token might be from Testing (that's why 401 error)")
    print()
    print("="*70)
    print("🎯 YOUR NEXT STEPS:")
    print("="*70)
    print()
    
    if not domain:
        print("1. ❌ Set up your FROM email address in .env")
        print("   EMAIL_FROM=your-email@your-domain.com")
        print()
    
    print("2. 🌐 Go to Mailtrap 'Sending' section:")
    print("   https://mailtrap.io/sending/domains")
    print()
    print("3. ➕ Add your domain and get DNS records")
    print()
    print("4. 🔧 Add DNS records to your domain registrar")
    print()
    print("5. ⏰ Wait 24-48 hours for verification")
    print()
    print("6. 🔑 Get API token from VERIFIED domain")
    print()
    print("7. 📝 Update .env with new token")
    print()
    print("8. ✅ Test with: python email_sender_api.py")
    print()
    print("="*70)
    print()
    print("💡 ALTERNATIVE (If you can't wait 24-48 hours):")
    print("="*70)
    print()
    print("Use Mailtrap's SMTP for sending (same as testing, different server):")
    print("1. Go to: Sending → Sending Domains → Your Domain → SMTP")
    print("2. Get PRODUCTION SMTP credentials (different from testing)")
    print("3. Update email_sender.py with production SMTP server")
    print("4. Sends to real emails immediately (no DNS wait)")
    print()
    print("="*70)


if __name__ == "__main__":
    check_mailtrap_sending_setup()
