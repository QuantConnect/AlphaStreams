from datetime import datetime

class Bid(object):
    """Information on a specific bid made to license an Alpha."""

    def __init__(self, json):

        # Unique ID of the did
        self.Id = json['id']

        # Expiration time of the bid.
        self.GoodUntil = datetime.utcfromtimestamp(json.get('good-until-time', 0))

        # Allocation that the alpha will be licensed to
        self.Allocation = json.get('allocation', 0)

        # Period that the alpha will be licensed to (in days)
        self.LicensePeriod = json.get('license-period', 0)

        # The maximum bid price per 4-week period
        self.MaximumPrice = json.get('maximum-price', 0)


    def __repr__(self):
        return (f'Bid of ${self.MaximumPrice} for a ${self.Allocation} allocation to license '
            + f'for the next {self.LicensePeriod} days is good until {self.GoodUntil}.')