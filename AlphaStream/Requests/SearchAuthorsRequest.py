class SearchAuthorsRequest(object): 

    def __init__(self, *args, **kwargs):
        self.Endpoint = "alpha/author/search"

        kwargs = kwargs.get('kwargs', kwargs)

        self.Start = kwargs.get('start', None)

        self.Location = kwargs.get('location', None)

        self.Languages = kwargs.get('languages', [])

        self.Biography = kwargs.get('biography', None)

        self.AlphasListedMinimum, self.AlphasListedMaximum = self._get_range(kwargs, 'alphasListed')

        self.SignedUpMinimum, self.SignedUpMaximum = self._get_range(kwargs, 'signedUp')

        self.LastLoginMinimum, self.LastLoginMaximum = self._get_range(kwargs, 'lastLogin')

        self.ForumDiscussionsMinimum, self.ForumDiscussionsMaximum = self._get_range(kwargs, 'forumDiscussions')

        self.ForumCommentsMinimum, self.ForumCommentsMaximum = self._get_range(kwargs, 'forumComments')

        self.ProjectsMinimum, self.ProjectsMaximum = self._get_range(kwargs, 'projects')


    def _get_range(self, kwargs, key):

        # If we have the key, it is a list with the minimum and maximum values
        value = kwargs.get(key, [])
        if isinstance(value, list) and len(value) > 0:
            return min(value), max(value)

        return kwargs.get(f'{key}Minimum', None), kwargs.get(f'{key}Maximum', None)

    def GetPayload(self):
        """ Construct author search query data payload from the initialized properties """

        # Common default properties
        payload = {
            "start": self.Start 
        }

        # Optional properties
        if self.Location is not None:
            payload['location'] = self.Location

        if len(self.Languages) > 0:
            if (len(self.Languages) > 1) and (type(self.Languages) != str):  ## i.e., ['Py', 'C#']
                languages = ','.join(self.Languages)
                payload['languages'] = languages
            elif (len(self.Languages) == 1) and (type(self.Languages) == list): ## i.e., ['Py, C#'] or ['Py']
                payload['languages'] = str(self.Languages)
            else:
                payload['languages'] = self.Languages

        if self.Biography is not None:
            payload['biography'] = self.Biography

        if self.AlphasListedMinimum is not None: 
            payload['alphas-minimum'] = self.AlphasListedMinimum

        if self.AlphasListedMaximum is not None:
            payload['alphas-maximum'] = self.AlphasListedMaximum 
            
        if self.SignedUpMinimum is not None:
            payload['signed-up-minimum'] = self.SignedUpMinimum

        if self.SignedUpMaximum is not None:
            payload['signed-up-maximum'] = self.SignedUpMaximum

        if self.LastLoginMinimum is not None:
            payload['last-login-minimum'] = self.LastLoginMinimum

        if self.LastLoginMaximum is not None:
            payload['last-login-maximum'] = self.LastLoginMaximum

        if self.ForumDiscussionsMinimum is not None:
            payload['forum-discussions-minimum'] = self.ForumDiscussionsMinimum

        if self.ForumDiscussionsMaximum is not None:
            payload['forum-discussions-maximum'] = self.ForumDiscussionsMaximum

        if self.ForumCommentsMinimum is not None:
            payload['forum-comments-minimum'] = self.ForumCommentsMinimum

        if self.ForumCommentsMaximum is not None:
            payload['forum-comments-maximum'] = self.ForumCommentsMaximum

        if self.ProjectsMinimum is not None:
            payload['projects-minimum'] = self.ProjectsMinimum

        if self.ProjectsMaximum is not None:
            payload['projects-maximum'] = self.ProjectsMaximum

        return payload