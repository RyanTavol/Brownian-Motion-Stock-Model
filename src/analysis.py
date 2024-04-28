import numpy as np

def correlation_coefficient(true_prices, simulated_prices):
    """
    Calculate the correlation coefficient (r) between true and simulated prices.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices (numpy.ndarray): Simulated stock prices.

    Returns:
        r (float): Correlation coefficient between true and simulated prices.
    """
    n = len(true_prices)
    sum_xy = np.sum(true_prices * simulated_prices)
    sum_x = np.sum(true_prices)
    sum_y = np.sum(simulated_prices)
    sum_x_squared = np.sum(true_prices ** 2)
    sum_y_squared = np.sum(simulated_prices ** 2)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = np.sqrt((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2))

    r = numerator / denominator

    return r

def correlation_coefficient_multi(true_prices, simulated_prices_multi):
    """
    Calculate the correlation coefficient (r) between true and simulated prices for multiple paths.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices_multi (numpy.ndarray): Simulated stock prices for multiple paths (shape: num_paths x num_steps).

    Returns:
        r (float): Correlation coefficient between true and simulated prices.
    """
    num_paths, num_steps = simulated_prices_multi.shape
    correlations = np.zeros(num_paths)

    for i in range(num_paths):
        correlations[i] = np.corrcoef(true_prices, simulated_prices_multi[i])[0, 1]

    r = np.mean(correlations)

    return r

def mean_absolute_percentage_error(true_prices, simulated_prices):
    """
    Calculate the mean absolute percentage error (MAPE) between true and simulated prices.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices (numpy.ndarray): Simulated stock prices.

    Returns:
        mape (float): Mean absolute percentage error between true and simulated prices.
    """
    n = len(true_prices)
    absolute_percentage_errors = np.abs((true_prices - simulated_prices) / true_prices)
    mape = np.sum(absolute_percentage_errors) / n

    return mape

def mean_absolute_percentage_error_multi(true_prices, simulated_prices_multi):
    """
    Calculate the mean absolute percentage error (MAPE) between true and simulated prices for multiple paths.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices_multi (numpy.ndarray): Simulated stock prices for multiple paths (shape: num_paths x num_steps).

    Returns:
        mape (float): Mean absolute percentage error between true and simulated prices.
    """
    num_paths, num_steps = simulated_prices_multi.shape
    absolute_percentage_errors = np.zeros((num_paths, num_steps))

    for i in range(num_paths):
        absolute_percentage_errors[i] = np.abs((true_prices - simulated_prices_multi[i]) / true_prices)

    mape = np.mean(absolute_percentage_errors)

    return mape

def percentage_of_correct_predictions(true_prices, simulated_prices, threshold=0.1):
    """
    Calculate the percentage of correct predictions within a threshold.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices (numpy.ndarray): Simulated stock prices.
        threshold (float): Threshold for considering predictions correct.

    Returns:
        percentage (float): Percentage of correct predictions within the threshold.
    """
    absolute_errors = np.abs(true_prices - simulated_prices)
    correct_predictions = absolute_errors <= threshold
    percentage = np.mean(correct_predictions) * 100

    return percentage

def percentage_of_correct_predictions_multi(true_prices, simulated_prices_multi, threshold=0.1):
    """
    Calculate the percentage of correct predictions within a threshold for multiple simulated paths.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices_multi (numpy.ndarray): Simulated stock prices for multiple paths (shape: num_paths x num_steps).
        threshold (float): Threshold for considering predictions correct.

    Returns:
        percentage (float): Percentage of correct predictions within the threshold.
    """
    num_paths, num_steps = simulated_prices_multi.shape
    correct_predictions = np.zeros(num_steps)

    for i in range(num_steps):
        absolute_errors = np.abs(true_prices[i] - simulated_prices_multi[:, i])
        correct_predictions[i] = np.mean(absolute_errors <= threshold)

    percentage = np.mean(correct_predictions) * 100

    return percentage

def analyzeAllSingle(true_prices, simulated_prices):
    """
    Analyzes single method simulations against true stock prices.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices (numpy.ndarray): Simulated stock prices.

    Returns:
        list: A list of tuples containing analysis results for each metric.
            Each tuple contains the name of the metric and its corresponding value.
    """
    results = \
            [ \
               ("Correlation Coefficient", correlation_coefficient(true_prices, simulated_prices)),
               ("MAPE", mean_absolute_percentage_error(true_prices, simulated_prices)),
               ("Percentage Inliers", percentage_of_correct_predictions(true_prices, simulated_prices))
            ]
    return results

def analyzeAllMulti(true_prices, simulated_prices_multi): 
    """
    Analyzes multi-method simulations against true stock prices.

    Args:
        true_prices (numpy.ndarray): True stock prices.
        simulated_prices_multi (numpy.ndarray): Simulated stock prices for multiple methods.

    Returns:
        list: A list of tuples containing analysis results for each metric.
            Each tuple contains the name of the metric and its corresponding value.
    """
    results = \
            [ \
               ("Correlation Coefficient", correlation_coefficient_multi(true_prices, simulated_prices_multi)),
               ("MAPE", mean_absolute_percentage_error_multi(true_prices, simulated_prices_multi)),
               ("Percentage Inliers", percentage_of_correct_predictions_multi(true_prices, simulated_prices_multi))
            ]
    return results

# Consider Improving This Function To Display It Nicer Or In A Better Format:
def analyzeAll(simulation_data):
    """
    Analyzes simulation results for all methods.

    Args:
        simulation_data (dict): Dictionary containing simulation data.

    Returns:
        dict: A dictionary containing analysis results for each method.
            Each key corresponds to a method name, and each value is a list of tuples
            containing analysis results for that method.
    """
    trueStockPrices = simulation_data['true_stock_prices']
    return {
        "Multi_Analysis" : analyzeAllMulti(trueStockPrices, simulation_data['simulation']),
        "Mean_Analysis" : analyzeAllSingle(trueStockPrices, simulation_data['mean_path']),
        "Median_Analysis" : analyzeAllSingle(trueStockPrices, simulation_data['median_path']),
        "Middle_Analysis" : analyzeAllSingle(trueStockPrices, simulation_data['middle_path']),
    }



