import unittest
import sys
from itertools import groupby
from datetime import datetime, timedelta

from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient


class Insights(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_get_insights(self):

        alphaId = "8f81cbb82c0527bca80ed85b0"
        start = 0
        insights = []
        # Fetch all Insights in the Alpha's backtest
        while start < 500:
            insights += self.client.GetAlphaInsights(alphaId, start)
            start += 100

        self.assertIsNotNone(insights)
        self.assertGreaterEqual(len(insights), 0)

        # check that Insights are in chronological order
        for i in range(len(insights) - 1):
            for j in insights[i+1:]:
                self.assertLessEqual(insights[i].CreatedTime, j.CreatedTime)

        insightCollection = sorted(insights, key=lambda x: x.CreatedTime)
        response_ids = [x.Id for x in insightCollection]

        expected_in_sample_ids = read_test_data("InsightTestData.txt")
        # check that response not in-sample IDs == expected not in-sample IDs
        self.assertEqual(len(response_ids), len(expected_in_sample_ids))
        self.assertListEqual(response_ids, expected_in_sample_ids)