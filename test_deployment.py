"""
Test suite for deployment configuration
Validates WSGI entry point and production setup
"""

import unittest
import sys
import os

# Add module paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'intelligence-engine'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api-gateway'))


class TestDeploymentConfiguration(unittest.TestCase):
    """Test deployment configuration and WSGI setup"""
    
    def test_wsgi_module_imports(self):
        """Test that wsgi module can be imported"""
        try:
            import wsgi
            self.assertIsNotNone(wsgi)
        except ImportError as e:
            self.fail(f"Failed to import wsgi module: {e}")
    
    def test_wsgi_app_exists(self):
        """Test that wsgi module exposes an app variable"""
        import wsgi
        self.assertTrue(hasattr(wsgi, 'app'), "wsgi module must expose 'app' variable")
    
    def test_wsgi_app_is_flask(self):
        """Test that the app is a Flask application"""
        import wsgi
        from flask import Flask
        self.assertIsInstance(wsgi.app, Flask, "wsgi.app must be a Flask instance")
    
    def test_wsgi_app_has_routes(self):
        """Test that the Flask app has the required routes"""
        import wsgi
        
        # Get all routes
        routes = [str(rule.rule) for rule in wsgi.app.url_map.iter_rules()]
        
        # Check for required endpoints
        required_routes = ['/', '/health', '/ingest-message', '/sessions']
        for route in required_routes:
            self.assertIn(route, routes, f"Route {route} not found in app")
    
    def test_api_key_configuration(self):
        """Test that API keys are properly configured"""
        from auth import VALID_API_KEYS
        
        # Should have at least the default keys
        self.assertGreater(len(VALID_API_KEYS), 0, "No API keys configured")
        
        # Default keys should be present (unless overridden by env)
        if 'API_KEYS' not in os.environ:
            self.assertIn('guvi-honeypot-key', VALID_API_KEYS)
            self.assertIn('test-key-123', VALID_API_KEYS)
    
    def test_flask_app_name(self):
        """Test that Flask app has correct name"""
        import wsgi
        # The app name comes from the module where it's created (main.py)
        self.assertEqual(wsgi.app.name, 'main')
    
    def test_requirements_has_gunicorn(self):
        """Test that requirements.txt includes gunicorn"""
        req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        with open(req_file, 'r') as f:
            requirements = f.read()
        
        self.assertIn('gunicorn', requirements.lower(), 
                     "requirements.txt must include gunicorn for production")
    
    def test_gitignore_exists(self):
        """Test that .gitignore exists and excludes __pycache__"""
        gitignore_file = os.path.join(os.path.dirname(__file__), '.gitignore')
        self.assertTrue(os.path.exists(gitignore_file), ".gitignore file must exist")
        
        with open(gitignore_file, 'r') as f:
            gitignore = f.read()
        
        self.assertIn('__pycache__', gitignore, ".gitignore must exclude __pycache__")


class TestWSGIAppFunctionality(unittest.TestCase):
    """Test that the WSGI app works correctly"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test client"""
        import wsgi
        cls.app = wsgi.app
        cls.client = cls.app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('name', data)
        self.assertIn('endpoints', data)
    
    def test_authentication_required(self):
        """Test that /ingest-message requires authentication"""
        response = self.client.post('/ingest-message',
                                   json={
                                       "sessionId": "test-001",
                                       "message": {
                                           "sender": "scammer",
                                           "text": "Test"
                                       },
                                       "conversationHistory": [],
                                       "metadata": {"channel": "SMS"}
                                   })
        self.assertEqual(response.status_code, 401, 
                        "Should return 401 when API key is missing")
    
    def test_authentication_with_valid_key(self):
        """Test that /ingest-message works with valid API key"""
        response = self.client.post('/ingest-message',
                                   json={
                                       "sessionId": "test-002",
                                       "message": {
                                           "sender": "scammer",
                                           "text": "Test message"
                                       },
                                       "conversationHistory": [],
                                       "metadata": {"channel": "SMS"}
                                   },
                                   headers={'x-api-key': 'test-key-123'})
        
        self.assertEqual(response.status_code, 200,
                        "Should return 200 with valid API key")
    
    def test_sessions_endpoint_requires_auth(self):
        """Test that /sessions requires authentication"""
        response = self.client.get('/sessions')
        self.assertEqual(response.status_code, 401)
        
        # Now with valid key
        response = self.client.get('/sessions', 
                                  headers={'x-api-key': 'test-key-123'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    print("=" * 60)
    print("Running Deployment Configuration Tests")
    print("=" * 60)
    unittest.main(verbosity=2)
