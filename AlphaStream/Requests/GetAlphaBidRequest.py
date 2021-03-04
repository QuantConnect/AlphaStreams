class GetAlphaBidRequest:
    """ Fetch Alpha's latest bid """

    def __init__(self, alphaId):
        self.Id = alphaId
        self.Endpoint = f"alpha/{self.Id}/prices/bids/read"

    def GetPayload(self):
        return { "id": self.Id }
