from clr import AddReference
AddReference("QuantConnect.Research")
from QuantConnect import * 
from QuantConnect.Research import QuantBook
from QuantConnect.Statistics import *
from factors import Sortino, Drawdown

from datetime import timedelta
import pandas as pd

def get_performance_statistics(composite_equity_curve, bechmark_security_id="SPY R735QTJ8XC9X"):
    """
    Calculates several performance statistics on the composite equity curve.
    
    Input:
     - composite_equity_curve
        Equity curve of the optimized portfolio
     - bechmark_security_id
        Security ID of the benchmark to use in some of the statistic calculations (like Beta)
    
    Returns a DataFrame that lists the performance statistics of the composite equity curve.
    """
    performance_statistics = {}
    daily_returns = list(composite_equity_curve.pct_change().dropna().values)
    
    # CompoundingAnnualPerformance
    start_equity = composite_equity_curve.iloc[0]
    end_equity = composite_equity_curve.iloc[-1]
    num_years = (composite_equity_curve.index[-1] - composite_equity_curve.index[0]).days / 365
    comp_annual_performance = Statistics.CompoundingAnnualPerformance(start_equity, end_equity, num_years)
    performance_statistics['CompoundingAnnualPerformance'] = "{:.2%}".format(comp_annual_performance)
    
    # AnnualPerformance
    performance_statistics['AnnualPerformance'] = Statistics.AnnualPerformance(daily_returns, 365)
    
    # AnnualVariance
    performance_statistics['AnnualVariance'] = Statistics.AnnualVariance(daily_returns, 365)
    
    # AnnualStandardDeviation
    performance_statistics['AnnualStandardDeviation'] = Statistics.AnnualStandardDeviation(daily_returns, 365)
    
    # Fetch daily benchmark returns
    qb = QuantBook()
    start_date = composite_equity_curve.index[0] - timedelta(days=5) # 5 day buffer incase of holidays/weekends
    end_date = composite_equity_curve.index[-1] + timedelta(days=5)
    benchmark_symbol = qb.Symbol(bechmark_security_id)
    history = qb.History(benchmark_symbol, start_date, end_date, Resolution.Daily)
    closes = history.loc[benchmark_symbol].close
    closes = closes.resample('D').mean().interpolate(method='linear')
    closes = closes.reindex(pd.DatetimeIndex(composite_equity_curve.index)) # Line up benchmark index with portfolio index
    benchmark_daily_returns = list(closes.pct_change().dropna().values)
    
    # Beta
    performance_statistics['Beta'] = Statistics.Beta(daily_returns, benchmark_daily_returns)
    
    # Alpha
    performance_statistics['Alpha'] = Statistics.Alpha(daily_returns, benchmark_daily_returns, 0)
    
    # Tracking Error
    performance_statistics['TrackingError'] = Statistics.TrackingError(daily_returns, benchmark_daily_returns, 365)
    
    # Information Ratio
    performance_statistics['InformationRatio'] = Statistics.InformationRatio(daily_returns, benchmark_daily_returns)
    
    # Sharpe
    performance_statistics['SharpeRatio'] = Statistics.SharpeRatio(daily_returns, 0)
    
    # Sortino
    performance_statistics['Sortino'] = Sortino.evaluate(composite_equity_curve)
    
    # Max Drawdown
    performance_statistics['MaxDrawdown'] = "{:.2%}".format(Drawdown.evaluate(composite_equity_curve))
    
    # Treynor Ratio
    performance_statistics['TreynorRatio'] = Statistics.TreynorRatio(daily_returns, benchmark_daily_returns, 0)
    
    # PSR
    #benchmark_sharpe = Statistics.SharpeRatio(benchmark_daily_returns, 0)
    #performance_statistics['ProbabilisticSharpeRatio'] = Statistics.ProbabilisticSharpeRatio(daily_returns, benchmark_sharpe)
    
    # Observed Sharpe Ratio
    performance_statistics['ObservedSharpeRatio'] = Statistics.ObservedSharpeRatio(daily_returns)
    
    # Round the statistics for a nice display
    for key, value in performance_statistics.items():
        if not isinstance(value, str):
            performance_statistics[key] = round(value, 4)
    
    return pd.DataFrame(pd.Series(performance_statistics, name='value'))
