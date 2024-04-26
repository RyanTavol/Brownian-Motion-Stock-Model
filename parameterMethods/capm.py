import numpy as np
from fetchStocks import StockData
import pandas as pd


def muCAPM(stock: StockData, estimations, T, dt):
    end_date = stock.end_date
    start_date = end_date - pd.DateOffset(years=T) 

    beta = stock.calcBeta(start_date, end_date)

    mu = stock.risk_free_rate + beta * (stock.market_return - stock.risk_free_rate )
    # mu /= 10
    # print("Mu", mu)
    return mu

def sigmaCAPM(stock: StockData, estimations, T, dt):
   # Calculate the end date based on the total time T
    end_date = stock.end_date
    start_date = end_date - pd.DateOffset(years=T)

    # print(start_date)
    # print(end_date)
    # Filter stock data for the previous T years
    stock_data_filtered = stock.getStockDataRange(start_date, end_date)

    # Calculate daily returns
    daily_returns = stock_data_filtered['Adj Close'].pct_change().dropna()

    # Calculate daily standard deviation
    s = daily_returns.std()

    # Calculate annualized volatility
    tau = T * dt  # Assuming 250 trading days per year
    sigma = s / np.sqrt(tau)

    # print("Sigma", sigma)

    return sigma