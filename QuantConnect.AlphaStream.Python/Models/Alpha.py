from datetime import datetime
from Models.Author import Author
from Models.Project import Project


class Alpha(object):
    """Model describing an Alpha from the QuantConnect Alpha Streams repository"""

    def __init__(self, json):
        self.Accuracy = json['accuracy']

        self.Authors = []

        for a in json['authors']:
            self.Authors.append(Author(a))

        self.AuthorTrading = json['author-trading']

        self.AnalysesPerformed = json['analyses-performed']

        self.AssetClasses = json['asset-classes']

        self.Description = json['description']

        self.EstimatedDepth = json['estimated-depth']

        self.ExclusiveAvailable = json['exclusive-available']

        self.ExclusiveSubscriptionFee = json['exclusive-subscription-fee']

        self.EstimatedEffort = json['estimated-effort']

        self.ListedTime = datetime.utcfromtimestamp(json['listed-time'])

        self.Id = json['id']

        self.Project = Project(json['project'])

        self.Uniqueness = json['uniqueness']

        self.SharpeRatio = json['sharpe-ratio']

        self.SharedSubscriptionFee = json['subscription-fee']

        self.Version = json['version']

        self.Status = json['status']
