import unittest
from epi import routes

class TestAPI(unittest.TestCase):
    def test_valid(self):
        value=(routes.prediction(lat=50.9917119,lng=10.2136589,stdate="28.12.2021",sttime="06:45",enddate="29.12.2021",endtime="23:59",dur=180)[0]["ideal start"])
        self.assertEqual(value, "28/12/2021 12:15:00")

    def test_start_date(self):
        value=(routes.prediction(lat=50,lng=10,stdate="30.12.2021",sttime="06:45",enddate="29.12.2021",endtime="23:59",dur=180)[0]["error"])
        self.assertEqual(value, "end before start")

    def test_point_in_time(self):
        value=(routes.prediction(lat=50,lng=10,stdate="30.06.2021",sttime="06:45",enddate="29.07.2021",endtime="23:59",dur=180)[0]["error"])
        self.assertEqual(value, "enter upcoming timeframe")

    def test_geo(self):
        value=(routes.prediction(lat=80,lng=80,stdate="28.12.2021",sttime="06:45",enddate="29.12.2021",endtime="23:59",dur=180)[0]["error"])
        self.assertEqual(value, "enter german coodrinates")

    def test_lat(self):
        value=(routes.prediction(lat=91,lng=10,stdate="28.12.2021",sttime="06:45",enddate="29.12.2021",endtime="23:59",dur=180)[0]["error"])
        self.assertEqual(value, "lattitude out of rang")

    def test_lng(self):
        value=(routes.prediction(lat=50,lng=181,stdate="28.12.2021",sttime="06:45",enddate="29.12.2021",endtime="23:59",dur=180)[0]["error"])
        self.assertEqual(value, "longitude out of range")

if __name__ == '__main__':
    unittest.main()