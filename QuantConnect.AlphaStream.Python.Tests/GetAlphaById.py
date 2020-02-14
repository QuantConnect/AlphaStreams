import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class GetAlphaByID(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_get_alpha_by_id(self):
        alphaId = "d0fc88b1e6354fe95eb83225a"
        response = self.client.GetAlphaById(alphaId=alphaId)
        self.assertIsNotNone(response)
        self.assertEqual(response.Id, alphaId)
