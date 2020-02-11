from clr import AddReference
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")

from QuantConnect import *
from QuantConnect.Brokerages import *
from QuantConnect.Data.Market import *

BrokerageSupportedSecurities = {
    "AlpacaBrokerageModel": [SecurityType.Equity],
    "AlphaStreamsBrokerageModel": [SecurityType.Equity, SecurityType.Forex, SecurityType.Crypto, SecurityType.Future, SecurityType.Option, SecurityType.Cfd, SecurityType.Base],
    "BitfinexBrokerageModel": [SecurityType.Crypto],
    "DefaultBrokerageModel": [SecurityType.Equity, SecurityType.Forex, SecurityType.Crypto, SecurityType.Future, SecurityType.Option, SecurityType.Cfd, SecurityType.Base],
    "FxcmBrokerageModel": [SecurityType.Forex, SecurityType.Cfd],
    "GDAXBrokerageModel": [SecurityType.Crypto],
    "InteractiveBrokersBrokerageModel": [SecurityType.Equity, SecurityType.Forex, SecurityType.Future, SecurityType.Option],
    "OandaBrokerageModel": [SecurityType.Forex, SecurityType.Cfd],
    "TradierBrokerageModel": [SecurityType.Equity]
}

def BrokerageErrorMessage(symbol, brokerage):
    ErrorMessage = {
        "AlpacaBrokerageModel": f"Alpaca Brokerage doesn't support trading {symbol.Value}.",
        "AlphaStreamsBrokerageModel": f"Alpha Streams Brokerage doesn't support data for {symbol.Value}.",
        "BitfinexBrokerageModel": f"Bitfinex Brokerage doesn't support trading {symbol.Value}.",
        "DefaultBrokerageModel": f"Default Brokerage doesn't support data for {symbol.Value}.",
        "FxcmBrokerageModel": f"FXCM Brokerage doesn't support trading {symbol.Value}.",
        "GDAXBrokerageModel": f"GDAX Brokerage doesn't support trading {symbol.Value}.",
        "InteractiveBrokersBrokerageModel": f"Interactive Brokers doesn't support trading {symbol.Value}.",
        "OandaBrokerageModel": f"Oanda Brokerage doesn't support trading {symbol.Value}.",
        "TradierBrokerageModel": f"Tradier Brokerage doesn't support trading {symbol.Value}."
    }

    return ErrorMessage[brokerage]