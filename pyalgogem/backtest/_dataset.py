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
    reset :
        -reset sample dataset to a new copy of raw dataset
    drop_col :
        -drop columns
    add_log_returns :
        -add 'returns' column equal to the log-returns
        of that day
        -note - first data point will be dropped
    set_return_lags :
        -create numlags number of log-returns lags in
        sample dataset
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
            self.sample = new_raw
            if self.sample is not None:
                self.add_log_returns()
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
            self.__newcols = set()
            self.numlags = None
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
            self.set_return_lags(numlags)
            self.__numlags = numlags

    def reset(self):
        """Resets sample data to match raw dataset"""
        if self.raw is None:
            self.sample = None
        else:
            self.sample = self.raw.copy()

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
                        self.sample.drop(name, axis=1, inplace=True)
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
        # drop open/high/low/close prices from sample dataset
        self.drop_col(['close', 'high', 'low', 'open'])

    def drop_volume_data(self):
        # drop open/high/low/close prices from sample dataset
        self.drop_col(['vol_to', 'vol_from'])

    def add_log_returns(self):
        """Add log-returns column to sampled dataset"""
        self.reset()
        data = self.sample
        data['returns'] = log(data['close'] / data['close'].shift(1))
        self.sample = data.dropna()
        self.numlags = None
        self.__newcols.add('returns')

    def set_return_lags(self, numlags):
        """Add n-lags to DataFrame"""
        if not (type(numlags) == int and numlags > 1):
            raise ValueError('Must have more than one lag')
        if numlags > len(self.sample) + 1:
            raise ValueError('Must have less lags than length of sample dataset')
        # create 'returns' column if not already there
        if 'returns' not in self.sample.columns:
            # only return columns that are currently in sample dataset
            orig_cols = self.sample.columns
            self.add_log_returns()
            for col in self.sample.columns:
                if col not in orig_cols:
                    self.drop_col(col)
        data = self.sample
        for i in range(numlags):
            num = i + 1
            if len(str(numlags)) == 2:
                lagname = 'returns_{:02d}'.format(num)
            elif len(str(numlags)) == 3:
                lagname = 'returns_{:03d}'.format(num)
            else:
                lagname = 'returns_{}'.format(num)
            if lagname not in data.columns:
                data[lagname] = data['returns'].shift(num)
                self.__newcols.add(lagname)
        self.sample = data.dropna()
        self.__newcols = set(self.sample.columns)
