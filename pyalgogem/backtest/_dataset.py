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
    nlags : int
        number of return lags to use in sample dataset
        -log-returns must first be calculated

    Methods
    =======
    reset_sample_data :
        -reset sample dataset to a new copy of raw dataset
    drop_col :
        -drop columns
    add_log_returns :
        -add 'returns' column equal to the log-returns
        of that day
        -note - first data point will be dropped
    set_return_lags :
        -create nlags number of log-returns lags in
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
        self.nlags = None

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
        else:
            raise ValueError('Must be Pandas DataFrame object')

    @property
    def nlags(self):
        """Number of lags to have in sample data"""
        return self.__nlags

    @nlags.setter
    def nlags(self, nlags):
        if nlags is None:
            self.__nlags = None
        elif type(nlags) != int:
            raise ValueError('Must be an integer value')
        elif nlags <= 1:
            raise ValueError('Must be greater than 1')
        else:
            self.set_return_lags(nlags)
            self.__nlags = nlags

    def reset_sample_data(self):
        """Resets sample data to match raw dataset"""
        if self.raw is None:
            self.sample = None
        else:
            self.sample = self.raw.copy()

    def add_log_returns(self):
        """Add log-returns column to sampled dataset"""
        self.reset_sample_data()
        data = self.sample
        data['returns'] = log(data['close'] / data['close'].shift(1))
        self.sample = data.dropna()
        self.nlags = None

    def set_return_lags(self, nlags):
        """Add n-lags to DataFrame"""
        if not (type(nlags) == int and nlags > 1):
            raise ValueError('Must have more than one lag')
        if nlags > len(self.sample) + 1:
            raise ValueError('Must have less lags than length of sample dataset')
        self.add_log_returns()
        data = self.sample
        for i in range(nlags):
            num = i + 1
            lagname = 'returns_{}'.format(num)
            if lagname not in data.columns:
                data[lagname] = data['returns'].shift(num)
        self.sample = data.dropna()

    def drop_col(self, col):
        if type(col) != str:
            raise ValueError('Must pass string object for column name')
        if col in self.sample.columns:
            self.sample.drop(col,axis=1)
