import numpy as np
from fetchStocks import StockData
from simulateSDE import simulate_stock_prices, select_middle_path, compute_median_path, compute_mean_path
from plot import multi_SDE_plot, dual_multi_SDE_plot, plot_single_estimated_path, plot_comparison_mid
from analysis import *

import sys
sys.path.append('./parameterMethods')
from fixedParameters import muFixedParam, sigmaFixedParam
from capm import muCAPM, sigmaCAPM
# from mle import muMLE, sigmaMLE
from kde import muKDE, sigmaKDE
# from bayesian import muBayesian, sigmaBayesian
from bootstrap import muBootstrap, sigma1Bootstrap, sigma2Bootstrap

print("Running Main:")

def simulateAndCompare(ticker, data_start_date, data_end_date, sim_end_date, muFunction, sigmaFunction):

    # Set Up Stock And "Previous History"
    stock = StockData(ticker)
    data = StockData(ticker, stock.getStockDataRange(data_start_date, data_end_date), stock.market_data_df)
    trueStockData = StockData(ticker,stock.getStockDataRange(data.end_date, sim_end_date), stock.market_data_df)

    trueStockPrices = trueStockData.getClosingPrices()  
    # Simulate Stock Price
    simulation = simulate_stock_prices(data, muFunction, sigmaFunction, dt = 1/(len(trueStockPrices)-1))

    # Extrapolate Single Paths
    middle = select_middle_path(simulation)
    median = compute_median_path(simulation)
    mean = compute_mean_path(simulation)

    # Analyze Comparison Metrics
    print("Multi Analysis:\t\t", analyzeAllMulti(trueStockPrices, simulation))
    print("Mean Analysis:\t\t", analyzeAllSingle(trueStockPrices, mean))
    print("Median Analysis:\t", analyzeAllSingle(trueStockPrices, median))
    print("Middle Analysis:\t", analyzeAllSingle(trueStockPrices, middle))

    # Plot Results
    dual_multi_SDE_plot(simulation, trueStockPrices, ticker)
    plot_comparison_mid(trueStockPrices, median, middle, mean, ticker)

def simulateFuture():
    pass

stockTicker = "IBM"
dataStart = None
dataEnd = "2023-01-01"
simEnd = "2024-01-01"
muFunc = muBootstrap
sigmaFunc = sigma1Bootstrap

simulateAndCompare(stockTicker, dataStart, dataEnd, simEnd, muFunc, sigmaFunc)

