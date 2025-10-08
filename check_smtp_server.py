"""
Mailtrap Server Configuration Checker
Help identify if you're using the right SMTP server for production
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("🔍 MAILTRAP SMTP SERVER ANALYSIS")
print("="*70)
print()

current_host = os.getenv('MAILTRAP_HOST', 'Not set')
print(f"Current SMTP Host: {current_host}")
print()

print("="*70)
print("📊 MAILTRAP SMTP SERVER TYPES")
print("="*70)
print()

servers = {
    "sandbox.smtp.mailtrap.io": {
        "purpose": "Testing/Development",
        "delivers_to": "Mailtrap inbox ONLY",
        "description": "Catches all emails - nothing goes to real recipients",
        "use_case": "Safe testing environment"
    },
    "bulk.smtp.mailtrap.io": {
        "purpose": "Bulk Testing API",
        "delivers_to": "Mailtrap inbox ONLY (maybe)",
        "description": "API endpoint for bulk operations, might still intercept emails",
        "use_case": "Testing bulk email functionality"
    },
    "live.smtp.mailtrap.io": {
        "purpose": "Production Sending",
        "delivers_to": "REAL recipient inboxes",
        "description": "Actually sends emails to real people",
        "use_case": "Production email campaigns"
    },
    "send.smtp.mailtrap.io": {
        "purpose": "Production Sending (Alternative)",
        "delivers_to": "REAL recipient inboxes",
        "description": "Production sending endpoint (some accounts use this)",
        "use_case": "Production email campaigns"
    }
}

for server, info in servers.items():
    indicator = "👉 YOU ARE HERE" if server == current_host else "   "
    print(f"{indicator} Server: {server}")
    print(f"    Purpose: {info['purpose']}")
    print(f"    Delivers to: {info['delivers_to']}")
    print(f"    Description: {info['description']}")
    print(f"    Use case: {info['use_case']}")
    print()

print("="*70)
print("🎯 DIAGNOSIS")
print("="*70)
print()

if current_host == "sandbox.smtp.mailtrap.io":
    print("❌ You're using SANDBOX mode")
    print("   Emails go to Mailtrap inbox only - NOT to real recipients")
    print()
    print("✅ FIX: Change to live.smtp.mailtrap.io or send.smtp.mailtrap.io")
    
elif current_host == "bulk.smtp.mailtrap.io":
    print("⚠️  You're using BULK API mode")
    print("   This might still be intercepting your emails!")
    print()
    print("✅ FIX: Change to live.smtp.mailtrap.io or send.smtp.mailtrap.io")
    
elif current_host == "live.smtp.mailtrap.io":
    print("✅ You're using PRODUCTION mode (correct!)")
    print("   Emails should go to real recipients")
    print()
    print("If emails still not arriving:")
    print("   1. Check recipient spam folders")
    print("   2. Verify domain is actually verified in Mailtrap")
    print("   3. Check Mailtrap dashboard for any sending limits")
    
elif current_host == "send.smtp.mailtrap.io":
    print("✅ You're using PRODUCTION mode (correct!)")
    print("   Emails should go to real recipients")
    print()
    print("If emails still not arriving:")
    print("   1. Check recipient spam folders")
    print("   2. Verify domain is actually verified in Mailtrap")
    print("   3. Check Mailtrap dashboard for any sending limits")
    
else:
    print("❓ Unknown SMTP server")
    print(f"   Current: {current_host}")
    print()
    print("Please check your Mailtrap dashboard for the correct server")

print()
print("="*70)
print("🔑 WHERE TO FIND THE CORRECT SERVER")
print("="*70)
print()
print("1. Go to: https://mailtrap.io")
print("2. Click 'Sending' (NOT 'Testing') in left sidebar")
print("3. Click 'Sending Domains'")
print("4. Click on 'zoutedevelopers.tech'")
print("5. Look for 'SMTP Settings' or 'Credentials' tab")
print()
print("You should see:")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("Host: live.smtp.mailtrap.io")
print("      OR")
print("Host: send.smtp.mailtrap.io")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()
print("⚠️  If you see 'bulk.smtp.mailtrap.io', look for a different")
print("    section labeled 'Production' or 'Live Sending'")
print()
print("="*70)
print()
print("💡 QUICK FIX:")
print("="*70)
print()
print("Try updating your .env file with:")
print()
print("MAILTRAP_HOST=live.smtp.mailtrap.io")
print()
print("Then run production_sender.py again")
print()
print("="*70)
