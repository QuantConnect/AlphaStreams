from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Algorithm.Framework")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Orders import *
from QuantConnect.Algorithm import *
from QuantConnect.Brokerages import *
from QuantConnect.Data.Market import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Alphas import *

import threading
from itertools import groupby
from datetime import timedelta, datetime
from BrokerageSupportedSecurities import *


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
        self.Id = alphaId
        self.lock = threading.Lock()

        self.liveInsightCollection = []
        self.backtestInsightCollection = {}
        self.backtestInsightIndex = 0
        self.algorithm = algorithm
        self.supportedSecurities = BrokerageSupportedSecurities[str(algorithm.BrokerageModel)[24:]]
        self.dataResolution = {}
        self.canExecute = []
        if not algorithm.LiveMode:
            insights = []
            hasData = True
            start = 0

            # Fetch all Insights in the Alpha's backtest
            while hasData:
                responseInsights = client.GetAlphaInsights(alphaId, start)  # Fetch alpha Insights (backtest and live)
                insights += [self.AlphaInsightToFrameworkInsight(x) for x in responseInsights if
                             x.Source == 'in sample']
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
            self.EndDate = self.backtestInsightKeys[-1] + list(self.backtestInsightCollection.values())[-1][ 0].Period  # Get date of last Insight
            self.dataResolution = {x.Symbol: Resolution.Minute if x.GeneratedTimeUtc.second == 0 else Resolution.Second for x in list(set([item for sublist in list(self.backtestInsightCollection.values()) for item in sublist]))}  # List of data resolution for each symbol

            # Data check for all Insights
            allInsights = [item for sublist in list(self.backtestInsightCollection.values()) for item in sublist]
            for insight in allInsights:
                # Check that the security type is supported by the brokerage model
                self.EnsureExecution(insight.Symbol)
                # Add data for the Insight Symbol if necessary
                self.EnsureData(insight.Symbol)

    def Update(self, algorithm, data):
        ''' Updates this alpha model with the latest data from the algorithm.
            This is called each time the algorithm receives data for subscribed securities
            Args:
                algorithm: The algorithm instance
                data: The new data available
            Returns:
                The insights
        '''

        insights = []

        # Fetch Insights to be emitted
        if algorithm.LiveMode:
            # Lock thread to modify insight collection
            self.lock.acquire()
            insights = [self.liveInsightCollection.pop(self.liveInsightCollection.index(x)) for x in self.liveInsightCollection if (x.GeneratedTimeUtc <= algorithm.UtcTime.replace(tzinfo=None)) and (algorithm.ActiveSecurities.ContainsKey(x.Symbol))]
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
            algorithm.Log(f'{algorithm.Time} :: In {self.Id} Update(), emitting Insight: {i.ToString()}')

        return insights

    def Listener(self, insight):
        ''' Called in the thread when messages are received via Rabbit MQ. It checks if
            data needs to be added for the new Insight and then adds the Insight to the
            Insight collection.

            Args:
                insight: Insight streamed from the live Alpha
        '''

        # Check that the security type is supported by the brokerage model, else kill algorithm
        self.EnsureExecution(insight.Symbol)

        # Add data for the Insight Symbol if necessary
        self.EnsureData(insight.Symbol)

        # Lock thread to modify insight collection
        self.lock.acquire()
        self.liveInsightCollection += [insight]
        self.lock.release()
        self.algorithm.Log(f'{self.algorithm.Time} :: In {self.Id} Listener(), adding Insight: {insight.ToString()}')

    def EnsureExecution(self, symbol):
        ''' Called from Listener() to see if the security type of the Insight can be traded on the selected brokerage

            Args:
                insight: Framework Insight being streamed in
            Returns: True if brokerage supports the security type, false otherwise
        '''
        if symbol in self.canExecute:
            return

        if symbol.SecurityType not in self.supportedSecurities:
            self.algorithm.Log(f'{BrokerageErrorMessage(symbol, str(self.algorithm.BrokerageModel)[24:])}')
            self.algorithm.Quit()
        else:
            self.canExecute += [symbol]

    def EnsureData(self, symbol):
        ''' Called from Listener method to see if data needs to be added for new Insights

            Args:
                symbol: Symbol of the asset underlying the Insight
        '''

        if not self.algorithm.Securities.ContainsKey(symbol):
            symbolResolution = Resolution.Second
            if not self.algorithm.LiveMode:
                symbolResolution = self.dataResolution[symbol]

            if symbol.SecurityType == SecurityType.Equity:
                self.algorithm.AddEquity(symbol.Value, symbolResolution, symbol.ID.Market).Symbol
            elif symbol.SecurityType == SecurityType.Forex:
                self.algorithm.AddForex(symbol.Value, symbolResolution, symbol.ID.Market).Symbol
            elif symbol.SecurityType == SecurityType.Cfd:
                self.algorithm.AddCfd(symbol.Value, symbolResolution, symbol.ID.Market).Symbol
            elif symbol.SecurityType == SecurityType.Crypto:
                self.algorithm.AddCrypto(symbol.Value, symbolResolution, symbol.ID.Market).Symbol


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

        insight = Insight(symbol, timedelta(seconds=alphaInsight.Period), InsightType.Price, direction, alphaInsight.Magnitude, alphaInsight.Confidence, alphaInsight.SourceModel, alphaInsight.Weight)

        insight.GeneratedTimeUtc = alphaInsight.CreatedTime if alphaInsight.CreatedTime is not None else alphaInsight.GeneratedTimeUtc
        insight.CloseTimeUtc = insight.GeneratedTimeUtc + insight.Period

        self.algorithm.Log(f'{alphaInsight.Symbol} :: AS Insight ID {alphaInsight.Id} ---> Framework Insight ID {insight.Id} :: Alpha ID: {self.Id}')
        return insight