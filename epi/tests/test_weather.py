import unittest
from epi.forcast import weather
from epi import config

class TestAPI(unittest.TestCase):
    def test_valid(self):
        value=(weather._get_url(42,42))
        self.assertEqual(value, f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=42&lon=42&units=metric&appid={config.openweathermap_key}")

if __name__ == '__main__':
    unittest.main()