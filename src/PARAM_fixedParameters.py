from SRC_fetchStocks import StockData

def muFixedParam(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Calculate the drift parameter (mu) for the Geometric Brownian Motion (GBM) model using a fixed parameter.

     Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating
        futureTimeIndex (int): Index for how far along the estimation we are

    Returns:
        float: Drift parameter (mu).
    """
    return 0.08

def sigmaFixedParam(stock: StockData, estimations, T, dt, pathIndex, futureTimeIndex):
    """
    Calculate the volatility parameter (sigma) for the Geometric Brownian Motion (GBM) model using a fixed parameter.

     Args:
        stock (StockData): Object containing historical stock data.
        estimations: Not used in this function.
        T (float): Time horizon (in years) for simulation.
        dt (float): Time step (in years) for simulation.
        pathIndex (int): Index for the current path estimating
        futureTimeIndex (int): Index for how far along the estimation we are

    Returns:
        float: Volatility parameter (sigma).
    """
    return 0.2