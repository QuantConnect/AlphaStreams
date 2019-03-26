from datetime import datetime

class SearchAuthorsRequest(object): 

    def __init__(self, *args, **kwargs):
        self.Endpoint = "alpha/author/search"
        
        kwargs = kwargs.get('kwargs', kwargs)
        
        self.Location = kwargs.get('location', None)
        
        self.Languages = kwargs.get('languages', [])
        
        self.Biography = kwargs.get('biography', None)
        
        self.AlphasListedMinimum = kwargs.get('alphasListedMinimum', None)
        
        self.AlphasListedMaximum = kwargs.get('alphasListedMaximum', None)
        
        self.SignedUpMinimum = kwargs.get('signedUpMinimum', None)
        
        self.SignedUpMaximum = kwargs.get('signedUpMaximum', None)
        
        self.LastLoginMinimum = kwargs.get('lastLoginMinimum', None)
        
        self.LastLoginMaximum = kwargs.get('lastLoginMaximum', None)
        
        self.ForumDiscussionsMinimum = kwargs.get('forumDiscussionsMinimum', None)
        
        self.ForumDiscussionsMaximum = kwargs.get('forumDiscussionsMaximum', None)
        
        self.ForumCommentsMinimum = kwargs.get('forumCommentsMinimum', None)
        
        self.ForumCommentsMaximum = kwargs.get('forumCommentsMaximum', None)
        
        self.ProjectsMinimum = kwargs.get('projectsMinimum', None)
        
        self.ProjectsMaximum = kwargs.get('projectsMaximum', None)
        
        self.Start = kwargs.get('start', None)
        
        
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