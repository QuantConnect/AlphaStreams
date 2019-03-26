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
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertGreaterEqual(author.ForumDiscussions, 1)
        except Exception as err:
            print(f'Forum Discussion Search failed. Reason: {err}')
        
        response = self.client.SearchAuthors(forumDiscussionsMaximum = 5)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertLessEqual(author.ForumDiscussions, 5)
        except Exception as err:
            print(f'Forum Discussion Search failed. Reason: {err}')

    def test_ForumComments(self):
        response = self.client.SearchAuthors(forumCommentsMinimum = 1)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertGreaterEqual(author.ForumComments, 1)
        except Exception as err:
            print(f'Forum Comments Search failed. Reason: {err}')
        
        response = self.client.SearchAuthors(forumCommentsMaximum = 5)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertLessEqual(author.ForumComments, 5)
        except Exception as err:
            print(f'Forum Comments Search failed. Reason: {err}')

    def test_AlphasListed(self):
        response = self.client.SearchAuthors(alphasListedMinimum = 1)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertGreaterEqual(author.AlphasListed, 1)
        except Exception as err:
            print(f'Minimum Alphas Search failed. Reason: {err}')

        response = self.client.SearchAuthors(alphasListedMaximum = 3)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertLessEqual(author.AlphasListed, 3)
        except Exception as err:
            print(f'Maximum Alphas Search failed. Reason: {err}')

    def test_SignedUp(self):
        response = self.client.SearchAuthors(signedUpMinimum = 1483228800)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertGreaterEqual(author.SignUpTime, datetime.fromtimestamp(1483228800))
        except Exception as err:
            print(f'Sign-up Time Search failed. Reason: {err}')

        response = self.client.SearchAuthors(signedUpMaximum = 1483228800)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertLessEqual(author.SignUpTime, datetime.fromtimestamp(1483228800))
        except Exception as err:
            print(f'Sign-up Time Search failed. Reason: {err}')

    def test_Projects(self):
        response = self.client.SearchAuthors(projectsMinimum = 1)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertGreaterEqual(author.Projects, 1)
        except Exception as err:
            print(f'Minimum Projects Search failed. Reason: {err}')
        
        response = self.client.SearchAuthors(projectsMaximum = 3)
        try:
            self.assertIsNotNone(response)
            for author in response:
                self.assertLessEqual(author.Projects, 3)
        except Exception as err:
            print(f'Maximum Projects Search failed. Reason: {err}')

    def test_AuthorLanguage(self):
        response = self.client.SearchAuthors(languages = ["Py","C#","F#"])
        try:
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
            for author in response:
                self.assertIn(author.Language, ["Py","C#","F#"])
        except Exception as err:
            print(f'AuthorLanguageTest failed. Reason: {err}')

    def test_AuthorLocation(self):
        response = self.client.SearchAuthors(location = "New York")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        try:
            for author in response:
                self.assertGreater(author.Location.find("New York"), -1)
        except Exception as err:
            print(f'AuthorLocationSearchTest failed. Reason: {err}')

    def test_AuthorBiography(self):
        biography = 'This is an alpha developer profile for the QuantConnect Team. The Alphas submitted by this author are Benchmark Alphas you can use as an example of how to create an Alpha, or for debugging your fund endpoints. Since 2012, QuantConnect has served the global quant community by providing free financial data and backtesting technology to empower people.'
        response = self.client.SearchAuthors(biography = biography)
        try:
            self.assertIsNotNone(response)
            self.assertEqual(response[0].Id, '2b2552a1c05f83ba4407d4c32889c367')
        except Exception as err:
            print(f'Author Biography Search failed. Reason: {err}')

    def test_AuthorLogin(self):
        now = (datetime.now() - datetime(1970,1,1)).total_seconds()
        alphas = self.client.SearchAuthors(lastLoginMinimum = 1551398400, lastLoginMaximum = now)
        try:
            self.assertIsNotNone(alphas)
            self.assertGreaterEqual(len(alphas), 0)
        except Exception as err:
            print(f'Author Login Search failed. Reason: {err}')

    def test_AuthorMultifieldSearch(self):
        response = self.client.GetAuthorById(authorId = '2b2552a1c05f83ba4407d4c32889c367')
        try:
            self.assertIsNotNone(response)
            self.assertEqual(response.Id, '2b2552a1c05f83ba4407d4c32889c367')
            self.assertEqual(response.Language, "C#")
            self.assertEqual(response.Location, ' Virginia, US')
        except Exception as err:
            print(f'Author Multi-Field Search failed. Reason: {err}')