#
# PyAlgoGem Project
# data/cryptocompare_api
#
# functions to interact with Cryptocompare API
#
# Andrew Edmonds - 2018
#

import requests
import datetime as dt
import pandas as pd

URL_BASE = 'https://min-api.cryptocompare.com/data/'


class CryptoCompareAPI(object):
    """
    Wrapper class object for Retrieval of Price Data
    For Cryptocurrencies Using the CryptoCompare API
    """

    def current_price(self, symbol, comparison_symbols=['USD'], exchange='Gemini'):
        """Get the price of a currency against multiple currencies

        Parameters
        ==========
        symbol : str
            name of desired currency
        comparison_symbols : list
            reference currencies
        exchange : str
            name of exchange to source from
        """
        data = None
        url = URL_BASE + 'price?fsym={}&tsyms={}' \
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
        if exchange:
            url += '&e={}'.format(exchange)

        try:
            page = requests.get(url)
            data = page.json()
        except:
            print('Error: unable to connect to Cryptocompare API')

        return data

    def historical_price(self, symbol, ts, comparison_symbols=['USD'], exchange='Gemini'):
        """Get the price of a currency against multiple currencies at any
        given timestamp

        Parameters
        ==========
        symbol : str
            name of desired currency
        ts : timeseries
            specific instance to retrieve price from
        comparison_symbols : list
            reference currencies
        exchange : str
            name of exchange to source from
        """
        data = None
        url = URL_BASE + 'pricehistorical?fsym={}&tsyms={}'.format(
            symbol.upper(), ','.join(comparison_symbols).upper())
        if ts is not None and isinstance(ts, dt.datetime):
            url += {'ts'.format(ts)}
        if exchange:
            url += '&e={}'.format(exchange)

        try:
            page = requests.get(url)
            data = page.json()
        except:
            print('Error: unable to connect to Cryptocompare API')

        return data

    def historical_price_daily(self, symbol, comparison_symbol='USD', all_data=True,
                               limit=1, aggregate=1, exchange='Gemini'):
        """Retrieve Daily OHLC prices, and to/from volume
        -values based on 00:00:00 GMT time

        Parameters
        ==========
        symbol : str
            name of desired currency
        comparison_symbol : str
            reference currency
        all_data : bool
            get all the available data (default True)
        limit : int
            limit number of days retrieved
            -default : 30
            -max : 2000
        aggregate : int
            grouped into number of days
            -default : 1
            -max : 30
        exchange : str
            name of exchange to source from
        """
        df = None
        url = URL_BASE + 'histoday?fsym={}&tsym={}&limit={}&aggregate={}' \
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
        if exchange:
            url += '&e={}'.format(exchange)
        if all_data:
            url += '&allData=true'

        try:
            page = requests.get(url)
            df = pd.DataFrame(page.json()['Data'])
            df.index = [dt.datetime.fromtimestamp(d) for d in df.time]
            df = df.drop('time', axis=1)
        except:
            print('Error: unable to connect to Cryptocompare API')

        return df

    def historical_price_hourly(self, symbol, comparison_symbol='USD', limit=1,
                                aggregate=1, exchange='Gemini'):
        """Retrieve Hourly OHLC prices, and to/from volume
        -values based on 00:00:00 GMT time

        Parameters
        ==========
        symbol : str
            name of desired currency
        comparison_symbol : str
            reference currency
        limit : int
            limit number of days retrieved
            -default : 168
            -max : 2000
        aggregate : int
            grouped into number of days
            -default : 1
            -max : None
        exchange : str
            name of exchange to source from
        """
        df = None
        url = URL_BASE + 'histohour?fsym={}&tsym={}&limit={}&aggregate={}' \
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
        if exchange:
            url += '&e={}'.format(exchange)

        try:
            page = requests.get(url)
            df = pd.DataFrame(page.json()['Data'])
            df.index = [dt.datetime.fromtimestamp(d) for d in df.time]
            df = df.drop('time', axis=1)
        except:
            print('Error: unable to connect to Cryptocompare API')

        return df

    def historical_price_minute(self, symbol, comparison_symbol='USD', limit=1,
                                aggregate=1, exchange='Gemini'):
        """Retrieve Minute OHLC prices, and to/from volume
        -values based on 00:00:00 GMT time

        Parameters
        ==========
        symbol : str
            name of desired currency
        comparison_symbol : str
            reference currency
        limit : int
            limit number of days retrieved
            -default : 1440
            -max : 2000
        aggregate : int
            grouped into number of days
            -default : 1
            -max : None
        exchange : str
            name of exchange to source from
        """
        df = None
        url = URL_BASE + 'histominute?fsym={}&tsym={}&limit={}&aggregate={}' \
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
        if exchange:
            url += '&e={}'.format(exchange)

        try:
            page = requests.get(url)
            df = pd.DataFrame(page.json()['Data'])
            df.index = [dt.datetime.fromtimestamp(d) for d in df.time]
            df = df.drop('time', axis=1)
        except:
            print('Error: unable to connect to Cryptocompare API')

        return df
