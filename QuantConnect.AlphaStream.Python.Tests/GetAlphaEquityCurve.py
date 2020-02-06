import sys
import unittest
import pandas as pd
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaEquityCurveRequest(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_get_equity_curve(self):
        alphaId = "d0fc88b1e6354fe95eb83225a"
        response = self.client.GetAlphaEquityCurve(alphaId=alphaId)
        self.assertIsInstance(response, pd.DataFrame)
        self.assertGreater(response.shape[0], 0)
        self.assertGreater(response.shape[1], 0)
        self.assertListEqual(list(response.columns), ['equity', 'sample'])