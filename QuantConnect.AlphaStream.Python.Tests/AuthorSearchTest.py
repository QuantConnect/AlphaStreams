import unittest
import sys
from test_config import *
from datetime import datetime

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class AuthorSearch(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_ForumDiscussions(self):
        response = self.client.SearchAuthors(forumDiscussionsMinimum = 1)
        self.assertIsNotNone(response)
        for author in response:
            self.assertGreaterEqual(author.ForumDiscussions, 1)

        response = self.client.SearchAuthors(forumDiscussionsMaximum = 5)
        self.assertIsNotNone(response)
        for author in response:
            self.assertLessEqual(author.ForumDiscussions, 5)

    def test_ForumComments(self):
        response = self.client.SearchAuthors(forumCommentsMinimum = 1)
        self.assertIsNotNone(response)
        for author in response:
            self.assertGreaterEqual(author.ForumComments, 1)

        response = self.client.SearchAuthors(forumCommentsMaximum = 5)
        self.assertIsNotNone(response)
        for author in response:
            self.assertLessEqual(author.ForumComments, 5)

    def test_AlphasListed(self):
        response = self.client.SearchAuthors(alphasListedMinimum = 1)
        self.assertIsNotNone(response)
        for author in response:
            self.assertGreaterEqual(author.AlphasListed, 1)

        response = self.client.SearchAuthors(alphasListedMaximum = 5)
        self.assertIsNotNone(response)
        for author in response:
            self.assertLessEqual(author.AlphasListed, 5)

    def test_SignedUp(self):
        response = self.client.SearchAuthors(signedUpMinimum = 1483228800)
        self.assertIsNotNone(response)
        for author in response:
            self.assertGreaterEqual(author.SignUpTime, datetime.fromtimestamp(1483228800))

        response = self.client.SearchAuthors(signedUpMaximum = 1483228800)
        self.assertIsNotNone(response)
        for author in response:
            self.assertLessEqual(author.SignUpTime, datetime.fromtimestamp(1483228800))

    def test_Projects(self):
        response = self.client.SearchAuthors(projectsMinimum = 1)
        self.assertIsNotNone(response)
        for author in response:
            self.assertGreaterEqual(author.Projects, 1)

        response = self.client.SearchAuthors(projectsMaximum = 3)
        self.assertIsNotNone(response)
        for author in response:
            self.assertLessEqual(author.Projects, 3)

    def test_AuthorLanguage(self):
        response = self.client.SearchAuthors(languages = ["Py","C#","F#"])
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        for author in response:
            self.assertIn(author.Language, ["Py","C#","F#"])

    def test_AuthorLocation(self):
        response = self.client.SearchAuthors(location = "New York")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        for author in response:
            self.assertGreater(author.Location.find("New York"), -1)

    def test_AuthorBiography(self):
        biography = 'This is an alpha developer profile for the QuantConnect Team. The Alphas submitted by this author are Benchmark Alphas you can use as an example of how to create an Alpha, or for debugging your fund endpoints. Since 2012, QuantConnect has served the global quant community by providing free financial data and backtesting technology to empower people.'
        response = self.client.SearchAuthors(biography = biography)
        self.assertIsNotNone(response)
        self.assertEqual(response[0].Id, '2b2552a1c05f83ba4407d4c32889c367')

    def test_AuthorLogin(self):
        now = (datetime.now() - datetime(1970,1,1)).total_seconds()
        alphas = self.client.SearchAuthors(lastLoginMinimum = 1551398400, lastLoginMaximum = now)
        self.assertIsNotNone(alphas)
        self.assertGreaterEqual(len(alphas), 0)

    def test_AuthorMultifieldSearch(self):
        response = self.client.GetAuthorById(authorId = '2b2552a1c05f83ba4407d4c32889c367')
        self.assertIsNotNone(response)
        self.assertEqual(response.Id, '2b2552a1c05f83ba4407d4c32889c367')
        self.assertEqual(response.Language, "C#")
        self.assertEqual(response.Location, ' Virginia, US')
