import unittest
import sys
from test_config import *
import numpy as np
import time

sys.path.append('../')

from AlphaStream import AlphaStreamClient

class CreateConversationRequest(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_create_conversation(self):
        alphaId = '118d1cbc375709792ea4d823a'
        email = 'support@quantconnect.com'
        subject = "Alpha Conversation"
        message = "Hello World!"
        cc = "support@quantconnect.com"
        request = self.client.CreateConversation(alphaId = alphaId, email = email, subject = subject, message = message,
                                                 cc=cc)
        self.assertIsNotNone(request)
        self.assertEqual(request, 'Conversation thread was successfully created.')

        readResponse = self.client.ReadConversation(alphaId = alphaId)
        self.assertIsNotNone(readResponse)
        self.assertEqual(readResponse, 'Conversation thread was successfully read.')
        self.assertGreaterEqual(len(readResponse), 34)