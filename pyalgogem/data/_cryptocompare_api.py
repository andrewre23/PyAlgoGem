#
# PyAlgo Project
# data/cryptocompare_api
#
# functions to interact with Cryptocompare API
#
# Andrew Edmonds - 2018
#

import requests
import datetime as dt
import pandas as pd


class CryptoCompareAPI(object):
    """Object for housing data retrieval
    functions with CryptoCompare site
    """

    URL_BASE = 'https://min-api.cryptocompare.com/data/'

    def current_price(symbol, comparison_symbols=['USD'], exchange='Gemini'):
        """Retrieve current price of currencies"""
        url = URL_BASE + 'price?fsym={}&tsyms={}' \
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
        if exchange:
            url += '&e={}'.format(exchange)
        page = requests.get(url)
        data = page.json()
        return data

    def historical_price_daily(symbol, comparison_symbol='USD', all_data=True, \
                               limit=1, aggregate=1, exchange='Gemini'):
        """Retrieve historical prices by day"""
        url = URL_BASE + 'histoday?fsym={}&tsym={}&limit={}&aggregate={}' \
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
        if exchange:
            url += '&e={}'.format(exchange)
        if all_data:
            url += '&allData=true'
        page = requests.get(url)
        df = pd.DataFrame(page.json()['Data'])
        df.index = [dt.datetime.fromtimestamp(d) for d in df.time]
        df = df.drop('time', axis=1)
        return df

    def historical_price_hourly(symbol, comparison_symbol='USD', limit=1, \
                                aggregate=1, exchange='Gemini'):
        """Retrieve historical prices by hour"""
        url = URL_BASE + 'histohour?fsym={}&tsym={}&limit={}&aggregate={}' \
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
        if exchange:
            url += '&e={}'.format(exchange)
        page = requests.get(url)
        df = pd.DataFrame(page.json()['Data'])
        df.index = [dt.datetime.fromtimestamp(d) for d in df.time]
        df = df.drop('time', axis=1)
        return df

    def historical_price_minute(symbol, comparison_symbol='USD', limit=1, \
                                aggregate=1, exchange='Gemini'):
        """Retrieve historical prices by hour"""
        url = URL_BASE + 'histominute?fsym={}&tsym={}&limit={}&aggregate={}' \
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
        if exchange:
            url += '&e={}'.format(exchange)
        page = requests.get(url)
        df = pd.DataFrame(page.json()['Data'])
        df.index = [dt.datetime.fromtimestamp(d) for d in df.time]
        df = df.drop('time', axis=1)
        return df
