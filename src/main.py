
import numpy as np
from mainHelpers import *

print("Running Main:")

FIXEDPARAM = "Fixed Parameters"
CAPM = "Capital Asset Pricing Model (CAPM)"
BOOTSTRAP_CV = "Bootstrap (Common Volatility)"
BOOTSTRAP_LV = "Bootstrap (Log Volatility)"

# Main Function For Interactability
# Please Feel Free To Change The Code In Main To Test Whatever You Would Like
# Make Sure You Only Use The Function

if __name__=='__main__':
    setSeed()  

    stockTicker = "IBM"
    dataStart = None
    dataEnd = "2023-01-01"
    simEnd = "2025-01-01"
    muFunc = muBootstrap
    sigmaFunc = sigma1Bootstrap
    methodName = "Bootstrap (Common Volatility)"


    # simulation_data_all = simulateAllMethods(stockTicker, dataStart, dataEnd, simEnd)
    # compareMultipleMethods(simulation_data_all, compact = True, plot = True)

    # data = simulateSingleMethod(stockTicker, dataStart, dataEnd, simEnd, BOOTSTRAP_LV)
    # compareSingle(data)

    sim = simulateFutureSingle(stockTicker, None, simEnd, FIXEDPARAM)
    plotSingleFuture(sim)

    # sim = simulateFutureAllMethods(stockTicker, None, simEnd)
    # plotMultipleFuture(sim)