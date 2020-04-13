from .OrderEnums import *
from datetime import datetime


class OrderEvent:
    def __init__(self, json):

        self.AlgorithmId = json.get('algorithm-id')

        self.OrderId = json.get('order-id')

        self.OrderEventId = json.get('order-event-id')

        self.Id = f"{self.AlgorithmId}-{self.OrderId}-{self.OrderEventId}"

        self.Symbol = json.get('symbol')

        self.Time = datetime.utcfromtimestamp(json.get('time'))

        self.Status = OrderStatus(json.get('status'))

        self.OrderFeeAmount = json.get('order-fee-amount')

        self.OrderFeeCurrency = json.get('order-fee-currency')

        self.FillPrice = json.get('fill-price')

        self.FillPriceCurrency = json.get('fill-price-currency')

        self.FillQuantity = json.get('fill-quantity')

        self.Direction = OrderDirection(json.get('direction'))

        self.Message = json.get('message', '')

        self.IsAssignment = json.get('is-assignment')

        self.Quantity = json.get('quantity')

        self.StopPrice = json.get('stop-price')

        self.LimitPrice = json.get('limit-price')


    def __repr__(self, extended = True):

        if (extended):
            rep = f'Time: {self.Time} ID: {self.Id} Symbol: {self.Symbol} Status: {self.Status.name} Quantity: {self.Quantity}'
        else:
            rep = f'Time: {self.Time} OrderId: {self.OrderId} Status: {self.Status.name} Quantity: {self.Quantity}'

        if self.FillQuantity != 0:
            rep += f' Fill Quantity: {self.FillQuantity} Fill Price: {self.FillPrice} {self.FillPriceCurrency}'

        if self.LimitPrice is not None:
            rep += f' Limit Price: {self.LimitPrice}'

        if self.StopPrice is not None:
            rep += f' Stop Price: {self.StopPrice}'

        if self.OrderFeeAmount != 0:
            rep += f' Order Fee: {self.OrderFeeAmount} {self.OrderFeeCurrency}'

        if len(self.Message) > 0:
            rep += f' Message: "{self.Message}"'

        return rep