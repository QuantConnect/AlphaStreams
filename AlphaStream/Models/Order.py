from .OrderEnums import *
from .OrderEvent import *
from datetime import datetime


class Order:
    def __init__(self, json):

        self.AlgorithmId = json.get('algorithm-id')

        self.OrderId = json.get('order-id')

        self.Id = f"{self.AlgorithmId}-{self.OrderId}"

        self.Symbol = json.get('symbol')

        self.ContingentId = json.get('contingent-id', 0)

        self.BrokerId = json.get('broker-id', [])

        self.Price = json.get('price')

        self.PriceCurrency = json.get('price-currency')

        self.CreatedTime = datetime.utcfromtimestamp(json.get('created-time'))

        self.LastFillTime = datetime.utcfromtimestamp(json.get('last-fill-time')) if json.get('last-fill-time') is not None else None

        self.LastUpdateTime = datetime.utcfromtimestamp(json.get('last-update-time')) if json.get('last-update-time') is not None else None

        self.CanceledTime = datetime.utcfromtimestamp(json.get('canceled-time')) if json.get('canceled-time') is not None else None

        self.Quantity = json.get('quantity')

        self.Type = OrderType(json.get('type'))

        self.Status = OrderStatus(json.get('status'))

        self.Tag = json.get('tag')

        self.Direction = OrderDirection(json.get('direction'))

        self.SubmissionLastPrice = json.get('submission-last-price')

        self.SubmissionAskPrice = json.get('submission-ask-price')

        self.SubmissionBidPrice = json.get('submission-bid-price')

        self.StopPrice = json.get('stop-price')

        self.StopTriggered = json.get('stop-triggered')

        self.LimitPrice = json.get('limit-price')

        self.TimeInForceType = json.get('time-in-force-type')

        self.TimeInForceExpiry = datetime.utcfromtimestamp(json.get('time-in-force-expiry')) if json.get('time-in-force-expiry') is not None else None

        self.Source = json.get('source')

        self.OrderEvents = [OrderEvent(x) for x in json.get('events', [])]

    def __repr__(self):
        rep = f'ID: {self.Id} Source: "{self.Source}" Symbol: {self.Symbol} Status: {self.Status.name} CreatedTime: {self.CreatedTime} Direction: {self.Direction.name} Quantity: {self.Quantity} Type: {self.Type.name} TimeInForceType: {self.TimeInForceType}'

        if self.TimeInForceExpiry is not None:
            rep += f' TimeInForceExpiry: {self.TimeInForceExpiry}'

        if len(self.BrokerId) > 0:
            rep += f' BrokerID: {",".join(self.BrokerId)}'

        if self.Price != 0:
            rep += f' Price: {self.Price} {self.PriceCurrency}'

        if self.ContingentId != 0:
            rep += f' ContingentId: {self.ContingentId}'

        if self.LastUpdateTime is not None:
            rep += f' LastUpdateTime: {self.LastUpdateTime}'

        if self.LastFillTime is not None:
            rep += f' LastFillTime: {self.LastFillTime}'

        if self.CanceledTime is not None:
            rep += f' CanceledTime: {self.CanceledTime}'

        if self.LimitPrice is not None:
            rep += f' LimitPrice: {self.LimitPrice}'

        if self.StopPrice is not None:
            rep += f' StopPrice: {self.StopPrice}'

        if self.SubmissionLastPrice != 0:
            rep += f' SubmissionLastPrice: {self.SubmissionLastPrice}'

        if self.SubmissionAskPrice != 0:
            rep += f' SubmissionAskPrice: {self.SubmissionAskPrice}'

        if self.SubmissionBidPrice != 0:
            rep += f' SubmissionBidPrice: {self.SubmissionBidPrice}'

        if self.Tag is not None:
            rep += f' Tag: {self.Tag}'

        if len(self.OrderEvents) > 0:
            rep += ' OrderEvents: [{' + "},{".join([x.__repr__(extended = False) for x in self.OrderEvents]) + '}]'

        return rep
