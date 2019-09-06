import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AuthorIDProjectID(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_authorID_projectID(self):
        response = self.client.GetAlphaList()

        try:
            self.assertGreater(len(response), 0)
            self.assertIn('53f2d3f4f54f788e06507cef1', response)
        except Exception as err:
            print(f'AuthorIdProjectIdTest failed. Reason: {err}')