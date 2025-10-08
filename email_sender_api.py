"""
Email Sender with Mailtrap API (Production)
This script sends emails using Mailtrap's Sending API with token authentication
"""

import requests
import time
from dotenv import load_dotenv
import os
import pandas as pd
from templates import *

# Load environment variables
load_dotenv()


class MailtrapAPISender:
    """Handle sending emails via Mailtrap API (Production)"""
    
    def __init__(self):
        self.api_token = os.getenv('MAILTRAP_API_TOKEN')
        # PRODUCTION API - sends to real emails
        self.api_url = "https://send.api.mailtrap.io/api/send"
        self.from_email = os.getenv('EMAIL_FROM', 'admin@zoutedevelopers.tech')
        self.from_name = os.getenv('EMAIL_FROM_NAME', 'Zoute Developers')
        
        # Validate credentials
        if not self.api_token or self.api_token == 'your_mailtrap_api_token_here':
            raise ValueError(
                "⚠️  Mailtrap API token not found!\n"
                "Please get your token from: https://mailtrap.io/api-tokens\n"
                "And set it in .env file as: MAILTRAP_API_TOKEN=your_token"
            )
    
    def create_email_payload(self, to_email, gym_name, contact_number=None, isWebsite=None):
        """
        Create email payload for Mailtrap API
        
        Args:
            to_email: Recipient's email address
            gym_name: Name of the gym
            contact_number: Phone number (optional)
            isWebsite: Whether gym has a website
        
        Returns:
            dict: API payload
        """
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
        
        # HTML version (using your templates)
        if (isWebsite == 'Yes' or isWebsite == 'yes' or isWebsite == 'YES'):
            html_content = export_html_template(first_name=gym_name)
        else:
            html_content = export_html_websitenotfound_template(first_name=gym_name)
        
        # Create API payload
        payload = {
            "from": {
                "email": self.from_email,
                "name": self.from_name
            },
            "to": [
                {
                    "email": to_email
                }
            ],
            "subject": f"Partnership Opportunity with {gym_name}",
            "text": text_content,
            "html": html_content,
            "category": "Gym Outreach"
        }
        
        return payload
    
    def send_email(self, to_email, gym_name, contact_number=None, isWebsite=None):
        """
        Send an email via Mailtrap API
        
        Args:
            to_email: Recipient's email address
            gym_name: Name of the gym
            contact_number: Phone number (optional)
            isWebsite: Whether gym has a website
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create payload
            payload = self.create_email_payload(to_email, gym_name, contact_number, isWebsite)
            
            # Set headers
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            # Send request
            response = requests.post(self.api_url, json=payload, headers=headers)
            
            # Check response
            if response.status_code == 200:
                return True, f"✅ Email sent to {to_email}"
            else:
                return False, f"❌ Failed to send to {to_email}: {response.status_code} - {response.text}"
            
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
        print("📧 Starting Bulk Email Campaign (Production API)")
        print("="*60)
        
        # Identify email column
        email_col = 'Unnamed: 4' if 'Unnamed: 4' in df.columns else 'Email'
        gym_col = 'Unnamed: 0' if 'Unnamed: 0' in df.columns else 'Gym Name'
        phone_col = 'Unnamed: 1' if 'Unnamed: 1' in df.columns else 'Contact Number'
        website_col = 'Unnamed: 2' if 'Unnamed: 2' in df.columns else 'Website'
        
        print(f"📊 Found {len(df)} total rows")
        print(f"📧 Email column: {email_col}")
        print(f"🏋️  Gym name column: {gym_col}")
        print(f"📞 Phone column: {phone_col}")
        print(f"🌐 Website column: {website_col}\n")
        
        for index, row in df.iterrows():
            stats['total'] += 1
            
            # Get email and gym name
            email = row.get(email_col)
            gym_name = row.get(gym_col, f"Gym #{index}")
            phone = row.get(phone_col)
            isWebsite = row.get(website_col)
            
            # Skip if no email or email is NaN
            if pd.isna(email) or not email or '@' not in str(email):
                print(f"⏭️  Row {index}: Skipping '{gym_name}' - No valid email")
                stats['skipped'] += 1
                continue
            
            # Send email
            print(f"\n📬 Sending to: {email} ({gym_name})")
            success, message = self.send_email(email, gym_name, phone, isWebsite)
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
    
    print("🚀 Mailtrap API Email Sender (Production)")
    print("="*60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  WARNING: .env file not found!")
        print("📝 Please create a .env file with your Mailtrap API token")
        print("\n📖 How to get Mailtrap API token:")
        print("   1. Go to https://mailtrap.io")
        print("   2. Sign in to your account")
        print("   3. Go to Settings → API Tokens")
        print("   4. Create a new token or copy existing one")
        print("   5. Add to .env file: MAILTRAP_API_TOKEN=your_token\n")
        return
    
    try:
        # Initialize sender
        sender = MailtrapAPISender()
        print("✅ Mailtrap API configured")
        
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
        print("⚠️  READY TO SEND EMAILS (PRODUCTION)")
        print("="*60)
        valid_emails = df[df[email_col].notna() & df[email_col].str.contains('@', na=False)]
        print(f"Found {len(valid_emails)} valid email addresses")
        print("\n🚨 WARNING: This will send REAL emails to actual recipients!")
        print("💡 Make sure your email content is ready for production")
        
        response = input("\n🤔 Do you want to proceed? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            # Send emails
            stats = sender.send_bulk_emails(df, delay=1)
            
            print("\n✅ Email campaign completed!")
            print(f"📨 {stats['sent']} emails sent successfully")
            
            # Save results to file
            results_file = f"campaign_results_{int(time.time())}.txt"
            with open(results_file, 'w') as f:
                f.write("Campaign Results\n")
                f.write("="*60 + "\n")
                f.write(f"Total: {stats['total']}\n")
                f.write(f"Sent: {stats['sent']}\n")
                f.write(f"Failed: {stats['failed']}\n")
                f.write(f"Skipped: {stats['skipped']}\n\n")
                f.write("Detailed Results:\n")
                for result in stats['results']:
                    f.write(f"{result['gym']} ({result['email']}): {result['message']}\n")
            
            print(f"📄 Results saved to: {results_file}")
            
        else:
            print("\n❌ Email sending cancelled")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
