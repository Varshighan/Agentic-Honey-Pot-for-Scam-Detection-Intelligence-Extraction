# Deployment Checklist

## ✅ Pre-Deployment

- [ ] All Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Python 3.8+ verified (`python --version`)
- [ ] All modules importable (run `python integration_test.py`)
- [ ] Port 5000 available or custom port configured

## 🔑 Configuration

- [ ] API keys configured in `api-gateway/auth.py` or via environment variable
- [ ] GUVI callback URL verified in `intelligence-engine/guvi_callback.py`
- [ ] Server host/port configured (default: 0.0.0.0:5000)
- [ ] Logging directory writable for `honeypot.log`

## 🧪 Testing

- [ ] Integration tests pass: `python integration_test.py`
- [ ] Existing detector tests pass: `python test_suite.py`
- [ ] Quick test passes: `python quick_test.py`
- [ ] Verification passes: `python verify.py`

## 🚀 Startup

### Development
```bash
python app.py
```

### Production (using gunicorn)
```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app --timeout 120
```

**Note**: For cloud deployment (Render, Heroku, etc.), see **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** for detailed instructions.

### Using startup scripts
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

## 📡 API Validation

Test each endpoint:

### 1. Health Check
```bash
curl http://localhost:5000/health
```
Expected: `{"status": "healthy", "active_sessions": 0}`

### 2. Message Ingestion
```bash
curl -X POST http://localhost:5000/ingest-message \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-key-123" \
  -d '{
    "sessionId": "deploy-test-001",
    "message": {
      "sender": "scammer",
      "text": "Your account blocked! Pay now",
      "timestamp": "2026-01-31T10:00:00Z"
    },
    "conversationHistory": [],
    "metadata": {"channel": "SMS", "language": "English", "locale": "IN"}
  }'
```
Expected: `{"status": "success", "reply": "..."}`

### 3. Session Listing
```bash
curl http://localhost:5000/sessions \
  -H "x-api-key: test-key-123"
```
Expected: `{"status": "success", "sessions": [...]}`

### 4. Authentication
```bash
curl -X POST http://localhost:5000/ingest-message \
  -H "Content-Type: application/json"
```
Expected: `401 Unauthorized`

## 🔍 Monitoring

- [ ] Check logs in `honeypot.log`
- [ ] Monitor session count via `/sessions` endpoint
- [ ] Verify state transitions in logs
- [ ] Confirm callbacks sent to GUVI endpoint

## 🛡️ Security

- [ ] API keys are secure (not default values)
- [ ] Keys stored in environment variables (not hardcoded)
- [ ] HTTPS enabled for production (if applicable)
- [ ] Rate limiting configured (if applicable)

## 📊 Intelligence Validation

- [ ] UPI IDs extracted correctly from test messages
- [ ] Phone numbers detected with proper format
- [ ] URLs/phishing links captured
- [ ] Keywords detected in proper categories
- [ ] Confidence filtering works (2+ occurrences)

## 🔄 State Machine

Verify state transitions:
- [ ] INIT → SUSPECTED (when scam detected)
- [ ] SUSPECTED → ENGAGING (when continuing conversation)
- [ ] ENGAGING → INTEL_COMPLETE (when criteria met)
- [ ] INTEL_COMPLETE → REPORTED (after callback sent)

## 📤 GUVI Callback

- [ ] Callback URL reachable: `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`
- [ ] Payload format matches specification
- [ ] Callback sent exactly once per session
- [ ] Timeout handling works (5 seconds)
- [ ] Success/failure logged appropriately

## 🎯 Success Criteria

- [ ] All API endpoints respond correctly
- [ ] Sessions tracked and state managed
- [ ] Scam detection integrated properly
- [ ] Intelligence extracted accurately
- [ ] Final callback sent successfully
- [ ] No errors in logs during testing
- [ ] System handles errors gracefully

## 📝 Documentation

- [ ] README.md updated
- [ ] INTEGRATION_GUIDE.md complete
- [ ] API contracts in `contracts/` folder
- [ ] Code comments comprehensive
- [ ] Examples in `api_examples.py` work

## 🚨 Known Issues / Limitations

- Agent interface is mock implementation (placeholder)
- Session storage in-memory (not persistent)
- No rate limiting on endpoints
- Single-threaded Flask development server

## 🔧 Troubleshooting

### Server won't start
- Check port 5000 not already in use
- Verify all dependencies installed
- Check Python version >= 3.8

### Import errors
- Ensure running from scam-detector directory
- Check all `__init__.py` files present
- Verify sys.path includes current directory

### API returns 500 errors
- Check `honeypot.log` for detailed errors
- Verify existing detector modules work: `python detector.py`
- Run integration tests: `python integration_test.py`

### Callbacks failing
- Check internet connectivity
- Verify GUVI endpoint URL correct
- Check timeout settings (5 seconds)
- Review logs for detailed error messages

## 📞 Support

For issues:
1. Check `honeypot.log` for detailed errors
2. Run `python integration_test.py` to validate system
3. Review state transitions in logs
4. Verify API key authentication

---

## ✅ Deployment Complete

When all items checked:
- System is production-ready
- All components integrated
- Monitoring in place
- Ready for GUVI evaluation
