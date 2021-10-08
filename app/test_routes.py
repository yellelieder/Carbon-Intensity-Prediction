import unittest
import routes


class TestAPI(unittest.TestCase):
    def test_prediction(self):
        self.assertEqual(routes.prediction(lat="50.9917119",long="10.2136589",stdate="28.10.2021",sttime="06:45",endate="29.10.2021",entime="23:59",dur="180"), "29/10/2021 01:15:00")


if __name__ == '__main__':
    unittest.main()