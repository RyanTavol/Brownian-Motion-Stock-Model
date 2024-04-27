import numpy as np
from fetchStocks import StockData
import pandas as pd

def muBootstrap(stock: StockData, estimations, T, dt):
    """
    Calculate the drift parameter (mu) using Bootstrap method.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.

    Returns:
        float: Drift parameter (mu).
    """
    # Calculate stock returns
    returns = (stock.stock_data_df['Close'] - stock.stock_data_df['Close'].shift(1)) / stock.stock_data_df['Close'].shift(1)
    
    # Calculate mu
    mu = returns.mean() / dt

    return mu

import numpy as np
from fetchStocks import StockData

def sigma1Bootstrap(stock: StockData, estimations, T, dt):
    """
    Calculate the volatility parameter (sigma1) using Bootstrap method.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.

    Returns:
        float: Volatility parameter (sigma1).
    """
    # Calculate stock returns
    returns = (stock.stock_data_df['Close'] - stock.stock_data_df['Close'].shift(1)) / stock.stock_data_df['Close'].shift(1)
    
    # Calculate sigma1 (Common Volatility)
    sigma1 = np.sqrt(((returns - returns.mean())**2).sum() / ((len(returns) - 1) * dt))
    
    return sigma1

def sigma2Bootstrap(stock: StockData, estimations, T, dt):
    """
    Calculate the volatility parameter (sigma2) using Bootstrap method.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.

    Returns:
        float: Volatility parameter (sigma2).
    """
    # Calculate log returns
    log_returns = np.log(stock.stock_data_df['Close']) - np.log(stock.stock_data_df['Close'].shift(1))
    
    # Calculate sigma2 (Log Volatility)
    sigma2 = np.sqrt(((log_returns - log_returns.mean())**2).sum() / ((len(log_returns) - 1) * dt))
    
    return sigma2
