from .OrderEnums import *
from .OrderEvent import *
from datetime import datetime


class Order:
    def __init__(self, json):

        # Unique hash of the algorithm
        self.AlgorithmId = json.get('algorithm-id')

        # Unique hash of the order
        self.OrderId = json.get('order-id')

        # Unique hash of the source of the order
        self.Id = f"{self.AlgorithmId}-{self.OrderId}"

        # QuantConnect identifier of the order asset
        self.Symbol = json.get('symbol')

        # Id of any orders to be filled before triggering this order
        self.ContingentId = json.get('contingent-id', 0)

        # Id of the brokerage the order was placed with
        self.BrokerId = json.get('broker-id', [])

        # Order fill price
        self.Price = json.get('price')

        # Currency of the order price
        self.PriceCurrency = json.get('price-currency')

        # Unix time when the order was created
        self.CreatedTime = datetime.utcfromtimestamp(json.get('created-time'))

        # Unix time the order was last filled (fully or partially)
        self.LastFillTime = datetime.utcfromtimestamp(json.get('last-fill-time')) if json.get('last-fill-time') is not None else None

        # Unix time the order was last updated
        self.LastUpdateTime = datetime.utcfromtimestamp(json.get('last-update-time')) if json.get('last-update-time') is not None else None

        # Unix time the order was canceled
        self.CanceledTime = datetime.utcfromtimestamp(json.get('canceled-time')) if json.get('canceled-time') is not None else None

        # Number of shares of the order
        self.Quantity = json.get('quantity')

        # Order type - market, market on open, market on close, limit, stop limit, stop market, option exercise
        self.Type = OrderType(json.get('type'))

        # Fill-status of the order - new, submitted, partially filled, filled, canceled, none, invalid, cancel pending, update submitted
        self.Status = OrderStatus(json.get('status'))

        # Message attached to the order
        self.Tag = json.get('tag')

        # Order direction - buy, sell, hold
        self.Direction = OrderDirection(json.get('direction'))

        # Mid-price of the security when the order was submitted
        self.SubmissionLastPrice = json.get('submission-last-price')

        # Ask price of the security when the order was submitted
        self.SubmissionAskPrice = json.get('submission-ask-price')

        # Bid price of the security when the order was submitted
        self.SubmissionBidPrice = json.get('submission-bid-price')

        # Stop-price set for the order
        self.StopPrice = json.get('stop-price')

        # Boolean if the stop price was hit
        self.StopTriggered = json.get('stop-triggered')

        # Limit-price set for the order
        self.LimitPrice = json.get('limit-price')

        # Type of order fill duration
        self.TimeInForceType = json.get('time-in-force-type')

        # Unix time when the order time-in-force ends
        self.TimeInForceExpiry = datetime.utcfromtimestamp(json.get('time-in-force-expiry')) if json.get('time-in-force-expiry') is not None else None

        # Where the order was placed - in sample, out of sample, live trading
        self.Source = json.get('source')

        # List of OrderEvents associated with the order
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
