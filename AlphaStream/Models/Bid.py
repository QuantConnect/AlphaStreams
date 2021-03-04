from datetime import datetime

class Bid(object):
    """Information on a specific bid made to license an Alpha."""

    def __init__(self, json):

        # Unique ID of the did
        self.Id = json['id']

        # True if the bid will be automatically renewed when the license expires
        self.AutoRenew = json.get('auto-renew', False)

        # Expiration time of the bid.
        self.GoodUntil = datetime.utcfromtimestamp(json.get('good-until-time', 0))

        # Allocation that the alpha will be licensed to
        self.Allocation = json.get('allocation', 0)

        # Period that the alpha will be licensed to (in days)
        self.LicensePeriod = json.get('license-period', 0)

        # The maximum bid price per 4-week period
        self.MaximumPrice = json.get('maximum-price', 0)


    def __repr__(self):
        return f'''
Bid Id: {self.Id}
    Auto renew: {self.AutoRenew}
    Good until: {self.GoodUntil}
    Allocation: {self.Allocation}
    License period: {self.LicensePeriod} days
    Maximum price: {self.MaximumPrice}'''