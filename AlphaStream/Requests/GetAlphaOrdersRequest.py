class GetAlphaOrdersRequest:
    """ Fetch an alpha's orders in batches, starting from `start` """

    def __init__(self, alphaId, start=0):
        self.Id = alphaId
        self.Start = start
        self.Endpoint = "alpha/{}/orders".format(alphaId)

    def GetPayload(self):
        payload = {
            "id": self.Id,
            "start": self.Start
        }
        return payload