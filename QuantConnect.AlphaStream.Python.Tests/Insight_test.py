import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient


class Insights(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_get_insights(self):

        alpha_id = "53f2d3f4f54f788e06507cef1"

        offset = 0
        in_sample_insights = []
        response = self.client.GetAlphaInsights(alpha_id, offset)

        while len(response) > 0:

            for insight in response:
                offset += 1
                if insight.Source == "in sample":
                    in_sample_insights.append(insight)

            response = self.client.GetAlphaInsights(alpha_id, offset)
            
        expected_in_sample_insights = read_test_data("get_insights.txt")
        result_in_sample = get_string_list(in_sample_insights)

        self.assertEqual(len(result_in_sample), len(expected_in_sample_insights))
        self.assertListEqual(result_in_sample, expected_in_sample_insights)
