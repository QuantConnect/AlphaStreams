from datetime import datetime

class BidReponse(object):
    """Result of a bid to license an Alpha."""

    def __init__(self, json):

        # Boolean indicating success
        self.Success = json.get('success', False)

        # Capacity allocated if the bid is successful
        self.CapacityAllocated = json.get('capacity-allocated', 0)

        # True if the bid resulted in a new license
        self.Licensed = json.get('licensed', False)

        # True if the out bid
        self.Outbid = json.get('outbid', False)

    def __repr__(self):
        if self.Licensed:
            return f'Licensed for {self.CapacityAllocated}'
        if self.Outbid:
            return 'Outbid'
        return 'Not licenced nor outbid' if self.Success else 'Failed to place a bid'