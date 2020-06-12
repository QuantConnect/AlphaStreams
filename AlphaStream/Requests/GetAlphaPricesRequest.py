class GetAlphaPricesRequest:
    """ Fetch an alpha price history in batches, starting from `start` for a maximum of 1000 values """

    def __init__(self, alphaId, start = 0):
        self.Id = alphaId
        self.Start = start
        self.Endpoint = "alpha/{}/prices".format(alphaId)
        
    def GetPayload(self):
        payload = {
            "id" : self.Id,
            "start" : self.Start
        }
        return payload