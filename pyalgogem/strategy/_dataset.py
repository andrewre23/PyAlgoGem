#
# PyAlgoGem Project
# strategy/dataset
#
# class definition for Dataset object
#
# Andrew Edmonds - 2018
#

from numpy import log
from pandas import DataFrame


class Dataset(object):
    """
    Object to house both raw and resampled
    datasets to then be used for backtesting

    Attributes
    ==========
    raw : DataFrame
        raw dataset directly loaded from HDF5 file
        -stays the same throughout use unless reloading
        Dataset
    returns : DataFrame
        dataset containing log-returns of instrument
        -length len(raw)- 1

    Methods
    =======
    initialize_returns :
        -recalculates returns based on raw dataset

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

    def __str__(self):
        """When printing, print sample dataset"""
        return self.raw.__str__()

    @property
    def raw(self):
        """Raw dataset to load from disk"""
        return self.__raw

    @raw.setter
    def raw(self, new_raw):
        if new_raw is None or \
                isinstance(new_raw, DataFrame):
            self.__raw = new_raw
            self.initialize_returns()
        else:
            raise ValueError('Must be Pandas DataFrame object')

    @property
    def returns(self):
        """Returns dataset from raw sample"""
        return self.__returns

    @returns.setter
    def returns(self, new_returns):
        if new_returns is None or \
                isinstance(new_returns, DataFrame):
            self.__returns = new_returns
        else:
            raise ValueError('Must be Pandas DataFrame object')

    def initialize_returns(self):
        """Resets sample data to match raw dataset"""
        if self.raw is None:
            self.returns = None
        else:
            data = self.raw.copy()
            self.returns = DataFrame({'returns': log(data['close'] / data['close'].shift(1))})
