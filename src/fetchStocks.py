import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay

class StockData:
    # For now I am going to require that a start date and end date are required fields
    # If time permits I want to allow for adaptable parameters

    def __init__(self, ticker, stock_data_df = None, start_date = None, end_date = None):
        # Do some basic logic about checking if ticker, start, and end are valid
        # But for now let's assume they are all fine
        if(stock_data_df is None):
            self.stock_data_df = pd.DataFrame(self.__fetchDailyStockData(ticker, start_date, end_date))
        else:
            self.stock_data_df = stock_data_df

        self.start_date = datetime.strptime(self.stock_data_df.index[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.end_date = datetime.strptime(self.stock_data_df.index[-1].strftime('%Y-%m-%d'), '%Y-%m-%d')
        # self.end_date += BDay(1)

        self.market_data_df = pd.DataFrame(self.__fetchDailyStockData("^GSPC", self.start_date, self.end_date + BDay(1)))
        self.beta = self.__calcBeta(self.stock_data_df, self.market_data_df)

        # risk free rate is calculated typically using the bond price
        self.risk_free_rate = 0.2
        # market return is on average the return of the SP500 (I will only concern myself with stocks in this market)
        self.market_return = 0.8
        
    @classmethod
    def from_dataframe(cls, df):
        # Create a new instance of StockData class with data from the provided DataFrame
        instance = cls.__new__(cls)
        instance.stock_data_df = df
        instance.start_date = df.index[0]
        instance.end_date = df.index[-1]
        # Assuming that the market data for beta calculation is not available in this case
        instance.beta = None
        instance.risk_free_rate = None
        instance.market_return = None
        return instance

    def __fetchDailyStockData(self, ticker, start_date = None, end_date = None):
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
        # Calculate daily returns for stock and market
        stock_returns = stock_data['Adj Close'].pct_change()
        market_returns = market_data['Adj Close'].pct_change()

        # Remove NaN values
        stock_returns = stock_returns.dropna()
        market_returns = market_returns.dropna()

        # Perform linear regression to calculate beta
        beta = np.cov(stock_returns, market_returns)[0, 1] / np.var(market_returns)

        return beta
    
    def getClosingPrices(self):
        return self.stock_data_df['Close'].values
    
    # Assumes a valid date accessed
    def getAllForDate(self, date):
        return self.stock_data_df.loc[date]
    
    def getMostCurrentPrice(self):
        # Get the most recent date (last row of the DataFrame)
        most_recent_date = self.stock_data_df.index[-1]
    
        # Get the closing price for the most recent date
        return self.stock_data_df.loc[most_recent_date, 'Close']
    
    def getStockDataRange(self, start_date, end_date):
        # Convert None to the minimum and maximum dates available if not provided
        # if start_date is None:
        #     start_date = self.start_date
        # if end_date is None:
        #     end_date = self.end_date
        # # Allows for string or date input of dates
        # start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
        # end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
        # # Check if start_date and end_date are valid datetime objects
        # if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
        #     raise ValueError("start_date and end_date must be valid datetime objects")

        # Check if start_date is before end_date
        # if start_date > end_date:
        #     raise ValueError("start_date must be before end_date")

        # # Check if start_date and end_date are within the range of available data
        # if start_date < self.start_date:
        #     raise ValueError("start_date is before the available data range")
        # if end_date > self.end_date:
        #     raise ValueError("end_date is after the available data range")

        
        return self.stock_data_df[start_date:end_date]
    

# apple = StockData("AAPL")

# print(apple.getStockDataRange('2023-01-01', '2023-12-31'))

