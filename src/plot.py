import matplotlib.pyplot as plt
# This file has all the functions responsible for plotting my results


# Plotting with multiple SDE estimations only
def multi_SDE_plot(simulated_prices, ticker):
    """
    Plots multiple simulated stock price paths.

    Args:
        simulated_prices (numpy.ndarray): Matrix containing simulated stock prices.
        ticker (str): Ticker symbol of the stock.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    
    # Plot simulated stock prices
    for i in range(simulated_prices.shape[0]):
        plt.plot(simulated_prices[i], color='blue', alpha=0.5, label='Simulated Prices' if i == 0 else '')
    # plt.plot(simulated_prices[0], color='blue', alpha=0.5, label='Simulated Prices')
    # Plot true stock prices
    
    plt.title(f'Simulated Stock Prices {ticker}')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotting with multiple SDE estimations compared to true stock value
def dual_multi_SDE_plot(simulated_prices, true_prices, ticker):
    """
    Plots multiple simulated stock price paths compared to true stock prices.

    Args:
        simulated_prices (numpy.ndarray): Matrix containing simulated stock prices.
        true_prices (numpy.ndarray): True stock prices.
        ticker (str): Ticker symbol of the stock.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    
    # Plot simulated stock prices
    for i in range(simulated_prices.shape[0]):
        plt.plot(simulated_prices[i], color='blue', alpha=0.5, label='Simulated Prices' if i == 0 else '')
    # plt.plot(simulated_prices[0], color='blue', alpha=0.5, label='Simulated Prices')
    # Plot true stock prices
    plt.plot(true_prices, color='red', label='True Prices')
    
    plt.title(f'Simulated vs. True Stock Prices {ticker}')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotting single aggregate SDE estimation compared to true stock value
def plot_single_estimated_path(true_path, estimated_path, ticker):
    """
    Plots a single estimated stock price path compared to true stock prices.

    Args:
        true_path (numpy.ndarray): True stock prices.
        estimated_path (numpy.ndarray): Estimated stock prices.
        ticker (str): Ticker symbol of the stock.

    Returns:
        None
    """
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

# Plotting function to compare true stock price, median stock price, and middle stock price
def plot_comparison_mid(true_prices, median_prices, middle_prices, mean_prices, ticker):
    """
    Plots a comparison of true, median, middle, and mean stock prices.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        median_prices (numpy.ndarray): Median stock prices.
        middle_prices (numpy.ndarray): Middle stock prices.
        mean_prices (numpy.ndarray): Mean stock prices.

    Returns:
        None
    """
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

# Plotting Other Error Metrics