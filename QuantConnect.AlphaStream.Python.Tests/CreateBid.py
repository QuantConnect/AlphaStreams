import unittest
import sys
from test_config import *
from datetime import datetime, timedelta

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class SharedBidCreate(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_shared_bid(self):
        bid = self.client.CreateBid(alphaId = 'd0fc88b1e6354fe95eb83225a', shared = 1, good_until = datetime.utcnow() + timedelta(seconds = 3610))
        self.assertIsNotNone(bid)
        self.assertEqual(bid, 'Bid price was successfully created.')

    def test_exclusive_bid(self):
        alphaID = "d0fc88b1e6354fe95eb83225a"
        bid = self.client.CreateBid(alphaId = alphaID, exclusive = 1, good_until = datetime.utcnow() + timedelta(seconds = 3610))
        self.assertIsNotNone(bid)
        self.assertEqual(bid, 'Bid price was successfully created.')
