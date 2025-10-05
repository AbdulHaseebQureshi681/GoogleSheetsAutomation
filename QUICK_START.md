# 🚀 QUICK START: 5-Minute Setup Guide

## ✅ What's Already Done

- ✅ Python packages installed (`python-dotenv`, `pandas`, `requests`, `beautifulsoup4`)
- ✅ Email sender script created (`email_sender.py`)
- ✅ Environment files created (`.env`, `.env.example`)
- ✅ Security configured (`.gitignore` protects credentials)
- ✅ Professional email templates ready (HTML + plain text)

## 🎯 What You Need To Do

### 1️⃣ Get Mailtrap Credentials (2 minutes)

1. Go to: **https://mailtrap.io**
2. Click "Sign Up" (use Google/GitHub for faster signup)
3. After login, click "Email Testing" → "Inboxes"
4. Click on "My Inbox" or create a new one
5. Click the "SMTP Settings" tab
6. You'll see something like:

```
Host: sandbox.smtp.mailtrap.io
Port: 2525
Username: a1b2c3d4e5f6g7    ← Copy this
Password: h8i9j0k1l2m3n4    ← Copy this
```

### 2️⃣ Update .env File (1 minute)

Open `.env` file and replace the placeholders:

```bash
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525
MAILTRAP_USERNAME=a1b2c3d4e5f6g7    ← Paste your username here
MAILTRAP_PASSWORD=h8i9j0k1l2m3n4    ← Paste your password here

EMAIL_FROM=yourname@example.com     ← Your email
EMAIL_FROM_NAME=Your Name           ← Your name or business name
```

### 3️⃣ Run the Script (1 minute)

```bash
# Make sure you're in the project directory
cd "/home/abdul-haseeb-qureshi/ArkhamArchive/Web dev/PythonScratching"

# Run the email sender
python email_sender.py
```

### 4️⃣ Confirm and Send

The script will:
1. Load your Google Sheets data
2. Show preview of emails to send
3. Ask for confirmation
4. Type `yes` to proceed

### 5️⃣ Check Mailtrap Inbox

1. Go back to Mailtrap.io
2. Click on your inbox
3. See all the "sent" emails appear
4. Click on any email to see how it looks

## 🎉 That's It!

You're now sending emails! The emails go to Mailtrap (not real recipients), so it's 100% safe for testing.

## 📊 What The Script Does

```
Scrapes Google Sheets → Validates Emails → Sends Personalized Emails → Mailtrap Inbox
```

## 🔥 Quick Commands

```bash
# Run the email sender
python email_sender.py

# View your environment variables (safe, shows *** for passwords)
cat .env

# Check installed packages
pip list | grep -E "pandas|requests|beautifulsoup4|python-dotenv"

# View email sender code
cat email_sender.py
```

## 🚨 Common Issues

**"Mailtrap credentials not found"**
→ Make sure `.env` file has your actual username/password from Mailtrap

**"Authentication failed"**
→ Double-check you copied credentials correctly (no extra spaces)

**"No valid email addresses"**
→ Your Google Sheets might not have emails in the expected column

## 💡 Next Steps

After testing in Mailtrap:
- Customize email template in `email_sender.py`
- Adjust rate limiting (delay between emails)
- Filter specific gyms to contact
- Move to production SMTP when ready

---

Need detailed guide? Check `README_EMAIL.md`

Happy emailing! 📧✨
