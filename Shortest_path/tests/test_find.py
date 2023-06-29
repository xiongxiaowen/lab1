## test the find_shortest_path function
import unittest
from unittest.mock import patch 
from shortest_path import app, geocode, find_shortest_path

class TestFindShortestPath(unittest.TestCase):
    @patch('shortest_path.geocode')
    def test_find_shortest_path(self, mock_geocode):
        start_coordinates = (60.1711, 24.9415)  # Central Railway Station
        end_coordinates = (60.3174, 24.9633)  # Helsinki Airport

        # Mock the geocoding service to return real-life addresses
        mock_geocode.side_effect = lambda address: {
            'Central Railway Station': (60.1711, 24.9415),
            'Helsinki Airport': (60.3174, 24.9633),
            'Kamppi Center': (60.1695, 24.9337),
            'Denver': (60.1789, 24.9134)
        }[address]

        # Call the function under test
        path = find_shortest_path(start_coordinates, end_coordinates)
        # Print the actual path
        print("Actual Path:", path)

        # Assert the result
        expected_turning_points = [
            (60.1711, 24.9415),   # Central Railway Station
            (60.1699, 24.9529),  
            (60.1789, 24.9134),  
            (60.3174, 24.9633)  # Helsinki Airport
        ]

        for point in expected_turning_points:
            is_present = any(point == coordinates for coordinates in path)
            self.assertTrue(is_present)

if __name__ == '__main__':
    unittest.main()
