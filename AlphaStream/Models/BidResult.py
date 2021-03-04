from datetime import datetime
from .Bid import Bid

class BidResult(object):
    """Result of a bid to license an Alpha."""

    def __init__(self, json):

        # True if the bid is successful
        self.Success = json.get('success', None)

        # Alpha's Insight magnitude accuracy
        self.ActiveBid = json.get('active-bid', None)
        if self.ActiveBid:
            self.ActiveBid = Bid(self.ActiveBid)

        # Time that the next auction will occur
        self.NextAuctionTime = datetime.utcfromtimestamp(json.get('next-auction-time', 0))

        # Alpha's capacity for the next auction
        self.NextAuctionCapacity = json.get('next-auction-capacity', 0)

        # Minimum capital required to place a bid
        self.MinimumCapitalRequired = json.get('minimum-capital-required', 0)

    def __repr__(self):
        if not self.Success:
            return 'Unsuccessful bid'
        return f'''{self.ActiveBid}
    Next auction time: {self.NextAuctionTime}
    Next auction capacity: {self.NextAuctionCapacity}
    Minimum capital required: {self.MinimumCapitalRequired}'''