from datetime import datetime, timedelta

class RemoveAlphaBidRequest(object):
    """ Request used to remove an bid for an alpha. """
    def __init__(self, *args, **kwargs):
        '''Create a new instance of CreateBidPriceRequest
        Args:
            alphaId: Unique id hash of an Alpha published to the marketplace.
            bidId: Unique id of an Bid made to the Alpha.'''
        self.Id = kwargs.get('alphaId')
        self.BidId  = kwargs.get('bidId')
        self.Endpoint = f'alpha/{self.Id}/prices/bids/delete'

    def GetPayload(self):
        return { 'id': self.Id, 'bid-id': self.BidId }