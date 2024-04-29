import numpy as np
from fetchStocks import StockData

def muMethodOfMoments(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Estimate the drift parameter (mu) using the Method of Moments.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating.
        futureTimeIndex (int): Index for how far along the estimation we are.

    Returns:
        float: Estimated drift parameter (mu).
    """
    # Calculate stock returns
    combined = np.append(stock.getClosingPrices(), estimations[pathIndex, : futureTimeIndex])
    returns = (np.log(combined) - np.log(np.roll(combined, 1)))[1:]  # Log returns excluding the first NaN value

    # Use the sample mean as the estimate for mu
    mu = np.mean(returns) / dt

    return mu

def sigmaMethodOfMoments(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Estimate the volatility parameter (sigma) using the Method of Moments.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating.
        futureTimeIndex (int): Index for how far along the estimation we are.

    Returns:
        float: Estimated volatility parameter (sigma).
    """
    # Calculate stock returns
    combined = np.append(stock.getClosingPrices(), estimations[pathIndex, : futureTimeIndex])
    returns = (np.log(combined) - np.log(np.roll(combined, 1)))[1:]  # Log returns excluding the first NaN value

    # Use the sample standard deviation as the estimate for sigma
    sigma = np.std(returns) / np.sqrt(dt)

    return sigma
