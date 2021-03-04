from datetime import datetime
from .Author import Author


class Alpha(object):
    """Algorithm alpha model from the Alpha Streams marketplace."""

    def __init__(self, json):

        self.Id = json['id']

        self.Authors = []
        authors = json.get('authors', None)
        if authors is not None:
            for a in json['authors']:
                self.Authors.append(Author(a))

        # Assets classes traded in the Alpha: Equity, Forex, Crypto, CFDs, Options, Futures
        self.AssetClasses = json.get('asset-classes', None)

        # Alpha's Insight magnitude accuracy
        self.Accuracy = json.get('accuracy', None)

        # Number of backtests run on the alpha prior to submission
        self.AnalysesPerformed = json.get('analyses-performed', None)

        # Boolean - True if the author is trading this strategy else False
        self.AuthorTrading = json.get('author-trading', False)

        # Alpha description provided by the author
        self.Description = json.get('description', '')

        # Estimated depth of the Alpha in USD
        self.EstimatedDepth = json.get('estimated-depth', None)

        # Number of hours spent coding the project
        self.EstimatedEffort = json.get('estimated-effort', None)

        # Alpha name displayed in the marketplace
        self.Name = json.get('name', None)

        # 1 - Average correlation of the alpha with the rest of the market
        self.Uniqueness = json.get('uniqueness', None)

        # Live, rolling 90-day Sharpe ratio (annualized)
        self.SharpeRatio = json.get('sharpe-ratio', None)

        # Version of the alpha -- authors often submit multiple versions with various updates
        self.Version = json.get('version', None)

        # Alpha's running status - either "running" or "stopped"
        self.Status = json.get('status', None)

        # Number of Insights in the alpha backtest
        self.InSampleInsights = json.get('in-sample-insights', None)

        # Number of Insights in live trading
        self.LiveTradingInsights = json.get('live-trading-insights', None)

        # Number of Insights in the out-of-sample backtests run over the alpha's live period
        self.OutOfSampleInsights = json.get('out-of-sample-insights', None)

        # Tags assigned to the alpha by the author
        self.Tags = json.get('tags', [])

        # Number of parameters in the alpha
        self.Parameters = json.get('parameters', None)

        # Dynamic Time Warping distance between live and out-of-sample backtest returns
        self.OutOfSampleDtwDistance = json.get('out-of-sample-dtw-distance', None)

        # Returns correlation between live and out-of-sample backtest returns
        self.OutOfSampleReturnsCorrelation = json.get('out-of-sample-returns-correlation', None)

        # Alpha free-licensing trial period (days)
        self.Trial = json.get('trial', 0)

        # Alpha's capacity: the maximum funds that can be allocated to it
        self.Capacity = json.get('capacity', 0)

        # Alpha's allocated capacity: funds allocated so far
        self.CapacityAllocated = json.get('capacity-allocated', 0)

        # Alpha's reserve price
        self.ReservePrice = json.get('reserve-price', 0)

    def __repr__(self):
        return f'''
Alpha Id: {self.Id}
    Name: {self.Name}
    Sharpe Ratio: {self.SharpeRatio}
    Uniqueness: {self.Uniqueness}
    Capacity: {self.Capacity}
    Capacity Allocated: {self.CapacityAllocated}
    Reserve Price: {self.ReservePrice}
    Status: {self.Status}'''