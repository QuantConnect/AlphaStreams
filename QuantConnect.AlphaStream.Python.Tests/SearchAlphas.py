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
        list_response = self.client.SearchAlphas(accuracy = [0.25, 0.75])
        response = self.client.SearchAlphas(accuracyMinimum = 0.25, accuracyMaximum = 0.75)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
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
        list_response = self.client.SearchAlphas(exclusiveFee=[0, 100000])
        response = self.client.SearchAlphas(exclusiveFeeMinimum = 0, exclusiveFeeMaximum = 100000)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
            self.assertGreaterEqual(alpha.ExclusiveSubscriptionFee, 0)
            self.assertLessEqual(alpha.ExclusiveSubscriptionFee, 100000)

    def test_AlphaSharedFee(self):
        list_response = self.client.SearchAlphas(sharedFee=[0, 100000])
        response = self.client.SearchAlphas(sharedFeeMinimum = 0, sharedFeeMaximum = 100000)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
            self.assertGreaterEqual(alpha.SharedSubscriptionFee, 0)
            self.assertLessEqual(alpha.SharedSubscriptionFee, 100000)

    def test_AlphaSharpeRatio(self):
        list_response = self.client.SearchAlphas(sharpe=[-3, 3])
        response = self.client.SearchAlphas(sharpeMinimum = -3, sharpeMaximum = 3)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
            self.assertGreaterEqual(alpha.SharpeRatio, -3)
            self.assertLessEqual(alpha.SharpeRatio, 3)

    def test_AlphaTags(self):
        tags = ['Immediate', 'Global Macro', 'Lookahead Bias', 'Basket Selection', 'Events']
        response = self.client.SearchAlphas(includedTags = tags, excludedTags = ['Mean Reversion', 'Equal Weighting', 'Single Selection'])
        self.assertIsNotNone(response)
        alphas = [response[x].Id for x in range(len(response))]
        self.assertGreater(len(alphas), 0)
        self.assertIn('5443d94e213604f4fefbab185', alphas)

    def test_AlphaUniqueness(self):
        list_response = self.client.SearchAlphas(uniqueness = [0, 0.5])
        response = self.client.SearchAlphas(uniquenessMinimum = 0, uniquenessMaximum = 0.5)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
            self.assertGreaterEqual(alpha.Uniqueness, 0)
            self.assertLessEqual(alpha.Uniqueness, 0.5)

    def test_AlphaSymbols(self):
        response = self.client.SearchAlphas(symbols = ['AUDUSG 8G', 'EURAUD 8G', 'AUDJPY 8G'])
        self.assertIsNotNone(response)
        alphas = [response[x].Id for x in range(len(response))]
        self.assertGreater(len(alphas), 0)
        self.assertIn('5443d94e213604f4fefbab185', alphas)

    def test_AlphaDtwDistance(self):
        list_response = self.client.SearchAlphas(dtwDistance=[0, 0.2])
        response = self.client.SearchAlphas(dtwDistanceMinimum = 0, dtwDistanceMaximum = 0.2)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
            self.assertGreaterEqual(alpha.OutOfSampleDtwDistance, 0)
            self.assertLessEqual(alpha.OutOfSampleDtwDistance, 0.2)

    def test_AlphaReturnsCorrelation(self):
        list_response = self.client.SearchAlphas(returnsCorrelation=[0.25, 0.75])
        response = self.client.SearchAlphas(returnsCorrelationMinimum = 0.25, returnsCorrelationMaximum = 0.75)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
            self.assertGreaterEqual(alpha.OutOfSampleReturnsCorrelation, 0.25)
            self.assertLessEqual(alpha.OutOfSampleReturnsCorrelation, 0.75)

    def test_AlphaTrialPeriod(self):
        list_response = self.client.SearchAlphas(trial=[0, 100])
        response = self.client.SearchAlphas(trialMinimum = 0, trialMaximum = 100)
        self.assertIsNotNone(list_response)
        self.assertIsNotNone(response)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for alpha in response:
            self.assertGreaterEqual(alpha.Trial, 0)
            self.assertLessEqual(alpha.Trial, 100)