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
from QuantConnect.Algorithm.Framework.Risk import *
from QuantConnect.Algorithm.Framework.Alphas import *
from QuantConnect.Algorithm.Framework.Execution import *
from QuantConnect.Algorithm.Framework.Portfolio import *
from QuantConnect.Algorithm.Framework.Selection import *

from AlphaStreamsSocket import *
from AlphaStreamsAlphaModel import *
from AlphaStream.AlphaStreamClient import *
import sys


class AlphaStreamsRunnerAlgorithm(QCAlgorithm):
    ''' Basic template QC Algorithm to backtest or trade live using Alpha insights '''

    def Initialize(self):
        # Set the brokerage model and account settings for Financial Advisor accounts

        # self.SetBrokerageModel(InteractiveBrokersBrokerageModel())
        # self.DefaultOrderProperties = InteractiveBrokersOrderProperties()
        # self.DefaultOrderProperties.Account = ""
        # self.DefaultOrderProperties.FaGroup = ""
        # self.DefaultOrderProperties.FaMethod = ""
        # self.DefaultOrderProperties.FaPercentage = ""
        # self.DefaultOrderProperties.FaProfile  = ""

        # Set AlphaStream ID and API token
        clientId = "YOUR_ID"
        clientToken = "YOUR_TOKEN"
        client = AlphaStreamClient(clientId, clientToken)
        self.client = client

        # Create Alpha model(s)  --  test Alpha IDs that we used. First ID emits one EURUSD Insight every minute in live trading, second ID emits one Insight for SPY every minute in live trading. Both backtest using SPY only.
        self.alphaIds = ["a40aa4e9e72f3b3a2b1656952", "f0af692b1bc00ab83fe3ae76d"]

        # Build a dictionary containing the credentials necessary to stream Insights live
        streamClientInformation = {'UserName': "YOUR_USERNAME", 'Password': "YOUR_PASSWORD",
                                   'HostName': "35.231.13.1",
                                   'VirtualHost': "YOUR_HOST", 'ExchangeName': "YOUR_EXCHANGE",
                                   'Port': 5672}

        self.alphaModels = {id: AlphaStreamsAlphaModel(self, id, client) for id in self.alphaIds}

        # Add the alpha model(s) -- comma-separated arguments
        self.AddAlpha(CompositeAlphaModel(list(self.alphaModels.values())[0], list(self.alphaModels.values())[1]))




        # Set Start Date and End Date based on Alpha models
        self.SetStartDate(min([x.StartDate for x in self.alphaModels.values()]))  # Set Start Date
        self.SetEndDate(max([x.EndDate for x in self.alphaModels.values()]))  # Set End Date
        self.SetCash(1000000)  # Set Strategy Cash

        # Initialize security prices using most recent historical data
        self.SetSecurityInitializer(self.HistoricalSecurityInitializer)

        # Use null benchmark to avoid brokerage/data conflicts
        self.SetBenchmark(lambda x: 0)

        # Set the portfolio construction model to turn Insights into Portfolio Targets
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())

        # Set the execution model to turn Portfolio Targets into orders
        self.SetExecution(ImmediateExecutionModel())

        # If trading live, stream the Insights
        if self.LiveMode:
            for id, model in self.alphaModels.items():
                model.EnsureState(client)
            self.socket = AlphaStreamsSocket(self, client, streamClientInformation, self.alphaIds)


    def HistoricalSecurityInitializer(self, security):
        if security.IsCustomData():
            return
        bar = self.GetLastKnownPrice(security)
        security.SetMarketPrice(bar)

    def OnEndOfAlgorithm(self):
        if self.LiveMode:
            for i in self.alphaIds:
                try:
                    self.client.Unsubscribe(i)
                    self.Log(f'Unsubscribed from {i}')
                except:
                    unsubscribeError = sys.exc_info()[1].args[0]
                    self.Log(f'Could not unsubscribe from {i} on exiting algorithm: {unsubscribeError[48:]}')

    def OnOrderEvent(self, orderEvent):
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        if orderEvent.Status == OrderStatus.Filled:
            self.Log("{0}: {1}: {2}".format(self.Time, order.Type, orderEvent))