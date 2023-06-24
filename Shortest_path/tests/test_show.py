import unittest
from flask import Flask
from flask.testing import FlaskClient
from Shortest_path import app, show_shortest_path

class ShowShortestPathTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_show_shortest_path(self):
        # Simulate a request with a valid file path
        response = self.client.get('/shortest_path?file_path=/path/to/file_123456.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/html')
        self.assertIn(b'shortest_path_123456.html', response.data)

        # Simulate a request with an invalid file path
        response = self.client.get('/shortest_path')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/shortest_path?file_path=')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/shortest_path?file_path=/path/to/nonexistent.html')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
