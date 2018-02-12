# PyAlgoGem

## Wrapper class for Gemini exchange for Cryptocurrencies (BTC & ETH).


### Data:

Store and read locally saved price data.

-Pull daily/hourly/minute price data using CryptoCompare API

-Store data locally in HDF5 (.h5) file for easy retrieval

### Backtest:

Backtest strategies on historical data.

-Easily add log-returns to dataset and create lags derived from returns

-Create SMA, momentum, or mean-reverting trade signals

### Deployment:

Deploy strategies to real-time trading.

-Get Gemini account information and place orders via API

-Connect to exchange using WebSocket API for live updates and monitoring

### Performance:

Monitor performance of an algorithm as it is live-traded.



# Start

import pyalgogem as pag

-Initialize algorithm environment object to house code

ae = pag.AlgorithmEnvironment()
