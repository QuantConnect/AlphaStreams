from datetime import datetime, timedelta

MARKETS = ['empty', 'USA', 'FXCM', 'Oanda', 'Dukascopy', 'Bitfinex', 'Globex', 'NYMEX', 'CBOT', 'ICE', 'CBOE', 'NSE',
           'GDAX', 'Kraken', 'Bittrex', 'Bithumb', 'Binance', 'Poloniex', 'Coinone', 'HitBTC', 'OkCoin', 'Bitstamp']

SECURITY_TYPES = ['Base', 'Equity', 'Option', 'Commodity', 'Forex', 'Future', 'Cfd', 'Crypto']

OPTION_STYLES = ['American', 'European']

OPTION_RIGHTS = ['Call', 'Put']


class Symbol:
    def __init__(self, security_id):
        self.security_type_width = 100
        self.security_type_offset = 1

        self.market_width = 1000
        self.market_offset = self.security_type_offset * self.security_type_width

        self.strike_default_scale = 4
        self.strike_default_scaleExpanded = 10 ** self.strike_default_scale
        self.strike_scale_width = 100
        self.strike_scale_offset = self.market_offset * self.market_width

        self.strike_width = 1000000
        self.strike_offset = self.strike_scale_offset * self.strike_scale_width

        self.option_style_width = 10
        self.option_style_offset = self.strike_offset * self.strike_width

        self.days_width = 100000
        self.days_offset = self.option_style_offset * self.option_style_width

        self.put_call_offset = self.days_offset * self.days_width
        self.put_call_width = 10

        self.ID = security_id
        is_option = False

        if '|' in security_id:
            # If contains '|' means it is an Option
            [security_id, underlying_id] = security_id.split('|')
            self.Underlying = Symbol(underlying_id)
            is_option = True

        symbol, properties = self.parse_security_id(security_id)
        self.Symbol = symbol
        self.SecurityType = SECURITY_TYPES[self.extract_from_properties(properties,
                                                                        self.security_type_offset,
                                                                        self.security_type_width)]
        self.Market = MARKETS[self.extract_from_properties(properties,
                                                           self.market_offset,
                                                           self.market_width)]
        if self.SecurityType == 'Equity' or self.SecurityType == 'Option' or self.SecurityType == 'Future':
            self.Date = self.extract_date_from_properties(properties)
        else:
            self.Date = None
        if is_option:
            self.OptionRight = OPTION_RIGHTS[self.extract_from_properties(properties,
                                                                          self.put_call_offset,
                                                                          self.put_call_width)]
            self.OptionStyle = OPTION_STYLES[self.extract_from_properties(properties,
                                                                          self.option_style_offset,
                                                                          self.option_style_width)]
            self.StrikePrice = self.extract_strike_price_from_properties(properties)

    def extract_from_properties(self, properties, offset, width):
        return (properties // offset) % width

    def extract_date_from_properties(self, properties):
        days = (properties // self.days_offset) % self.days_width
        return datetime(1899, 12, 30, 0, 0, 0) + timedelta(days=float(days))

    def extract_strike_price_from_properties(self, properties):
        scale = int((properties // self.strike_scale_offset) % self.strike_scale_width) - self.strike_default_scale
        unscaled_price = (properties // self.strike_offset) % self.strike_width
        return unscaled_price * 10 ** scale

    def parse_security_id(self, security_id):
        [symbol, code] = security_id.split(' ')
        properties = self.decode_base_36(code)
        return symbol, properties

    @staticmethod
    def decode_base_36(code):
        base = 1
        result = 0
        ord_zero = ord('0')
        ord_a = ord('A')
        for char in code[::-1]:
            ord_char = ord(char)
            value = ord_char - ord_zero if ord_char <= 57 else ord_char - ord_a + 10
            result += base * value
            base *= 36
        return result
