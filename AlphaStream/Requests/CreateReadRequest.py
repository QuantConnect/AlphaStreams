class CreateReadRequest(object):
    """ Read a conversation thread.
Read a conversation with the author(s) of the alpha via email. Quickly solve reconciliation issues or design automated filter questions. """

    def __init__(self, alphaId, message):
        '''Create a new instance of ReadConversationRequest
        Args:
            alphaId: Unique id hash of an Alpha published to the marketplace.
            email: Email that is going to be used to send the replies from the author(s).
            subject: The subject of the thread, this is going to be used for the email.
            message: Message to be sent to the author(s).
            cc: Comma separated list of emails that are going to be copied into the author(s) replies.'''
        self.Id = str(alphaId)
        self.Endpoint = f'alpha/{self.Id}/conversations/read'
        self.Message = str(message)

    def GetPayload(self):
        return { "id" : self.Id,
                 "subject" : self.Message
            }