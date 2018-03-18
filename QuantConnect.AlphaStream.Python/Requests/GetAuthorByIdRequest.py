class GetAuthorByIdRequest(object):

    """ Request a specific author with a matching Author Id """

    def __init__(self, authorId):
        self.Id = str(authorId)
        self.Endpoint = "alpha/author/" + self.Id
        
    def GetPayload(self):
        payload = {
            "id" : self.Id
        }
        return payload
    