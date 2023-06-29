import unittest
from flask import Flask, request, render_template
from unittest.mock import patch
from shortest_path import app, show_shortest_path

class ShowShortestPathTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_show_shortest_path(self):
        with app.test_request_context('/shortest_path?file_path=test_shortest_path.html'):
            response = self.app.get('/shortest_path')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'text/html')
            self.assertIn(b'test_shortest_path.html', response.data)

    @patch('flask.render_template')
    @patch('flask.request')
    def test_show_shortest_path_mocked(self, mock_request, mock_render_template):
        mock_request.args.get.return_value = 'test_shortest_path.html'
        expected_file_path = 'test_shortest_path.html'

        result = show_shortest_path()

        self.assertEqual(result, mock_render_template.return_value)
        mock_request.args.get.assert_called_once_with('file_path')
        mock_render_template.assert_called_once_with('results.html', file_path=expected_file_path)

if __name__ == '__main__':
    unittest.main()
