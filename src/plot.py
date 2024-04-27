import matplotlib.pyplot as plt

def multi_SDE_plot(simulation_data):
    """
    Plots multiple simulated stock price paths.

    Args:
        simulation_data (dict): Dictionary containing simulation data.

    Returns:
        None
    """
    simulated_prices = simulation_data['simulation']
    ticker = simulation_data['true_stock_data'].ticker

    plt.figure(figsize=(10, 6))
    
    # Plot simulated stock prices
    for i in range(simulated_prices.shape[0]):
        plt.plot(simulated_prices[i], color='blue', alpha=0.5, label='Simulated Prices' if i == 0 else '')

    plt.title(f'Simulated Stock Prices {ticker}')
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

    Returns:
        None
    """
    simulated_prices = simulation_data['simulation']
    true_prices = simulation_data['true_stock_prices']
    ticker = simulation_data['true_stock_data'].ticker

    plt.figure(figsize=(10, 6))
    
    # Plot simulated stock prices
    for i in range(simulated_prices.shape[0]):
        plt.plot(simulated_prices[i], color='blue', alpha=0.5, label='Simulated Prices' if i == 0 else '')

    # Plot true stock prices
    plt.plot(true_prices, color='red', label='True Prices')
    
    plt.title(f'Simulated vs. True Stock Prices {ticker}')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_single_estimated_path(simulation_data):
    """
    Plots a single estimated stock price path compared to true stock prices.

    Args:
        simulation_data (dict): Dictionary containing simulation data.

    Returns:
        None
    """
    true_path = simulation_data['true_stock_prices']
    estimated_path = simulation_data['mean_path']
    ticker = simulation_data['true_stock_data'].ticker

    plt.figure(figsize=(10, 6))
    
    # Plot true stock prices
    plt.plot(true_path, color='red', label='True Prices')
    
    # Plot estimated stock prices
    plt.plot(estimated_path, color='blue', label='Estimated Prices')
    
    plt.title(f'Single Estimated Path vs. True Stock Prices {ticker}')
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

    Returns:
        None
    """
    true_prices = simulation_data['true_stock_prices']
    median_prices = simulation_data['median_path']
    middle_prices = simulation_data['middle_path']
    mean_prices = simulation_data['mean_path']
    ticker = simulation_data['true_stock_data'].ticker

    plt.figure(figsize=(10, 6))
    
    # Plot true stock prices
    plt.plot(true_prices, color='red', label='True Prices')
    # Plot median stock prices
    plt.plot(median_prices, color='blue', label='Median Prices')
    # Plot middle stock prices
    plt.plot(middle_prices, color='green', label='Middle Prices')
    # Plot mean stock prices
    plt.plot(mean_prices, color='orange', label='Mean Prices')
    
    plt.title(f'Comparison of True, Median, Middle, and Mean Stock Prices {ticker}')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()
