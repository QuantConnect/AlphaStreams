import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaSubscribeUnsubscribe(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

        # Setup conditions
        alphaID = "d0fc88b1e6354fe95eb83225a"
        try:
            self.client.Subscribe(alphaId=alphaID)
            self.client.Unsubscribe(alphaId=alphaID)
        except:
            self.client.Unsubscribe(alphaId=alphaID)

    def test_alpha_subscribe_unsubscribe(self):
        alphaID = "d0fc88b1e6354fe95eb83225a"
        subscribeRequest = self.client.Subscribe(alphaId=alphaID)
        unsubscribeRequest = self.client.Unsubscribe(alphaId=alphaID)
        self.assertTrue(subscribeRequest)
        self.assertTrue(unsubscribeRequest)

    def test_alpha_double_subscribe(self):
        alphaID = "d0fc88b1e6354fe95eb83225a"
        self.client.Subscribe(alphaId = alphaID)
        self.assertRaises(Exception, self.client.Subscribe, alphaID)

        # Make sure to unsubscribe at the end
        self.client.Unsubscribe(alphaId=alphaID)

    def test_alpha_subscribe_subscribe_same_family(self):
        alphaID = "80bbae649ca2e4e328fe49c0f"
        same_family = "965559f6bd86a053e8042e1bf"

        first_subscribe_request = self.client.Subscribe(alphaId=alphaID)
        second_subscribe_request = self.client.Subscribe(alphaId=same_family)

        first_unsubscribe_request = self.client.Unsubscribe(alphaId=alphaID)
        second_unsubscribe_request = self.client.Unsubscribe(alphaId=same_family)

        self.assertTrue(first_subscribe_request)
        self.assertTrue(second_subscribe_request)
        self.assertEqual(first_subscribe_request, second_subscribe_request)

        self.assertTrue(first_unsubscribe_request)
        self.assertTrue(second_unsubscribe_request)
        self.assertEqual(first_unsubscribe_request, second_unsubscribe_request)


    def test_alpha_unsubscribe_not_subscribed(self):
        alphaID = "d0fc88b1e6354fe95eb83225a"
        self.assertRaises(Exception, self.client.Unsubscribe, alphaID)

    def test_alpha_subscribe_stopped_alpha(self):
        alphaId = "5443d94e213604f4fefbab185"
        self.assertRaises(Exception, self.client.Subscribe, alphaId)










