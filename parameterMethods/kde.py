import numpy as np
from sklearn.neighbors import KernelDensity
from fetchStocks import StockData

def muKDE(stock: StockData, estimations, T, dt):
    # Extract daily returns
    daily_returns = stock.stock_data_df['Adj Close'].pct_change().dropna()

    # Initialize and fit Kernel Density Estimation (KDE) to daily returns
    kde = KernelDensity(kernel='gaussian').fit(daily_returns.values.reshape(-1, 1))

    # Sample from KDE to estimate mu
    mu_samples = np.exp(kde.sample())

    # Return mean of the samples as the estimate for mu
    return np.mean(mu_samples)

def sigmaKDE(stock: StockData, estimations, T, dt):
    # Extract daily returns
    daily_returns = stock.stock_data_df['Adj Close'].pct_change().dropna()

    # Initialize and fit Kernel Density Estimation (KDE) to daily returns
    kde = KernelDensity(kernel='gaussian').fit(daily_returns.values.reshape(-1, 1))

    # Sample from KDE to estimate sigma
    sigma_samples = np.exp(kde.sample())

    # Return mean of the samples as the estimate for sigma
    return np.mean(sigma_samples)
