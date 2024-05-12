from mainHelpers import *

FIXEDPARAM = "Fixed Parameters"
CAPM = "Capital Asset Pricing Model (CAPM)"
BOOTSTRAP_CV = "Bootstrap (Common Volatility)"
BOOTSTRAP_LV = "Bootstrap (Log Volatility)"
METHOD_OF_MOMENTS = "Method Of Moments"

# Main Function For Interactability
# Please Feel Free To Change The Code In Main To Test Whatever You Would Like
# Please See mainHelpers.py for functions that you can call

if __name__=='__main__':
    print("Running Main:")

    # Feel Free To Set The Seed With An Integer Of Your Choice
    setSeed()  

    """
    Below are a number of variables that you can change in order to test this code however you would like.

    Please read the comments above each variable to understand how to use the variables and what will be
    acceptable versus what will safely throw and error. If you give an invalid value, you will (hopefully)
    be returned with a helpful and descriptive ValueError thrown in the terminal.

    If you want to change what functions you want to interact with, see the other block comment down below.
    """
    

    # Must be a valid Stock Ticker In The SP500
    stockTicker = "IBM"

    # Must be a list of valid Stock Tickers In The SP500
    stockList = ["IBM", "AAPL"]

    # Must be a valid date in the past to fetch the stock data from that point on
    # If dataStart is None, then the start date will be the very first date of this stock
    dataStart = None

    # Must be a valid date in the past to fetch the stock data from that point on
    # If dataEnd is None, then the end date will be the last business trading day
    dataEnd = "2023-01-01"

    # Must be a valid date greater than dataEnd. It cannot be None
    # If you want to use one of the simulate and compare functions, this must be a past date
        # So that the simulation can be compared to the true stock data
    # If you want to use one of the future simulation functions, this must be a future date
    simEnd = "2024-01-01"

    # Must be one of the constant variables above.
    # Determines which parameter finding method you want to test (if you are only testing 1)
    methodName = BOOTSTRAP_CV

    """
    Below are a number of different functions that you can comment or uncomment to test this code however
    you would like.

    Please read the comments above each function to understand how to use it and if there is any other important
    information to know. If any of your above variables are invalid, like I said earlier it will safely throw a 
    ValueError. For more information about the variables, please see the above block comment.

    If the comments below are not descriptive enough, please feel free to take a look inside of 'mainHelpers.py'
    which includes all of the functions you are able to interact with inside of main. Inside there each function
    is implemented, but also has a good description of it via their doc comments. 

    It is not recommended that you change any of the code below other than commenting/uncommenting certain lines.
    I intentionally tried my best to offer as much functionality as possible to do whatever you want. It is recommended
    also that you uncomment both (or more if there are more) lines under each comment. If you do choose to change the 
    code in here at all, please make sure you read the documentation inside 'mainHelpers.py' so you understand how to use it
    """


    # The following code is used to simulate a single parameter estimation method and compare it to real-life stock data
    # compareSingle has some additional optional parameters if you want to include/exclude the analysis data and the plotting 
    # as well as if you want the analysis data to be compact or not.
    # default values: analyze = True, plot = True, compact = False

    # singleSim = simulateSingleMethod(stockTicker, dataStart, dataEnd, simEnd, methodName)
    # compareSingle(singleSim)    



    # The following code is used to simulate all the parameter estimation methods and compare them to real-life stock data
    # compareMultiple has some additional optional parameters if you want to include/exclude the analysis data and the plotting
    # as well as if you want the analysis data to be compact or not. I recommend compact = True for this thought.
    # default values: analyze = True, plot = True, compact = False

    # allSims = simulateAllMethods(stockTicker, dataStart, dataEnd, simEnd)
    # compareMultipleMethods(allSims, compact=True)



    # The following code is used to simulate a single parameter estimation method for the future and plot it.

    # singleFutureSim = simulateFutureSingle(stockTicker, dataStart, simEnd, methodName)
    # plotSingleFuture(singleFutureSim)



    # The following code is used to simulate all the parameter estimation methods for the future and plot them.

    # allFutureSims = simulateFutureAllMethods(stockTicker, dataStart, simEnd)
    # plotMultipleFuture(allFutureSims)



    # The following code is used to compare a all parameter estimation methods for a list of stocks and aggregate results
    compareManyStocks(stockList, dataStart, dataEnd, simEnd)
    