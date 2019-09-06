class GetAlphaEquityCurveRequest:
    """ Fetch an alpha error history, starting from `start` for a maximum of 1000 values """

    def __init__(self, alphaId, date_format = 'date'):
        self.Id = alphaId
        self.Format = 'json'
        self.DateFormat = date_format
        self.Endpoint = f'/alpha/{alphaId}/equity'

    def GetPayload(self):
        payload = {
            "format": self.Format,
            "date-format": self.DateFormat
        }
        return payload