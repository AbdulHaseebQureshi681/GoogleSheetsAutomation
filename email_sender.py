"""
Email Sender with Mailtrap Integration
This script sends emails to addresses scraped from Google Sheets
"""
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import pandas as pd
from templates import *


# Load environment variables
load_dotenv()

class MailtrapSender:
    """Handle sending emails via Mailtrap SMTP"""
    
    def __init__(self):
        self.host = os.getenv('MAILTRAP_HOST', 'sandbox.smtp.mailtrap.io')
        self.port = int(os.getenv('MAILTRAP_PORT', 2525))
        self.username = os.getenv('MAILTRAP_USERNAME')
        self.password = os.getenv('MAILTRAP_PASSWORD')
        self.from_email = os.getenv('EMAIL_FROM', 'noreply@example.com')
        self.from_name = os.getenv('EMAIL_FROM_NAME', 'Fitness Outreach')
        
        # Validate credentials
        if not self.username or not self.password:
            raise ValueError("⚠️  Mailtrap credentials not found! Please set them in .env file")
    
    def create_email(self, to_email, gym_name, contact_number=None , isWebsite=None):
        """
        Create a personalized email message
        
        Args:
            to_email: Recipient's email address
            gym_name: Name of the gym
            contact_number: Phone number (optional)
        
        Returns:
            MIMEMultipart message object
        """
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

---
This is a test email sent via Mailtrap
        """
        
        # HTML version (more professional)
        if (isWebsite == 'Yes' or isWebsite == 'yes' or isWebsite == 'YES'):
            html_content = export_html_template(first_name=gym_name)
        else:
            print( isWebsite)
            html_content = export_html_websitenotfound_template(first_name=gym_name)

        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    def send_email(self, to_email, gym_name, contact_number=None , isWebsite=None):
        """
        Send an email via Mailtrap
        
        Args:
            to_email: Recipient's email address
            gym_name: Name of the gym
            contact_number: Phone number (optional)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create message
            msg = self.create_email(to_email, gym_name, contact_number , isWebsite)
            
            # Connect to Mailtrap
            with smtplib.SMTP(self.host, self.port) as server:
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True, f"✅ Email sent to {to_email}"
            
        except Exception as e:
            return False, f"❌ Failed to send to {to_email}: {str(e)}"
    
    def send_bulk_emails(self, df, delay=1):
        """
        Send emails to all valid addresses in the dataframe
        
        Args:
            df: Pandas DataFrame with email addresses
            delay: Seconds to wait between emails (rate limiting)
        
        Returns:
            dict: Statistics about sent emails
        """
        stats = {
            'total': 0,
            'sent': 0,
            'failed': 0,
            'skipped': 0,
            'results': []
        }
        
        print("\n" + "="*60)
        print("📧 Starting Bulk Email Campaign")
        print("="*60)
        
        # Identify email column (usually 'Unnamed: 4' based on your data)
        email_col = 'Unnamed: 4' if 'Unnamed: 4' in df.columns else 'Email'
        gym_col = 'Unnamed: 0' if 'Unnamed: 0' in df.columns else 'Gym Name'
        phone_col = 'Unnamed: 1' if 'Unnamed: 1' in df.columns else 'Contact Number'
        Website = 'Unnamed: 2' if 'Unnamed: 2' in df.columns else 'Website'
        
        
        print(f"📊 Found {len(df)} total rows")
        print(f"📧 Email column: {email_col}")
        print(f"🏋️  Gym name column: {gym_col}")
        print(f"📞 Phone column: {phone_col}\n")
        
        for index, row in df.iterrows():
            stats['total'] += 1
            
            # Get email and gym name
            email = row.get(email_col)
            gym_name = row.get(gym_col, f"Gym #{index}")
            phone = row.get(phone_col)
            isWebsite = row.get(Website)
            
            # Skip if no email or email is NaN
            if pd.isna(email) or not email or '@' not in str(email):
                print(f"⏭️  Row {index}: Skipping '{gym_name}' - No valid email")
                stats['skipped'] += 1
                continue
            
            # Send email
            print(f"\n📬 Sending to: {email} ({gym_name})")
            success, message = self.send_email(email, gym_name, phone , isWebsite)
            print(f"   {message}")
            
            stats['results'].append({
                'gym': gym_name,
                'email': email,
                'success': success,
                'message': message
            })
            
            if success:
                stats['sent'] += 1
            else:
                stats['failed'] += 1
            
            # Rate limiting - wait between emails
            if index < len(df) - 1:  # Don't wait after last email
                time.sleep(delay)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 Campaign Summary")
        print("="*60)
        print(f"Total rows processed: {stats['total']}")
        print(f"✅ Successfully sent: {stats['sent']}")
        print(f"❌ Failed: {stats['failed']}")
        print(f"⏭️  Skipped (no email): {stats['skipped']}")
        print("="*60)
        
        return stats


def main():
    """Main function to demonstrate email sending"""
    
    print("🚀 Mailtrap Email Sender")
    print("="*60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  WARNING: .env file not found!")
        print("📝 Please create a .env file with your Mailtrap credentials")
        print("   You can copy .env.example and fill in your credentials")
        print("\n📖 How to get Mailtrap credentials:")
        print("   1. Go to https://mailtrap.io")
        print("   2. Sign up for free account")
        print("   3. Go to Inboxes → Select inbox → SMTP Settings")
        print("   4. Copy credentials to .env file\n")
        return
    
    try:
        # Initialize sender
        sender = MailtrapSender()
        print("✅ Mailtrap connection configured")
        
        # Load data from Google Sheets
        print("\n📥 Loading data from Google Sheets...")
        sheet_id = "1uDufrhJdfYPgbNAPw7sLbxpbXfrnt4_fZzVWlkyGw7Y"
        gid = "1085790850"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        
        df = pd.read_csv(csv_url)
        print(f"✅ Loaded {len(df)} rows")
        
        # Preview data
        print("\n📋 Data Preview (first 3 rows with emails):")
        email_col = 'Unnamed: 4' if 'Unnamed: 4' in df.columns else 'Email'
        preview = df[df[email_col].notna()].head(3)
        print(preview[['Unnamed: 0', 'Unnamed: 1', email_col]].to_string())
        
        # Ask for confirmation
        print("\n" + "="*60)
        print("⚠️  READY TO SEND EMAILS")
        print("="*60)
        valid_emails = df[df[email_col].notna() & df[email_col].str.contains('@', na=False)]
        print(f"Found {len(valid_emails)} valid email addresses")
        print("\n💡 This will send test emails to Mailtrap (not real recipients)")
        
        response = input("\n🤔 Do you want to proceed? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            # Send emails
            stats = sender.send_bulk_emails(df, delay=1)
            
            print("\n✅ Email campaign completed!")
            print("📨 Check your Mailtrap inbox to see the emails")
            
        else:
            print("\n❌ Email sending cancelled")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please update your .env file with valid Mailtrap credentials")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
