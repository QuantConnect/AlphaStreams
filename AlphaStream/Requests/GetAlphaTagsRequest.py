class GetAlphaTagsRequest(object):
    """ Search for alphas matching this search criteria """

    def __init__(self):
        self.Endpoint = "alpha/tags/read"

    def GetPayload(self):
        """ Construct search query data payload from the initialized properties """
        payload = {}

        return payload