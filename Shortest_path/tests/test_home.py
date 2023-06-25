#test the home function in the Shortest_path.py
import unittest
from unittest import TestCase, mock
from unittest.mock import patch, MagicMock
from geopy.geocoders import Nominatim
from flask import Flask, url_for
from Shortest_path import app, geocode, find_shortest_path, plot_shortest_path

class TestHome(unittest.TestCase):
    def setUp(self):
        # Set up Flask app for testing
        app.testing = True
        self.app = app.test_client()

    @patch.object(Nominatim, 'geocode')
    @patch('Shortest_path.find_shortest_path')
    @patch('Shortest_path.plot_shortest_path')

    def test_home_with_valid_addresses(self, mock_plot_shortest_path, mock_find_shortest_path, mock_geocode):
        # Simulate a POST request with valid addresses
        mock_geocode.return_value = (40.7128, -74.0060)
        mock_find_shortest_path.return_value = [(40.7128, -74.0060), (34.0522, -118.2437)]
        response = self.app.post('/', data={'start': 'New York, USA', 'end': 'Los Angeles, USA'})
        
        # Check if the response is a redirect
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.location, None)

    def test_home_with_missing_addresses(self):
        # Simulate a POST request with missing addresses
        response = self.app.post('/', data={'start': '', 'end': 'Los Angeles, USA'})
        
        # Check if the response is a redirect back to the home page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    @mock.patch('Shortest_path.geocode')
    def test_home_with_geocoding_failure(self, mock_geocode):
        # Define a side_effect function that returns None for invalid addresses
        def side_effect(address):
            if address.startswith('Invalid'):
                return None
            else:
                return (0.0, 0.0)
        mock_geocode.side_effect = side_effect
        # Simulate a POST request with addresses that cannot be geocoded
        response = self.app.post('/', data={'start': 'Invalid Start Address', 'end': 'Invalid End Address'})
        
        # Check if the response is rendering the index.html template with an error message
        self.assertEqual(response.status_code, 320)
        self.assertIn(b"Unable to find coordinates", response.data)

    def test_home_with_no_path_found(self):
        response = self.app.post('/', data={'start': 'New York, USA', 'end': 'Paris, France'})
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b"Unable to find a path", response.data)

    def test_home_with_get_request(self):
        response = self.app.get('/')      

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Start Address", response.data)
        self.assertIn(b"End Address", response.data)


if __name__ == '__main__':
    unittest.main()
