# test plot_shortest_path function
import os
import random
import string
import unittest
from unittest.mock import patch, MagicMock
import requests
import polyline
import folium
from Shortest_path import plot_shortest_path


#tests the behavior of the plot_shortest_path function 
class PlotShortestPathMockTestCase(unittest.TestCase):
    @patch('Shortest_path.requests.get')
    @patch('Shortest_path.polyline.decode')
    @patch('Shortest_path.folium.Map')
    @patch('Shortest_path.folium.Marker')
    @patch('Shortest_path.folium.PolyLine')
    def test_plot_shortest_path(self, mock_polyline, mock_map, mock_marker, mock_decode, mock_get):
        # Patch the plot_shortest_path function
        with patch('Shortest_path.plot_shortest_path') as mock_plot_shortest_path:
            # Set the return value of plot_shortest_path to a mock file path
            mock_plot_shortest_path.return_value = '/path/to/file.html'

            start_coordinates = [40.7128, -74.0060]
            end_coordinates = [34.0522, -118.2437]
            shortest_path = [start_coordinates, end_coordinates]

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
        mock_get.assert_called_once_with("http://router.project-osrm.org/route/v1/driving/-74.006,40.7128;-118.2437,34.0522")
        mock_polyline.assert_called_once_with(mock_decode.return_value)
        mock_map.assert_called_once_with(location=start_coordinates, zoom_start=13)
        mock_marker.assert_any_call(start_coordinates, popup="Start")
        mock_marker.assert_any_call(end_coordinates, popup="Destination")
        mock_polyline.assert_called_with(mock_decode.return_value, color="blue", weight=2.5, opacity=1)
        mock_map_instance.save.assert_called_once_with('/path/to/file.html')


# when the 'routes' key or 'geometry' key missing 
class PlotShortestPathErrorTestCase(unittest.TestCase):
    def test_missing_routes_key(self):
        # Patch the requests.get function to return a response without 'routes' key
        with patch('Shortest_path.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {}

            start_coordinates = [40.7128, -74.0060]
            end_coordinates = [34.0522, -118.2437]
            shortest_path = [start_coordinates, end_coordinates]

            # Assert that the function raises a KeyError
            with self.assertRaises(KeyError):
                plot_shortest_path(start_coordinates, end_coordinates, shortest_path)

    def test_missing_geometry_key(self):
        # Patch the requests.get function to return a response without 'geometry' key
        with patch('Shortest_path.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {'routes': [{}]}

            start_coordinates = [40.7128, -74.0060]
            end_coordinates = [34.0522, -118.2437]
            shortest_path = [start_coordinates, end_coordinates]

            # Assert that the function raises a KeyError
            with self.assertRaises(KeyError):
                plot_shortest_path(start_coordinates, end_coordinates, shortest_path)

#file creation functionality
class PlotShortestPathFileTestCase(unittest.TestCase):
    def test_plot_shortest_path(self):
        for _ in range(10):
            start_lat = random.uniform(-90, 90)
            start_lon = random.uniform(-180, 180)
            end_lat = random.uniform(-90, 90)
            end_lon = random.uniform(-180, 180)

            start_coordinates = [start_lat, start_lon]
            end_coordinates = [end_lat, end_lon]
            shortest_path = [start_coordinates, end_coordinates]

            # Call the function and get the file path
            file_path = plot_shortest_path(start_coordinates, end_coordinates, shortest_path)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(file_path.endswith(".html"))

#invalid_coordinates
class InvalidCoordinatesTestCase(unittest.TestCase):
    def test_invalid_coordinates(self):
        # Test with invalid coordinates
        start_coordinates = [91.1234, -200]
        end_coordinates = [-100.9876, 300]
        shortest_path = [start_coordinates, end_coordinates]

        # Assert that the function raises a ValueError
        with self.assertRaises(ValueError):
            plot_shortest_path(start_coordinates, end_coordinates, shortest_path)


# different sets of coordinates
class DifferentCoordinatesTestCase(unittest.TestCase):
    def test_different_coordinates(self):
        for _ in range(10):
            start_lat = random.uniform(-90, 90)
            start_lon = random.uniform(-180, 180)
            end_lat = random.uniform(-90, 90)
            end_lon = random.uniform(-180, 180)

            start_coordinates = [start_lat, start_lon]
            end_coordinates = [end_lat, end_lon]
            shortest_path = [start_coordinates, end_coordinates]

            # Call the function and get the file path
            file_path = plot_shortest_path(start_coordinates, end_coordinates, shortest_path)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(file_path.endswith(".html"))

if __name__ == '__main__':
    unittest.main()