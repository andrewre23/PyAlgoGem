#
# PyAlgoGem Project
# data/gemini_streamer_api
#
# functions to interact with Gemini API
#
# Modeld after  pygem_socket class written by:
# Michael Schwed and Dr. Yves Hilpsch
#
# Andrew Edmonds - 2018
#


class GeminiStreamAPI(object):
    """
    Wrapper class object for Retrieval of Price Data
    For Cryptocurrencies Using the CryptoCompare API
    """

    def __init__(self, key, secret_key):
        self.__key = key
        self.__secret_key = secret_key

    def tester(self):
        print('test','3, 4')