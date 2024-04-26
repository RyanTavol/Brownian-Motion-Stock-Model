import numpy as np
from fetchStocks import StockData
from simulateSDE import simulate_stock_prices, select_middle_path, compute_median_path, compute_mean_path
from plot import multi_SDE_plot, dual_multi_SDE_plot, plot_single_estimated_path, plot_comparison_mid

import sys
sys.path.append('./parameterMethods')
from fixedParameters import muFixedParam, sigmaFixedParam
from capm import muCAPM, sigmaCAPM

print("Running Main:")

stockTicker = "IBM"

stock = StockData(stockTicker)
data = StockData(stockTicker, stock.getStockDataRange(None, "2023-01-01"))
trueStockPrice = StockData(stockTicker,stock.getStockDataRange(data.end_date, "2024-01-01"))
# simulation = simulate_stock_prices(data, muFixedParam, sigmaFixedParam, dt = 1/(len(trueStockPrice.getClosingPrices())-1))
simulation = simulate_stock_prices(data, muCAPM, sigmaCAPM, dt = 1/(len(trueStockPrice.getClosingPrices())-1))
middle = select_middle_path(simulation)
median = compute_median_path(simulation)
mean = compute_mean_path(simulation)


dual_multi_SDE_plot(simulation, trueStockPrice.getClosingPrices(), stockTicker)
plot_comparison_mid(trueStockPrice.getClosingPrices(), median, middle, mean)
# plot_single_estimated_path(trueStockPrice.getClosingPrices(), estimation, stockTicker)


