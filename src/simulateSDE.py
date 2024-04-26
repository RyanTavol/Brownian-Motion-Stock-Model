import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from fetchStocks import StockData

def simulate_stock_prices(stock_history: StockData, mu_function, sigma_function, T = 1, dt = 1/250, num_paths = 10):
    """
    Simulates future stock prices using the Geometric Brownian Motion (GBM) model.

    Args:
        stock_history (StockData): Object containing historical stock data.
        mu_function (function): Function to compute the drift parameter (mu) for the GBM model.
        sigma_function (function): Function to compute the volatility parameter (sigma) for the GBM model.
        T (float): Time horizon (in years) for simulation. Default is 1.
        dt (float): Time step (in years) for simulation. Default is 1/250 (1 trading day).
        num_paths (int): Number of paths to simulate. Default is 10.

    Returns:
        numpy.ndarray: Matrix describing the multiple paths.
    """
    # Initialize arrays to store stock prices
    prices = np.zeros((num_paths, int(T/dt)+1))
    
    # Iterate over each path
    for i in range(num_paths):
        # Initialize stock price at time 0
        prices[i, 0] = stock_history.getMostCurrentPrice()
        
        # Generate future stock prices using GBM
        for j in range(1, int(T/dt)+1):
            # Generate random increments (Brownian motion)
            dW = np.random.normal(0, np.sqrt(dt))
            # Update stock price using GBM formula
            mu = mu_function(stock_history, prices, T, dt)
            sigma = sigma_function(stock_history, prices, T, dt)
            prices[i, j] = prices[i, j-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * dW)
    
    return prices

def compute_cumulative_distance(simulated_paths):
    """
    Computes the cumulative distance to all other paths for each path.

    Args:
        simulated_paths (numpy.ndarray): Matrix containing simulated stock prices.

    Returns:
        numpy.ndarray: Array containing cumulative distances.
    """
    num_paths = len(simulated_paths)
    cumulative_distances = np.zeros(num_paths)
    
    for i in range(num_paths):
        cumulative_distance = 0
        for j in range(num_paths):
            if i != j:
                # Compute Euclidean distance between paths i and j
                distance = np.linalg.norm(simulated_paths[i] - simulated_paths[j])
                cumulative_distance += distance
        cumulative_distances[i] = cumulative_distance
    
    return cumulative_distances

def select_middle_path(simulated_paths):
    """
    Selects the path with the smallest cumulative distance.

    Args:
        simulated_paths (numpy.ndarray): Matrix containing simulated stock prices.

    Returns:
        numpy.ndarray: The middle path.
    """
    cumulative_distances = compute_cumulative_distance(simulated_paths)
    middle_path_index = np.argmin(cumulative_distances)
    middle_path = simulated_paths[middle_path_index]
    return middle_path

def compute_median_path(simulated_paths):
    """
    Computes the median path from simulated paths.

    Args:
        simulated_paths (numpy.ndarray): Matrix containing simulated stock prices.

    Returns:
        numpy.ndarray: Median path.
    """
    num_paths, num_steps = simulated_paths.shape
    median_path = np.zeros(num_steps)
    
    for i in range(num_steps):
        # Extract prices at time step i from all paths
        prices_at_step_i = simulated_paths[:, i]
        # Compute median price at time step i
        median_price = np.median(prices_at_step_i)
        # Store median price in median path
        median_path[i] = median_price
    
    return median_path

# Function to compute the mean path from simulated prices
def compute_mean_path(simulated_prices):
    return np.mean(simulated_prices, axis=0)