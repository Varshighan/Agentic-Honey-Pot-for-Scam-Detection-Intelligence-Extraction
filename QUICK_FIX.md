# Quick Fix for Your Render Deployment Issue

## The Problem
Your third PowerShell request failed with 401 Unauthorized because you forgot to include the `x-api-key` header. However, the underlying issue is that your Render deployment wasn't configured correctly to use a production WSGI server.

## The Solution

### Step 1: Update Your Render Configuration

1. Log in to your Render dashboard
2. Go to your web service settings
3. Update the **Start Command** to:
   ```
   gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app --timeout 120
   ```

### Step 2: Redeploy

Click "Manual Deploy" > "Deploy latest commit" or push a new commit to trigger automatic deployment.

### Step 3: Test Your Deployment

**With API Key (should work):**
```powershell
Invoke-WebRequest -Uri "https://agentic-honey-pot-for-scam-detection-ruq6.onrender.com/ingest-message" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "x-api-key"="guvi-honeypot-key"} `
  -Body '{"sessionId": "session-013", "message": {"sender": "scammer", "text": "Test message"}, "conversationHistory": [], "metadata": {"channel": "SMS"}}' `
  -UseBasicParsing
```

**Without API Key (should return 401):**
```powershell
Invoke-WebRequest -Uri "https://agentic-honey-pot-for-scam-detection-ruq6.onrender.com/ingest-message" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"sessionId": "session-014", "message": {"sender": "scammer", "text": "Test message"}, "conversationHistory": [], "metadata": {"channel": "SMS"}}' `
  -UseBasicParsing
```

## What Changed?

1. **Added wsgi.py**: A production-ready WSGI entry point for your Flask app
2. **Added gunicorn**: A production WSGI server (already in requirements.txt)
3. **Updated documentation**: See RENDER_DEPLOYMENT.md for complete guide

## Why Your Third Request Failed

Looking at your PowerShell commands, the third request was missing the API key:
- ✅ Request 1: Had `"x-api-key"="guvi-honeypot-key"` → SUCCESS
- ✅ Request 2: Had `"x-api-key"="guvi-honeypot-key"` → SUCCESS  
- ❌ Request 3: Missing `x-api-key` header → 401 UNAUTHORIZED

**Always include the API key header** in your requests!

## Security Note

The default API keys in the code are:
- `test-key-123`
- `guvi-honeypot-key`

For production, set a custom `API_KEYS` environment variable in Render with your own secure keys:
```
my-secure-key-1,my-secure-key-2,my-secure-key-3
```

## Need Help?

See the complete deployment guide: **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)**
