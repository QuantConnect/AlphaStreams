from .Order import Order
from .Insight import Insight
from .OrderEvent import OrderEvent

class AlphaResultPackage:
    """Package holding a group of insights, orders, and/or order events from one moment of time."""

    def __init__(self, json):

        self.AlphaId = json['alpha-id']

        self.AlgorithmId = json['algorithm-id']

        self.Insights = []

        self.Orders = []

        insights = json.get('insights', [])

        for i in insights:
            i['source'] = 'live trading'
            self.Insights.append(Insight(i))

        orderEvents = [OrderEvent(x) for x in json.get('order-events', [])]
        orders = json.get('orders', [])
        for order in orders:
            order['source'] = 'live trading'
            ord = Order(order)

            if len(orderEvents) == 0:
                raise Exception(f'No OrderEvents were provided for order {ord.Id}')

            ord.OrderEvents = [x for x in orderEvents if x.Id.startswith(ord.Id)]
            self.Orders.append(ord)