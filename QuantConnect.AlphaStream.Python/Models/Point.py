from datetime import datetime


class Point:
    """Time-value pair"""

    def __init__(self, json):
        if not isinstance(json, dict):
            self.Time = None
            self.Value = None
            return

        self.Time = datetime.utcfromtimestamp(json['time']) if 'time' in json else None
        self.Value = json.get('value', None)