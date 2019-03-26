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
        
        try:
            self.assertIsNotNone(response)
            self.assertGreaterEqual(len(response), 0)
            self.assertIn('5443d94e213604f4fefbab185', response)
        except Exception as err:
            print(f'AlphaIdTest failed. Reason: {err}')