import unittest
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Try importing from backend
try:
    from backend.app import app, clean_up_sentence, bag_of_words, predict_class, get_response
    APP_AVAILABLE = True
    print(" Backend imported successfully")
except ImportError as e:
    print(f"Could not import backend: {e}")
    APP_AVAILABLE = False
    app = None

class ChatbotTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client() if app else None
        
        # Load intents if available
        intents_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'intents.json')
        try:
            with open(intents_path, 'r') as f:
                self.intents = json.load(f)
        except FileNotFoundError:
            self.intents = {"intents": []}
    
    def test_app_imports(self):
        """Test if app imports successfully."""
        self.assertTrue(APP_AVAILABLE, "App should import successfully")
    
    def test_clean_up_sentence(self):
        """Test sentence cleaning."""
        if not APP_AVAILABLE:
            self.skipTest("Backend not available")
        result = clean_up_sentence("Hello! How are you?")
        self.assertIsInstance(result, list)
        self.assertIn('hello', result)
    
    def test_bag_of_words(self):
        """Test bag of words generation."""
        if not APP_AVAILABLE:
            self.skipTest("Backend not available")
        result = bag_of_words("hello")
        self.assertIsNotNone(result)
    
    def test_predict_class(self):
        """Test intent prediction."""
        if not APP_AVAILABLE:
            self.skipTest("Backend not available")
        result = predict_class("hello")
        self.assertIsInstance(result, list)
    
    def test_get_response(self):
        """Test response generation."""
        if not APP_AVAILABLE:
            self.skipTest("Backend not available")
        intents_list = [{"intent": "greeting", "probability": "0.95"}]
        response = get_response(intents_list, self.intents)
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")
    
    def test_health_endpoint(self):
        """Test health endpoint."""
        if not self.app:
            self.skipTest("App not available")
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_home_endpoint(self):
        """Test home endpoint."""
        if not self.app:
            self.skipTest("App not available")
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
    
    def test_chat_endpoint(self):
        """Test chat endpoint."""
        if not self.app:
            self.skipTest("App not available")
        response = self.app.post('/chat', 
            json={'message': 'hello'},
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertIn('confidence', data)

if __name__ == '__main__':
    unittest.main()