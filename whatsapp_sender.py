"""
WhatsApp Sender using Twilio
Separate script for WhatsApp messaging
"""
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class WhatsAppSender:
    """Handle sending WhatsApp messages via Twilio"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        # Validate credentials
        if not self.account_sid or not self.auth_token:
            raise ValueError("⚠️  Twilio credentials not found! Please set them in .env file")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_template_message(self, to_number, template_sid, variables):
        """
        Send WhatsApp message using a template
        
        Args:
            to_number: Recipient's phone number (format: +923036512058)
            template_sid: Twilio template SID
            variables: Template variables as JSON string
        
        Returns:
            tuple: (success: bool, message_sid or error: str)
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message = self.client.messages.create(
                from_=self.from_number,
                content_sid=template_sid,
                content_variables=variables,
                to=to_number
            )
            
            return True, message.sid
            
        except Exception as e:
            return False, str(e)
    
    def send_simple_message(self, to_number, body_text):
        """
        Send simple WhatsApp message (non-template)
        
        Args:
            to_number: Recipient's phone number
            body_text: Message text
        
        Returns:
            tuple: (success: bool, message_sid or error: str)
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message = self.client.messages.create(
                from_=self.from_number,
                body=body_text,
                to=to_number
            )
            
            return True, message.sid
            
        except Exception as e:
            return False, str(e)


def main():
    """Example usage"""
    
    print("📱 Twilio WhatsApp Sender")
    print("="*60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  WARNING: .env file not found!")
        print("📝 Please create a .env file with your Twilio credentials")
        return
    
    try:
        # Initialize sender
        sender = WhatsAppSender()
        print("✅ Twilio connection configured")
        
        # Example: Send template message
        print("\n📤 Sending template message...")
        success, result = sender.send_template_message(
            to_number='+923036512058',
            template_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
            variables='{"1":"12/1","2":"3pm"}'
        )
        
        if success:
            print(f"✅ Message sent! SID: {result}")
        else:
            print(f"❌ Failed to send: {result}")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please update your .env file with valid Twilio credentials")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
