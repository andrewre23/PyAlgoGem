#
# PyAlgoGem Project
# strategy/indicator
#
# class definition for Indicator object
#
# Andrew Edmonds - 2018
#

from pyalgogem.strategy import Dataset

import numpy as np
from pandas import DataFrame
from scipy.optimize import brute


class IndicatorSMA(object):
    """
    Object for creating an SMA indicator with
    2 parameters, SMA1 and SMA2

    Attributes
    ==========
    dataset : Dataset
        object to house dataset used for testing
    results : DataFrame
        object to house results of strategy
    sma1 : int
        first parameter for SMA strategy
    sma2 : int
        second parameter for SMA strategy

    Methods
    =======
    reset_results :
        reset results DataFrame to equal dataset's sample DataFrame
    execute_strategy :
        recalculate results DataFrame based on current SMA parameters
    plot_results :
        plot results of strategy with current SMA parameters
    """

    def __init__(self, sma1, sma2, dataset, symbol):
        """
        Creates container environment to create and backtest
        trading signal or predictor easily at the CLI

        Parameters
        ==========
        """
        self.dataset = dataset
        self.sma1 = sma1
        self.sma2 = sma2
        self.symbol = symbol

    @property
    def dataset(self):
        """Object to house raw and sampled data"""
        return self.__dataset

    @dataset.setter
    def dataset(self, new_dataset):
        if new_dataset is None or \
                isinstance(new_dataset, Dataset):
            self.__dataset = new_dataset
            self.results = self.dataset.sample.copy()
        else:
            raise ValueError('Must be Dataset object or None')

    @property
    def results(self):
        """Object to house results of strategy"""
        return self.__results

    @results.setter
    def results(self, new_results):
        if new_results is None or \
                isinstance(new_results, DataFrame):
            self.__results = new_results
        else:
            raise ValueError('Must be DataFrame object or None')

    @property
    def sma1(self):
        """SMA1 parameter"""
        return self.__sma1

    @sma1.setter
    def sma1(self, new_sma1):
        if (isinstance(new_sma1, int) and
                1 < new_sma1 < len(self.dataset.sample)):
            self.__sma1 = new_sma1
            self.results['SMA1'] = self.results['close'].rolling(new_sma1).mean()
        else:
            raise ValueError('SMA1 must be greater than 1 and less than the size of the data')

    @property
    def sma2(self):
        """SMA2 parameter"""
        return self.__sma2

    @sma2.setter
    def sma2(self, new_sma2):
        if (isinstance(new_sma2, int) and
                1 < new_sma2 < len(self.dataset.sample)):
            self.__sma2 = new_sma2
            self.results['SMA2'] = self.results['close'].rolling(new_sma2).mean()
        else:
            raise ValueError('SMA2 must be greater than 1 and less than the size of the data')

    def reset_results(self):
        """
        Reset results DataFrame
        """
        self.results = self.dataset.sample.copy()
        if (self.sma1 and self.sma2):
            self.results['SMA1'] = self.results['close'].rolling(self.sma1).mean()
            self.results['SMA2'] = self.results['close'].rolling(self.sma2).mean()

    def execute_strategy(self):
        """
        Run vectorized backtesting of strategy and generate various performance metrics
        """
        data = self.results.copy().dropna()
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, 0)
        data['strategy'] = data['position'].shift(1) * data['returns']
        data['creturns'] = data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # absolute performance of indicator
        aperf = data['cstrategy'].ix[-1]
        # out/under performance of indicator
        operf = aperf - data['creturns'].ix[-1]
        return round(aperf, 2), round(operf, 2)

    def plot_results(self):
        """
        Plot cumulative performance of strategy vs underlying security
        """
        self.execute_strategy()
        # absolute performance of indicator
        aperf = self.results['cstrategy'].ix[-1]
        # out/under performance of indicator
        operf = aperf - self.results['creturns'].ix[-1]
        title = '%s | SMA1 = %d, SMA2 = %d | APerf = %d, OPerf = %d' % \
                (self.symbol, self.sma1, self.sma2, aperf, operf)
        self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(10, 6))

    def update_and_run(self, SMA):
        """
        Updates SMA parameters and negative absolute performance
        for minimization algorithm

        Parameters
        ==========
        SMA : tuple
            SMA parameter tuple
        """
        self.sma1, self.sma2 = int(SMA[0]), int(SMA[1])
        self.reset_results()
        return -self.execute_strategy()[0]

    def optimize_parameters(self, rangeSMA1, rangeSMA2):
        """
        Find global maximum given range of SMA parameters

        Parameters
        ==========
        rangeSMA1, rangeSMA2 : tuple
            range of SMA parameters of the form (start, end, step size)
        """
        opt = brute(self.update_and_run, (rangeSMA1, rangeSMA2), finish=None)
        self.sma1, self.sma2 = int(opt[0]), int(opt[1])
        return opt, -self.update_and_run(opt)


