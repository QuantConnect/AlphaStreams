import unittest
import sys
from test_config import *
from datetime import datetime, timedelta
from AlphaStream.Models import HeartbeatPackage, Insight

sys.path.append('../')

from AlphaStream import *
class StreamAlphaInsights(unittest.TestCase):
    def setUp(self):
        config = test_config()

        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])
        self.streamClient = AlphaInsightsStreamClient(config['rabbitmq_user'], config['rabbitmq_password'], config['rabbitmq_ipaddress'], config['rabbitmq_virtualhost'], config['rabbitmq_exchange'])

        # Setup conditions
        alphaID = "31ac5498164db7341b041a732"
        try:
            self.client.Subscribe(alphaId=alphaID)
            self.client.Unsubscribe(alphaId=alphaID)
        except:
            self.client.Unsubscribe(alphaId=alphaID)

    def test_StreamInsights(self):
        ## Emits 1 BTCUSD insight every minute
        alphaId = '31ac5498164db7341b041a732'
        received = []
        self.client.Subscribe(alphaId)

        for response in self.streamClient.StreamSynchronously(alphaId, timeout = 60):
            received += [response]
        self.assertGreater(len(received), 0)

        for response in received:
            if isinstance(response, Insight):
                self.assertEqual(response.Direction, 'flat')
                self.assertEqual(response.Source, 'live trading')
                self.assertEqual(response.Period, 86400.0)
                self.assertEqual(response.Symbol, 'BTCUSD XJ')
                self.assertEqual(response.Type, 'price')
                self.assertEqual(response.SourceModel, 'e2687a6a-24dd-47aa-b8c5-fcab7a30c70d')
                self.assertEqual(response.Weight, 0.5)
                self.assertEqual(response.Confidence, 0.5)
                self.assertEqual(response.Magnitude, 0.5)
                self.assertLessEqual(response.CreatedTime, datetime.utcnow())
                self.assertGreater(response.CloseTime, datetime.utcnow())
                self.assertEqual(response.CreatedTime + timedelta(seconds = response.Period), response.CloseTime)

            elif isinstance(response, HeartbeatPackage):
                self.assertEqual(response.AlphaId, alphaId)
                self.assertLessEqual(datetime.strptime(response.MachineTime, "%Y-%m-%dT%H:%M:%S.%fz"), datetime.utcnow())
                self.assertEqual(response.AlgorithmId, 'A-f338cce0ac051831979d58e38fb7cc03')

        self.client.Unsubscribe(alphaId)

