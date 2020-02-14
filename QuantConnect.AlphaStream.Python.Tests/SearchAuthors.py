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
        list_response = self.client.SearchAuthors(forumDiscussions = [1, 5])
        response = self.client.SearchAuthors(forumDiscussionsMinimum = 1, forumDiscussionsMaximum = 5)
        self.assertIsNotNone(list_response)
        self.assertGreater(len(list_response), 0)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for author in response:
            self.assertGreaterEqual(author.ForumDiscussions, 1)
            self.assertLessEqual(author.ForumDiscussions, 5)

    def test_ForumComments(self):
        list_response = self.client.SearchAuthors(forumComments = [1, 5])
        response = self.client.SearchAuthors(forumCommentsMinimum = 1, forumCommentsMaximum = 5)
        self.assertIsNotNone(list_response)
        self.assertGreater(len(list_response), 0)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for author in response:
            self.assertGreaterEqual(author.ForumComments, 1)
            self.assertLessEqual(author.ForumComments, 5)

    def test_AlphasListed(self):
        list_response = self.client.SearchAuthors(alphasListed = [1,5])
        response = self.client.SearchAuthors(alphasListedMinimum = 1, alphasListedMaximum = 5)
        self.assertIsNotNone(list_response)
        self.assertGreater(len(list_response), 0)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for author in response:
            self.assertGreaterEqual(author.AlphasListed, 1)
            self.assertLessEqual(author.AlphasListed, 5)

    def test_SignedUp(self):
        now = datetime.now().timestamp()
        list_response = self.client.SearchAuthors(signedUp = [1483228800, now])
        response = self.client.SearchAuthors(signedUpMinimum = 1483228800, signedUpMaximum = now)
        self.assertIsNotNone(list_response)
        self.assertGreater(len(list_response), 0)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        self.assertListEqual([x.Id for x in list_response], [x.Id for x in response])
        for author in response:
            self.assertGreaterEqual(author.SignUpTime, datetime.fromtimestamp(1483228800))
            self.assertLessEqual(author.SignUpTime, datetime.fromtimestamp(now))

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
        self.assertGreater(len(response), 0)
        self.assertEqual(response[0].Id, '2b2552a1c05f83ba4407d4c32889c367')

    def test_AuthorLogin(self):
        now = datetime.utcnow().timestamp()
        authors = self.client.SearchAuthors(lastLoginMinimum = 1551398400, lastLoginMaximum = now)
        self.assertIsNotNone(authors)
        self.assertGreaterEqual(len(authors), 0)
        for author in authors:
            self.assertGreaterEqual(author.LastOnlineTime, datetime.utcfromtimestamp(1551398400))
            self.assertLessEqual(author.LastOnlineTime, datetime.utcfromtimestamp(now))

    def test_AuthorMultifieldSearch(self):
        language = "C#"
        location = ' Virginia, US'
        response = self.client.SearchAuthors(languages = language, location = location)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        self.assertEqual(response[0].Language, language)
        self.assertEqual(response[0].Location, location)
        self.assertIn("2b2552a1c05f83ba4407d4c32889c367", [x.Id for x in response])

    def test_get_alpha_author(self):
        alphaId = "d0fc88b1e6354fe95eb83225a"
        authorId = "2b2552a1c05f83ba4407d4c32889c367"

        author = self.client.GetAuthorById(authorId)
        alpha = self.client.GetAlphaById(alphaId)
        self.assertIsNotNone(alpha)
        self.assertIsNotNone(author)

        authorAlphas = author.Alphas
        self.assertIsInstance(authorAlphas, list)
        self.assertGreater(len(authorAlphas), 0)
        self.assertIn(alphaId, authorAlphas)