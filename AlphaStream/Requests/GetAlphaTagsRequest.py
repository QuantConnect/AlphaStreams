class GetAlphaTagsRequest(object):
    """ Fetch all alpha tags and the number of alphas tagged with each. Tags can be used in SearchAlphas() """

    def __init__(self):
        self.Endpoint = "alpha/tags/read"

    def GetPayload(self):
        """ Construct search query data payload from the initialized properties """
        payload = {}

        return payload