import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from fetchStocks import StockData

# Function to simulate future stock prices using the GBM model
"""
Function to simulate future stock prices using the GBM model. 
Uses the precise solution to the SDE, not an approximated solution
Has adaptable parameter functionality

stock_history:      a list of stock data as described in fetchStocks
mu_function:        a function with parameters (...) that returns a valid mu parameter
sigma_function:     a function with parameters (...) that returns a valid mu parameter
T:                  an integer describing the time (in years) that you want to simulate
dt:                 a float describing the time-step (typically 1/250) (1 trading day)
num_paths:          an integer the number of paths simulated

return:             a matrix describing the multiple paths 
"""
def simulate_stock_prices(stock_history: StockData, mu_function, sigma_function, T = 1, dt = 1/250, num_paths = 10):
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

# Function to compute cumulative distance to all other paths for each path
def compute_cumulative_distance(simulated_paths):
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

# Function to select the path with the smallest cumulative distance
def select_middle_path(simulated_paths):
    cumulative_distances = compute_cumulative_distance(simulated_paths)
    middle_path_index = np.argmin(cumulative_distances)
    middle_path = simulated_paths[middle_path_index]
    return middle_path

# Function to compute the median path from simulated paths
def compute_median_path(simulated_paths):
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