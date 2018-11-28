class CreateConversationsRequest(object):
    """ Create a conversation thread.
Start a conversation with the author(s) of the alpha via email. Quickly solve reconciliation issues or design automated filter questions. """

    def __init__(self, alphaId, email, subject, message, cc = ''):
        '''Create a new instance of CreateConversationRequest
        Args:
            alphaId: Unique id hash of an Alpha published to the marketplace.
            email: Email that is going to be used to send the replies from the author(s).
            subject: The subject of the thread, this is going to be used for the email.
            message: Message to be sent to the author(s).
            cc: Comma separated list of emails that are going to be copied into the author(s) replies.'''
        self.Id = str(alphaId)
        self.Endpoint = f'alpha/{self.Id}/conversations/create'
        self.From = email
        self.Subject = subject
        self.Message = message
        self.CC = cc
        

    def GetPayload(self):
        return { "id" : self.Id,
            "from"    : self.From,
            "subject" : self.Subject,
            "message" : self.Message,
            "cc"      : self.CC 
            }