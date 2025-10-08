"""
PRODUCTION EMAIL SENDER - VERIFIED DOMAIN READY
Sends emails to REAL recipients using verified Mailtrap domain
"""

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import pandas as pd
from templates import *
from datetime import datetime

# Load environment variables
load_dotenv()


class ProductionEmailSender:
    """Production-ready email sender with verified domain"""
    
    def __init__(self):
        self.host = os.getenv('MAILTRAP_HOST', 'bulk.smtp.mailtrap.io')
        self.port = int(os.getenv('MAILTRAP_PORT', 587))
        self.username = os.getenv('MAILTRAP_USERNAME')
        self.password = os.getenv('MAILTRAP_PASSWORD')
        self.from_email = os.getenv('EMAIL_FROM', 'admin@zoutedevelopers.tech')
        self.from_name = os.getenv('EMAIL_FROM_NAME', 'ZouteDevelopers')
        
        # Validate credentials
        if not self.username or not self.password:
            raise ValueError("⚠️  Production credentials not found in .env file!")
        
        print(f"✅ Production SMTP Configured")
        print(f"   Host: {self.host}")
        print(f"   Port: {self.port}")
        print(f"   From: {self.from_email}")
    
    def create_email(self, to_email, gym_name, contact_number=None, isWebsite=None):
        """Create personalized email message"""
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['To'] = to_email
        msg['Subject'] = f"Partnership Opportunity with {gym_name}"
        
        # Plain text version
        text_content = f"""
Hello {gym_name} Team,

We hope this email finds you well!

We are reaching out to explore potential partnership opportunities with {gym_name}.

{f'Phone: {contact_number}' if contact_number else ''}

We would love to discuss how we can work together to benefit your members.

Best regards,
{self.from_name}
        """
        
        # HTML version (professional template)
        if (isWebsite == 'Yes' or isWebsite == 'yes' or isWebsite == 'YES'):
            html_content = export_html_template(first_name=gym_name)
        else:
            html_content = export_html_websitenotfound_template(first_name=gym_name)

        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    def send_email(self, to_email, gym_name, contact_number=None, isWebsite=None):
        """
        Send a single email with STARTTLS authentication
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create message
            msg = self.create_email(to_email, gym_name, contact_number, isWebsite)
            
            # Connect with STARTTLS (production security)
            with smtplib.SMTP(self.host, self.port, timeout=30) as server:
                server.starttls()  # Enable TLS encryption
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True, f"✅ Email sent successfully to {to_email}"
            
        except smtplib.SMTPAuthenticationError as e:
            return False, f"❌ Authentication failed: {str(e)}"
        except smtplib.SMTPException as e:
            return False, f"❌ SMTP error: {str(e)}"
        except Exception as e:
            return False, f"❌ Failed: {str(e)}"
    
    def send_bulk_emails(self, df, delay=2, max_emails=None, start_from=0):
        """
        Send emails to multiple recipients with production safety features
        
        Args:
            df: DataFrame with email addresses
            delay: Seconds between emails (rate limiting)
            max_emails: Maximum number of emails to send (None = all)
            start_from: Start from this row number (for resuming)
        
        Returns:
            dict: Statistics about the campaign
        """
        print("\n" + "="*60)
        print("📧 PRODUCTION EMAIL CAMPAIGN")
        print("="*60)
        
        stats = {
            'total_rows': len(df),
            'emails_sent': 0,
            'emails_failed': 0,
            'skipped': 0,
            'start_time': datetime.now()
        }
        
        # Column names
        email_col = 'Unnamed: 4' if 'Unnamed: 4' in df.columns else 'Email'
        name_col = 'Unnamed: 0' if 'Unnamed: 0' in df.columns else 'Gym Name'
        phone_col = 'Unnamed: 1' if 'Unnamed: 1' in df.columns else 'Contact Number'
        website_col = 'Unnamed: 5' if 'Unnamed: 5' in df.columns else 'Website'
        
        print(f"📊 Total rows: {stats['total_rows']}")
        print(f"📧 Email column: {email_col}")
        print(f"🏋️  Name column: {name_col}")
        print(f"📞 Phone column: {phone_col}")
        print(f"⏱️  Delay between emails: {delay} seconds")
        if max_emails:
            print(f"🎯 Max emails to send: {max_emails}")
        if start_from > 0:
            print(f"▶️  Starting from row: {start_from}")
        print()
        
        emails_sent_this_session = 0
        
        for idx, row in df.iterrows():
            # Skip until start_from
            if idx < start_from:
                continue
            
            # Check max_emails limit
            if max_emails and emails_sent_this_session >= max_emails:
                print(f"\n🎯 Reached max email limit ({max_emails})")
                break
            
            # Extract data
            email = row.get(email_col)
            gym_name = row.get(name_col, 'Gym')
            phone = row.get(phone_col, '')
            isWebsite = row.get(website_col, 'No')
            
            # Validate email
            if pd.isna(email) or not isinstance(email, str) or '@' not in email:
                print(f"⏭️  Row {idx}: Skipping '{gym_name}' - No valid email")
                stats['skipped'] += 1
                continue
            
            # Send email
            print(f"\n📬 [{idx}] Sending to: {email} ({gym_name})")
            success, message = self.send_email(email, gym_name, phone, isWebsite)
            
            if success:
                print(f"   {message}")
                stats['emails_sent'] += 1
                emails_sent_this_session += 1
            else:
                print(f"   {message}")
                stats['emails_failed'] += 1
            
            # Rate limiting (skip delay on last email)
            if emails_sent_this_session < (max_emails or float('inf')) and idx < len(df) - 1:
                print(f"   ⏳ Waiting {delay} seconds...")
                time.sleep(delay)
        
        # Final statistics
        stats['end_time'] = datetime.now()
        stats['duration'] = (stats['end_time'] - stats['start_time']).total_seconds()
        
        print("\n" + "="*60)
        print("📊 CAMPAIGN SUMMARY")
        print("="*60)
        print(f"✅ Emails sent: {stats['emails_sent']}")
        print(f"❌ Failed: {stats['emails_failed']}")
        print(f"⏭️  Skipped: {stats['skipped']}")
        print(f"⏱️  Duration: {stats['duration']:.1f} seconds")
        print(f"📈 Success rate: {stats['emails_sent']/(stats['emails_sent']+stats['emails_failed'])*100:.1f}%" if (stats['emails_sent']+stats['emails_failed']) > 0 else "N/A")
        print("="*60)
        
        return stats


def main():
    """Main function - Production email campaign"""
    
    print("🚀 PRODUCTION EMAIL SENDER")
    print("="*60)
    print("⚠️  WARNING: This sends REAL emails to REAL recipients!")
    print("="*60)
    
    # Initialize sender
    try:
        sender = ProductionEmailSender()
    except ValueError as e:
        print(f"\n❌ {e}")
        return
    
    # Load data
    print("\n📥 Loading gym data from Google Sheets...")
    sheet_id = "1uDufrhJdfYPgbNAPw7sLbxpbXfrnt4_fZzVWlkyGw7Y"
    gid = "1085790850"
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    try:
        df = pd.read_csv(sheet_url)
        print(f"✅ Loaded {len(df)} rows")
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return
    
    # Preview data
    print("\n📋 Data Preview (first 3 rows with emails):")
    email_col = 'Unnamed: 4' if 'Unnamed: 4' in df.columns else 'Email'
    preview = df[df[email_col].notna()].head(3)
    print(preview[['Unnamed: 0', 'Unnamed: 1', email_col]].to_string())
    
    # Count valid emails
    valid_emails = df[df[email_col].notna() & df[email_col].str.contains('@', na=False)]
    
    # Campaign options
    print("\n" + "="*60)
    print("🎯 CAMPAIGN OPTIONS")
    print("="*60)
    print(f"📧 Valid emails found: {len(valid_emails)}")
    print(f"📨 From: {os.getenv('EMAIL_FROM', 'admin@zoutedevelopers.tech')}")
    print(f"🌐 Domain: zoutedevelopers.tech ✅ VERIFIED")
    print()
    print("Choose campaign mode:")
    print("  1. 🧪 TEST MODE (send 3 test emails)")
    print("  2. 📦 BATCH MODE (send 10 emails)")
    print("  3. 🚀 FULL CAMPAIGN (send to all 57+ emails)")
    print("  4. 🎯 CUSTOM (specify start position and count)")
    print("  5. ❌ CANCEL")
    print()
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == '1':
        # Test mode
        print("\n🧪 TEST MODE: Sending 3 test emails...")
        confirm = input("Proceed? (yes/no): ").lower().strip()
        if confirm == 'yes':
            stats = sender.send_bulk_emails(df, delay=2, max_emails=3)
    
    elif choice == '2':
        # Batch mode
        print("\n📦 BATCH MODE: Sending 10 emails...")
        confirm = input("Proceed? (yes/no): ").lower().strip()
        if confirm == 'yes':
            stats = sender.send_bulk_emails(df, delay=2, max_emails=10)
    
    elif choice == '3':
        # Full campaign
        print(f"\n🚀 FULL CAMPAIGN: Sending to ALL {len(valid_emails)} emails...")
        print("⚠️  This will take approximately", len(valid_emails) * 2 / 60, "minutes")
        confirm = input("\n⚠️  ARE YOU SURE? Type 'SEND ALL' to confirm: ").strip()
        if confirm == 'SEND ALL':
            stats = sender.send_bulk_emails(df, delay=2)
        else:
            print("❌ Campaign cancelled")
    
    elif choice == '4':
        # Custom
        print("\n🎯 CUSTOM MODE")
        try:
            start = int(input("Start from row number (0 = beginning): ").strip())
            count = int(input("How many emails to send: ").strip())
            print(f"\n📧 Will send {count} emails starting from row {start}")
            confirm = input("Proceed? (yes/no): ").lower().strip()
            if confirm == 'yes':
                stats = sender.send_bulk_emails(df, delay=2, max_emails=count, start_from=start)
        except ValueError:
            print("❌ Invalid input")
    
    else:
        print("❌ Campaign cancelled")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
