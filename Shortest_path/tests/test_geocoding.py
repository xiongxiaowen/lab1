
import unittest
from geopy.geocoders import Nominatim
import math

# making an instance of Nominatim class
geolocator = Nominatim(user_agent="shortest_path_app")

GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"

class GeocodingTestCase(unittest.TestCase):
    def test_geocoding(self):
        #incl. both valid and invalid addresses
        addresses = [
            ("90100 Oulu, Finland", 65.01235, 25.4651),
            ("Helsinki, Finland", 60.16986, 24.9384),
            ("Tampere, Finland", 61.49777, 23.7609),
            ("Invalid Address, 1", None, None)
        ]

        for address, expected_lat, expected_lon in addresses:
            location = geolocator.geocode(address)
            if expected_lat is not None and expected_lon is not None:
                self.assertIsNotNone(location)
                self.assertEqual(round(location.latitude, 2), round(expected_lat, 2))
                self.assertEqual(round(location.longitude, 2), round(expected_lon, 2))
            else:
                self.assertIsNone(location)

if __name__ == '__main__':
    unittest.main()