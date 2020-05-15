from datetime import datetime

class Author(object):
    """ Author object for storing user information """

    def __init__(self, json):

        # Unique author ID hash
        self.Id = json['id']

        # List of alphas IDs by the author
        self.Alphas = json.get('alphas', [])

        # Number of author's alphas listed on the market
        self.AlphasListed = json.get('alphas-listed', None)

        # Average number of hours the author spent coding on an alpha
        self.AnalysisAverageLength = json.get('analysis-average-length', None)

        # Total number of backtests performed by the author
        self.Backtests = json.get('backtests', None)

        # Biography provided by the author
        self.Biography = json.get('biography', None)

        # Number of forum discussions the author has participated in
        self.ForumDiscussions = json.get('forum-discussions', None)

        # Number of comments the author has posted in the community forum
        self.ForumComments = json.get('forum-comments', None)

        # Author's preferred coding language
        self.Language = json.get('language', None)

        # UTC time the author was last online
        self.LastOnlineTime = datetime.utcfromtimestamp(json['last-online-time']) if 'last-online-time' in json else None

        # Author's location - city, state, country
        self.Location = json.get('location', None)

        # Total number of projects the author has created
        self.Projects = json.get('projects', None)

        # UTC time the author signed up with QuantConnect
        self.SignUpTime = datetime.utcfromtimestamp(json['signup-time']) if 'signup-time' in json else None

        # Author's social media profile
        self.SocialMedia = json.get('social-media', None)

    def __repr__(self):
        return f'Alpha Stream Author {self.Id[:5]:>5} is from {self.Location}. Signed up {self.SignUpTime} and codes in {self.Language}'