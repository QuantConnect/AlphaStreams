from datetime import datetime, timedelta

class CreateBidPriceRequest(object):
    """ Create a bid price request. """
    def __init__(self, *args, **kwargs):
        '''Create a new instance of CreateBidPriceRequest
        Args:
            alphaId: Unique id hash of an Alpha published to the marketplace.
            exclusive: Bid for the exclusive price (optional if shared is defined).
            shared: Bid for the shared price (optional if exclusive is defined).
            good_until: Expiration time of the bid.'''
        kwargs = kwargs.get('kwargs', kwargs)
        self.Id = kwargs.get('alphaId')
        self.Endpoint = f'alpha/{self.Id}/prices/bids/create'
        self.Bid = kwargs.get('bid', 0)
        self.Allocation = self.GetPrice('allocation', kwargs)
        self.Period = kwargs.get('period', 0)

        good_until = kwargs.get('good_until', datetime.utcnow() + timedelta(seconds=3602))
        self.GoodUntil = (good_until - datetime(1970, 1, 1)).total_seconds()


    def GetPrice(self, key, kwargs):
        value = kwargs.get(key, 0)
        if value == int(value):
            return int(value)
        raise Exception(f'Please bid the {key} in whole dollar amounts, without cents')


    def GetPayload(self):
        payload = { 'id': self.Id, 'good-until': self.GoodUntil }
        if self.Bid > 0:
            payload['bid'] = self.Bid
        if self.Allocation > 0:
            payload['allocation'] = self.Allocation
        if self.Period > 0:
            payload['period'] = self.Period
        return payload