import numpy as np
from SRC_fetchStocks import StockData
import pandas as pd

def muBootstrap(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Calculate the drift parameter (mu) using Bootstrap method.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating
        futureTimeIndex (int): Index for how far along the estimation we are

    Returns:
        float: Drift parameter (mu).
    """
    # Calculate stock returns

    combined = np.append(stock.getClosingPrices(), estimations[pathIndex, : futureTimeIndex])
    
    returns = (combined - np.roll(combined, 1)) / np.roll(combined, 1)

    # Calculate mu
    mu = returns.mean() / dt

    return mu

import numpy as np
from SRC_fetchStocks import StockData

def sigma1Bootstrap(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Calculate the volatility parameter (sigma1) using Bootstrap method.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating
        futureTimeIndex (int): Index for how far along the estimation we are

    Returns:
        float: Volatility parameter (sigma1).
    """
    # Calculate stock returns
    combined = np.append(stock.getClosingPrices(), estimations[pathIndex, : futureTimeIndex])
    
    returns = (combined - np.roll(combined, 1)) / np.roll(combined, 1) 

    # Calculate sigma1 (Common Volatility)
    sigma1 = np.sqrt(((returns - returns.mean())**2).sum() / ((len(returns) - 1) * dt))
    
    return sigma1

def sigma2Bootstrap(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Calculate the volatility parameter (sigma2) using Bootstrap method.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating
        futureTimeIndex (int): Index for how far along the estimation we are

    Returns:
        float: Volatility parameter (sigma2).
    """
    # Calculate log returns
    combined = np.append(stock.getClosingPrices(), estimations[pathIndex, : futureTimeIndex])
    
    log_returns = np.log(combined) - np.log(np.roll(combined, 1))
    
    # Calculate sigma2 (Log Volatility)
    sigma2 = np.sqrt(((log_returns - log_returns.mean())**2).sum() / ((len(log_returns) - 1) * dt))
    
    return sigma2
