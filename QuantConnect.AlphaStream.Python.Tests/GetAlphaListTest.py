import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaIDList(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

   
    def test_get_alpha_list(self):
        response = self.client.GetAlphaList()
        self.assertIsNotNone(response)
        self.assertGreaterEqual(len(response), 0)
        self.assertIn('8f81cbb82c0527bca80ed85b0', response)

    def test_get_alpha_by_id(self):
        alphaId = "8f81cbb82c0527bca80ed85b0"
        response = self.client.GetAlphaById(alphaId=alphaId)
        self.assertIsNotNone(response)
        self.assertEqual(response.Id, alphaId)
        self.assertEqual(response.Authors[0].Id, "604b579e6e335059d878dc6b412d1c15")
        self.assertEqual(response.Name, "AS SDK Test Alpha")