#
# PyAlgo Project
# data/gemini_api
#
# functions to interact with Gemini API
#
# Andrew Edmonds - 2018
#


class GeminiAPI(object):
    """
    Wrapper class object for Retrieval of Price Data
    For Cryptocurrencies Using the CryptoCompare API
    """

    def __init__(self, key, secret_key):
        self.__key = key
        self.__secret_key = secret_key

    def tester(self):
        print('test','1, 2')