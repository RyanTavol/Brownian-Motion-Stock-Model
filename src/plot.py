import matplotlib.pyplot as plt

def multi_SDE_plot(simulation_data):
    """
    Plots multiple simulated stock price paths.

    Args:
        simulation_data (dict): Dictionary containing simulation data.
            It should contain the following keys:
            - 'simulation': Matrix containing simulated stock prices.
            - 'true_stock_data' (StockData): Object containing historical stock data.
            - 'true_stock_prices' (numpy.ndarray): True stock prices.
            - 'ticker' (str): Ticker symbol of the stock.

    Returns:
        None
    """
    simulated_prices = simulation_data['simulation']
    ticker = simulation_data['true_stock_data'].ticker
    method_name = simulation_data['method_name']

    plt.figure(figsize=(10, 6))
    
    # Plot simulated stock prices
    for i in range(simulated_prices.shape[0]):
        plt.plot(simulated_prices[i], color='blue', alpha=0.5, label='Simulated Prices' if i == 0 else '')

    plt.title(f'{method_name} -\nSimulated Stock Prices {ticker}')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def dual_multi_SDE_plot(simulation_data):
    """
    Plots multiple simulated stock price paths compared to true stock prices.

    Args:
        simulation_data (dict): Dictionary containing simulation data.
            It should contain the following keys:
            - 'simulation': Matrix containing simulated stock prices.
            - 'true_stock_prices' (numpy.ndarray): True stock prices.
            - 'true_stock_data' (StockData): Object containing historical stock data.
            - 'ticker' (str): Ticker symbol of the stock.

    Returns:
        None
    """
    simulated_prices = simulation_data['simulation']
    true_prices = simulation_data['true_stock_prices']
    ticker = simulation_data['true_stock_data'].ticker
    method_name = simulation_data['method_name']

    plt.figure(figsize=(10, 6))
    
    # Plot simulated stock prices
    for i in range(simulated_prices.shape[0]):
        plt.plot(simulated_prices[i], color='blue', alpha=0.5, label='Simulated Prices' if i == 0 else '')

    # Plot true stock prices
    plt.plot(true_prices, color='red', label='True Prices')
    
    plt.title(f'{method_name} -\nSimulated vs. True Stock Prices {ticker}')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_comparison_mid(simulation_data):
    """
    Plots a comparison of true, median, middle, and mean stock prices.

    Args:
        simulation_data (dict): Dictionary containing simulation data.
            It should contain the following keys:
            - 'true_stock_prices' (numpy.ndarray): True stock prices.
            - 'median_path' (numpy.ndarray): Median stock prices.
            - 'middle_path' (numpy.ndarray): Middle stock prices.
            - 'mean_path' (numpy.ndarray): Mean stock prices.
            - 'true_stock_data' (StockData): Object containing historical stock data.
            - 'ticker' (str): Ticker symbol of the stock.

    Returns:
        None
    """
    true_prices = simulation_data['true_stock_prices']
    median_prices = simulation_data['median_path']
    middle_prices = simulation_data['middle_path']
    mean_prices = simulation_data['mean_path']
    ticker = simulation_data['true_stock_data'].ticker
    method_name = simulation_data['method_name']

    plt.figure(figsize=(10, 6))
    
    # Plot true stock prices
    plt.plot(true_prices, color='red', label='True Prices')
    # Plot median stock prices
    plt.plot(median_prices, color='blue', label='Median Prices')
    # Plot middle stock prices
    plt.plot(middle_prices, color='green', label='Middle Prices')
    # Plot mean stock prices
    plt.plot(mean_prices, color='orange', label='Mean Prices')
    
    plt.title(f'{method_name} -\nSingle Path Estimation vs. True Stock Prices {ticker}')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def combined_plot_comparison(simulation_data):
    """
    Creates a combined plot showing multiple simulated stock price paths compared to true stock values 
    and the comparison of true, median, middle, and mean stock prices. This function creates two subplots.
    The left plot is the same as the plot created by dual_multi_SDE_plot and the plot on the right is the
    one created by plot_comparison_mid.

    Args:
        simulation_data (dict): Dictionary containing simulation data.
            It should contain the following keys:
            - 'simulation': Matrix containing simulated stock prices.
            - 'true_stock_prices' (numpy.ndarray): True stock prices.
            - 'true_stock_data' (StockData): Object containing historical stock data.
            - 'median_path' (numpy.ndarray): Median stock prices.
            - 'middle_path' (numpy.ndarray): Middle stock prices.
            - 'mean_path' (numpy.ndarray): Mean stock prices.
            - 'ticker' (str): Ticker symbol of the stock.

    Returns:
        None
    """
    simulated_prices = simulation_data['simulation']
    true_prices = simulation_data['true_stock_prices']
    median_prices = simulation_data['median_path']
    middle_prices = simulation_data['middle_path']
    mean_prices = simulation_data['mean_path']
    ticker = simulation_data['true_stock_data'].ticker
    method_name = simulation_data['method_name']

    # Get the date range for the simulation
    dates = simulation_data['true_stock_data'].market_data_df.index

    plt.figure(figsize=(16, 6))

    # Plot simulated stock prices
    plt.subplot(1, 2, 1)
    for i in range(simulated_prices.shape[0]):
        plt.plot(dates, simulated_prices[i], color='blue', alpha=0.5, label='Simulated Prices' if i == 0 else '')
    plt.plot(dates, true_prices, color='red', label='True Prices')
    plt.title(f'{method_name} -\nSimulated vs. True Stock Prices {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    # Plot comparison of true, median, middle, and mean stock prices
    plt.subplot(1, 2, 2)
    plt.plot(dates, true_prices, color='red', label='True Prices')
    plt.plot(dates, median_prices, color='blue', label='Median Prices')
    plt.plot(dates, middle_prices, color='green', label='Middle Prices')
    plt.plot(dates, mean_prices, color='orange', label='Mean Prices')
    plt.title(f'{method_name} -\nSingle Path Estimation vs. True Stock Prices {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()