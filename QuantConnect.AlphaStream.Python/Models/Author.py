from datetime import datetime

class Author(object):
    """ Author object for storing user information """

    def __init__(self, json):
    
        self.Id = json['id']
        
        self.Alphas = json['alphas']
        
        self.AlphasListed = json['alphas-listed']
        
        self.AnalysisAverageLength = json['analysis-average-length']
        
        self.Backtests = json['backtests']
        
        self.Biography = json['biography']
        
        self.ForumComments = json['forum-comments']
        
        self.ForumDiscussions = json['forum-discussions']
        
        self.Id = json['id']
        
        self.Language = json['language']
        
        self.LastOnlineTime = datetime.utcfromtimestamp(  json['last-online-time'] )
        
        self.Location = json['location']
        
        self.Projects = json['projects']
        
        self.SignUpTime = datetime.utcfromtimestamp( json['signup-time'] )
        
        self.SocialMedia = json['social-media']
        
        