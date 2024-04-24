import numpy as np
from fetchStocks import StockData
from simulateSDE import simulate_stock_prices
from plot import multi_SDE_plot

import sys
sys.path.append('./parameterMethods')
from fixedParameters import muFixedParam, sigmaFixedParam

apple = StockData("AAPL", '2023-01-01', '2023-12-31')
# print(apple.stock_data_df)
# print(apple.getAllForDate("2023-01-05"))

simulation = simulate_stock_prices(apple, muFixedParam, sigmaFixedParam)
multi_SDE_plot(simulation)
# print(simulation)

print("Test")