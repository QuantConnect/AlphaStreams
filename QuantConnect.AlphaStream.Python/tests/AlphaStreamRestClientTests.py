from AlphaStreamClient import AlphaStreamClient
import unittest
import os
from datetime import datetime

TestAlphaId  = "392a40ccab3740287a1c30bc6"
TestAuthorId = "1f48359f6c6cbad65b091232eaae73ce"

# Please add your credentials. Found at https://www.quantconnect.com/account
clientId = "c7bd966e930c4b15b2ec13eb0d6170d9"
apiToken    = "7030e89cfcc1948f4f93e91edd93d6f687c737844a6969d99d609a78f8d0a5c4091ef11f31c4c0e9cccacefe36ff4c2ad0e15525a85c65b0eafa34064cd11b1c"

class AlphaStreamRestClientTests(unittest.TestCase):

    def setUp(self):
        # Create a new instance of the client module:
        self.client = AlphaStreamClient(clientId, apiToken)

    def test_GetsAlphaById(self):
        response = self.client.GetAlphaById(alphaId = TestAlphaId)
        self.assertIsNotNone(response)
        self.assertEqual(response.Id, TestAlphaId)

    def test_GetAlphaInsights(self):
        response = self.client.GetAlphaInsights(alphaId = TestAlphaId)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)

    def test_GetAuthorById(self):
        response = self.client.GetAuthorById(authorId = TestAuthorId)
        self.assertIsNotNone(response)
        self.assertEqual(response.Id, TestAuthorId)
        self.assertEqual(response.Language, "C#")

    def test_GetAlphaPrices(self):
        response = self.client.GetAlphaPrices(alphaId = TestAlphaId)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        price = response[0]
        self.assertEquals(price.PriceType, 'ask')
        self.assertEquals(price.ExclusivePrice, 104000)
        self.assertEquals(price.SharedPrice, 104000)

    def test_GetAlphaErrors(self):
        response = self.client.GetAlphaErrors(alphaId = TestAlphaId)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        error = response[0]
        self.assertEquals(error.Error[:10], 'Test Error')
        self.assertEquals(error.Stacktrace[:10], 'Test stack')

    def test_SearchAlphas(self):
        response = self.client.SearchAlphas(
                sharedFeeMinimum = 0,
                sharedFeeMaximum = 999999)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        for alpha in response:
            self.assertGreater(alpha.SharedSubscriptionFee, 0)
            self.assertLess(alpha.SharedSubscriptionFee, 999999)

    def test_SearchAuthors(self):
        response = self.client.SearchAuthors(languages = ["Py"], location = "New York")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        for author in response:
            self.assertEquals(author.Language, "Py")
            self.assertGreater(author.Location.find("New York"), -1)

    def test_Subscribe(self):
        response = self.client.Subscribe(alphaId = TestAlphaId)
        self.assertIsNotNone(response)
        self.assertTrue(response)

    def test_Unsubscribe(self):
        response = self.client.Unsubscribe(alphaId = TestAlphaId)
        self.assertIsNotNone(response)
        self.assertTrue(response)
    
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)