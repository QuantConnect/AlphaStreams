class GetAlphaListRequest(object):
    """ Listing all alpha ids so you can maintain a dictionary and detect programatically when a new alpha is added to the API. """

    def __init__(self):
        self.Endpoint = "alpha/list"

    def GetPayload(self):
        return None