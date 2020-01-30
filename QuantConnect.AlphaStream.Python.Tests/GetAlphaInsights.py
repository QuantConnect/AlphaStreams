import unittest
import sys
from itertools import groupby

from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient


class Insights(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_get_insights(self):

        alphaId = "8f81cbb82c0527bca80ed85b0"
        hasData = True
        start = 0
        insights = []
        # Fetch all Insights in the Alpha's backtest
        while hasData:
            responseInsights = self.client.GetAlphaInsights(alphaId, start)  # Fetch alpha Insights (backtest and live)
            insights += [x for x in responseInsights if x.Source != 'live trading']
            hasData = len(responseInsights)
            start += 100

        insightCollection = [list(g) for k, g in groupby(sorted(insights, key=lambda x: x.CreatedTime),
                                                         key=lambda x: x.CreatedTime)]
        insightCollection = [item for sublist in insightCollection for item in sublist]
        response_ids = [x.Id for x in insightCollection]

        expected_in_sample_ids = read_test_data("InsightTestData.txt")
        self.assertEqual(len(response_ids), len(expected_in_sample_ids))
        self.assertListEqual(response_ids, expected_in_sample_ids)
        self.assertIsNotNone(response_ids)
        self.assertGreaterEqual(len(response_ids), 0)