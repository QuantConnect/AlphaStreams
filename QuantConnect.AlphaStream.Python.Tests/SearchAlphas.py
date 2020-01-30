import unittest
import sys
from test_config import *
from datetime import datetime

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaSearch(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_AlphaAccuracy(self):
        alphas = self.client.SearchAlphas(accuracyMinimum = 0.25, accuracyMaximum = 0.75)
        self.assertIsNotNone(alphas)
        for alpha in alphas:
            self.assertGreaterEqual(alpha.Accuracy, 0.25)
            self.assertLessEqual(alpha.Accuracy, 0.75)

    def test_AlphaAssetClasses(self):
        assetClasses = ['Forex','Equity','Crypto']
        for asset in assetClasses:
            alphas = self.client.SearchAlphas(assetClasses = asset)
            self.assertIsNotNone(alphas)
            self.assertGreaterEqual(len(alphas), 0)

    def test_AlphaAuthorID(self):
        alphas = self.client.SearchAlphas(author = '2b2552a1c05f83ba4407d4c32889c367')
        self.assertIsNotNone(alphas)
        self.assertEqual(alphas[0].Authors[0].Id, '2b2552a1c05f83ba4407d4c32889c367')

    def test_AlphaExclusiveFee(self):
        alphas = self.client.SearchAlphas(exclusiveFeeMinimum = 0, exclusiveFeeMaximum = 1000000)
        for alpha in alphas:
            self.assertGreaterEqual(alpha.ExclusiveSubscriptionFee, 0)
            self.assertLessEqual(alpha.ExclusiveSubscriptionFee, 1000000)

    def test_AlphaSharedFee(self):
        alphas = self.client.SearchAlphas(sharedFeeMinimum = 0, sharedFeeMaximum = 1000000)
        for alpha in alphas:
            self.assertGreaterEqual(alpha.SharedSubscriptionFee, 0)
            self.assertLessEqual(alpha.SharedSubscriptionFee, 1000000)

    def test_AlphaSharpeRatio(self):
        response = self.client.SearchAlphas(sharpeMinimum = -10, sharpeMaximum = 10)
        self.assertIsNotNone(response)
        for alpha in response:
            self.assertGreaterEqual(alpha.SharpeRatio, -10)
            self.assertLessEqual(alpha.SharpeRatio, 10)

    def test_AlphaTags(self):
        tags = ['Immediate', 'Global Macro', 'Lookahead Bias', 'Basket Selection', 'Events']
        response = self.client.SearchAlphas(includedTags = tags, excludedTags = ['Mean Reversion', 'Equal Weighting', 'Single Selection'])
        alphas = [response[x].Id for x in range(len(response))]
        self.assertIsNotNone(response)
        self.assertGreater(len(alphas), 0)
        self.assertIn('5443d94e213604f4fefbab185', alphas)

    def test_AlphaUniqueness(self):
        response = self.client.SearchAlphas(uniquenessMinimum = 0, uniquenessMaximum = 1)
        self.assertIsNotNone(response)
        for alpha in response:
            self.assertGreaterEqual(alpha.Uniqueness, 0)
            self.assertLessEqual(alpha.Uniqueness, 1)

    def test_AlphaSymbols(self):
        response = self.client.SearchAlphas(symbols = ['AUDUSG 8G', 'EURAUD 8G', 'AUDJPY 8G'])
        alphas = [response[x].Id for x in range(len(response))]
        self.assertIsNotNone(response)
        self.assertGreater(len(alphas), 0)
        self.assertIn('5443d94e213604f4fefbab185', alphas)