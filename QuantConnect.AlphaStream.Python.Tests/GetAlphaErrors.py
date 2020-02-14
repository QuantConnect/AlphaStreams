import unittest
import sys
from test_config import *
from datetime import datetime

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaErrorRequest(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_price_request(self):
        response = self.client.GetAlphaErrors(alphaId = '5443d94e213604f4fefbab185')
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        self.assertEqual(response[0].Time, datetime(2019, 2, 19, 6, 7, 41))
        self.assertEqual(str(response[0]), 'Error at 2019-02-19 06:07:41, message: Algorithm., stacktrace: System.Exc')
