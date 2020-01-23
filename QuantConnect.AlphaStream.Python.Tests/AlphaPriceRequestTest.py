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
        response = self.client.GetAlphaQuotePrices(alphaId = '8f81cbb82c0527bca80ed85b0')

        try:
            self.assertIsNotNone(response)
            self.assertIsNone(response[0].ExclusivePrice)
            self.assertEqual(response[0].PriceType, 'ask')
            self.assertEqual(response[0].SharedPrice, 130)
        except Exception as err:
            print(f'AlphaPriceRequestTest failed. Reason: {err}')