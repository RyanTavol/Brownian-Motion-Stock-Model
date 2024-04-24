import numpy as np
from fetchStocks import StockData
from simulateSDE import simulate_stock_prices
from plot import multi_SDE_plot, dual_multi_SDE_plot

import sys
sys.path.append('./parameterMethods')
from fixedParameters import muFixedParam, sigmaFixedParam


apple = StockData("AAPL")
data = StockData.from_dataframe(apple.getStockDataRange(None, "2022-01-01"))
trueStockPrice = StockData.from_dataframe(apple.getStockDataRange(data.end_date, "2023-01-01"))
simulation = simulate_stock_prices(data, muFixedParam, sigmaFixedParam)
print(simulation)
print(simulation.shape)
print(len(trueStockPrice.getClosingPrices()))
dual_multi_SDE_plot(simulation, trueStockPrice)

# print(apple.stock_data_df)
# print(apple.getAllForDate("2023-01-05"))

# simulation = simulate_stock_prices(apple, muFixedParam, sigmaFixedParam)
# multi_SDE_plot(simulation)
# print(simulation)

print("Test")