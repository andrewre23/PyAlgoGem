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
        self.data_raw = input_data
        self.nlags = None

    def __str__(self):
        """When printing, print sample dataset"""
        return self.data_sample.__str__()

    @property
    def data_raw(self):
        """Raw dataset to load from disk"""
        return self.__data_raw

    @data_raw.setter
    def data_raw(self, new_data_raw):
        if new_data_raw is None or \
                isinstance(new_data_raw, DataFrame):
            self.__data_raw = new_data_raw
            self.data_sample = new_data_raw
            if self.data_sample is not None:
                self.add_log_returns()
        else:
            raise ValueError('Must be Pandas DataFrame object')

    @property
    def data_sample(self):
        """In-Memory dataset to use for training and backtesting"""
        return self.__data_sample

    @data_sample.setter
    def data_sample(self, new_data_sample):
        if new_data_sample is None or \
                isinstance(new_data_sample, DataFrame):
            self.__data_sample = new_data_sample
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
            self.__nlags = nlags

    def reset_sample_data(self):
        """Resets sample data to match raw dataset"""
        if self.data_raw is None:
            self.data_sample = None
        else:
            self.data_sample = self.data_raw.copy()

    def add_log_returns(self):
        """Add log-returns column to sampled dataset"""
        self.reset_sample_data()
        data = self.data_sample
        data['returns'] = log(data['close'] / data['close'].shift(1))
        self.data_sample = data.dropna()
        self.nlags = None

    def set_return_lags(self, nlags):
        """Add n-lags to DataFrame"""
        if not (type(nlags) == int and nlags > 1):
            raise ValueError('Must have more than one lag')
        if nlags > len(self.data_sample) + 1:
            raise ValueError('Must have less lags than length of sample dataset')
        self.add_log_returns()
        data = self.data_sample
        for i in range(nlags):
            num = i + 1
            lagname = 'returns_{}'.format(num)
            if lagname not in data.columns:
                data[lagname] = data['returns'].shift(num)
        self.data_sample = data.dropna()
