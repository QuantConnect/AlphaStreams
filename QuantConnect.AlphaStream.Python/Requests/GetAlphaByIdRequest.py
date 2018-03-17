

class GetAlphaByIdRequest(object):
    """ Request a specific alpha with a matching Alpha Id """

    def __init__(self, alphaId):
        self.Id = str(alphaId)
        self.Endpoint = "alpha/" + self.Id
        
    def GetPayload(self):
        payload = {
            "id" : self.Id
        }
        return payload