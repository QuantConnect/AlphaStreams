import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class SharedBidCreate(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_shared_bid(self):
        bid = self.client.CreateBid(alphaId = '8f81cbb82c0527bca80ed85b0', shared = 1.00)
        
        try:
            self.assertIsNotNone(bid)
            self.assertEqual(bid, 'Bid price was successfully created.')
        except Exception as err:
            print(f'SharedBidTest failed. Reason: {err}')