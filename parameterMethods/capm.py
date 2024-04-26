import numpy as np
from fetchStocks import StockData
import pandas as pd


def muCAPM(stock: StockData, estimations, T, dt):
    mu = stock.risk_free_rate + stock.beta * (stock.market_return - stock.risk_free_rate )

    # print("Mu", mu)

    return mu

def sigmaCAPM(stock: StockData, estimations, T, dt):
   # Calculate the end date based on the total time T

    # Calculate daily returns
    daily_returns = stock.stock_data_df['Adj Close'].pct_change().dropna()

    # Calculate daily standard deviation
    s = daily_returns.std()

    # Calculate annualized volatility
    tau = T * dt
    sigma = s / np.sqrt(tau)

    # print("Sigma", sigma)

    return sigma