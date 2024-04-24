import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class StockData:
    # For now I am going to require that a start date and end date are required fields
    # If time permits I want to allow for adaptable parameters

    def __init__(self, ticker, start_date = None, end_date = None):
        # Do some basic logic about checking if ticker, start, and end are valid
        # But for now let's assume they are all fine
        self.stock_data_df = pd.DataFrame(self.__fetchDailyStockData(ticker, start_date, end_date))
        self.start_date = start_date

        self.start_date = start_date
        self.end_date = end_date
        
        # self.start_date = datetime.strptime(self.stock_data_df.index[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
        # self.end_date = datetime.strptime(self.stock_data_df.index[-1].strftime('%Y-%m-%d'), '%Y-%m-%d')

        # self.end_date += timedelta(days=1)

        self.market_data_df = pd.DataFrame(self.__fetchDailyStockData("^GSPC", self.start_date, self.end_date))
        self.beta = self.__calcBeta(self.stock_data_df, self.market_data_df)

        # risk free rate is calculated typically using the bond price
        # market return is on average the return of the SP500 (I will only concern myself with stocks in this market)
        self.risk_free_rate = 0.2
        self.market_return = 0.8
        

    def __fetchDailyStockData(self, ticker, start_date = None, end_date = None):
        if(start_date != None and end_date != None):
            return yf.download(ticker, start_date, end_date)
        if(start_date != None and end_date == None):
            return yf.download(ticker, start = start_date)
        if(start_date == None and end_date != None):
            return yf.download(ticker, end = end_date)
        
        # Returns the entire history of stock data
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

apple = StockData("AAPL", '2023-01-01', '2023-12-31')
print(apple.stock_data_df)
print(apple.getAllForDate("2023-01-05"))