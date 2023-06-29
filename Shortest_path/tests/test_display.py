# test display_map function
import unittest
from flask import Flask, send_file
from shortest_path import app
import random, string, os

class TestDisplayMap(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_display_map(self):
        cache_bust = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        file_name = f"shortest_path_{cache_bust}.html"
        file_path = os.path.join(os.getcwd(), 'templates', file_name)
        response = self.app.get(f'/display_map/{file_path}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/octet-stream')
        self.assertEqual(response.headers['Content-Disposition'], f'attachment; filename={file_path}')

if __name__ == '__main__':
    unittest.main()