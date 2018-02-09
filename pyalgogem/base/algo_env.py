#
# PyAlgoGem Project
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

import configparser

config = configparser.ConfigParser()
config.read('my_keys.cfg')


class AlgorithmEnvironment(object):
    """
    Wrapper class object for Algorithmic Trading of Cryptocurrencies
    Using the CryptoCompare API, HDF5, Sci-kit Learn, and Gemini exchange
    """

    def __init__(self, sandbox=True, debug=False):
        """
        Creates container environment to store all data
        for algorithm development, backtesting, and deployment

        Parameters
        ==========
        sandbox : bool
            set to using sandbox account or live account
        debug : bool
            if true, print requests and function outputs

        Attributes
        ==========

        symbol : str
            symbol of currency to be used - must be
            -BTC : Bitcoin
            -ETH : Ethereum
        window : str
            time window to be used for data - must be:
            -'D' : Daily
            -'H' : Hourly
            -'M' : Minute
        file : str
            name of datafile to be used by environment
            on update: creates new HDF5 file in CWD
                with same name
        """

        # ensure valid Gemini API keys in config file
        try:
            self.__key = config['gemini']['key']
            self.__secret_key = config['gemini']['secret_key']
        except KeyError:
            print('Error: please check .cfg file keys and formatting')
        if self.__key == '' or self.__secret_key == '':
            raise ValueError('Please enter proper API keys')

        # ensure debug is set to permitted value
        if debug not in [True, False]:
            raise ValueError("Enter valid boolean value for 'debug'")

        # set initial attributes
        self.sandbox = sandbox
        self.__debug = debug

        # set initial algorithm attributes
        self.symbol = None
        self.window = None

        # set data attributes
        self.data_raw = None
        self.data_sample = None
        self.file = 'data.h5'

        # create API objects for Cryptocompare and Gemini
        self.CC = data.CryptoCompareAPI()
        self.GEMINI = data.GeminiAPI(self.__key, self.__secret_key, self.sandbox, self.__debug)
        self.GSTREAM = data.GeminiStreamAPI(self.__key, self.__secret_key, self.sandbox, self.__debug)

    @property
    def sandbox(self):
        """Switch from sandbox to live-acount"""
        return self.__sandbox

    @sandbox.setter
    def sandbox(self, new_sandbox):
        """Only allow True/False values"""
        if new_sandbox in [True, False]:
            self.__sandbox = new_sandbox
            if new_sandbox:
                self.__url = 'https://api.sandbox.gemini.com/v1/'
            else:
                self.__url = 'https://api.gemini.com/v1/'
        else:
            raise ValueError('Must be boolean value')

    @property
    def symbol(self):
        """Symbol of cryptocurrency to utilize in environment"""
        return self.__symbol

    @symbol.setter
    def symbol(self, new_symbol):
        """Only allow 'ETH', 'BTC' or 'None'"""
        symbol_str = str(new_symbol)
        if new_symbol is None:
            self.__symbol = new_symbol
        elif symbol_str.upper() not in ['BTC', 'ETH']:
            raise ValueError("Symbol must be BTC or ETH")
        else:
            self.__symbol = new_symbol.upper()

    @property
    def window(self):
        """Time window to use when selecting sample data"""
        return self.__window

    @window.setter
    def window(self, new_window):
        """Only allow 'D', 'H', or 'M'"""
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
        if new_data_sample is None or \
                isinstance(new_data_sample, DataFrame):
            self.__data_sample = new_data_sample
        else:
            raise ValueError('Must be Pandas DataFrame object')

    @property
    def file(self):
        """Name of data file to read/write from"""
        return self.__file

    @file.setter
    def file(self, new_file):
        if new_file:
            self.__file = data.create_datafile(str(new_file))
        else:
            raise ValueError('Enter a valid name for data file.')

    def check_key_attributes(self):
        """
        Raise error  if AlgorithmEnvironment has not
        chosen valid symbol and window attributes
        """
        if not (self.symbol and self.window and self.file):
            raise ValueError('Please ensure you have chosen: ',
                             'a symbol, time window, and local file')
        else:
            return

    def update_all_historical(self):
        """
        Retrieve all possible available daily
        from CryptoCompare and append missing values
        to currently-selected data-file
        """
        self.check_key_attributes()
        if self.window == 'D':
            hist_df = self.CC.historical_price_daily(self.symbol)
        elif self.window == 'H':
            hist_df = self.CC.historical_price_hourly(self.symbol)
        elif self.window == 'M':
            hist_df = self.CC.historical_price_minute(self.symbol)
        old_min, old_max = data.get_minmax_daterange(self.symbol, self.file)
        # select subset of data that isn't within range of old min/max
        new_df = data.select_new_values(dataframe=hist_df, old_min=old_min, old_max=old_max)
        # as long as there is new data to add, add to datafile
        if new_df is None:
            print('No new data for {} found - no data saved locally'. \
                  format(self.symbol))
        else:
            data.append_to_datafile(symbol=self.symbol, data=new_df)
            print('All available historical data for {} has been successfully loaded!'. \
                  format(self.symbol))

    def read_stored_data(self, start=None, end=None, all_data=True):
        """
        Load available locally-stored data into
        self.data_raw attribute
        -Can select subset of timeseries as ts object
        """
        self.check_key_attributes()
        self.data_raw = data.read_datafile(symbol=self.symbol, \
                                           start=start, end=end, file=self.file, all_data=all_data)
        if self.data_raw:
            print("Data has been loaded into 'data_raw'!")
