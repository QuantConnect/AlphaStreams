from datetime import datetime


class Error:
    """ Individual error set for an Alpha in the QuantConnect Alpha Streams market """

    def __init__(self, json):
        self.Time = datetime.utcfromtimestamp(json['time'])

        self.Error = json.get('error', None)

        self.Stacktrace = json.get('stacktrace', None)
