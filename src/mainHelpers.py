import numpy as np
# from prettytable import PrettyTable 
from tabulate import tabulate
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

PARAMETER_FUNCTIONS =   {
                            "Fixed Parameters": (muFixedParam, sigmaFixedParam),
                            "Capital Asset Pricing Model (CAPM)": (muCAPM, sigmaCAPM),
                            "Bootstrap (Common Volatility)" : (muBootstrap, sigma1Bootstrap),
                            "Bootstrap (Log Volatility)": (muBootstrap, sigma2Bootstrap),
                            # "Kernel Density Estimation (KDE)" : (muKDE, sigmaKDE),
                        }

# [\
#                             ["Fixed Parameters", (muFixedParam, sigmaFixedParam) ],
#                             ["Capital Asset Pricing Model (CAPM)", (muCAPM, sigmaCAPM)],
#                             ["Bootstrap (Common Volatility)", (muBootstrap, sigma1Bootstrap)],
#                             ["Bootstrap (Log Volatility)", (muBootstrap, sigma2Bootstrap)],
#                             # ["Kernel Density Estimation (KDE)", (muKDE, sigmaKDE)],
#                             # Add other parameter methods here
#                         ]
SIMULATION_SEED = None
def setSeed(seed = None):
    SIMULATION_SEED = seed
    if(SIMULATION_SEED is None):
        SIMULATION_SEED = np.random.randint(0,1000)
    np.random.seed(SIMULATION_SEED)
    print("Seed:", SIMULATION_SEED)

# Functions For Simulating Based On Methods Compared To True Stock Value

def simulateSingleMethod(ticker, data_start_date, data_end_date, sim_end_date, method_name, stock_data = None):
    """
    Simulate a single method for stock price prediction.

    Args:
        ticker (str): Ticker symbol of the stock.
        data_start_date (str): Start date of historical data.
        data_end_date (str): End date of historical data.
        sim_end_date (str): End date of the simulation.
        mu_function (function): Function to calculate the mean parameter.
        sigma_function (function): Function to calculate the standard deviation parameter.
        method_name (str): Name of the simulation method.
        stock_data (StockData, optional): Object containing historical stock data. Defaults to None.

    Returns:
        dict: Dictionary containing simulation data.
    """
    mu_function, sigma_function = PARAMETER_FUNCTIONS[method_name]
    # Set Up Stock And "Previous History"
    if(stock_data is None):
        stock = StockData(ticker)
    else:
        stock = stock_data
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
                            'ticker': ticker,
                            'method_name': method_name,
                            'true_stock_data': trueStockData,
                            'true_stock_prices': trueStockPrices,
                            'simulation': simulation,
                            'middle_path': middle,
                            'median_path': median,
                            'mean_path': mean,
                        }
    
    return simulation_data

def simulateAllMethods(ticker, data_start_date, data_end_date, sim_end_date):
    """
    Simulate all methods for stock price prediction.

    Args:
        ticker (str): Ticker symbol of the stock.
        data_start_date (str): Start date of historical data.
        data_end_date (str): End date of historical data.
        sim_end_date (str): End date of the simulation.

    Returns:
        list: List of dictionaries containing simulation data for each method.
    """
    # Each Time You Compare Remember To Reset The Seed
    # Going To Be A List Of (Methodname: Dictionary)
    simulation_results = []
    stock = StockData(ticker)
    for method_name, param_funcs in PARAMETER_FUNCTIONS.items():
        np.random.seed(SIMULATION_SEED)
        simulation_data = simulateSingleMethod(ticker, data_start_date, data_end_date, sim_end_date, method_name, stock)
        print(f"Simulation Complete: [{method_name}]")
        simulation_results.append(simulation_data)
        
    return simulation_results


# Functions For Comparing Simulations To Truck Stock Value

def compareSingle(simulation_data, analyze = True, plot = True, compact = False):
    """
    Compare a single simulation.

    Args:
        simulation_data (dict): Dictionary containing simulation data.
        analyze (boolean): Boolean determine if it should run the code to analyze
        plot (boolean): Boolean to determine if it should plot the results

    Returns:
        return analysis dictionary object as returned by analyzeAll
    """
   
    if analyze:
        print("\nAnalysis For: ",simulation_data["ticker"])
        print(createTable([simulation_data], compact))
        # analysis = analyzeAll(simulation_data)
        # print(analysis)
    if plot:
        combined_plot_comparison(simulation_data)


