#
# PyAlgo Project
# base/
#
# main module containing AlgorithmEnvironment object
#
# Andrew Edmonds - 2018
#


import pyalgogem.data as data
import pyalgogem.backtest as backtest
import pyalgogem.deployment as deployment
import pyalgogem.performance as performance

from pandas import DataFrame


class AlgorithmEnvironment(object):
    """
    Wrapper class object for Algorithmic Trading of Cryptocurrencies
    Using the CryptoCompare API, HDFS, Sci-kit Learn, and Gemini exchange
    """

    def __init__(self, key=None, secret_key=None, sandbox=True, debug=False):
        """
        Creates algorithm_environment object (ae)

        Parameters
        ==========
        key : string
            Gemini API key
        secret_key:  string
            Gemini secret API key
        sandbox : bool
            set to using sandbox account or live account
        debug : bool
            if true, print requests and function outputs

        Attributes
        ==========
        filename : str
            name of datafile to be used by environment
            on update: creates new HDF5 file in CWD
                with same name
        instrument : str
            name of instrument to be used - must be BTC or ETH

        """

        # set parametric values
        if key is None or secret_key is None:
            raise ValueError('Please enter proper API keys')
        self.__key = key
        self.__secret_key = secret_key
        if sandbox:
            self.__url = 'https://api.sandbox.gemini.com/v1/'
        else:
            self.__url = 'https://api.gemini.com/v1/'
        self.__debug = debug

        # set initial attributes
        self.file = 'data.h5'
        self.instrument = None
        self.window = None
        self.data_raw = None
        self.data_sample = None

        # create API objects for Cryptocompare and Gemini
        self.CC = data.CryptoCompareAPI()
        self.GEMINI = data.GeminiAPI(self.__key, self.__secret_key)
        self.GSTREAM = data.GeminiStreamAPI(self.__key, self.__secret_key)

    @property
    def file(self):
        """Name of data file to read/write from"""
        return self.__file

    @file.setter
    def file(self, new_file):
        if new_file is not None:
            self.__file = data.create_datafile(str(new_file))
        else:
            raise ValueError('Enter a valid name for data file.')

    @property
    def instrument(self):
        """Name of data file to read/write from"""
        return self.__instrument

    @instrument.setter
    def instrument(self, new_instrument):
        """Instrument to be used in algorithm"""
        if new_instrument is None:
            self.__instrument = None
        elif new_instrument.upper() not in [None, 'BTC', 'ETH']:
            raise ValueError("Instrument must be BTC or ETH")
        else:
            self.__instrument = new_instrument.upper()

    @property
    def window(self):
        """Time window to use when selecting sample data"""
        return self.__window

    @window.setter
    def window(self, new_window):
        if new_window is None:
            self.__window = None
        elif new_window.upper() in ['D', 'H', 'M']:
            self.__window = new_window.upper()
        else:
            raise ValueError("Time window must be: 'D', 'H', 'M'")

    @property
    def data_raw(self):
        """Raw retrieval of data from dataset"""
        return self.__data_raw

    @data_raw.setter
    def data_raw(self, new_data_raw):
        """Raw retrieval of data from dataset"""
        if new_data_raw is None or \
                isinstance(new_data_raw, DataFrame):
            self.__data_raw = new_data_raw
        else:
            raise ValueError('Must be Pandas DataFrame object')

    @property
    def data_sample(self):
        """In-Sample data to use for training and backtesting"""
        return self.__data_sample

    @data_sample.setter
    def data_sample(self, new_data_sample):
        """In-Sample data to use for training and backtesting"""
        if new_data_sample is None or \
                isinstance(new_data_sample, DataFrame):
            self.__data_sample = new_data_sample
        else:
            raise ValueError('Must be Pandas DataFrame object')

    def update_all_historical(self):
        """
        Retrieve all possible available daily
        from CryptoCompare and append missing values
        to currently-selected data-file
        """
        if self.instrument is None:
            raise ValueError('Must select an instrument first')
        if self.window is None:
            raise ValueError('Must select valid window (D/M/H)')
        if self.window == 'D':
            hist_df = self.CC.historical_price_daily(self.instrument)
        elif self.window == 'H':
            hist_df = self.CC.historical_price_hourly(self.instrument)
        elif self.window == 'M':
            hist_df = self.CC.historical_price_minute(self.instrument)
        old_min, old_max = data.get_minmax_daterange(self.instrument, self.file)
        # select subset of data that isn't within range of old min/max
        new_df = data.select_new_values(dataframe=hist_df, \
                                        old_min=old_min, old_max=old_max)
        # as long as there is new data to add, add to datafile
        if new_df is not None:
            data.append_to_datafile(symbol=self.instrument, data=new_df)
        print('All available historical data has been successfully loaded!')