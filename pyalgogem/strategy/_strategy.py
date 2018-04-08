#
# PyAlgoGem Project
# strategy/strategy
#
# main module to house strategy object
#
# Andrew Edmonds - 2018
#

from pyalgogem.strategy import Dataset

from pandas import DataFrame

class Strategy(object):
    """"
    Wrapper class for Strategy object used to
    create, develop, and train strategies for trading
    """
    def __init__(self, dataset):
        """
        Creates container environment to store all
        data and models needed for developing strategies
        """
        self.dataset = dataset
        self.signals = DataFrame()

    @property
    def dataset(self):
        """Object to house raw and sampled data"""
        return self.__dataset

    @dataset.setter
    def dataset(self, new_dataset):
        if new_dataset is None or \
                isinstance(new_dataset, Dataset):
            self.__dataset = new_dataset
        else:
            raise ValueError('Must be Dataset object or None')

    @property
    def signals(self):
        """Object to house trading signals"""
        return self.__signals

    @signals.setter
    def signals(self, new_signals):
        if new_signals is None or \
                isinstance(new_signals, DataFrame):
            self.__signals = new_signals
        else:
            raise ValueError('Must be Pandas DataFrame object or None')

