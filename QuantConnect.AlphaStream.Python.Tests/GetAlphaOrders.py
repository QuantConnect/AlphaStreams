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
            self.assertNotEqual(OrderStatus.NoneOrder, order.Status)
            self.assertNotEqual(0, len(order.Symbol))
            self.assertNotEqual(0, len(order.AlgorithmId))
            self.assertNotEqual(0, order.OrderId)
            self.assertNotEqual(0, order.SubmissionLastPrice)
            self.assertNotEqual(0, order.SubmissionAskPrice)
            self.assertNotEqual(0, order.SubmissionBidPrice)
            self.assertNotEqual(0, len(order.Source))

            if all([order.Type == x for x in [OrderType.Market, OrderType.MarketOnOpen, OrderType.MarketOnClose]]) and (order.Status == OrderStatus.Filled):
                self.assertNotEqual(0, order.Price)

            if order.Status == OrderStatus.Filled:
                orderEvent = order.OrderEvents[-1]
                self.assertTrue(orderEvent.Status == OrderStatus.Filled)
                self.assertNotEqual(0, orderEvent.FillPrice)
                self.assertNotEqual(0, len(orderEvent.FillPriceCurrency))

            elif order.Status == OrderStatus.Canceled:
                orderEvent = order.OrderEvents[-1]
                self.assertTrue(orderEvent.Status == OrderStatus.Canceled)
                # Order ID a51cf825449183c9b4e87c8f28f2b7c4-9 was canceled manually, so this will fail but no cause for concern
                self.assertTrue(order.OrderEvents[-2].Status == OrderStatus.CancelPending)

            if (order.Type == OrderType.Limit) or (order.Type == OrderType.StopLimit):
                self.assertFalse(any([x.LimitPrice == 0 for x in order.OrderEvents]))
            if (order.Type == OrderType.StopMarket) or (order.Type == OrderType.StopLimit):
                self.assertFalse(any([x.StopPrice == 0 for x in order.OrderEvents]))
