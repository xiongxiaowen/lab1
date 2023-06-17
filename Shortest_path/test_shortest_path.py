import unittest
from unittest.mock import patch, MagicMock
from geopy.geocoders import Nominatim
from Shortest_path import app, geocode, find_shortest_path, plot_shortest_path
import os
from unittest import TestCase, mock


#test the home function in the Flask program.
class HomeTestCase(unittest.TestCase):
    #Interacts with the program
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    #simulates the post request, sends the post request to the root URL with the data of 2 points
    def test_home(self):
        response = self.client.post('/', data={'start': 'New York', 'end': 'Los Angeles'})
        self.assertEqual(response.status_code, 302)
        expected_location = 'http://localhost/shortest_path?file_path=/path/to/file.html'
        self.assertEqual(response.location, expected_location)


# test the error scenarios where geocoding fails or shortest path cannot be found
class ErrorHandlingTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_geocoding_failure(self):
        # Mock the geocoding function to always return None
        with patch('Shortest_path.geocode', return_value=None):
            response = self.client.post('/', data={'start': 'Invalid Start', 'end': 'Invalid End'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Unable to find coordinates for the given addresses.", response.data)

    def test_shortest_path_not_found(self):
        # Mock the find_shortest_path function to return None
        with patch('Shortest_path.find_shortest_path', return_value=None):
            response = self.client.post('/', data={'start': 'Start', 'end': 'End'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Unable to find a path.", response.data)


class GeocodeTestCase(unittest.TestCase):
    @patch.object(Nominatim, 'geocode')
    def test_geocode(self, mock_geocode):
        mock_location = MagicMock()
        mock_location.latitude = 40.7128
        mock_location.longitude = -74.0060
        mock_geocode.return_value = mock_location

        coordinates = geocode('New York')
        self.assertEqual(coordinates, (40.7128, -74.0060))
        mock_geocode.assert_called_once_with('New York')


class FindShortestPathTestCase(unittest.TestCase):
    def test_find_shortest_path(self):
        start_coordinates = (40.7128, -74.0060)
        end_coordinates = (34.0522, -118.2437)

        shortest_path = find_shortest_path(start_coordinates, end_coordinates)

        self.assertIsNotNone(shortest_path)
        self.assertIsInstance(shortest_path, list)
        self.assertGreater(len(shortest_path), 0)


class PlotShortestPathTestCase(TestCase):
    @patch('Shortest_path.requests.get')
    @patch('Shortest_path.polyline.decode')
    @patch('Shortest_path.folium.Map')
    @patch('Shortest_path.folium.Marker')
    @patch('Shortest_path.folium.PolyLine')
    def test_plot_shortest_path(self, mock_polyline, mock_map, mock_marker, mock_decode, mock_get):
        # Patch the plot_shortest_path function
        with mock.patch('test_shortest_path.plot_shortest_path') as mock_plot_shortest_path:
            # Set the return value of plot_shortest_path to a mock file path
            mock_plot_shortest_path.return_value = '/path/to/file.html'

            start_coordinates = {'lat': 40.7128, 'lng': -74.0060}
            end_coordinates = {'lat': 34.0522, 'lng': -118.2437}
            shortest_path = ['Location A', 'Location B', 'Location C']
            
            # Call the function under test
            file_path = plot_shortest_path(start_coordinates, end_coordinates, shortest_path)
            
            # Assert the return value
            self.assertEqual(file_path, '/path/to/file.html')

        # Assert function calls using MagicMock
        mock_map_instance = MagicMock()
        mock_map.return_value = mock_map_instance

        mock_encoded_polyline = MagicMock()
        mock_decode.return_value = [(40.7128, -74.0060), (34.0522, -118.2437)]
        mock_encoded_polyline.decode.return_value = mock_decode.return_value
        mock_polyline.return_value = mock_encoded_polyline

        start_coordinates = (40.7128, -74.0060)
        end_coordinates = (34.0522, -118.2437)
        shortest_path = [(40.7128, -74.0060), (34.0522, -118.2437)]

        file_path = plot_shortest_path(start_coordinates, end_coordinates, shortest_path)

        # Assert that the file_path is not None
        self.assertIsNotNone(file_path)
        
        # Assert function calls using MagicMock assertions
        mock_get.assert_called_once()
        mock_polyline.assert_called_once_with(mock_decode.return_value)
        mock_map.assert_called_once_with(location=start_coordinates, zoom_start=13)
        mock_marker.assert_any_call(start_coordinates, popup="Start")
        mock_marker.assert_any_call(end_coordinates, popup="Destination")
        mock_polyline.assert_called_with(mock_decode.return_value, color="blue", weight=2.5, opacity=1)
        mock_map_instance.save.assert_called_once_with('/path/to/file.html')


if __name__ == '__main__':
    unittest.main()
