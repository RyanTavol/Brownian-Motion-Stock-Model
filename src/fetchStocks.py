import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay

class StockData:
    """
    Class representing stock data, providing methods for fetching and analyzing stock data.

    Attributes:
        ticker (str): Ticker symbol of the stock.
        stock_data_df (pandas.DataFrame): DataFrame containing historical stock data.
        start_date (datetime): Start date of the stock data.
        end_date (datetime): End date of the stock data.
        market_data_df (pandas.DataFrame): DataFrame containing historical market data.
        beta (float): Beta value calculated for the stock.
        risk_free_rate (float): Risk-free rate of return.
        market_return (float): Expected return of the market portfolio.

    Methods:
        __init__: Initializes a StockData object.
        from_dataframe: Creates a StockData object from an existing DataFrame.
        __fetchDailyStockData: Fetches daily stock data from Yahoo Finance.
        __calcBeta: Calculates the beta value of the stock.
        calcBetaDateRange: Calculates beta value for a specified date range.
        getClosingPrices: Returns an array of closing prices.
        getAllForDate: Returns stock data for a specific date.
        getMostCurrentPrice: Returns the most recent closing price.
        getStockDataRange: Returns stock data for a specified date range.
    """

    def __init__(self, ticker, stock_data_df = None, start_date = None, end_date = None):
        """
        Initializes a StockData object.

        Args:
            ticker (str): Ticker symbol of the stock.
            stock_data_df (pandas.DataFrame): DataFrame containing historical stock data.
            start_date (datetime): Start date of the stock data.
            end_date (datetime): End date of the stock data.

        Returns:
            None
        """
        # Do some basic logic about checking if ticker, start, and end are valid
        # But for now let's assume they are all fine
        if(stock_data_df is None):
            self.stock_data_df = pd.DataFrame(self.__fetchDailyStockData(ticker, start_date, end_date))
        else:
            self.stock_data_df = stock_data_df

        self.start_date = datetime.strptime(self.stock_data_df.index[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.end_date = datetime.strptime(self.stock_data_df.index[-1].strftime('%Y-%m-%d'), '%Y-%m-%d')

        self.market_data_df = pd.DataFrame(self.__fetchDailyStockData("^GSPC", self.start_date, self.end_date + BDay(1)))
        self.beta = self.__calcBeta(self.stock_data_df, self.market_data_df)

        # risk free rate is calculated typically using the bond price
        self.risk_free_rate = 0.05
        # market return is on average the return of the SP500 (I will only concern myself with stocks in this market)
        self.market_return = 0.10

    def __fetchDailyStockData(self, ticker, start_date = None, end_date = None):
        """
        Fetches daily stock data from Yahoo Finance.

        Args:
            ticker (str): Ticker symbol of the stock.
            start_date (datetime): Start date for fetching data.
            end_date (datetime): End date for fetching data.

        Returns:
            stock_data_df (pandas.DataFrame): DataFrame containing daily stock data.
        """
        print(f"Fetching Stock Data For {ticker}")
        if start_date and end_date:
            return yf.download(ticker, start=start_date, end=end_date)
        elif start_date:
            return yf.download(ticker, start=start_date)
        elif end_date:
            return yf.download(ticker, end=end_date)
        else:
            return yf.download(ticker)
    
    def __calcBeta(self, stock_data, market_data):
        """
        Calculates the beta value of the stock.

        Args:
            stock_data (pandas.DataFrame): DataFrame containing stock data.
            market_data (pandas.DataFrame): DataFrame containing market data.

        Returns:
            beta (float): Beta value of the stock.
        """
        # Calculate daily returns for stock and market
        stock_returns = stock_data['Adj Close'].pct_change()
        market_returns = market_data['Adj Close'].pct_change()

        # Remove NaN values
        stock_returns = stock_returns.dropna()
        market_returns = market_returns.dropna()

        # Perform linear regression to calculate beta
        beta = np.cov(stock_returns, market_returns)[0, 1] / np.var(market_returns)

        return beta

    def calcBetaDateRange(self, start_date=None, end_date=None):
        """
        Calculates beta value for a specified date range.

        Args:
            start_date (datetime): Start date for calculating beta.
            end_date (datetime): End date for calculating beta.

        Returns:
            beta (float): Beta value of the stock.
        """
        # Filter stock data for the specified range of dates
        stock_data_filtered = self.getStockDataRange(start_date, end_date)
        
        # Filter market returns for the same date range as stock data
        market_data_filtered = self.market_data_df[start_date:end_date]
        
        # Calculate daily returns for stock and market
        stock_returns = stock_data_filtered['Adj Close'].pct_change().dropna()
        market_returns = market_data_filtered['Adj Close'].pct_change().dropna()
        
        # Perform linear regression to calculate beta
        beta = np.cov(stock_returns, market_returns)[0, 1] / np.var(market_returns)
        
        return beta

    def getClosingPrices(self):
        """
        Returns an array of closing prices.

        Returns:
            prices (numpy.ndarray): Array of closing prices.
        """
        return self.stock_data_df['Close'].values
    
    # Assumes a valid date accessed
    def getAllForDate(self, date):
        """
        Returns stock data for a specific date.

        Args:
            date (datetime): Date for which to retrieve stock data.

        Returns:
            stock_data (pandas.Series): Stock data for the specified date.
        """
        return self.stock_data_df.loc[date]
    
    def getMostCurrentPrice(self):
        """
        Returns the most recent closing price.

        Returns:
            price (float): Most recent closing price.
        """
        # Get the most recent date (last row of the DataFrame)
        most_recent_date = self.stock_data_df.index[-1]
    
        # Get the closing price for the most recent date
        return self.stock_data_df.loc[most_recent_date, 'Close']
    
    def getStockDataRange(self, start_date, end_date):
        """
        Returns stock data for a specified date range.

        Args:
            start_date (datetime): Start date of the range.
            end_date (datetime): End date of the range.

        Returns:
            stock_data (pandas.DataFrame): DataFrame containing stock data for the specified range.
        """
        # TODO Add error handling
        return self.stock_data_df[start_date:end_date]