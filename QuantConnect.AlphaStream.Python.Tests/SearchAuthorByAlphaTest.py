import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AlphaIDAuthor(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_get_alpha_author(self):

        ## Get all Alphas for each author
        alphaIDs = self.client.GetAlphaList()
        authors = {}
        for alphaId in alphaIDs:
            alpha = self.client.GetAlphaById(alphaId)
            alphaAuthorId = alpha.Authors[0].Id
            authorResponse = self.client.GetAuthorById(alphaAuthorId)
            authorAlphas = authorResponse.Alphas
            self.assertIsNotNone(alpha)
            self.assertIsNotNone(authorResponse)
            self.assertIsInstance(authorAlphas, list)
            self.assertIn(alphaId, authorAlphas)