from fetchStocks import StockData

def muFixedParam(stock: StockData, estimations, T, dt):
    return 0.08

def sigmaFixedParam(stock: StockData, estimations, T, dt):
    return 0.02