#
# PyAlgo Project
# base/
#
# main module containing AlgorithmEnvironment object
#
# Andrew Edmonds - 2018
#

import pyalgogem.data as data
import pyalgogem.backtest as backtest
import pyalgogem.deployment as deployment
import pyalgogem.performance as performance


class AlgorithmEnvironment(object):
    """
    Main class for Gemini wrapper and interactive tool

    """

    def __init__(self, key=None, secret_key=None, sandbox=True, debug=False):
        """
        Creates algorithm_environment object (ae)

        Parameters
        ==========
        key : string
            Gemini API key
        secret_key:  string
            Gemini secret API key
        sandbox : bool
            set to using sandbox account or live account
        debug : bool
            if true, print requests and function outputs

        Attributes
        ==========
        filename : str
            name of datafile to be used by environment
            on update: creates new HDF5 file in CWD
                with same name
        instrument : str
            name of instrument to be used - must be BTC or ETH

        """

        # set parametric values
        if key is None or secret_key is None:
            raise ValueError('Please enter proper API keys')
        self.__key = key
        self.__secret_key = secret_key
        if sandbox:
            self.__url = 'https://api.sandbox.gemini.com/v1/'
        else:
            self.__url = 'https://api.gemini.com/v1/'
        self.__debug = debug

        # set initial attributes
        self.file = 'data.h5'
        self.instrument = None

    @property
    def instrument(self):
        """Name of data file to read/write from"""
        return self.__instrument

    @instrument.setter
    def instrument(self, new_instrument):
        """Instrument to be used in algorithm"""
        if new_instrument is None:
            self.__instrument = None
        elif new_instrument.upper() not in [None, 'BTC', 'ETH']:
            raise ValueError("Instrument must be BTC or ETH")
        else:
            self.__instrument = new_instrument.upper()

    @property
    def file(self):
        """Name of data file to read/write from"""
        return self.__file

    @file.setter
    def file(self, new_file):
        self.__file = data.create_datafile(str(new_file))

