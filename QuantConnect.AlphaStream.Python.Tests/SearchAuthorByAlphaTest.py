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

        ## Get local test data
        expected_author_list = read_test_data("AlphaAuthorTestData.txt")
        expected = sorted(expected_author_list[:30])
        expected_ids = list(set([entry.split(":")[0] for entry in expected]))

        ## Get API responses
        responseAlphaAuthors = []
        alphaIDs = self.client.GetAlphaList()
        matchedIDs = [id for id in alphaIDs if id in expected_ids]
        for id in matchedIDs:
            alpha = self.client.GetAlphaById(id)
            responseAlphaAuthors.append(str(id) + ":" + str(alpha.Project.Author))
        expected = sorted(expected[:len(matchedIDs)])
        response = sorted(responseAlphaAuthors[:len(expected)])

        try:
            self.assertCountEqual(response, expected)
            self.assertListEqual(response, expected)
        except Exception as err:
                print(f'AlphaAuthorTest failed. Reason: {err}')