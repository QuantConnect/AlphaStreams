from datetime import datetime


class Price:
    """Record of the price of an Alpha or a bid made for it."""

    def __init__(self, json):
        self.Time = datetime.utcfromtimestamp(json['time']) if 'time' in json else None

        self.SharedPrice = json.get('shared-price', None)

        self.ExclusivePrice = json.get('exclusive-price', None)

        self.PriceType = json.get('price-type', 'ask')

    def __repr__(self):
        return f'{self.PriceType.title()} price from {self.Time}: Shared ${self.SharedPrice:,.2f}. Exclusive ${self.ExclusivePrice:,.2f}'