def compareMultipleMethods(simulation_data_list, analyze = True, plot = True, compact = False):
    """
    Compare multiple simulations.

    Args:
        simulation_data_list (list): List of dictionaries containing simulation data for each method.

    Returns:
        None
    """
    for simulation_data in simulation_data_list:
        if plot:
            compareSingle(simulation_data, False, True)
    if analyze:
        print("\nAnalysis For: ",simulation_data_list[0]["ticker"])
        print(createTable(simulation_data_list, compact))

        
def createTable(simulation_data_list, compact = False):
    myData = []
    for simulation_data in simulation_data_list:
        analysis = analyzeAll(simulation_data)
        multiA = analysis["Multi_Analysis"]
        meanA = analysis["Mean_Analysis"]
        medianA = analysis["Median_Analysis"]
        middleA = analysis["Middle_Analysis"]
        methodName = simulation_data["method_name"]

        myData.append([methodName, "Multiple Paths", multiA[0][1], multiA[1][1], multiA[2][1]])
        if not compact:
            myData.append([methodName, "Mean Path", meanA[0][1], meanA[1][1], meanA[2][1]])
            myData.append([methodName, "Median Path", medianA[0][1], medianA[1][1], medianA[2][1]])
            myData.append([methodName, "Middle Path", middleA[0][1], middleA[1][1], middleA[2][1]])
        avgCC = np.mean([meanA[0][1], medianA[0][1],middleA[0][1]])
        avgMAPE = np.mean([meanA[1][1], medianA[1][1],middleA[1][1]])
        avgPI = np.mean([meanA[2][1], medianA[2][1],middleA[2][1]])
        myData.append([methodName, "Average of Single Paths", avgCC, avgMAPE, avgPI])
              
    head = ["Method Name", "Analysis Group", "Correlation Coefficient", "MAPE", "Percentage Inliers"]
    table = tabulate(myData, headers=head, tablefmt="grid")
    return table

# Functions For Simulating The Future Of A Stock

def simulateFutureSingle(ticker, data_start_date, sim_end_date, method_name, stock_data = None):
    """
    Simulate future stock prices from today. Simulations have nothing to compare them to.

    Returns:
        dict: Dictionary containing simulation data.
    """
    mu_function, sigma_function = PARAMETER_FUNCTIONS[method_name]
    if(stock_data is None):
        stock = StockData(ticker)
    else:
        stock = stock_data
    data = StockData(ticker, stock.getStockDataRange(data_start_date, None), stock.market_data_df)

    date_range = pd.date_range(start = data.end_date, end=sim_end_date, freq='B')  # 'B' stands for business days
    time = len(date_range) / 252

    simulation = simulate_stock_prices(data, mu_function, sigma_function, T = time, dt = 1/252)

    # Extrapolate Single Paths
    middle = select_middle_path(simulation)
    median = compute_median_path(simulation)
    mean = compute_mean_path(simulation)

    simulation_data =   {
                            'ticker': ticker,
                            'method_name': method_name,
                            'simulation': simulation,
                            'middle_path': middle,
                            'median_path': median,
                            'mean_path': mean,
                        }
    
    return simulation_data

def simulateFutureAllMethods(ticker, data_start_date, sim_end_date):
    """
    Simulates future stock prices using different methods.

    Args:
        ticker (str): Ticker symbol of the stock.
        data_start_date (str): Start date for historical data.
        sim_end_date (str): End date for simulation.

    Returns:
        list: List of dictionaries containing simulation data for each method.
    """
    simulation_results = []
    stock = StockData(ticker)
    for method_name, param_funcs in PARAMETER_FUNCTIONS.items():
        np.random.seed(SIMULATION_SEED)
        # mu_function, sigma_function = param_funcs
        simulation_data = simulateFutureSingle(ticker, data_start_date, sim_end_date, method_name, stock)
        print(f"Simulation Complete: [{method_name}]")
        simulation_results.append(simulation_data)
        
    return simulation_results

# Functions For Plotting The Future Stock Simulations

def plotSingleFuture(simulation_data):
    """
    Plots future stock price predictions for a single method.

    Args:
        simulation_data (dict): Dictionary containing simulation data.

    Returns:
        None
    """
    combined_plot_future(simulation_data)


def plotMultipleFuture(simulation_data_list):
    """
    Plots future stock price predictions for multiple methods.

    Args:
        simulation_data_list (list): List of dictionaries containing simulation data for each method.

    Returns:
        None
    """
    for simulation_data in simulation_data_list:
        plotSingleFuture(simulation_data)