

class UnsubscribeRequest(object):
    """ Send subscription stop request for an Alpha """

    def __init__(self, alphaId):
        self.Id    = str(alphaId)
        self.Endpoint   = "alpha/" + self.Id + "/unsubscribe" 
        
    def GetPayload(self):
        payload = {
            "id" : self.Id
        }
        return payload