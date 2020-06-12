from .OrderEnums import *
from datetime import datetime


class OrderEvent:
    def __init__(self, json):

        # Unique hash of the algorithm
        self.AlgorithmId = json.get('algorithm-id')

        # Unique hash of the source of the order that the order event is associated with
        self.OrderId = json.get('order-id')

        # Unique hash of the order event
        self.OrderEventId = json.get('order-event-id')

        # Unique hash of the source of the order event
        self.Id = f"{self.AlgorithmId}-{self.OrderId}-{self.OrderEventId}"

        # QuantConnect identifier for the order asset
        self.Symbol = json.get('symbol')

        # Unix time when the order event occurred
        self.Time = datetime.utcfromtimestamp(json.get('time'))

        # Fill-status of the order - new, submitted, partially filled, filled, canceled, none, invalid, cancel pending, update submitted
        self.Status = OrderStatus(json.get('status'))

        # Total fees for the order
        self.OrderFeeAmount = json.get('order-fee-amount')

        # Currency of the order fees
        self.OrderFeeCurrency = json.get('order-fee-currency')

        # Order fill price
        self.FillPrice = json.get('fill-price')

        # Currency of the order price
        self.FillPriceCurrency = json.get('fill-price-currency')

        # Number of shares filled
        self.FillQuantity = json.get('fill-quantity')

        # Direction of the order - buy, sell, hold
        self.Direction = OrderDirection(json.get('direction'))

        # Message attached to the order conveying additional information about the order event by the author
        self.Message = json.get('message', '')

        # Boolean if the order is an option assignment
        self.IsAssignment = json.get('is-assignment')

        # Number of shares of the order
        self.Quantity = json.get('quantity')

        # Stop price set for the order
        self.StopPrice = json.get('stop-price')

        # Limit price set for the order
        self.LimitPrice = json.get('limit-price')


    def __repr__(self, extended = True):

        if (extended):
            rep = f'Time: {self.Time} ID: {self.Id} Symbol: {self.Symbol} Status: {self.Status.name} Quantity: {self.Quantity}'
        else:
            rep = f'Time: {self.Time} OrderEventId: {self.OrderEventId} Status: {self.Status.name} Quantity: {self.Quantity}'

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