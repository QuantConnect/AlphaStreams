from clr import AddReference
AddReference("QuantConnect.Research")
from QuantConnect import * 
from QuantConnect.Research import QuantBook

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Factor(ABC):
    """
    Abstract base class used to create factors
    """
    @abstractmethod
    def evaluate(equity_curve):
        """
        Calculates the factor value using the provided equity curve.
        
        Input: 
         - equity_curve
            The equity curve to calculate the factor on
    
        Returns the factor value when applied to the equity curve.
        """
        raise Exception("evaluate method not implemented yet.")

        
class Sortino(Factor):
    """
    Sortino Ratio
    """
    def evaluate(equity_curve):
        returns = equity_curve.pct_change().dropna()
        ann_ret = ((np.mean(returns) + 1) ** 252) - 1
        ann_down_std = np.std(returns.loc[returns < 0]) * np.sqrt(252)
        return ann_ret / ann_down_std if ann_down_std is not 0 else None
    
    
class Beta(Factor):
    """
    Beta
    """
    benchmark_data = pd.DataFrame()
    
    @staticmethod
    def load_data(benchmark_security_id='SPY R735QTJ8XC9X', benchmark_name='*Benchmark*'):
        """
        Loads the benchmark data so we can calculate the factor value
        
        Input:
         - benchmark_security_id
            Security ID of the benchmark security
         - benchmark_name
            The column name to use for the benchmark in the DataFrame that's loaded
        """
        Beta.benchmark_data = pd.DataFrame()
        qb = QuantBook()
        benchmark_symbol = qb.Symbol(benchmark_security_id)
        
        # Load benchmark history
        history = qb.History(benchmark_symbol, datetime(1998, 1, 2), datetime.now(), Resolution.Daily)
        Beta.benchmark_data = history.loc[benchmark_symbol].close
        Beta.benchmark_data = Beta.benchmark_data.resample('D').mean().interpolate(method='linear', limit_area='inside')        
        Beta.benchmark_data.name = benchmark_name
    
    def evaluate(equity_curve):    
        # Get benchmark equity curve
        if Beta.benchmark_data.empty:
            Beta.load_data()
        start = equity_curve.index[0]
        end = equity_curve.index[-1] + timedelta(days=1)
        benchmark_equity_curve = Beta.benchmark_data.loc[start:end]
        
        # Calculate Beta
        equity_curve_returns = equity_curve.pct_change().dropna()
        benchmark_returns = benchmark_equity_curve.pct_change().dropna()
        equity_df = pd.concat([equity_curve_returns, benchmark_returns], axis=1)
        corr = equity_df.corr()[benchmark_equity_curve.name][0]
        std = equity_curve_returns.std()
        if std == 0:
            return np.nan
        std_ratio = benchmark_returns.std() / std
        return corr * std_ratio
    
    
class Drawdown(Factor):
    """
    Drawdown
    """
    def evaluate(equity_curve):
        equity_curve = equity_curve.values
        i = np.argmax(np.maximum.accumulate(equity_curve) - equity_curve)
        if equity_curve[:i].size == 0:
            return np.nan
        j = np.argmax(equity_curve[:i])
        return abs((equity_curve[i]/equity_curve[j]) - 1) #round(abs((equity_curve[i]/equity_curve[j]) - 1), 3)
