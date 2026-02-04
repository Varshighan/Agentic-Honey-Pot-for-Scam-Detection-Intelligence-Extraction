# Render Deployment Guide

This guide explains how to deploy the Agentic Honeypot system to Render.

## Prerequisites

- A Render account (https://render.com)
- A GitHub repository with the code

## Deployment Steps

### 1. Create a New Web Service on Render

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select the repository: `Agentic-Honey-Pot-for-Scam-Detection-Intelligence-Extraction`

### 2. Configure the Web Service

Use the following settings:

- **Name**: `agentic-honeypot` (or your preferred name)
- **Region**: Choose the region closest to your users
- **Branch**: `main` (or your deployment branch)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app --timeout 120`

### 3. Environment Variables

Set the following environment variables in Render:

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | (auto-set by Render) | Port number for the server |
| `API_KEYS` | `your-secure-key-1,your-secure-key-2` | Comma-separated list of valid API keys |

**Important**: Replace the default API keys with secure, random keys for production!

**Note**: Render automatically detects the Python version from your code. If you need a specific version, create a `runtime.txt` file with content like `python-3.11.0`.

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Once deployed, you'll get a URL like: `https://your-app-name.onrender.com`

## Testing Your Deployment

### Health Check

```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "active_sessions": 0}
```

### Test Message Ingestion

```bash
curl -X POST https://your-app-name.onrender.com/ingest-message \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secure-key-1" \
  -d '{
    "sessionId": "test-001",
    "message": {
      "sender": "scammer",
      "text": "Send money urgently!"
    },
    "conversationHistory": [],
    "metadata": {"channel": "SMS"}
  }'
```

### Test Authentication

```bash
curl -X POST https://your-app-name.onrender.com/ingest-message \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-002",
    "message": {"sender": "scammer", "text": "Test"},
    "conversationHistory": [],
    "metadata": {"channel": "SMS"}
  }'
```

This should return a 401 error since the API key is missing.

## PowerShell Testing (Windows)

```powershell
# With API key (should work)
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/ingest-message" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "x-api-key"="your-secure-key-1"} `
  -Body '{"sessionId": "test-001", "message": {"sender": "scammer", "text": "Test message"}, "conversationHistory": [], "metadata": {"channel": "SMS"}}' `
  -UseBasicParsing

# Without API key (should fail with 401)
Invoke-WebRequest -Uri "https://your-app-name.onrender.com/ingest-message" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"sessionId": "test-002", "message": {"sender": "scammer", "text": "Test message"}, "conversationHistory": [], "metadata": {"channel": "SMS"}}' `
  -UseBasicParsing
```

## Troubleshooting

### 401 Unauthorized Error

**Cause**: Missing or invalid API key in the request header.

**Solution**: 
- Ensure you're sending the `x-api-key` header with every request
- Verify the API key matches one of the keys in the `API_KEYS` environment variable
- Check the Render logs to see which API keys are active

### 500 Internal Server Error

**Cause**: Application error or missing dependencies.

**Solution**:
- Check the Render logs for detailed error messages
- Verify all dependencies are listed in `requirements.txt`
- Ensure environment variables are set correctly

### Application Won't Start

**Cause**: Incorrect start command or build errors.

**Solution**:
- Verify the start command is: `gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app --timeout 120`
- Check build logs for any pip installation errors
- Ensure Python version is 3.8 or higher

## Monitoring

1. **Logs**: View real-time logs in the Render dashboard
2. **Metrics**: Monitor CPU and memory usage in the Render dashboard
3. **Health Endpoint**: Set up automated monitoring using `/health` endpoint

## Scaling

To handle more traffic:

1. Upgrade to a higher tier plan on Render
2. Increase the number of Gunicorn workers in the start command:
   ```
   gunicorn -w 8 -b 0.0.0.0:$PORT wsgi:app --timeout 120
   ```

## Security Best Practices

1. **Never commit API keys** to the repository
2. **Use environment variables** for all sensitive configuration
3. **Rotate API keys regularly**
4. **Enable HTTPS** (Render provides this automatically)
5. **Monitor logs** for suspicious activity
6. **Use strong, random API keys** (not the default ones)

## WSGI Application

The application uses Gunicorn as the WSGI server with the following configuration:

- **Workers**: 4 (adjustable based on your needs)
- **Timeout**: 120 seconds (to handle long-running intelligence extraction)
- **Bind**: `0.0.0.0:$PORT` (Render sets the PORT environment variable)
- **App Module**: `wsgi:app` (the Flask application instance)

## Files

- `wsgi.py`: WSGI entry point for production deployment
- `app.py`: Development server entry point (for local testing)
- `requirements.txt`: Python dependencies (includes gunicorn)

## Default API Keys

For development/testing, the default API keys are:
- `test-key-123`
- `guvi-honeypot-key`

**Always override these in production using the `API_KEYS` environment variable!**
