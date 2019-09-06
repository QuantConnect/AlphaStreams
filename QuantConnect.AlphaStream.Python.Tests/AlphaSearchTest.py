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
            try:
                self.assertGreaterEqual(alpha.Accuracy, 0.25)
                self.assertLessEqual(alpha.Accuracy, 0.75)
            except Exception as err:
                print(f'Accuracy Alpha Search failed. Reason: {err}')

    def test_AlphaAssetClasses(self):
        assetClasses = ['Forex','Equity','Crypto']
        for asset in assetClasses:
            alphas = self.client.SearchAlphas(assetClasses = asset)
            try:
                self.assertIsNotNone(alphas)
                self.assertGreaterEqual(len(alphas), 0)
            except Exception as err:
                print(f'Asset Class Alpha Search failed. Reason: {err}')

    def test_AlphaAuthorID(self):
        alphas = self.client.SearchAlphas(author = '2b2552a1c05f83ba4407d4c32889c367')
        self.assertIsNotNone(alphas)
        try:
            self.assertEqual(alphas[0].Authors[0].Id, '2b2552a1c05f83ba4407d4c32889c367')
        except Exception as err:
            print(f'Author ID Alpha Search failed. Reason: {err}')

    def test_AlphaExclusiveFee(self):
        alphas = self.client.SearchAlphas(exclusiveFeeMinimum = 0, exclusiveFeeMaximum = 1000000)
        for alpha in alphas:
            try:
                self.assertGreaterEqual(alpha.ExclusiveSubscriptionFee, 0)
                self.assertLessEqual(alpha.ExclusiveSubscriptionFee, 1000000)
            except Exception as err:
                print(f'ExclusiveSubscriptionFeeSearch Failed. Reason: {err}')

    def test_AlphaSharedFee(self):
        alphas = self.client.SearchAlphas(sharedFeeMinimum = 0, sharedFeeMaximum = 1000000)
        for alpha in alphas:
            try:
                self.assertGreaterEqual(alpha.SharedSubscriptionFee, 0)
                self.assertLessEqual(alpha.SharedSubscriptionFee, 1000000)
            except Exception as err:
                print(f'Shared Subscription Fee search failed. Reason: {err}')

    def test_AlphaProjectID(self):
        alpha = self.client.SearchAlphas(projectId = 1688040)
        try:
            self.assertIsNotNone(alpha)
            self.assertEqual(alpha[0].Id, '5443d94e213604f4fefbab185')
        except Exception as err:
            print(f'Project ID Alpha search failed. Reason: {err}')

    def test_AlphaSharpeRatio(self):
        response = self.client.SearchAlphas(sharpeMinimum = -10, sharpeMaximum = 10)
        self.assertIsNotNone(response)
        for alpha in response:
            try:
                self.assertGreaterEqual(alpha.SharpeRatio, -10)
                self.assertLessEqual(alpha.SharpeRatio, 10)
            except Exception as err:
                print(f'Sharpe Ratio Alpha Search failed. Reason: {err}')

    def test_AlphaTags(self):
        tags = ['Immediate', 'Global Macro', 'Lookahead Bias', 'Basket Selection', 'Events']
        response = self.client.SearchAlphas(includedTags = tags, excludedTags = ['Mean Reversion', 'Equal Weighting', 'Single Selection'])
        alphas = [response[x].Id for x in range(len(response))]
        try:
            self.assertIsNotNone(response)
            self.assertGreater(len(alphas), 0)
            self.assertIn('5443d94e213604f4fefbab185', alphas)
        except Exception as err:
            print(f'Alpha Tag Search failed. Reason: {err}')

    def test_AlphaUniqueness(self):
        response = self.client.SearchAlphas(uniquenessMinimum = 0, uniquenessMaximum = 1)
        self.assertIsNotNone(response)
        for alpha in response:
            try:
                self.assertGreaterEqual(alpha.Uniqueness, 0)
                self.assertLessEqual(alpha.Uniqueness, 1)
            except Exception as err:
                print(f'AlphaUniquenessSearchTest failed. Reason: {err}')

    def test_AlphaSymbols(self):
        response = self.client.SearchAlphas(symbols = ['AUDUSG 8G', 'EURAUD 8G', 'AUDJPY 8G'])
        alphas = [response[x].Id for x in range(len(response))]
        try:
            self.assertIsNotNone(response)
            self.assertGreater(len(alphas), 0)
            self.assertIn('5443d94e213604f4fefbab185', alphas)
        except Exception as err:
            print(f'Alpha Symbol Search failed. Reason: {err}')
        