from datetime import datetime


class Price:
    """ Individual price set for an Alpha in the QuantConnect Alpha Streams market """

    def __init__(self, json):
        self.Time = datetime.utcfromtimestamp(json['time'])

        self.SharedPrice = json.get('shared-price', None)

        self.ExclusivePrice = json.get('exclusive-price', None)

        self.PriceType = json.get('price-type', None)
