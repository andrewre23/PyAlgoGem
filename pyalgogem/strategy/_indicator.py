#
# PyAlgoGem Project
# strategy/indicator
#
# class definition for Indicator object
#
# Andrew Edmonds - 2018
#

from pyalgogem.strategy import Dataset


class IndicatorBase(object):
    """
    Base object to create and backtest trading signal
    or predictor for later use with Strategy object

    Attributes
    ==========


    Methods
    =======

    """

    def __init__(self):
        """
        Creates container environment to create and backtest
        trading signal or predictor easily at the CLI
        """


class IndicatorSMA(IndicatorBase):
    """
    SMA Indicator object

    Parameters
    ==========
    dataset : Dataset
        object to house dataset used for testing
    """

    def __init__(self, dataset, SMA1=None, SMA2=None):
        """
        Create SMA Indicator object
        """
        self.dataset = dataset

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
