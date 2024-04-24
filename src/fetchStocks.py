import yfinance as yf

def get_stock_history(ticker):
    """
    Function to retrieve entire historical stock data for a given ticker symbol.

    Parameters:
    ticker (str): The ticker symbol of the stock.

    Returns:
    pandas.DataFrame: DataFrame containing historical stock data.
    """
    # Fetch historical data using yfinance
    stock_data = yf.download(ticker)
    
    return stock_data

# Example usage:
ticker_symbol = 'AAPL'  # Example ticker symbol

# Fetch entire historical data for the given ticker
stock_history = get_stock_history(ticker_symbol)

print(stock_history)  # Display the first few rows of the historical data
