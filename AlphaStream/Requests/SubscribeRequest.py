

class SubscribeRequest(object):
    """ Send subscription request for an Alpha. Defaults to a shared subscription request. """

    def __init__(self, alphaId, exclusive=False):
        self.Id    = str(alphaId)
        self.Endpoint   = "alpha/" + self.Id + "/subscribe"
        self.Exclusive  = exclusive
        
    def GetPayload(self):
        payload = {
            "id"        : self.Id,
            "exclusive" : self.Exclusive
        }
        return payload