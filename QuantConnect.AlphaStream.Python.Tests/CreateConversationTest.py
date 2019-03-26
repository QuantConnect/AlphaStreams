import unittest
import sys
from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class CreateConversationRequest(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_CreateConversation(self):
        try:
            request = self.client.CreateConversation(alphaId = '5443d94e213604f4fefbab185', email = 'support@quantconnect.com',
                                                    subject = 'Alpha Conversation', message = 'Create Conversation API test.', cc = "support@quantconnect.com")
            self.assertIsNotNone(request)
            self.assertEqual(request, 'Conversation thread was successfully created.')

        except Exception as err:
                print(f'CreateConversationTest failed. Reason: {err}')