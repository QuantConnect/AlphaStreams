from datetime import datetime

class Conversation:
    """ Conversation created between a client and an author """
    def __init__(self, result):
        self.Subject = result.get('subject', None)
        self.From = result.get('from', None)
        self.Message = result.get('message', None)
        self.TimeReceived = datetime.utcfromtimestamp(result.get('timestamp', None)) if result.get('timestamp', None) is not None else None

    def __repr__(self):
        return f'Conversation from {self.From["id"]} at {self.TimeReceived}. Subject: {self.Subject}.  ::  Message: {self.Message}'