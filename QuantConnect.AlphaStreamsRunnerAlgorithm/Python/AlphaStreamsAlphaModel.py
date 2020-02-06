from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Algorithm.Framework")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.Market import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Alphas import *

import threading
from itertools import groupby
from datetime import timedelta, datetime


class AlphaStreamsAlphaModel(AlphaModel):
    '''
        Alpha Model that backtests and streams live Insights. Backtest Insights are collected in batch
        and then iterated over. Live Insights are streamed and emitted in real-time.

        Arguments:
            algorithm: QCAlgorithm that is being run
            alphaId: ID of the Alpha being tested
            client: AlphaStreamsClient to fetch Insights
    '''

    def __init__(self, algorithm, alphaId, client):

        self.StartDate = datetime(1900, 1, 1)
        self.EndDate = datetime(2050, 1, 1)
        self.Symbols = []
        self.Id = alphaId
        self.lock = threading.Lock()

        self.liveInsightCollection = []
        self.backtestInsightCollection = {}
        self.backtestInsightIndex = 0
        self.algorithm = algorithm
        if not algorithm.LiveMode:
            insights = []
            hasData = True
            start = 0

            # Fetch all Insights in the Alpha's backtest
            while hasData:
                responseInsights = client.GetAlphaInsights(alphaId, start)  # Fetch alpha Insights (backtest and live)
                insights += [self.AlphaInsightToFrameworkInsight(x) for x in responseInsights if
                             x.Source != 'live trading']
                hasData = len(responseInsights)
                start += 100

            # Raise exception if there are no Insights
            if len(insights) == 0:
                raise Exception(f'No insights from alpha {alphaId}')

            # Group insights by time created
            self.backtestInsightCollection = {k: list(g) for k, g in
                                              groupby(sorted(insights, key=lambda x: x.GeneratedTimeUtc),
                                                      key=lambda x: x.GeneratedTimeUtc)}
            self.backtestInsightKeys = list(self.backtestInsightCollection.keys())  # Create list of dictionary keys
            self.StartDate = self.backtestInsightKeys[0]  # Get date of first Insight
            self.EndDate = self.backtestInsightKeys[-1] + list(self.backtestInsightCollection.values())[-1][
                0].Period  # Get date of last Insight
            self.Symbols = list(set(
                [item.Symbol for sublist in list(self.backtestInsightCollection.values()) for item in
                 sublist]))  # List of all unique Symbols in Alpha backtest

    def Update(self, algorithm, data):
        ''' Updates this alpha model with the latest data from the algorithm.
            This is called each time the algorithm receives data for subscribed securities
            Args:
                algorithm: The algorithm instance
                data: The new data available
            Returns:
                The insights generated'''

        insights = []

        if data.ContainsKey('NullDataSource'):
            algorithm.Log(f'{algorithm.Time} :: NullDataSource :: {data["NullDataSource"]}')

        # Fetch Insights to be emitted
        if algorithm.LiveMode:
            # Lock thread to modify insight collection
            self.lock.acquire()
            insights = [self.liveInsightCollection.pop(self.liveInsightCollection.index(x)) for x in
                        self.liveInsightCollection if
                        (x.GeneratedTimeUtc <= algorithm.UtcTime.replace(tzinfo=None)) and (
                            algorithm.ActiveSecurities.ContainsKey(x.Symbol))]
            self.lock.release()

        else:
            if self.backtestInsightIndex == len(self.backtestInsightKeys):
                return []

            algoTime = algorithm.UtcTime.replace(tzinfo=None)
            while algoTime >= self.backtestInsightKeys[self.backtestInsightIndex]:
                insights += self.backtestInsightCollection[self.backtestInsightKeys[self.backtestInsightIndex]]
                self.backtestInsightIndex += 1
                if self.backtestInsightIndex == len(self.backtestInsightKeys):
                    break

        for i in insights:
            algorithm.Log(f'{algorithm.Time} :: In Update(), emitting Insight: {i.ToString()}')

        return insights

    def Listener(self, insight):
        ''' Called in the thread when messages are received via Rabbit MQ. It checks if
            data needs to be added for the new Insight and then adds the Insight to the
            Insight collection.

            Args:
                insight: Insight streamed from the live Alpha
        '''
        # Add data for the Insight Symbol if necessary
        dummy = self.EnsureData(insight.Symbol)

        # Lock thread to modify insight collection
        self.lock.acquire()
        self.liveInsightCollection += [insight]
        self.lock.release()

        self.algorithm.Log(f'{self.algorithm.Time} :: In Listener(), adding Insight: {insight.ToString()}')

    def EnsureData(self, symbol):
        ''' Called from Listener method to see if data needs to be added for new Insights

            Args:
                symbol: Symbol of the asset underlying the Insight
        '''
        if not self.algorithm.ActiveSecurities.ContainsKey(symbol):
            if symbol.SecurityType == SecurityType.Equity:
                x = self.algorithm.AddEquity(symbol.Value, Resolution.Minute, symbol.ID.Market).Symbol
            elif symbol.SecurityType == SecurityType.Forex:
                x = self.algorithm.AddForex(symbol.Value, Resolution.Minute, symbol.ID.Market).Symbol
            elif symbol.SecurityType == SecurityType.Cfd:
                x = self.algorithm.AddCfd(symbol.Value, Resolution.Minute, symbol.ID.Market).Symbol
            elif symbol.SecurityType == SecurityType.Crypto:
                x = self.algorithm.AddCrypto(symbol.Value, Resolution.Minute, symbol.ID.Market).Symbol
            self.algorithm.Log(
                f'{self.algorithm.Time} :: Just added {x.Value}. Initialized price: {self.algorithm.Securities[x].Price}')
            return None
        else:
            self.algorithm.Log(f'{symbol.Value} already in active securities')
            return None

    # Converts AlphaStream Insight types to QC Insight types
    def AlphaInsightToFrameworkInsight(self, alphaInsight):
        ''' Converts Alpha Stream Insights to QC Algorithm Framework Insights, which is the format
            required.

            Args:
                alphaInsight: Alpha Streams Insight (live or backtest)

            Returns:
                insight: QC Algorithm Framework Insight
        '''
        if alphaInsight.Direction.lower() == 'up':
            direction = InsightDirection.Up
        elif alphaInsight.Direction.lower() == 'down':
            direction = InsightDirection.Down
        else:
            direction = InsightDirection.Flat

        symbol = self.algorithm.Symbol(alphaInsight.Symbol)

        insight = Insight(symbol, timedelta(seconds=alphaInsight.Period),
                          InsightType.Price if alphaInsight.Type.lower() == 'price' else InsightType.Volatility,
                          direction, alphaInsight.Magnitude, alphaInsight.Confidence, alphaInsight.SourceModel,
                          alphaInsight.Weight)

        insight.GeneratedTimeUtc = alphaInsight.CreatedTime if alphaInsight.CreatedTime is not None else alphaInsight.GeneratedTimeUtc
        insight.CloseTimeUtc = insight.GeneratedTimeUtc + insight.Period
        return insight