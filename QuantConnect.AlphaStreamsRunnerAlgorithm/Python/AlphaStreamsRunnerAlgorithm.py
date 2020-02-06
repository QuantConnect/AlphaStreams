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
from NullData import *
from datetime import timedelta, datetime

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

        # Use this or other Forex ticker when deploying to forex-only brokerage. QC default benchmark is SPY
        self.SetBenchmark(Symbol.Create("GBPUSD", SecurityType.Forex, Market.Oanda))

        # Build a dictionary containing the credentials necessary to stream Insights live
        streamClientInformation = {'UserName': "YOUR_USERNAME", 'Password': "YOUR_PASSWORD",
                                   'HostName': "35.231.13.1",
                                   'VirtualHost': "YOUR_HOST", 'ExchangeName': "YOUR_EXCHANGE",
                                   'Port': 5672}

        # Create Alpha model(s)  --  this Alpha ID is one we used to test. It will emit 1 flat Insight for EURUSD every minute.
        alphaIds = ["a40aa4e9e72f3b3a2b1656952"]  # f0af692b1bc00ab83fe3ae76d is a test ID for equities (1 Up Insight for SPY every minute)
        self.alphaIds = alphaIds
        self.alphaModels = {id: AlphaStreamsAlphaModel(self, id, client) for id in alphaIds}
        alphaModels = [value for key, value in self.alphaModels.items()]

        # Set Start Date and End Date based on Alpha models
        self.SetStartDate(min([x.StartDate for x in alphaModels]))  # Set Start Date
        self.SetEndDate(max([x.EndDate for x in alphaModels]))  # Set End Date
        self.SetCash(1000000)  # Set Strategy Cash

        # Add the alpha model(s) -- comma-separated arguments
        self.AddAlpha(CompositeAlphaModel(alphaModels[0]))

        # Set the portfolio construction model to turn Insights into Portfolio Targets
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())

        # Set the execution model to turn Portfolio Targets into orders
        self.SetExecution(ImmediateExecutionModel())

        # Initialize security prices using most recent historical data
        self.SetSecurityInitializer(self.HistoricalSecurityInitializer)

        # If trading live, stream the Insights
        if self.LiveMode:
            soc = AlphaStreamsSocket(self)
            soc.Stream(alphaIds, client, streamClientInformation)
        # If Backtesting, we can pass the symbols in here
        else:
            self.AddData(NullData, 'NullDataSource', Resolution.Second)
            allSymbols = []
            for model in alphaModels:
                allSymbols += model.Symbols
            allSymbols = list(set(allSymbols))
            self.SetUniverseSelection(ManualUniverseSelectionModel(allSymbols))

    def HistoricalSecurityInitializer(self, security):
        if security.Type in [SecurityType.Future, SecurityType.Option, SecurityType.Cfd]:
            raise Exception("Alpha Streams does not support Futures or Options data yet.")
        elif security.IsCustomData():
            if self.LiveMode:
                bar = TradeBar(datetime.utcnow().replace(microsecond=0), security.Symbol, 1, 1, 1, 1, 1)
            else:
                bar = TradeBar(self.Time, security.Symbol, 1, 1, 1, 1, 1)
            security.SetMarketPrice(bar)
        else:
            price = self.History([security.Symbol], 10000, Resolution.Minute).loc[security.Symbol].tail(1)
            if security.Type == SecurityType.Equity:
                for index, row in price.iterrows():
                    bar = TradeBar(index, security.Symbol, row.close, row.open, row.high, row.low, row.volume)
                security.SetMarketPrice(bar)
            elif security.Type == SecurityType.Forex:
                for index, row in price.iterrows():
                    askBar = Bar(row.askclose, row.askopen, row.askhigh, row.asklow)
                    bidBar = Bar(row.bidclose, row.bidopen, row.bidhigh, row.bidlow)
                    bar = QuoteBar(index, security.Symbol, bidBar, 0, askBar, 0, timedelta(minutes=1))
                security.SetMarketPrice(bar)
            elif security.Type == SecurityType.Crypto:
                for index, row in price.iterrows():
                    askBar = Bar(row.askclose, row.askopen, row.askhigh, row.asklow)
                    bidBar = Bar(row.bidclose, row.bidopen, row.bidhigh, row.bidlow)
                    bar = QuoteBar(index, security.Symbol, bidBar, 0, askBar, 0, timedelta(minutes=1))
                security.SetMarketPrice(bar)

    def OnEndOfAlgorithm(self):
        if self.LiveMode:
            for i in self.alphaIds:
                try:
                    self.client.Unsubscribe(i)
                    self.Log(f'Unsubscribed from {i}')
                except Exception as err:
                    self.Log(err)

    def OnOrderEvent(self, orderEvent):
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        if orderEvent.Status == OrderStatus.Filled:
            self.Log("{0}: {1}: {2}".format(self.Time, order.Type, orderEvent))