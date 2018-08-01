from datetime import datetime


class RuntimeError:
    """Individual error set for an Alpha in the QuantConnect Alpha Streams market"""

    def __init__(self, json):
        self.Time = datetime.utcfromtimestamp(json['time']) if 'time' in json else None

        self.Error = json.get('error', None)

        self.Stacktrace = json.get('stacktrace', None)

    def __repr__(self):
        error = '' if self.Error is None else self.Error[:10]
        stacktrace = '' if self.Stacktrace is None else self.Stacktrace[:10]
        return f'Error at {self.Time}, message: {error}, stacktrace: {stacktrace}'