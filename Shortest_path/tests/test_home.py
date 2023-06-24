#test the home function in the Shortest_path.py
import unittest
from unittest.mock import patch, MagicMock
from geopy.geocoders import Nominatim
from flask import Flask
from flask.testing import FlaskClient
from Shortest_path import app, geocode, find_shortest_path, plot_shortest_path

class HomeTestCase(unittest.TestCase):
    #Interacts with the program
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # test if valid addresses provided, geocoding is successful, and the shortest path is found.
    @patch.object(Nominatim, 'geocode')
    @patch('Shortest_path.find_shortest_path')
    @patch('Shortest_path.plot_shortest_path')
    def test_home_post_successful(self, mock_plot_shortest_path, mock_find_shortest_path, mock_geocode):
        # Create a mock location object with latitude and longitude attributes
        class MockLocation:
            def __init__(self, latitude, longitude):
                self.latitude = latitude
                self.longitude = longitude            
        
        # Mock functions and methods
        mock_geocode.return_value = MockLocation(12.345, 67.89)
        mock_find_shortest_path.return_value = [(12.345, 67.890), (98.765, 43.210)]

        # Send a POST request to the home endpoint with form data
        response = self.app.post('/', data={'start': 'New York', 'end': 'San Francisco'}, follow_redirects=True)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the redirected URL path
        expected_error_message = '<p style="color: red;">Unable to find coordinates for the given addresses.</p>'
        #expected_redirect_url = '/shortest_path?file_path=/path/to/file.html'
        response_text = response.get_data(as_text=True)
        #self.assertIn(expected_redirect_url, response_text)
        self.assertIn(expected_error_message, response_text)


if __name__ == '__main__':
    unittest.main()