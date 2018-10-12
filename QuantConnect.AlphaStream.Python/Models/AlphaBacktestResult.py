import pandas as pd
from datetime import datetime

class AlphaBacktestResult:
    '''AlphaBacktestResult represents the backtest result of a successfully executed algorithm'''

    def __init__(self, json):
        ''' Creates a new instance of AlphaBacktestResult '''
        self.Statistics = json.get('Statistics', None)
        self.AlphaRuntimeStatistics  = json.get('AlphaRuntimeStatistics', None)
        self.ClosedTrades = self.__create_closed_trades_table(json)
        self.Charts = self.__create_charts_table(json)
        self.ProfitLoss = self.__create_profit_loss_table(json)
        self.Orders = self.__create_order_table(json)
        self.RollingWindow = self.__create_rolling_window_table(json)


    def __create_order_table(self, json):
        '''Creates a dataframe with the orders information'''
        if 'Orders' not in json:
            return None

        def __status_int_to_str(value):
            if value is None: return None
            values = [ 'New', 'Submitted', 'PartiallyFilled', 'Filled', 'Canceled', 'None', 'Invalid', 'CancelPending' ]
            return str(values) if value >= len(values) else values[value]

        def __security_type_int_to_str(value):
            if value is None: return None
            values = [ 'Base', 'Equity', 'Option', 'Commodity', 'Forex', 'Future', 'Cfd', 'Crypto' ]
            return str(values) if value >= len(values) else values[value]

        def __type_int_to_str(value):
            if value is None:   return None
            values = [ 'Market', 'Limit', 'StopMarket', 'StopLimit', 'MarketOnOpen', 'MarketOnClose', 'OptionExercise' ]
            return str(values) if value >= len(values) else values[value]

        columns = [
            'Id', 'Time', 'SecurityType', 'Symbol', 'PriceCurrency', 
            'Quantity', 'Direction', 'Price', 'Type', 'Status', 'Tag',
            'LastFillTime', 'LastUpdateTime', 'CanceledTime' ]

        drop_columns = [
            'BrokerId', 'ContingentId', 'CreatedTime', 'IsMarketable', 'Value',
            'AbsoluteQuantity', 'OrderSubmissionData', 'Properties', 'TimeInForce'] 

        df = pd.DataFrame([v for k, v in json['Orders'].items()], columns = columns + drop_columns)
        df = df.set_index('Id').drop(drop_columns, axis=1)
        df['Time'] = df['Time'].apply(self.__str_to_datetime)
        df['CanceledTime'] = df['CanceledTime'].apply(self.__str_to_datetime)
        df['LastFillTime'] = df['LastFillTime'].apply(self.__str_to_datetime)
        df['LastUpdateTime'] = df['LastUpdateTime'].apply(self.__str_to_datetime)
        df['Symbol'] = df['Symbol'].apply(lambda x: x['ID'])
        df['Type'] = df['Type'].apply(__type_int_to_str)
        df['Direction'] = df['Direction'].apply(self.__direction_int_to_str)
        df['Status'] = df['Status'].apply(__status_int_to_str)

        df['SecurityType'] = df['SecurityType'].apply(__security_type_int_to_str)
        return df.dropna(how='all', axis=1)


    def __create_profit_loss_table(self, json):
        '''Creates a dataframe with the algorithm P&L'''
        if 'ProfitLoss' not in json:
            return None

        df = pd.DataFrame({'profit_loss' : json['ProfitLoss']})
        df.index.name = 'time'
        df.index = df.index.map(self.__str_to_datetime)
        return df


    def __create_closed_trades_table(self, json):
        '''Creates a dataframe with the closed trades information'''
        if 'TotalPerformance' not in json:
            return None

        total = json['TotalPerformance']
        if 'ClosedTrades' not in total:
            return None

        columns = ['Symbol', 'Quantity', 'Direction',
            'EntryTime', 'EntryPrice', 'ExitPrice', 'ExitTime', 'Duration',
            'EndTradeDrawdown', 'MAE', 'MFE', 'ProfitLoss', 'TotalFees']

        df = pd.DataFrame(total['ClosedTrades'], columns = columns)
        df['Symbol'] = df['Symbol'].apply(lambda x: x['ID'])
        df['Direction'] = df['Direction'].apply(self.__direction_int_to_str)
        df['EntryTime'] = df['EntryTime'].apply(self.__str_to_datetime)
        df['ExitTime'] = df['ExitTime'].apply(self.__str_to_datetime)
        df['Duration'] = df['ExitTime'] - df['EntryTime']
        return df.set_index('EntryTime')


    def __create_charts_table(self, json):
        '''Creates a dataframe with the charts information. 
        By converting the json into a dataframe, it makes data visualization easier'''
        if 'Charts' not in json:
            return None

        df_charts = dict()
        charts = dict(json['Charts'])
        for name, chart in charts.items():
            columns = list()
            for column, series in chart['Series'].items():
                df = pd.DataFrame(series['Values'])
                df['x'] = pd.to_datetime(df['x'], unit='s')
                df = df.rename(index=str, columns={"x": "time", "y": column})
                columns.append(df.set_index('time'))            
            df = pd.concat(columns, axis = 1, sort = True)
            df = df.fillna(method = 'ffill')
            df = df.fillna(method = 'bfill')
            df_charts[name] = df
        return df_charts


    def __create_rolling_window_table(self, json):
        '''Creates a dataframe with the rolling statistics information. 
        By converting the json into a dataframe, it makes data visualization easier'''
        if 'RollingWindow' not in json:
            return None

        series = dict()
        if 'TotalPerformance' in json:
            window = json['TotalPerformance']
            stats = window.get('PortfolioStatistics', dict())
            stats.update(window.get('TradeStatistics', dict()))
            series = {'TotalPerformance': pd.Series(stats)}

        for row, window in json['RollingWindow'].items():
            stats = window.get('PortfolioStatistics', dict())
            stats.update(window.get('TradeStatistics', dict()))
            series.update({row: pd.Series(stats)})

        return pd.DataFrame(series).transpose()


    def __direction_int_to_str(self, value):
        if value is None: return None
        return [ 'Buy', 'Sell', 'Hold' ][value]


    def __str_to_datetime(self, value):
        if value is None: return None
        fmt = '%Y-%m-%dT%H:%M:%SZ' if len(value) == 20 else '%Y-%m-%dT%H:%M:%S.%fZ'
        return datetime.strptime(value, fmt)