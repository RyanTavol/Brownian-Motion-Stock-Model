import numpy as np
from fetchStocks import StockData
import pandas as pd


def muCAPM(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Calculate the drift parameter (mu) for the Geometric Brownian Motion (GBM) model using the Capital Asset Pricing Model (CAPM).

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
    mu = stock.risk_free_rate + stock.beta * (stock.market_return - stock.risk_free_rate )

    # print("Mu", mu)

    return mu

def sigmaCAPM(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Calculate the volatility parameter (sigma) for the Geometric Brownian Motion (GBM) model using the Capital Asset Pricing Model (CAPM).

     Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating
        futureTimeIndex (int): Index for how far along the estimation we are

    Returns:
        float: Volatility parameter (sigma).
    """

    # Calculate daily returns
    daily_returns = stock.stock_data_df['Close'].pct_change().dropna()

    # Calculate daily standard deviation
    s = daily_returns.std()

    # Calculate annualized volatility
    tau = T * dt
    sigma = s / np.sqrt(tau)

    # print("Sigma", sigma)

    return sigma