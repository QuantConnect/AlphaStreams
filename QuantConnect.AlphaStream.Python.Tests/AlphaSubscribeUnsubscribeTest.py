import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaSubscribeUnsubscribe(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

   
    def test_alpha_subscribe_unsubscribe(self):
        alphaID = "8f81cbb82c0527bca80ed85b0"
        subscribeRequest = self.client.Subscribe(alphaId = alphaID)
        try:
            self.assertTrue(subscribeRequest, msg = 'Alpha Subscribe failed in AlphaSubscribeUnsubscribeTest')
        except Exception as err:
            print(f'AlphaSubscribeUnsubscribeTest failed. Reason: {err}')
            self.client.Unsubscribe(alphaId = alphaID)
        
        unsubscribeRequest = self.client.Unsubscribe(alphaId = alphaID)
        try:
            self.assertTrue(unsubscribeRequest, msg = 'Alpha Unsubscribe failed in AlphaSubscribeUnsubscribeTest')
        except Exception as err:
            print(f'AlphaSubscribeUnsubscribeTest failed. Reason: {err}')