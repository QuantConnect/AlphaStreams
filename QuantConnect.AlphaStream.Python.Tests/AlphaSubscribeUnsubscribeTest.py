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
        try:
            self.client.Subscribe(alphaId=alphaID)
        except:
            self.client.Unsubscribe(alphaId=alphaID)
            subscribeRequest = self.client.Subscribe(alphaId=alphaID)
            self.assertTrue(subscribeRequest)

        try:
            self.client.Unsubscribe(alphaId=alphaID)
        except:
            self.client.Subscribe(alphaId=alphaID)
            unsubscribeRequest = self.client.Unsubscribe(alphaId=alphaID)
            self.assertTrue(unsubscribeRequest)

    def test_alpha_double_subscribe(self):
        alphaID = "8f81cbb82c0527bca80ed85b0"
        try:
            self.client.Subscribe(alphaId = alphaID)
        except:
            self.assertRaises(Exception, self.client.Subscribe, alphaID)
        self.assertRaises(Exception, self.client.Subscribe, alphaID)
        self.client.Unsubscribe(alphaId=alphaID)

    def test_alpha_subscribe_subscribe_same_family(self):
        alphaID = "8f81cbb82c0527bca80ed85b0"
        same_family = "019262286c58ee31ca7bf852f"

        try:
            first_subscribe_request = self.client.Subscribe(alphaId=alphaID)
            try:
                second_subscribe_request = self.client.Subscribe(alphaId=same_family)
            except:
                self.client.Unsubscribe(alphaId=alphaID)
                second_subscribe_request = self.client.Subscribe(alphaId=alphaID)
        except:
            self.client.Unsubscribe(alphaId=alphaID)
            first_subscribe_request = self.client.Subscribe(alphaId=alphaID)
            try:
                second_subscribe_request = self.client.Subscribe(alphaId=same_family)
            except:
                self.client.Unsubscribe(alphaId=alphaID)
                second_subscribe_request = self.client.Subscribe(alphaId=alphaID)

        self.assertTrue(first_subscribe_request)
        self.assertTrue(second_subscribe_request)
        self.assertEqual(first_subscribe_request, second_subscribe_request)
        self.client.Unsubscribe(alphaId=alphaID)
        self.client.Unsubscribe(alphaId=same_family)

    def test_alpha_unsubscribe_not_subscribed(self):
        alphaID = "8f81cbb82c0527bca80ed85b0"
        self.assertRaises(Exception, self.client.Unsubscribe, alphaID)










