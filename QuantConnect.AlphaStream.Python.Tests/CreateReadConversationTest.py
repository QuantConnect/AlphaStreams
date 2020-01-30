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

    def test_CreateConversation(self):
        alphaId = '8f81cbb82c0527bca80ed85b0'
        email = 'support@quantconnect.com'
        subject = "Alpha Conversation"
        message = "Hello World!"
        cc = "support@quantconnect.com"
        request = self.client.CreateConversation(alphaId = alphaId, email = email, subject = subject, message = message,
                                                 cc=cc)
        self.assertIsNotNone(request)
        self.assertEqual(request, 'Conversation thread was successfully created.')

        readResponse = self.client.ReadConversation(alphaId = alphaId, message = message)
        self.assertIsNotNone(readResponse)
        self.assertEqual(readResponse, 'Conversation thread was successfully read.')