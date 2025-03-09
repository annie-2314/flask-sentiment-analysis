import unittest
from app import app

class SentimentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_positive_sentiment(self):
        response = self.app.post('/predict', json={'text': 'I love this product'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('positive', response.get_json().values())
    
    def test_negative_sentiment(self):
        response = self.app.post('/predict', json={'text': 'This is terrible'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('negative', response.get_json().values())

if __name__ == '__main__':
    unittest.main()
