class GetAlphaEquityCurveRequest:
    """ Fetch an entire alpha equity curve with 1 point for the close of each day. """

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
