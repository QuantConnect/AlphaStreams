

class AddInsightsStreamRequest(object):
    """ Request streaming insights for this specific alpha. """

    def __init__(self, alphaId):
        self.AlphaId = str(alphaId)
        self.Endpoint = "alpha/" + self.Id
        
    def GetPayload(self):
        payload = {
            "AlphaId" : self.AlphaId
        }
        return payload