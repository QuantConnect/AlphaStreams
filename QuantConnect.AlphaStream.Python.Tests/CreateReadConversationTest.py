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
        #np.random.seed(42)
        #number = np.random.uniform(0, 10000)
        #subject = f'Test subject -- {number}'
        try:
            request = self.client.CreateConversation(alphaId = '5443d94e213604f4fefbab185', email = 'alpha+client.c280a2d860118be50c4c84c51bc84351b65a17c1ce8de3c4bee7d5584d5e@quantconnect.com',
                                                    subject = 'Create Conversation API test.', message = 'Conversation API Test')
            self.assertIsNotNone(request)
            self.assertEqual(request, 'Conversation thread was successfully created.')
        except Exception as err:
                print(f'CreateConversation failed. Reason: {err}')
#        time.sleep(150)
        try:
            readResponse = self.client.ReadConversation(alphaId = '5443d94e213604f4fefbab185', message = 'Conversation API Test')#message = 'Autoreply -- Conversation request successfully received.')
            
            self.assertIsNotNone(readResponse)
            self.assertEqual(readResponse, 'Conversation thread was successfully read.')
        except Exception as err:
            print(f'ReadConversation failed. Reason: {err}')