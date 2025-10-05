# 📧 Email Campaign with Mailtrap Integration

Send personalized emails to addresses scraped from Google Sheets using Mailtrap for safe testing.

## 🎯 What This Does

1. **Scrapes email addresses** from your Google Sheets
2. **Sends personalized emails** to each gym/business
3. **Uses Mailtrap** for safe testing (emails don't go to real recipients)
4. **Includes HTML templates** with professional styling
5. **Rate limiting** to avoid overwhelming SMTP server
6. **Error handling** for invalid emails

## 📋 Prerequisites

- Python 3.7+
- Free Mailtrap account (https://mailtrap.io)
- Google Sheets with public access or CSV export enabled

## 🚀 Quick Start Guide

### Step 1: Set Up Mailtrap Account

1. Go to **https://mailtrap.io** and sign up for free
2. After login, go to **Email Testing** → **Inboxes**
3. Select or create an inbox
4. Click on **SMTP Settings** tab
5. Choose **Python** from the integration dropdown
6. Copy your credentials:
   - Host: `sandbox.smtp.mailtrap.io`
   - Port: `2525`
   - Username: (your username)
   - Password: (your password)

### Step 2: Configure Environment Variables

1. Open the `.env` file in this directory
2. Replace the placeholder values with your actual Mailtrap credentials:

```bash
# Edit .env file
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525
MAILTRAP_USERNAME=your_actual_username_here
MAILTRAP_PASSWORD=your_actual_password_here

EMAIL_FROM=your-name@example.com
EMAIL_FROM_NAME=Your Name or Business Name
```

⚠️ **IMPORTANT**: Never commit the `.env` file to git! It's already in `.gitignore`.

### Step 3: Run the Email Sender

```bash
# Activate your virtual environment (if not already active)
source .venv/bin/activate

# Run the email sender
python email_sender.py
```

## 📁 Project Structure

```
.
├── email_sender.py          # Main email sending script
├── scratching.py           # Original data scraping script
├── .env                    # Your credentials (NEVER commit!)
├── .env.example           # Template for credentials
├── .gitignore            # Protects sensitive files
└── README_EMAIL.md       # This file
```

## 🎨 Email Features

### What's Included:

- ✅ **Personalized greetings** using gym name
- ✅ **HTML and plain text** versions
- ✅ **Professional styling** with colors and layout
- ✅ **Contact information** if available
- ✅ **Call-to-action button**
- ✅ **Rate limiting** (1 second between emails)
- ✅ **Error handling** for invalid addresses

### Email Preview:

The emails include:
- Professional header with green color scheme
- Personalized greeting with gym name
- Contact information (if available)
- Call-to-action button
- Professional footer

## 🔧 Customization

### Change Email Template

Edit the `create_email()` method in `email_sender.py`:

```python
def create_email(self, to_email, gym_name, contact_number=None):
    # Modify subject line
    msg['Subject'] = f"Your Custom Subject with {gym_name}"
    
    # Modify HTML content
    html_content = f"""
    <!-- Your custom HTML here -->
    """
```

### Change Rate Limiting

In the `send_bulk_emails()` method, adjust the delay:

```python
# Change delay parameter (in seconds)
stats = sender.send_bulk_emails(df, delay=2)  # 2 seconds between emails
```

### Filter Recipients

Add filtering before sending:

```python
# Only send to specific gyms
df_filtered = df[df['Unnamed: 0'].str.contains('Fitness', na=False)]
stats = sender.send_bulk_emails(df_filtered)
```

## 📊 Understanding the Output

When you run the script, you'll see:

```
🚀 Mailtrap Email Sender
============================================================
✅ Mailtrap connection configured

📥 Loading data from Google Sheets...
✅ Loaded 616 rows

📋 Data Preview (first 3 rows with emails):
   Gym Name              Contact Number    Email
0  Conquer Fitness       +61 402 300 024   example@email.com

============================================================
⚠️  READY TO SEND EMAILS
============================================================
Found 150 valid email addresses

💡 This will send test emails to Mailtrap (not real recipients)

🤔 Do you want to proceed? (yes/no):
```

### Campaign Statistics:

```
============================================================
📊 Campaign Summary
============================================================
Total rows processed: 616
✅ Successfully sent: 150
❌ Failed: 0
⏭️  Skipped (no email): 466
============================================================
```

## 🧪 Testing

### Test with Mailtrap:

1. Run the script
2. Go to your Mailtrap inbox
3. You'll see all "sent" emails
4. Click on each to see:
   - HTML preview
   - Plain text version
   - Email headers
   - Spam analysis
   - Validation checks

### Benefits of Mailtrap:

- ✅ **Safe testing** - no emails sent to real people
- ✅ **Unlimited emails** on free tier
- ✅ **Email preview** - see exactly how emails look
- ✅ **Spam score** - check if emails might be flagged
- ✅ **Debug info** - see technical details

## 🔒 Security Best Practices

1. ✅ **Never commit `.env` file** - already in `.gitignore`
2. ✅ **Use environment variables** - not hardcoded credentials
3. ✅ **Keep `.env.example`** - shows structure without secrets
4. ✅ **Rotate credentials** - change passwords periodically
5. ✅ **Test first** - always use Mailtrap before production

## 🚨 Common Issues & Solutions

### Issue: "Mailtrap credentials not found"
**Solution**: Make sure `.env` file exists and has correct credentials

### Issue: "Authentication failed"
**Solution**: Double-check username/password from Mailtrap

### Issue: "No valid email addresses found"
**Solution**: Check if Google Sheets has emails in 'Unnamed: 4' column

### Issue: "Connection timeout"
**Solution**: Check internet connection and Mailtrap status

## 📈 Next Steps

### Moving to Production (Sending Real Emails):

1. Replace Mailtrap with a production SMTP service:
   - **SendGrid** (free tier: 100 emails/day)
   - **Mailgun** (free tier: 5,000 emails/month)
   - **Amazon SES** (pay as you go)
   - **Gmail SMTP** (limited, not recommended for bulk)

2. Update `.env` with production credentials:
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_sendgrid_api_key
```

3. Add unsubscribe links (legally required for bulk emails)
4. Implement email tracking
5. Add retry logic for failed sends
6. Store sent email logs

### Enhancements:

- [ ] Add CSV export of campaign results
- [ ] Schedule emails for specific times
- [ ] Add A/B testing for email content
- [ ] Track open rates (needs production service)
- [ ] Add attachments (PDFs, images)
- [ ] Implement email queue system
- [ ] Add progress bar for bulk sending

## 📚 Additional Resources

- **Mailtrap Docs**: https://mailtrap.io/docs
- **Python SMTP**: https://docs.python.org/3/library/smtplib.html
- **Email Best Practices**: https://sendgrid.com/email-best-practices
- **CAN-SPAM Act**: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business

## 💡 Tips

1. **Start small** - test with 5-10 emails first
2. **Review templates** - check Mailtrap preview before bulk send
3. **Monitor results** - check campaign statistics
4. **Respect rate limits** - adjust delay if needed
5. **Keep it personal** - customize messages for better engagement

## 🆘 Need Help?

1. Check error messages in terminal
2. Review Mailtrap inbox for test emails
3. Verify `.env` file has correct credentials
4. Ensure Google Sheets is accessible
5. Check Python packages are installed: `pip list`

---

Made with ❤️ for gym outreach campaigns
