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



# Walk-through


## Start
Prerequisites and set-up

### Config
In your directory you must have config file ('my_keys.config') with:


['gemini']

key = your-api-key

secret_key = your-secret-api-key



### Import and Initialize
import pyalgogem as pag

-Initialize algorithm environment object to house code

ae = pag.AlgorithmEnvironment()

### Set up parameters

-Select ae.symbol ('BTC'/'ETH') and ae.window ('D'/'H'/'M' - daily/hour/minute)

ae.symbol = 'ETH'; ae.window = 'D' 

## Data
Retrieving and saving historical data from CryptoCompare
### Load historical data
-Update historical data for symbol and window combination and read into memory

--Can pass datetime objects for start/end of timeslice

ae.update_all_historical()

### Read data into Dataset object

ae.read_stored_data()

Now, dataset object (ae.dataset) created to house data

## Backtest
Testing hypotheses and training Machine Learning models on historical data
### Log-returns
-Add log-returns of close-price to sample data
ae.dataset.add_log_returns()

### Lags
-Add lags of log-returns to sample data
ae.dataset.set_return_lags(15)
