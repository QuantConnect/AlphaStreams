class GetAlphaInsightsRequest:
    """ Fetch an alpha insights in batches, starting from `start` for a maximum of 1000 insights """

    def __init__(self, alphaId, start = 0):
        self.Id = alphaId
        self.Start = start
        self.Endpoint = "alpha/{}/insights".format(alphaId)

    def GetPayload(self):
        payload = {
            "id" : self.Id,
            "start" : self.Start
        }
        return payload