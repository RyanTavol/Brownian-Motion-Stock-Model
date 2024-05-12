import numpy as np
import datetime
from tabulate import tabulate
from fetchStocks import StockData
from simulateSDE import *
from plot import *
from analysis import *

import sys
sys.path.append('./parameterMethods')
from fixedParameters import muFixedParam, sigmaFixedParam
from capm import muCAPM, sigmaCAPM
from bootstrap import muBootstrap, sigma1Bootstrap, sigma2Bootstrap
from kde import muKDE, sigmaKDE
# from mle import muMLE, sigmaMLE
# from bayesian import muBayesian, sigmaBayesian
from moments import muMethodOfMoments, sigmaMethodOfMoments

PARAMETER_FUNCTIONS =   {
                            "Fixed Parameters": (muFixedParam, sigmaFixedParam),
                            "Capital Asset Pricing Model (CAPM)": (muCAPM, sigmaCAPM),
                            "Bootstrap (Common Volatility)" : (muBootstrap, sigma1Bootstrap),
                            "Bootstrap (Log Volatility)": (muBootstrap, sigma2Bootstrap),
                            "Method Of Moments" : (muMethodOfMoments, sigmaMethodOfMoments),
                        }

SIMULATION_SEED = None
def setSeed(seed = None):
    SIMULATION_SEED = seed
    if(SIMULATION_SEED is None):
        SIMULATION_SEED = np.random.randint(0,1000)
    np.random.seed(SIMULATION_SEED)
    print("Seed:", SIMULATION_SEED)

# Function to check if a date string is in the correct format (YYYY-MM-DD)
def is_valid_date(date_str):
    if date_str is None:
        return True
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to check if a date is in the past
def is_past_date(date_str):
    if date_str is None:
        return False
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return date < datetime.datetime.now().date()
    except ValueError:
        return False

# Function to check if a date is after another date
def is_after_date(date1_str, date2_str):
    if date1_str is None or date2_str is None:
        return False
    try:
        date1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d").date()
        return date1 > date2
    except ValueError:
        return False

# Function to check if a date is before another date
def is_before_date(date1_str, date2_str):
    if date1_str is None or date2_str is None:
        return True
    try:
        date1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d").date()
        return date1 < date2
    except ValueError:
        return False

# Functions For Simulating Based On Methods Compared To True Stock Value

def simulateSingleMethod(ticker, data_start_date, data_end_date, sim_end_date, method_name, stock_data = None):
    """
    Simulate a single method for stock price prediction.

    Args:
        ticker (str): Ticker symbol of the stock.
        data_start_date (str): Start date of historical data.
        data_end_date (str): End date of historical data.
        sim_end_date (str): End date of the simulation.
        method_name (str): Name of the simulation method.
        stock_data (StockData, optional): Object containing historical stock data. Defaults to None.

    Returns:
        dict: Dictionary containing simulation data.
    """
    if not is_valid_date(data_start_date) or not is_valid_date(data_end_date) or not is_valid_date(sim_end_date):
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD' format.")
    if(sim_end_date is None):
        raise ValueError("sim_end_date cannot be None")
    if(is_after_date(data_start_date, data_end_date)):
        raise ValueError("data_end_date must be after data_start_date")
    if(is_before_date(sim_end_date, data_end_date)):
        raise ValueError("sim_end_date must be after data_end_date")
    if(not is_past_date(sim_end_date)):
        raise ValueError("simulation must be of past dates to compare to true stock values")
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

def simulateManyStocks(tickers, data_start_date, data_end_date, sim_end_date):
    """
    Simulate multiple stocks using a single method.

    Args:
        tickers (list): List of stock ticker symbols.
        data_start_date (str): Start date of historical data.
        data_end_date (str): End date of historical data.
        sim_end_date (str): End date of the simulation.
        method_name (str): Name of the simulation method.

    Returns:
        list: List of dictionaries containing simulation data for each stock.
    """
    stock_data_list = []
    for ticker in tickers:
        simulation_data = simulateAllMethods(ticker, data_start_date, data_end_date, sim_end_date)
        stock_data_list.append(simulation_data)
    return stock_data_list


