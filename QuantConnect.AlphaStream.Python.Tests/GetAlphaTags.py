import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import *

class AlphaPriceRequest(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_GetAlphaTags(self):
        response = self.client.GetAlphaTags()
        self.assertIsInstance(response, list)
        self.assertGreaterEqual(len(response), 40)
        for x in response:
            self.assertGreater(len(x.TagName), 0)
            self.assertGreaterEqual(x.Matches, 0)

    def test_SearchAlphaTagsMatch(self):
        get_tags_response = self.client.GetAlphaTags()
        for tag in get_tags_response:
            hasData = True
            search_alphas_response = []
            start = 0
            while hasData:
                response = self.client.SearchAlphas(includedTags = [f'{tag.TagName}'], start = start)
                search_alphas_response += response
                start += 100
                hasData = len(response)

            self.assertEqual(len(search_alphas_response), tag.Matches)
            for alpha in search_alphas_response:
                self.assertIn(tag.TagName, alpha.Tags)