class IndicatorMOM(object):
    """
    Object for creating an Momentum indicator with
    1 parameter, MOM

    Attributes
    ==========
    dataset : Dataset
        object to house dataset used for testing
    results : DataFrame
        object to house results of strategy
    mom : int
        momentum parameter for strategy

    Methods
    =======
    reset_results :
        reset results DataFrame to equal dataset's sample DataFrame
    execute_strategy :
        recalculate results DataFrame based on current SMA parameters
    plot_results :
        plot results of strategy with current SMA parameters
    """

    def __init__(self, mom, dataset, symbol):
        """
        Creates container environment to create and backtest
        trading signal or predictor easily at the CLI

        Parameters
        ==========
        """
        self.dataset = dataset
        self.mom = mom
        self.symbol = symbol

    @property
    def dataset(self):
        """Object to house raw and sampled data"""
        return self.__dataset

    @dataset.setter
    def dataset(self, new_dataset):
        if new_dataset is None or \
                isinstance(new_dataset, Dataset):
            self.__dataset = new_dataset
            self.results = self.dataset.sample.copy()
        else:
            raise ValueError('Must be Dataset object or None')

    @property
    def results(self):
        """Object to house results of strategy"""
        return self.__results

    @results.setter
    def results(self, new_results):
        if new_results is None or \
                isinstance(new_results, DataFrame):
            self.__results = new_results
        else:
            raise ValueError('Must be DataFrame object or None')

    @property
    def mom(self):
        """MOM parameter"""
        return self.__mom

    @mom.setter
    def mom(self, new_mom):
        if (isinstance(new_mom, int) and
                1 < new_mom < len(self.dataset.sample)):
            self.__mom = new_mom
        else:
            raise ValueError('MOM must be greater than 1 and less than the size of the data')

    def reset_results(self):
        """
        Reset results DataFrame
        """
        self.results = self.dataset.sample.copy()

    def execute_strategy(self):
        """
        Run vectorized backtesting of strategy and generate various performance metrics
        """
        data = self.results.copy().dropna()
        data['position'] = np.sign(data['returns'].rolling(self.mom).mean())
        data['strategy'] = data['position'].shift(1) * data['returns']
        # determine when trades take place
        # trades = data['position'].diff().fillna(0) != 0
        # subtract transaction costs from return where trades take place
        # data['strategy'][trades] -= self.tc
        data['creturns'] = data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # absolute performance of indicator
        aperf = data['cstrategy'].ix[-1]
        # out/under performance of indicator
        operf = aperf - data['creturns'].ix[-1]
        return round(aperf, 2), round(operf, 2)

    def plot_results(self):
        """
        Plot cumulative performance of strategy vs underlying security
        """
        self.execute_strategy()
        # absolute performance of indicator
        aperf = self.results['cstrategy'].ix[-1]
        # out/under performance of indicator
        operf = aperf - self.results['creturns'].ix[-1]
        title = '%s | MOM = %d | APerf = %d, OPerf = %d' % \
                (self.symbol, self.mom, aperf, operf)
        self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(10, 6))

    def update_and_run(self, MOM):
        """
        Updates MOM parameters and negative absolute performance
        for minimization algorithm

        Parameters
        ==========
        MOM : tuple
            MOM parameter
        """
        if type(MOM) not in [int, float]:
            self.mom = int(MOM[0])
        else:
            self.mom = int(MOM)
        self.reset_results()
        return -self.execute_strategy()[0]

    def optimize_parameters(self, rangeMOM):
        """
        Find global maximum given range of MOM parameters

        Parameters
        ==========
        rangeMOM : tuple
            range of MOM parameter of the form (start, end, step size)
        """
        opt = brute(self.update_and_run, (rangeMOM, (0, 1, 1)), finish=None)
        self.mom = int(opt[0])
        return opt, -self.update_and_run(opt)
