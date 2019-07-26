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

        ## Get local test data
        expected_author_list = read_test_data("AuthorIdProjectIdTestData.txt")
        expected = sorted(expected_author_list[:30])
        expected_ids = [entry.split(":")[0] for entry in expected]

        ## Get API responses
        responseAlphaAuthors = []
        alphaIDs = self.client.GetAlphaList()
        for id in alphaIDs:
            alpha = self.client.GetAlphaById(id)
            if alpha.Authors[0].Id in expected_ids:
                responseAlphaAuthors.append(str(alpha.Authors[0].Id) + ":" + str(alpha.Project.Id))

        response = sorted(responseAlphaAuthors[:30])

        try:
            self.assertCountEqual(response, expected)
            self.assertListEqual(response, expected)
        except Exception as err:
            print(f'AuthorIdProjectIdTest failed. Reason: {err}')