def compareManyStocks(tickers, data_start_date, data_end_date, sim_end_date):
    """
    Compare multiple stocks using a single method and averages the performance on the data set. 
    This function always uses the entire lifetime of the stock data for the simulation.
    This function also only compares the middle paths of the simulation.

    Args:
        stock_data_list (list): List of dictionaries containing stock data for each stock.

    Returns:
        None
    """
    stock_simulation_list = simulateManyStocks(tickers, data_start_date, data_end_date, sim_end_date)

    # Create a table for each stock
    analysis_dict = dict()
    for method in PARAMETER_FUNCTIONS.keys():
        analysis_dict[method] = [0,0,0]

    for simulation_data_list in stock_simulation_list:
        for simulation_data in simulation_data_list:
            # print(simulation_data)
            analysis = analyzeAll(simulation_data)
            meanA = analysis["Mean_Analysis"]
            medianA = analysis["Median_Analysis"]
            middleA = analysis["Middle_Analysis"]
            
            avgCC = np.mean([meanA[0][1], medianA[0][1],middleA[0][1]])
            avgMAPE = np.mean([meanA[1][1], medianA[1][1],middleA[1][1]])
            avgPI = np.mean([meanA[2][1], medianA[2][1],middleA[2][1]])

            analysis_dict[simulation_data["method_name"]][0] += avgCC
            analysis_dict[simulation_data["method_name"]][1] += avgMAPE
            analysis_dict[simulation_data["method_name"]][2] += avgPI


    for method in PARAMETER_FUNCTIONS.keys():
        analysis_dict[method][0] /= len(stock_simulation_list)
        analysis_dict[method][1] /= len(stock_simulation_list)
        analysis_dict[method][2] /= len(stock_simulation_list)
    
    myData = []
    for method in PARAMETER_FUNCTIONS.keys():
        myData.append([method, "Multiple Stocks", analysis_dict[method][0], analysis_dict[method][1], analysis_dict[method][2]])
    
    head = ["Method Name", "Analysis Group", "Correlation Coefficient", "MAPE", "Percentage Inliers"]
    table = tabulate(myData, headers=head, tablefmt="grid")

    print("\nAnalysis For Multiple Stocks With Tickers:", tickers)
    print(table)

        
def createTable(simulation_data_list, compact = False):
    """
    Create a table summarizing the analysis results for each simulation method.

    Args:
        simulation_data_list (list): List of dictionaries containing simulation data.
            Each dictionary should contain the following keys:
            - 'method_name' (str): Name of the simulation method.
            - 'simulation' (numpy.ndarray): Simulated stock prices.
            - 'mean_path' (numpy.ndarray): Mean stock prices.
            - 'median_path' (numpy.ndarray): Median stock prices.
            - 'middle_path' (numpy.ndarray): Middle stock prices.
            - 'true_stock_prices' (numpy.ndarray): True stock prices.
        compact (bool, optional): If True, only include analysis results for multiple paths. Defaults to False.

    Returns:
        str: String representation of the table.
    """
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

def simulateFutureSingle(ticker, data_start_date, sim_end_date, method_name, stock_data=None):
    """
    Simulate future stock prices from today using a specified method.

    Args:
        ticker (str): Ticker symbol of the stock.
        data_start_date (str): Start date for historical data.
        sim_end_date (str): End date for simulation.
        method_name (str): Name of the simulation method.
        stock_data (StockData, optional): Object containing historical stock data. Defaults to None.

    Returns:
        dict: Dictionary containing simulation data.
    """
    # Validate input dates
    if not is_valid_date(data_start_date) or not is_valid_date(sim_end_date):
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD' format.")

    if(sim_end_date is None):
        raise ValueError("sim_end_date cannot be None")

    if is_past_date(sim_end_date):
        raise ValueError("Simulation must be based on future stock prices")

    if is_after_date(data_start_date, sim_end_date):
        raise ValueError("Start date must be before simulation end date.")

    mu_function, sigma_function = PARAMETER_FUNCTIONS[method_name]
    if(stock_data is None):
        stock = StockData(ticker)
    else:
        stock = stock_data
    data = StockData(ticker, stock.getStockDataRange(data_start_date, None), stock.market_data_df)

    date_range = pd.date_range(start=data.end_date, end=sim_end_date, freq='B')  # 'B' stands for business days
    time = len(date_range) / 252

    simulation = simulate_stock_prices(data, mu_function, sigma_function, T=time, dt=1/252)

    # Extrapolate Single Paths
    middle = select_middle_path(simulation)
    median = compute_median_path(simulation)
    mean = compute_mean_path(simulation)

    simulation_data = {
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