# 🔄 Building This With n8n

## 🎯 Why n8n Might Be Better for You

### **Advantages:**
- ✅ **Visual workflow** - see the entire process
- ✅ **No coding** - drag and drop nodes
- ✅ **Built-in scheduler** - runs automatically
- ✅ **Error handling** - visual error paths
- ✅ **Testing** - test each node individually
- ✅ **Monitoring** - see execution history
- ✅ **Easy modifications** - change without coding

### **When to Use Each:**

| Use Python When... | Use n8n When... |
|-------------------|-----------------|
| Complex logic needed | Simple automation |
| Version control important | Quick setup needed |
| Part of larger codebase | Standalone workflow |
| Team knows Python | Non-technical users |

## 🚀 Quick Start with n8n

### **Option 1: Docker (Recommended)**

```bash
# Create directory for n8n data
mkdir ~/.n8n

# Run n8n with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Open browser to: http://localhost:5678
```

### **Option 2: NPM**

```bash
# Install n8n globally
npm install n8n -g

# Start n8n
n8n

# Open browser to: http://localhost:5678
```

### **Option 3: Cloud (No Installation)**

- Go to: https://n8n.io/cloud
- Sign up for free account
- Get 5,000 workflow executions/month free

## 📥 Import the Workflow

### **Step 1: Start n8n**

```bash
# If using Docker
docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# If using npm
n8n
```

### **Step 2: Import Workflow**

1. Open http://localhost:5678 in browser
2. Click **"Workflows"** in sidebar
3. Click **"Import from File"** button (top right)
4. Select `n8n-workflow.json` from this directory
5. The workflow will open automatically

### **Step 3: Configure Credentials**

1. Click on **"Settings"** (gear icon) → **"Credentials"**
2. Add new credential: **"SMTP"**
3. Fill in Mailtrap details:
   - **Host:** `sandbox.smtp.mailtrap.io`
   - **Port:** `2525`
   - **User:** Your Mailtrap username
   - **Password:** Your Mailtrap password
   - **Secure:** Unchecked (for Mailtrap sandbox)

### **Step 4: Set Environment Variables**

In n8n, click **"Settings"** → **"Environment Variables"**:

```
EMAIL_FROM=your-name@example.com
EMAIL_FROM_NAME=Your Name
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525
MAILTRAP_USERNAME=your_username
MAILTRAP_PASSWORD=your_password
```

### **Step 5: Test the Workflow**

1. Click **"Execute Workflow"** button
2. Watch each node execute in real-time
3. Check Mailtrap inbox for emails
4. Review execution log at bottom

## 🎨 Understanding the Workflow

### **Node Breakdown:**

```
1. ⏰ Schedule Trigger
   └─ Runs every Monday at 9 AM (customizable)

2. 📥 Fetch Google Sheets
   └─ Downloads CSV from your Google Sheets URL

3. 📊 Parse CSV
   └─ Converts CSV text into structured data

4. 🔀 Split Into Rows
   └─ Creates separate item for each gym

5. ✅ Filter Valid Emails
   └─ Checks if email exists and contains "@"
   ├─ TRUE → Send Email
   └─ FALSE → Log Skipped

6. 📧 Send Email
   └─ Sends personalized HTML email via Mailtrap

7. ⏱️ Rate Limit
   └─ Waits 1 second before next email

8. 📝 Log Success / Log Skipped
   └─ Tracks which emails were sent/skipped
```

## 🔧 Customization Guide

### **Change Schedule**

Click on "Schedule Trigger" node:
- **Daily at 9 AM:** `0 9 * * *`
- **Every Monday at 9 AM:** `0 9 * * 1`
- **Every hour:** `0 * * * *`
- **Twice daily (9 AM & 5 PM):** `0 9,17 * * *`

### **Change Email Template**

Click on "Send Email" node:
- Edit **Subject** field
- Edit **HTML** field (supports HTML)
- Use `{{ $json.gym_name }}` for gym name
- Use `{{ $json.email }}` for email
- Use `{{ $json.phone }}` for phone

### **Change Rate Limit**

Click on "Rate Limit" node:
- Change **Wait Time** (in milliseconds)
- 1000 = 1 second
- 2000 = 2 seconds
- 500 = 0.5 seconds

### **Add More Filters**

Add a new "IF" node after "Filter Valid Emails":
- Filter by gym name: `{{ $json.gym_name.includes('Fitness') }}`
- Filter by location: `{{ $json.location === 'Sydney' }}`
- Combine multiple conditions

## 📊 Monitoring & Analytics

### **View Execution History**

1. Go to **"Executions"** tab
2. See all past runs
3. Click any execution to see details
4. Export results as JSON/CSV

### **Track Success Rates**

n8n automatically tracks:
- ✅ Successful executions
- ❌ Failed executions
- ⏱️ Execution time
- 📊 Data flow through nodes

### **Set Up Notifications**

Add error handling:
1. Add "Send Email" node after errors
2. Connect to your own email
3. Get notified of failures

## 🆚 Python vs n8n Comparison

### **Your Current Python Setup:**

```python
# Load data
df = pd.read_csv(url)

# Send emails
for row in df:
    send_email(row['email'], row['gym_name'])
```

### **Same Thing in n8n:**

```
[HTTP Request] → [Split] → [Filter] → [Send Email]
```

**Result:** Same functionality, but visual and easier to maintain!

## 🎯 Which Should You Choose?

### **Choose Python If:**
- ✅ You're comfortable with Python
- ✅ Need complex data transformations
- ✅ Want version control (Git)
- ✅ Part of larger Python project
- ✅ Need custom logic/algorithms

### **Choose n8n If:**
- ✅ Want quick setup (5 minutes)
- ✅ Prefer visual workflows
- ✅ Need scheduling without cron
- ✅ Want easy modifications
- ✅ Non-technical team members will maintain it
- ✅ Want monitoring/analytics built-in

## 🔄 Using Both Together

You can also use both!

```
n8n → Triggers and schedules
  ↓
Python → Complex processing
  ↓
n8n → Send results via email
```

Use n8n's "Execute Command" node to run your Python script:

```bash
/home/abdul-haseeb-qureshi/.venv/bin/python email_sender.py
```

## 📚 Resources

- **n8n Documentation:** https://docs.n8n.io
- **n8n Community:** https://community.n8n.io
- **Workflow Templates:** https://n8n.io/workflows
- **Video Tutorials:** https://www.youtube.com/@n8n-io

## 💡 Pro Tips

1. **Test with Sample Data First**
   - Use "Execute Node" to test individual nodes
   - Don't run full workflow until tested

2. **Use Error Workflows**
   - Set up error notifications
   - Log failures to Google Sheets

3. **Version Your Workflows**
   - Export JSON regularly
   - Keep in Git for version control

4. **Use Webhook Triggers**
   - Trigger workflow from anywhere
   - Great for integrations

5. **Monitor Execution Times**
   - Optimize slow nodes
   - Use batch processing for large datasets

## 🚀 Next Steps

1. **Install n8n** (choose Docker, npm, or cloud)
2. **Import workflow** from `n8n-workflow.json`
3. **Configure credentials** (Mailtrap SMTP)
4. **Test with 1-2 emails** first
5. **Scale up** once working

## ❓ Need Help?

- Check n8n documentation
- Ask in n8n community forum
- Or stick with Python if you prefer! Both work great!

---

**Quick Decision:**
- **Got 5 minutes?** → Use n8n (faster setup)
- **Comfortable with code?** → Use Python (more control)
- **Not sure?** → Try both and see which you prefer!
