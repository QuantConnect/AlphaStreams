from datetime import datetime

class Author(object):
    """ Author object for storing user information """

    def __init__(self, json):

        self.Id = json['id']

        self.Alphas = json.get('alphas', [])

        self.AlphasListed = json.get('alphas-listed', None)

        self.AnalysisAverageLength = json.get('analysis-average-length', None)

        self.Backtests = json.get('backtests', None)

        self.Biography = json.get('biography', None)

        self.ForumDiscussions = json.get('forum-discussions', None)

        self.ForumComments = json.get('forum-comments', None)

        self.Language = json.get('language', None)

        self.LastOnlineTime = datetime.utcfromtimestamp(json['last-online-time']) if 'last-online-time' in json else None

        self.Location = json.get('location', None)

        self.Projects = json.get('projects', None)

        self.SignUpTime = datetime.utcfromtimestamp(json['signup-time']) if 'signup-time' in json else None

        self.SocialMedia = json.get('social-media', None)

    def __repr__(self):
        return f'Alpha Stream Author {self.Id[:5]:>5} is from {self.Location}. Signed up {self.SignUpTime} and codes in {self.Language}'