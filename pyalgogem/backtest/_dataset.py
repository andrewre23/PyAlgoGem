#
# PyAlgoGem Project
# backtest/dataset
#
# class definition for Dataset object
#
# Andrew Edmonds - 2018
#

from numpy import log
from pandas import DataFrame
from sklearn.preprocessing import label


class Dataset(object):
    """
    Object to house both raw and resampled
    datasets to then be used for backtesting

    Attributes
    ==========
    raw : DataFrame
        raw dataset directly loaded from HDF5 file
        -stays the same throughout use unless reloading
        Dataset object
    sample : DataFrame
        sample dataset to use for training and backtesting
    numlags : int
        number of return lags to use in sample dataset
        -log-returns must first be calculated
    newcols : list of strings (private)
        list of columns found in sample dataset that
        are not a part of the raw dataset

    Methods
    =======
    initialize_sample_data :
        -resets sample data to match the raw dataset
    add_log_returns :
        -add 'returns' column equal to the log-returns
        of that day
        -note - first data point will be dropped
    set_return_lags :
        -create numlags number of log-returns lags in
        sample dataset
    add_sma :
        -add short-term moving-averages of log-returns
        based on SMA parameter
    add_sma_std :
        -add short-term moving-average of std of log-returns
        based on SMA parameter
    add_col :
        -add column to sample dataset if not already in columns
        and update private newcols attributes
    drop_col :
        -drop column or columns passed as arguments
    drop_ohlc_prices :
        -drop open/high/low/close columns from sample dataset
    drop_volume_data :
        -open volume to/from columns from sample dataset
    ensure_log_returns :
        -create 'returns' column if not already present in sample
    select_matching_sample :
        -pass a DataFrame or Series object and function will return
        a column the same length as the sample object with values present
        where indicies match, and NA elsewhere
    update_newcols :
        -updates newcols attribute to those present columns not found in
        raw datatset
    remove_na :
        -remove all NA values from sample dataset
        -note : be sure you are reay to drop values, as no way to
        recover without recreating sample dataset from raw dataset
    """

    def __init__(self, input_data):
        """
        Creates container environment to house both raw and
        sampled datasets for ease of access at CLI

        Parameters
        ==========
        input_data: DataFrame
            initial dataset to be used as raw data
        """
        # raw dataset
        self.raw = input_data
        # number of lags for logs-returns
        self.numlags = None
        # names of columns not in original raw dataset
        self.__newcols = set()

    def __str__(self):
        """When printing, print sample dataset"""
        return self.sample.__str__()

    @property
    def raw(self):
        """Raw dataset to load from disk"""
        return self.__raw

    @raw.setter
    def raw(self, new_raw):
        if new_raw is None or \
                isinstance(new_raw, DataFrame):
            self.__raw = new_raw
            self.initialize_sample_data()
        else:
            raise ValueError('Must be Pandas DataFrame object')

    @property
    def sample(self):
        """In-Memory dataset to use for training and backtesting"""
        return self.__sample

    @sample.setter
    def sample(self, new_sample):
        if new_sample is None or \
                isinstance(new_sample, DataFrame):
            self.__sample = new_sample
            self.update_newcols()
        else:
            raise ValueError('Must be Pandas DataFrame object')

    @property
    def numlags(self):
        """Number of lags to have in sample data"""
        return self.__numlags

    @numlags.setter
    def numlags(self, numlags):
        if numlags is None:
            self.__numlags = None
        elif type(numlags) != int:
            raise ValueError('Must be an integer value')
        elif numlags <= 1:
            raise ValueError('Must be greater than 1')
        else:
            self.__numlags = numlags

    def initialize_sample_data(self):
        """Resets sample data to match raw dataset"""
        if self.raw is None:
            self.sample = None
        else:
            self.sample = self.raw.copy()

    def add_log_returns(self):
        """Add log-returns column to sampled dataset"""
        data = self.raw.copy()
        log_rets = log(data['close'] / data['close'].shift(1))
        self.add_column('returns', log_rets)
        self.numlags = None
        self.__newcols.add('returns')

    def set_return_lags(self, numlags):
        """Add n-lags to DataFrame"""
        if not (type(numlags) == int):
            raise ValueError('Must pass int object')
        elif numlags <= 1:
            raise ValueError('Must have more than one lag')
        elif numlags > len(self.sample) + 1:
            raise ValueError('Must have less lags than length of sample dataset')
        # create 'returns' column if not already there
        self.ensure_log_returns()
        for i in range(numlags):
            num = i + 1
            lagname = 'returns_{}'.format(num)
            self.add_column(lagname, self.sample['returns'].shift(num))
        if self.numlags and numlags < self.numlags:
            for lag in range(self.numlags - numlags):
                self.drop_col('returns_{}'.format(lag + numlags + 1))
        self.numlags = numlags

    def add_sma(self, sma):
        """Add SMA vector of log-returns"""
        if not type(sma) == int:
            raise ValueError('Must pass integer for SMA')
        if sma <= 1:
            raise ValueError('SMA must be at least 2 units')
        if sma > len(self.sample):
            raise ValueError("SMA can't be greater than length of sample data")
        # create 'returns' column if not already there
        self.ensure_log_returns()
        smaname = 'sma_{}'.format(sma)
        self.add_column(smaname, self.sample['returns'].rolling(sma).mean())

    def add_sma_std(self, sma):
        """Add SMA vector of std-dev of log-returns"""
        if not type(sma) == int:
            raise ValueError('Must pass integer for SMA')
        if sma <= 1:
            raise ValueError('SMA must be at least 2 units')
        if sma > len(self.sample):
            raise ValueError("SMA can't be greater than length of sample data")
        # create 'returns' column if not already there
        self.ensure_log_returns()
        smaname = 'sma_std_{}'.format(sma)
        self.add_column(smaname, self.sample['returns'].rolling(sma).std())

    def add_exponential_smoothing(self, alpha):
        """Add exponential smoothing vector of log-returns"""
        if not type(alpha) == int:
            raise ValueError('Must pass integer for Alpha')
        if alpha <= 0:
            raise ValueError('Alpha must be greater than 0')
        if alpha > 1:
            raise ValueError('Alpha must be no greater than 1')
        # create 'returns' column if not already there
        self.ensure_log_returns()
        alphaname = 'alpha_{}'.format(alpha)
        self.add_column(alphaname, self.sample['returns'].ewm(alpha=alpha).mean())


    def add_column(self, name, data):
        """Add parameterized function to sample dataset"""
        if name not in self.sample.columns:
            self.sample[name] = self.select_matching_sample(data)
        self.update_newcols()

    def drop_col(self, col):
        # case where list is passed
        if type(col) == list:
            if len(col) == 0:
                raise ValueError('Cannot pass empty list')
            else:
                for name in col:
                    # iterate to check if valid string objects before operating
                    if type(name) != str:
                        raise ValueError('List can only contain strings')
                for name in col:
                    if name in self.sample.columns:
                        self.drop_col(name)
                        if name in self.__newcols:
                            self.__newcols.remove(name)
        # case where string is passed
        elif type(col) == str:
            if col in self.sample.columns:
                self.sample.drop(col, axis=1, inplace=True)
                if col in self.__newcols:
                    self.__newcols.remove(col)
        else:
            raise ValueError('Must pass string or list of strings for column to drop')

    def drop_ohlc_prices(self):
        """Drop open/high/low/close prices from sample dataset"""
        self.drop_col(['close', 'high', 'low', 'open'])

    def drop_volume_data(self):
        """Drop open/high/low/close prices from sample dataset"""
        self.drop_col(['vol_to', 'vol_from'])

    def ensure_log_returns(self):
        """Ensure 'returns' is present in sample data"""
        if 'returns' not in self.sample.columns:
            self.add_log_returns()

    def select_matching_sample(self, input_df):
        """Returns sections of input_df that
        are currently present in sample dataset index"""
        if self.sample is None:
            raise ValueError('Nothing currently in sample')
        sample_index = self.sample.index
        return_df = None
        try:
            return_df = input_df.loc[sample_index]
        except KeyError:
            print('Error: no overlapping dates with sample dataset')
        return return_df

    def update_newcols(self):
        """Updates newcols hidden attributes"""
        self.__newcols = set()
        if self.sample is None: return
        for name in self.sample.columns:
            if name not in self.raw.columns:
                self.__newcols.add(name)

    def remove_na(self):
        """Remove all NAs from sample dataset"""
        if self.sample is not None:
            self.sample.dropna(inplace=True)
