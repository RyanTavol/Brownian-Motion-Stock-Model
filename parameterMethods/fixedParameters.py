from fetchStocks import StockData

def muFixedParam(stock: StockData, estimations, T, dt):
    """
    Calculate the drift parameter (mu) for the Geometric Brownian Motion (GBM) model using a fixed parameter.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.

    Returns:
        float: Drift parameter (mu).
    """
    return 0.08

def sigmaFixedParam(stock: StockData, estimations, T, dt):
    """
    Calculate the volatility parameter (sigma) for the Geometric Brownian Motion (GBM) model using a fixed parameter.

    Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.

    Returns:
        float: Volatility parameter (sigma).
    """
    return 0.1