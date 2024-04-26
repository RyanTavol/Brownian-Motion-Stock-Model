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
        correct_predictions[i] = np.mean(absolute_errors <= threshold) * 100

    percentage = np.mean(correct_predictions)

    return percentage
