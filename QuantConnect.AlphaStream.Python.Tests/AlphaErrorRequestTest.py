import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaPriceRequest(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_price_request(self):
        response = self.client.GetAlphaErrors(alphaId = '5443d94e213604f4fefbab185')
        try:
            self.assertIsNotNone(response)
            self.assertEqual(str(response[0]), 'Error at 2019-02-19 06:07:41, message: Algorithm., stacktrace: System.Exc')
        except:
            raise Exception('AlphaErrorRequestTest failed.')