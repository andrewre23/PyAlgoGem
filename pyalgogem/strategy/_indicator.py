#
# PyAlgoGem Project
# strategy/indicator
#
# class definition for Indicator object
#
# Andrew Edmonds - 2018
#


from numpy import log
from pandas import DataFrame
from sklearn.preprocessing import label


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

        Parameters
        ==========

        """