import unittest
import sys
from test_config import *
from datetime import datetime, timedelta
from AlphaStream.Models import HeartbeatPackage, OrderEvent, Order

sys.path.append('../')

from AlphaStream import *
class StreamAlphaOrderEvents(unittest.TestCase):
    def setUp(self):
        config = test_config()

        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])
        self.streamClient = AlphaStreamEventClient(config['rabbitmq_user'], config['rabbitmq_password'], config['rabbitmq_ipaddress'], config['rabbitmq_virtualhost'], config['rabbitmq_exchange'])

        # Setup conditions
        alphaID = "21a2a00a097117a84788c1434"
        try:
            self.client.Subscribe(alphaId=alphaID)
            self.client.Unsubscribe(alphaId=alphaID)
        except:
            self.client.Unsubscribe(alphaId=alphaID)

    def test_StreamOrderEvents(self):
        alphaId = '21a2a00a097117a84788c1434'
        received = []
        self.client.Subscribe(alphaId)

        for response in self.streamClient.StreamSynchronously(alphaId, timeout = 60):
            received += [response]
        self.assertGreater(len(received), 0)

        for response in received:
            if isinstance(response, Order):
                self.assertEqual(response.AlgorithmId, 'A-4f4343d0fd8e5ad2cf61ce69c2854434')
                self.assertEqual(response.Symbol, 'BTCUSD XJ')
                self.assertEqual(response.Source, 'live trading')
                if response.StopPrice is not None:
                    self.assertNotEqual(response.StopPrice, 0)
                if response.LimitPrice is not None:
                    self.assertNotEqual(response.StopPrice, 0)
                for x in [response.SubmissionLastPrice, response.SubmissionBidPrice, response.SubmissionAskPrice]:
                    self.assertNotEqual(x, 0)
                for x in response.OrderEvents:
                    self.assertTrue(x.Id.startswith(response.Id, 0, len(response.Id)))

            elif isinstance(response, HeartbeatPackage):
                self.assertEqual(response.AlphaId, alphaId)
                self.assertLessEqual(datetime.strptime(response.MachineTime, "%Y-%m-%dT%H:%M:%S.%fz"), datetime.utcnow())
                self.assertEqual(response.AlgorithmId, 'A-4f4343d0fd8e5ad2cf61ce69c2854434')