import unittest
import sys
from test_config import *
from datetime import datetime, timedelta

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class ExclusiveBidCreate(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_exclusive_bid(self):
        alphaID = "5443d94e213604f4fefbab185"
        bid = self.client.CreateBid(alphaId = alphaID, exclusive = 1.00, good_until = datetime.now() + timedelta(minutes = 120))
        try:
            self.assertIsNotNone(bid)
            self.assertEqual(bid, 'Bid price was successfully created.')
        except Exception as err:
            print(f'ExclusiveBidTest failed. Reason: {err}')



