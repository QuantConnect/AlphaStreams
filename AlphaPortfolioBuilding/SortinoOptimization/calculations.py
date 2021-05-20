from scipy.optimize import minimize, LinearConstraint
import numpy as np
import pandas as pd

from clr import AddReference
AddReference("QuantConnect.Research")
from QuantConnect import * 
from QuantConnect.Research import QuantBook

from factors import *


class AlphaStreamOptimizer:
    """
    Provides an implementation of a portfolio optimizer that maximizes the Sortino ratio.
    """

    def Optimize(self, equity_curves):
        """
        Use SciPy to optimize the portfolio weights of the alphas included in the `equity_curves` DataFrame.
        
        Input:
         - equity_curves
            DataFrame of trailing equity curves for n alphas
            
        Array of doubles, representing the optimized portfolio weights for the alphas
        """
        size = equity_curves.columns.size
        x0 = np.array(size * [1. / size]) # initial guess is equal-weighting
        
        # Σw <= 1
        constraints = [{'type': 'eq', 'fun': lambda weights: self.get_budget_constraint(weights)}]
        opt = minimize(lambda weights: self.objective_function(equity_curves, weights), # Objective function
                       x0,                                                              # Initial guess
                       bounds = self.get_boundary_conditions(size),                     # Bounds for variables: 0 ≤ w ≤ 1
                       constraints = constraints,                                       # Constraints definition
                       method='SLSQP',          # Optimization method:  Sequential Least Squares Programming
                       options ={'ftol': 1e-10, 'maxiter': 200, 'disp': False})                        # Additional options

        return opt['x'] if opt['success'] else x0
        
    def objective_function(self, equity_curves, weights):
        """
        Objective function to use when optimizing the portfolio weights
        
        Input:
         - equity_curves
            DataFrame of equity curves for the alphas
         - weights
            Test weights selected by the optimizer
        
        Returns a score for the weights that's calculated by applying the Sortino factor.
        """
        equity_curve = (equity_curves * weights).sum(axis=1)
        return self.f_scale(-Sortino.evaluate(equity_curve)) # negative so we maximize it
    
    def f_scale(self, x):
        """
        Bounds the value of `x` to [-5, +5] using a sigmoidal curve
        
        Input:
         - x
            Value to be bounded
        
        Returns the bounded `x` value.
        """
        return x*5/np.sqrt(10+x*x)


    def get_boundary_conditions(self, size):
        """
        Creates the boundary condition for the portfolio weights
        
        Input:
         - size
        """
        return tuple((0.0, 1.0) for x in range(size))
        

    def get_budget_constraint(self, weights):
        """
        Defines a budget constraint: the sum of the weights = 1
        
        Input:
         - weights
            Array of portfolio weights
        """
        return  np.sum(weights) - 1


def optimize_allocations(equity_curves, lookback):
    """
    Determines how much of the portfolio to allocate to each alpha on a monthly basis.
    
    Input:
     - equity_curves
        DataFrame of equity curves of individual Alpha Streams algorithms
     - lookback
        An integer representing the number of days to look back when calculating the factor values
    
    Returns a DataFrame that shows how much to allocate to each alpha for each month in order
    to maximize the trailing portfolio factor.
    """
    allocation_by_alpha_id = {}
    allocations_over_time = pd.DataFrame()
    optimizer = AlphaStreamOptimizer()
    month = 0
    print("Working please wait...")
    for time, row in equity_curves.iterrows():
        # Rebalance monthly
        if time.month == month:
            continue    
    
        # Select active alphas
        active_alphas = list(row.index[~row.isna()])
            
        # Get trailing history
        window = equity_curves[active_alphas].loc[:time].iloc[-lookback:].dropna(axis=1)
        active_alphas = list(window.columns)
        if len(active_alphas) < 2 or len(window) < lookback:
            continue
    
        month = time.month
    
        # Scale each equity curve to have start value of 1 over the lookback period
        normalized_equity_curves = window / window.iloc[0]
    
        best_allocation_scheme = optimizer.Optimize(normalized_equity_curves)
        
        # Save allocation scheme that the optimizer has selected
        allocation_by_alpha_id = dict(zip(window.columns, best_allocation_scheme))
        for alpha_name, allocation in allocation_by_alpha_id.items():
            allocations_over_time.loc[time.date(), alpha_name] = allocation
    return allocations_over_time


def get_composite_equity_curve(equity_curves, allocations_over_time):
    """
    Builds the composite equity curve that's produced by following the 
    allocations_over_time in real time.
    
    Input:
     - equity_curves
        A DataFrame holding the equity curves of all the alphas under analysis
     - allocations_over_time
        A DataFrame which lists how much to allocate to each alpha over time
    
    Returns the composite equity curve
    """
    composite_equity_curve = pd.Series()
    daily_returns = equity_curves.pct_change().shift(-1)
    current_allocation = pd.Series()
    for time, row in daily_returns.iterrows():
        date = time.date()
        if date in allocations_over_time.index:
            current_allocation = allocations_over_time.loc[date].dropna()
        if current_allocation.empty:
            continue
        daily_return = sum(current_allocation * row[current_allocation.index])
        composite_equity_curve = composite_equity_curve.append(pd.Series([daily_return], index=[date]))
    composite_equity_curve = (composite_equity_curve + 1).cumprod().shift(1).dropna()
    composite_equity_curve.name = '*CompositeAlpha*'
    return composite_equity_curve
