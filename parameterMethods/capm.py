import numpy as np
from fetchStocks import StockData
import pandas as pd


def muCAPM(stock: StockData, estimations, T, dt):
    """
    Calculate the drift parameter (mu) for the Geometric Brownian Motion (GBM) model using the Capital Asset Pricing Model (CAPM).

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.

    Returns:
        float: Drift parameter (mu).
    """
    mu = stock.risk_free_rate + stock.beta * (stock.market_return - stock.risk_free_rate )

    # print("Mu", mu)

    return mu

def sigmaCAPM(stock: StockData, estimations, T, dt):
    """
    Calculate the volatility parameter (sigma) for the Geometric Brownian Motion (GBM) model using the Capital Asset Pricing Model (CAPM).

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.

    Returns:
        float: Volatility parameter (sigma).
    """

    # Calculate daily returns
    daily_returns = stock.stock_data_df['Adj Close'].pct_change().dropna()

    # Calculate daily standard deviation
    s = daily_returns.std()

    # Calculate annualized volatility
    tau = T * dt
    sigma = s / np.sqrt(tau)

    # print("Sigma", sigma)

    return sigma