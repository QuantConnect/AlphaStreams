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
        alphaID = "8f81cbb82c0527bca80ed85b0"
        bid = self.client.CreateBid(alphaId = alphaID, exclusive = 1, good_until = datetime.utcnow() + timedelta(seconds = 3610))
        self.assertIsNotNone(bid)
        self.assertEqual(bid, 'Bid price was successfully created.')



