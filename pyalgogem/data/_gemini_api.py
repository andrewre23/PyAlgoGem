#
# PyAlgoGem Project
# data/gemini_api
#
# functions to interact with Gemini API
#
# Modeld after  pygem class written by:
# Michael Schwed and Dr. Yves Hilpsch
#
# Andrew Edmonds - 2018
#


class GeminiAPI(object):
    """
    Wrapper class object for Retrieval of Price Data
    For Cryptocurrencies Using the CryptoCompare API
    """

    def __init__(self, key, secret_key, sandbox=True,debug=False):
        self.__key = key
        self.__secret_key = secret_key
        self.__sandbox = sandbox
        self.__debug = debug
        self.__last_order_id = None

    def tester(self):
        print('test','1, 2')