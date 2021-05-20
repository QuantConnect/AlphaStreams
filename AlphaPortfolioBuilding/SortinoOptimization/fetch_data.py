from clr import AddReference
AddReference("QuantConnect.Research")
from QuantConnect import * 
from QuantConnect.Research import QuantBook

import pandas as pd
from io import StringIO

def get_live_equity_curves(alpha_id_by_name):
    """
    Gathers the live equity curves of active alphas. We declare an alpha as 'inactive' 
    if the last data point in its equity curve is older that the last data point in the
    equity curve of another alpha in the `alpha_id_by_name` dictionary. We truncate
    the start of the equity curves so that the resulting DataFrame has always atleast 
    2 live alphas running at each timestep.
    
    Input: 
     - client
        Client used to communicate with alpha stream REST api
     - alpha_id_by_name
        Dictionary of alpha IDs, keyed by the alpha name
        
    Returns a DataFrame of normalized live equity curves for the active alphas.
    """
    # Get equity curves into a DataFrame
    qb = QuantBook()
    url = "https://s3.amazonaws.com/alphastreams.quantconnect.com/alphas/equity-unified-live-factors.csv"
    csv = qb.Download(url)
    equity_curves = pd.read_csv(StringIO(csv))
    equity_curves['Time'] = pd.to_datetime(equity_curves['Time'])
    equity_curves.set_index('Time', inplace=True)
    equity_curves = equity_curves[[alpha_id for alpha_id in alpha_id_by_name.values()]]
    equity_curves.columns = [alpha_name for alpha_name in alpha_id_by_name.keys()]
    equity_curves = equity_curves.resample('D').mean().interpolate(method='linear', limit_area='inside')
    
    # Drop inactive alphas
    inactive_alphas = equity_curves.iloc[-1].isna().values
    for alpha_name in equity_curves.columns[inactive_alphas]:
        print(f"'{alpha_name}' excluded because it's marked as inactive.")
    has_data = equity_curves.columns[~inactive_alphas]
    
    # Truncate start of history to when there are atleast 2 alphas
    equity_curves = equity_curves[has_data].dropna(thresh=2)
    
    # Normalize the equity curves
    normalized_curves = pd.DataFrame()
    for alpha_id in equity_curves.columns:
        alpha_equity = equity_curves[alpha_id].dropna()
        alpha_equity = alpha_equity / alpha_equity.iloc[0]
        normalized_curves = normalized_curves.join(alpha_equity, how = 'outer')
    
    return normalized_curves
