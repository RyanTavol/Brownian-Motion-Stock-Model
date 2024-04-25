import numpy as np
from fetchStocks import StockData
from simulateSDE import simulate_stock_prices
from plot import multi_SDE_plot, dual_multi_SDE_plot

import sys
sys.path.append('./parameterMethods')
from fixedParameters import muFixedParam, sigmaFixedParam

print("Running Main:")

apple = StockData("AAPL")
data = StockData("AAPL", apple.getStockDataRange(None, "2018-01-01"))
trueStockPrice = StockData("AAPL",apple.getStockDataRange(data.end_date, "2019-01-01"))
simulation = simulate_stock_prices(data, muFixedParam, sigmaFixedParam, dt = 1/(len(trueStockPrice.getClosingPrices())-1))
dual_multi_SDE_plot(simulation, trueStockPrice.getClosingPrices())
