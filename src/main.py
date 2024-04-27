import numpy as np
from fetchStocks import StockData
from simulateSDE import *
from plot import *
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

# Set The Simulation Seed
SIMULATION_SEED = None
if(SIMULATION_SEED is None):
    SIMULATION_SEED = np.random.randint(0,1000)

np.random.seed(SIMULATION_SEED)
print("Seed:", SIMULATION_SEED)

# Consider changing this to a dictionary instead
PARAMETER_FUNCTIONS =   [\
                            ["Fixed Parameters", (muFixedParam, sigmaFixedParam) ],
                            ["Capital Asset Pricing Model (CAPM)", (muCAPM, sigmaCAPM)],
                            ["Bootstrap (Common Volatility)", (muBootstrap, sigma1Bootstrap)],
                            ["Bootstrap (Log Volatility)", (muBootstrap, sigma2Bootstrap)],
                            # Add other parameter methods here
                        ]


def simulateSingleMethod(ticker, data_start_date, data_end_date, sim_end_date, mu_function, sigma_function, method_name):

    # Set Up Stock And "Previous History"
    stock = StockData(ticker)
    data = StockData(ticker, stock.getStockDataRange(data_start_date, data_end_date), stock.market_data_df)
    trueStockData = StockData(ticker,stock.getStockDataRange(data.end_date, sim_end_date), stock.market_data_df)

    trueStockPrices = trueStockData.getClosingPrices()  
    # Simulate Stock Price
    simulation = simulate_stock_prices(data, mu_function, sigma_function, dt = 1/(len(trueStockPrices)-1))

    # Extrapolate Single Paths
    middle = select_middle_path(simulation)
    median = compute_median_path(simulation)
    mean = compute_mean_path(simulation)

    simulation_data =   {
                            'method_name': method_name,
                            'true_stock_data': trueStockData,
                            'true_stock_prices': trueStockPrices,
                            'simulation': simulation,
                            'middle_path': middle,
                            'median_path': median,
                            'mean_path': mean,
                        }
    
    return simulation_data


def compareSingle(simulation_data):
    print("\n"+simulation_data['method_name']+"\n")
    print(analyzeAll(simulation_data))
    combined_plot(simulation_data)

def simulateAllMethods(ticker, data_start_date, data_end_date, sim_end_date):
    # Each Time You Compare Remember To Reset The Seed
    # Going To Be A List Of (Methodname: Dictionary)
    simulation_results = []

    for method_name, param_funcs in PARAMETER_FUNCTIONS:
        np.random.seed(SIMULATION_SEED)
        mu_function, sigma_function = param_funcs
        simulation_data = simulateSingleMethod(ticker, data_start_date, data_end_date, sim_end_date, mu_function, sigma_function, method_name)
        print("Method:", method_name)
        simulation_results.append(simulation_data)
        

    return simulation_results

def compareMultiple(simulation_data_list):
    for simulation_data in simulation_data_list:
        compareSingle(simulation_data)


def simulateFuture():
    pass

if __name__=='__main__':
        
    stockTicker = "IBM"
    dataStart = None
    dataEnd = "2023-01-01"
    simEnd = "2024-01-01"
    muFunc = muBootstrap
    sigmaFunc = sigma1Bootstrap
    methodName = "Bootstrap (Common Volatility)"

    # simulateAndCompare(stockTicker, dataStart, dataEnd, simEnd, muFunc, sigmaFunc)

    # simulateAndCompareAllFunc(stockTicker, dataStart, dataEnd, simEnd )

    # simulation_data = simulateSingleMethod(stockTicker, dataStart, dataEnd, simEnd, muFunc, sigmaFunc, methodName)
    # compareSingle(simulation_data)

    simulation_data_all = simulateAllMethods(stockTicker, dataStart, dataEnd, simEnd)
    compareMultiple(simulation_data_all)
