import unittest
import sys
from itertools import groupby
from datetime import datetime, timedelta

from test_config import *

sys.path.append('../')
from AlphaStream.Models.OrderEnums import *
from AlphaStream import AlphaStreamClient


class GetAlphaOrders(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_GetAlphaOrders(self):
        start = 0
        orders = []
        alphaId = "21a2a00a097117a84788c1434"
        while start < 1000:
            response = self.client.GetAlphaOrders(alphaId, start = start)
            orders += response
            start += 100
        self.assertGreater(len(orders), 0)
        for i in range(len(orders) - 2):
            for order in orders[i+1 : len(orders) - i - 1]:
                self.assertLessEqual(orders[i].CreatedTime, order.CreatedTime)

            order = orders[i]
            self.assertNotEqual(OrderStatus('none'), order.Status);
            self.assertIsNotNone(order.Symbol);
            self.assertIsNotNone(order.AlgorithmId);
            self.assertNotEqual(0, order.OrderId);
            self.assertNotEqual(0, order.SubmissionLastPrice);
            self.assertNotEqual(0, order.SubmissionAskPrice);
            self.assertNotEqual(0, order.SubmissionBidPrice);
            self.assertIsNotNone(order.Source);

            if order.Status == OrderStatus('filled'):
                orderEvent = order.OrderEvents[-1]
                self.assertTrue(orderEvent.Status == OrderStatus('filled'))
                self.assertNotEqual(0, orderEvent.FillPrice)
                self.assertGreater(len(orderEvent.FillPriceCurrency), 0)

            elif order.Status == OrderStatus('canceled'):
                orderEvent = order.OrderEvents[-1]
                self.assertTrue(orderEvent.Status == OrderStatus('canceled'))

            if (order.Type == OrderType('limit')) or (order.Type == OrderType('stopLimit')):
                self.assertFalse(any([x.LimitPrice == 0 for x in order.OrderEvents]))
            if (order.Type == OrderType('stopMarket')) or (order.Type == OrderType('stopLimit')):
                self.assertFalse(any([x.StopPrice == 0 for x in order.OrderEvents]))
