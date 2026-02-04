"""
WSGI Entry Point for Production Deployment
This module exposes the Flask app instance for WSGI servers like Gunicorn
"""

import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Add module paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'intelligence-engine'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api-gateway'))

# Import modules
from bridge import create_scam_detector_bridge, create_agent_interface
from reporter import intelligence_reporter
from main import create_api_gateway

# Initialize components
logger.info("=" * 60)
logger.info("Initializing Agentic Honeypot System for Production")
logger.info("=" * 60)

# 1. Scam Detector Bridge
scam_detector = create_scam_detector_bridge()
logger.info("[OK] Scam Detector Bridge initialized")

# 2. Intelligence Engine
intelligence_engine = intelligence_reporter
logger.info("[OK] Intelligence Engine initialized")

# 3. Agent Interface
agent_interface = create_agent_interface()
logger.info("[OK] Agent Interface initialized")

# 4. API Gateway
api_gateway = create_api_gateway(
    scam_detector=scam_detector,
    intelligence_engine=intelligence_engine,
    agent_interface=agent_interface
)
logger.info("[OK] API Gateway initialized")

# Expose Flask app for WSGI servers
app = api_gateway.get_app()

logger.info("=" * 60)
logger.info("WSGI Application Ready")
logger.info("=" * 60)

if __name__ == "__main__":
    # For local testing with python wsgi.py
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
