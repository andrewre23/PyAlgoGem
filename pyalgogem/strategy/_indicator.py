#
# PyAlgoGem Project
# strategy/indicator
#
# class definition for Indicator object
#
# Andrew Edmonds - 2018
#




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
        dataset : Dataset
            object to house dataset used for testing
        """


class IndicatorSMA(IndicatorBase):
    """
    SMA Indicator object
    """
    def __init__(self, dataset, SMA1 = None, SMA2 = None):
        """
        Create SMA Indicator object
        """
        pass