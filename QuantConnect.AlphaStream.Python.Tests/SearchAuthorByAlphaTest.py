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
        for alpha in alphaIDs:
            author = self.client.GetAlphaById(alpha)
            authors[author.Authors[0].Id] = [x for x in author.Authors[0].Alphas]

        ## Confirm Search by Alpha ID matches author from search by author
        try:
            for author, alphas in authors.items():
                authorResponse = self.client.GetAuthorById(author)
                alphaReponse = authorResponse.Alphas
                self.assertIsNotNone(alphaReponse)
                self.assertListEqual(alphas, alphaReponse)
        except Exception as err:
                print(f'AlphaAuthorTest failed. Reason: {err}')