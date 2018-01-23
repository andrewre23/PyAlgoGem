#
# PyAlgo Project
# base/
#
#
# Andrew Edmonds - 2018
#

from ..data import initialize_data_directory


class algorithm_environment(object):
    """
    Main class for Gemini wrapper and interactive tool

    """

    def __init__(self, key, secret_key, sandbox=True, debug=False):
        """
        Creates algorithm_environment object (ae)

        Parameters
        ==========
        key: string
            Gemini API key
        secret_key: string
            Gemini secret API key
        sandbox: bool
            set to using sandbox account or live account
        debug: bool
            if true, print requests and function outputs
        """
        self.key = key
        self.secret_key = secret_key
        if sandbox:
            self.url = 'https://api.sandbox.gemini.com/v1/'
        else:
            self.url = 'https://api.gemini.com/v1/'
        self.debug = debug

    def setup_datastorage(self, path=None, folder=None, over_write=False):
        """
        Run to ensure data storage location is ready, and return path of store
        """
        return initialize_data_directory(path, folder, over_write)
