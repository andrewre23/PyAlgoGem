#
# PyAlgoGem Project
# deploy/gemini_api
#
# functions to interact with Gemini API
#
# Modeld after pygem class written by:
# Michael Schwed and Dr. Yves Hilpsch
#
# Andrew Edmonds - 2018
#

import hmac
import hashlib
import time
import base64
import json
import requests
import pandas as pd
import datetime as dt


class GeminiAPI(object):
    """
    Wrapper class object for Retrieval of Price Data
    For Cryptocurrencies Using the CryptoCompare API

    Methods
    =======
    send_public_request :
        sends all public requests to Gemini server
    send_private_request :
        sends all private requests to Gemini server
    new_order :
        create new trade order
    cancel_order :
        cancel trade order
    cancel_all_session_orders :
        kill all orders placed during current session
    cancel_all_active_orders :
        kill any open active order
    get_order_status :
        get current status of any order via order ID
    get_active_orders :
        get all open active orders
    get_past_trades :
        get past history of trades placed
    get_trade_volumes :
        get current volume of trades for currencies
    get_available_balances :
        get current available balances in your linked account
    heartbeat :
        test if connection remains to API
    get_symbols :
        get available symbols to trade with via Gemini
    get_ticker :
        get current price of available currencies
    get_current_order_book :
        get current order book on Gemini network
    get_trades_history :
        get history of trades on Gemini
    get_current_auction :
        get current status of exchange auction
    get_auction_history :
        get historical data of exchange auction
    make_timestamp :
        create timestamp to use for API calls
    """

    def __init__(self, key, secret_key, sandbox=True, debug=False):
        self.__key = key
        self.__secret_key = secret_key
        self.__sandbox = sandbox
        self.__debug = debug
        self.__last_order_id = None
        if sandbox:
            self.__url = 'https://api.sandbox.gemini.com/v1/'
        else:
            self.__url = 'https://api.gemini.com/v1/'

    def send_public_request(self, method, **kwargs):
        """Sends all public request to the Gemini server"""
        url = self.__url + method
        paras = list()

        for key in kwargs:
            paras.append('%s=%s' % (key, kwargs[key]))
        if len(paras) is not 0:
            paras_string = '&'.join(paras)
            url = url + '?' + paras_string
        if self.__debug:
            print('URL: ', url)

        return requests.get(url, timeout=10).json()

    def send_private_request(self, method, payload):
        """Sends all private requests to the Gemini server"""
        payload['nonce'] = str(int(time.time() * 100000))
        payload = json.dumps(payload)

        payload_encode = base64.b64encode(bytearray(payload, 'utf-8'))
        sig = hmac.new(bytearray(self.__secret_key, 'utf-8'),
                       payload_encode, hashlib.sha384).hexdigest()
        headers = {'X-GEMINI-APIKEY': self.__key,
                   'X-GEMINI-PAYLOAD': payload_encode,
                   'X-GEMINI-SIGNATURE': sig}
        url = self.__url + method
        if self.__debug:
            print('URL: ', url)
            print('Payload: ', payload)

        return requests.post(url, headers=headers, timeout=10).json()

    def new_order(self, symbol, amount, price, side, option='',
                  client_order_id=False):
        """
        Only limit orders are supported at this point.
        All orders on the exchange are 'Good Until Cancel' - they
        will stay active until either completely filled or cancelled.

        If you wish orders to be automatically cancelled when your
        session ends, see the require heartbeat section, or manually
        send the cancel all session orders message.

        Parameters
        ==========
        client_order_id (string, optional): A client-specified order id.
            This is only for custom purpose, pygem methods which need an
            order_id as input (as for example cancel_order()) always use
            the Gemini order_id, which can be found in the field
            'order_id' of the return.
        symbol : str
            The symbol for the new order
        amount : float
            Quoted decimal amount to purchase
        price : float
            Quoted decimal amount to spend per unit
        side : str
            'buy' or 'sell'
        type : str
            The order type. Only 'exchange limit' supported
            through this API
        option : str (optional)
            An optional order execution option.
            If not given, your order will be a standard limit order,
            it will immediately fill against any open orders at an equal
            or better price, then the remainder of the order will be posted
            to the order book.

            The available limit order options are:
            'maker-or-cancel': This order will only add liquidity to the
                order book. If any part of the order could be filled
                immediately, the whole order will instead be canceled before
                any execution occurs. If that happens, the response back
                from the API will indicate that the order has already been
                canceled ('is_cancelled': True).
            'immediate-or-cancel': This order will only remove liquidity
                from the order book. It will fill whatever part of the
                order it can immediately, then cancel any remaining amount
                so that no part of the order is added to the order book.
                If the order doesn't fully fill immediately, the response
                back from the API will indicate that the order has already
                been canceled ('is_cancelled': True).
            'auction-only': This order will be added to the auction-only
                book for the next auction for this symbol. The order will
                not show up on the public API Current Order Book.
                The order will show up in the private API Get Active Orders
                endpoint. The exchange will cancel any unfilled auction-only
                orders at the end of the auction. The order may be cancelled
                up until the the auction locks, after which cancel requests
                will be rejected.

        Result
        ======
        Result will be the same fields as returned by get_order_status()
        """
        method = 'order/new'
        params = {'request': '/v1/order/new',
                  'symbol': symbol,
                  'type': 'exchange limit'}

        try:
            amount = float(amount)
        except:
            raise TypeError('amount must be a number')
        try:
            price = float(price)
        except:
            raise TypeError('price must be a number')

        if side not in ['buy', 'sell']:
            raise ValueError('side must be either "buy" or "sell"')

        if option and option not in ['maker-or-cancel',
                                     'immediate-or-cancel',
                                     'auction-only']:
            raise ValueError(
                'option must either be empty or one of "maker-or-cancel", \
              "immediate-or-cancel", "auction-only"')

        params['amount'] = str(amount)
        params['price'] = str(price)
        params['side'] = side
        options = list()
        options.append(option)
        if len(option) is not 0:
            params['options'] = options

        if client_order_id is not False:

            if self.last_order_id and not client_order_id > self.last_order_id:
                raise ValueError(
                    'client_order_id is not increasing ( %s !> %s )'
                    % (client_order_id, self.last_order_id))

            self.last_order_id = client_order_id
            params['client_order_id'] = str(client_order_id)

        res = self.send_private_request(method, params)

        return res

    def cancel_order(self, order_id):
        """
        This will cancel an order. If the order is already canceled,
        the message will succeed but have no effect.

        Parameters
        ==========
        order_id: The order ID as given in the field 'order_id' of
            the return of new_order().

        Response
        ========
        Result of order_status for the canceled order. If the order
        was already canceled, then the request will have no effect
        and the status will be returned.
        """
        method = 'order/cancel'
        params = {'request': '/v1/order/cancel',
                  'order_id': str(order_id)}

        res = self.send_private_request(method, params)

        return res

    def cancel_all_session_orders(self):
        """
        This will cancel all orders opened by this session.

        Response
        ========
        The response will be a dictionary with the fields:

        result : str
            Will always be 'ok' if the response from the
            Gemini server is 200 OK.
        details : str
            Dictionary with two fields:
            cancelRejects (list): A list with the id's of the orders,
                which are not canceled.
            cancelledOrders (list): A list with the id's of the canceled
                orders.
        """
        method = 'order/cancel/session'
        params = {'request': '/v1/order/cancel/session'}

        res = self.send_private_request(method, params)

        return res

    def cancel_all_active_orders(self):
        """
        This will cancel all outstanding orders created by all sessions owned
        by this account, including interactive orders placed through the UI.
        Note that this cancels orders that were not placed using this API key.

        Typically cancel_all_session_orders is preferable, so that only orders
        related to the current connected session are cancelled.

        Response
        ========
        The response will be a dictionary with the fields:

        result : str
            Will always be 'ok' if the response from the
            Gemini server is 200 OK.
        details : dict
            Dictionary with two fields:
            cancelRejects (list): A list with the id's of the orders,
                which are not canceled.
            cancelledOrders (list): A list with the id's of the canceled
                orders.
        """
        method = 'order/cancel/all'
        params = {'request': '/v1/order/cancel/all'}

        res = self.send_private_request(method, params)
        return res

    def get_order_status(self, order_id):
        """
        Gets the status for an order.

        Parameters
        ==========
        order_id : The order id to get information on.

        Response
        ========
        order_id : str
            The order id
        client_order_id : str
            The optional client-specified order id
        symbol : str
            The symbol of the order
        exchange : str
            Will always be 'gemini'
        price : str
            The price the order was issued at
        avg_execution_price : str
            The average price at which this order
            as been executed so far.
            0 if the order has not been executed at all.
        side : str
            Either 'buy' or 'sell'.
        type : str
            Will always be 'exchange limit'
        timestamp : str
            The timestamp the order was submitted.
            Note that for compatibility reasons, this is returned
            as a string. We recommend using the timestampms field
            instead.
        timestampms : int
            The timestamp the order was submitted in milliseconds.
        is_live : bool
            True if the order is active on the book (has
            remaining quantity and has not been canceled)
        is_cancelled : bool
            True if the order has been canceled.
            Note the spelling, 'cancelled' instead of 'canceled'.
            This is for compatibility reasons.
        was_forced : bool
            Will always be False.
        executed_amount : str
            The amount of the order that has been filled.
        remaining_amount : str
            The amount of the order that has not been filled.
        original_amount : str
            The originally submitted amount of the order.
        """
        method = 'order/status'
        params = {'request': '/v1/order/status',
                  'order_id': str(order_id)}

        res = self.send_private_request(method, params)
        return res

    def get_active_orders(self):
        """
        Gets all live orders.

        Response
        ========
        A list of orders status as given by get_order_status()
        for all your live orders.
        """
        method = 'orders'
        params = {'request': '/v1/orders'}
        res = self.send_private_request(method, params)
        return res

    def get_past_trades(self, symbol, limit_trades=50, since=None):
        """
        Delivers information about your trades in the past.

        Parameters
        ==========
        symbol : str
            The symbol to retrieve trades for.
        limit_trades : int
            The maximum number of trades to return.
            Default is 50, max is 100 (optional).
        since : int or datetime.datetime
            Only return trades after this timestamp or date (optional).

        Reponse
        =======
        The response will be list of trade information items.

        price : str
            The price that the execution happened at.
        amount : str
            The quantity that was executed.
        timestamp : int
            The time that the trade happened.
        timestampms : int
            The time that the trade happened in milliseconds.
        type : str
            Will be either 'Buy' or 'Sell', indicating
            the side of the original order.
        aggressor : bool
            If True, this order was the taker in the trade.
        fee_currency : str
            Currency that the fee was paid in.
        fee_amount : str
            The amount charged.
        tid : int
            Unique identifier for the trade.
        order_id : str
            The order that this trade executed against.
        client_order_id : str
         The optional client-specified order id that this trade is associated with.
        break : str
            Will only be present if the trade has been
            reversed (broken).
            The field will contain one of these values:
                'manual': The trade was reversed manually. This means that
                    all fees, proceeds, and debits associated with the trade
                    have been credited or debited to the account seperately.
                    That means that this reported trade must be included for
                    order for the account balance to be correct.
                'full': The trade was fully broken. The reported trade should
                    not be accounted for. It will be as though the transfer
                    of fund associated with the trade had simply not happened.
        """
        method = 'mytrades'
        params = {'request': '/v1/mytrades',
                  'symbol': symbol}
        try:
            limit_trades = int(limit_trades)
        except:
            raise TypeError('limit_trades must be an integer')

        if since is None:
            since = ''
        elif isinstance(since, dt.date) or isinstance(since, dt.datetime):
            since = self.make_timestamp(since)
        else:
            try:
                since = int(since)
            except:
                raise TypeError('since must be of type datetime.date, \
                                   datetime.datetime or an integer')
        params['limit_trades'] = limit_trades
        params['timestamp'] = since

        res = self.send_private_request(method, params)

        return res

    def get_trade_volume(self):
        """
        Returns the trade volume.

        Response
        =======
        The response will be a nested list of up to 30 days of
        trade volume for each symbol.

           - Each of the inner lists contains the data for one
               symbol.
           - Each inner list item represents 1 day of trading
               volume. All dates are UTC dates.
           - Partial trading volume for the current day is not
               supplied.
           - Days without trading volume will be omitted from
               the array.

        The list items have the following fields:

        account_id : int
            Client account id.
        symbol : str
            The symbol.
        base_currency : str
            Quantity is denominated in this currency.
        notional_currency : str
            Price is denominated as the amount of notional currency
            per one unit of base currency. Notional values are
            denominated in this currency.
        data_date : str
            UTC date in yyyy-MM-dd format.
        total_volume_base : float
            Total trade volume for this day.
        maker_buy_sell_ratio : float
            Maker buy/sell ratio is the
            proportion of maker base volume on trades where the account
            was on the buy side versus all maker trades.
            If there is no maker base volume on the buy side, then this
            value is 0.
        buy_maker_base : float
            Quantity for this day where the account
            was a maker on the buy side of the trade.
        buy_maker_notional : float
            Notional value for this day where the
            account was a maker on the buy side of the trade.
        buy_maker_count : float
            Number of trades for this day where the
            account was a maker on the buy side of the trade.
        sell_maker_base : float
            Quantity for this day where the account
            was a maker on the sell side of the trade.
        sell_maker_notional : float
            Notional value for this day where the
            account was a maker on the sell side of the trade.
        sell_maker_count : float
            Number of trades for this day where the
            account was a maker on the sell side of the trade.
        buy_taker_base : float
            Quantity for this day where the account was
            a taker on the buy side of the trade.
        buy_taker_notional : float
            Notional value for this day where the
            account was a taker on the buy side of the trade.
        buy_taker_count : float
            Number of trades for this day where the
            account was a taker on the buy side of the trade.
        sell_taker_base : float
            Quantity for this day where the account
            was a taker on the sell side of the trade.
        sell_taker_notional : float
            Notional value for this day where the
            account was a taker on the sell side of the trade.
        sell_taker_count : float
            Number of trades for this day where the
            account was a taker on the sell side of the trade.
        """
        method = 'tradevolume'
        params = {'request': '/v1/tradevolume'}

        res = self.send_private_request(method, params)

        return res

    def get_available_balances(self):
        """
        This will show the available balances in the supported currencies.

        Response
        ========
        A list of elements, with one dictionary per currency. Each dictionary
        has the following fields:

        currency : str
            Currency symbol.
        amount : str
            The current balance.
        available : str
            The amount that is available to trade.
        availableWithdraw : str
            The amount that is available to withdraw.
        type : str
            Allways 'exchange'.
        """
        method = 'balances'
        params = {'request': '/v1/balances'}

        res = self.send_private_request(method, params)

        return res

    def heartbeat(self):
        """
        This will prevent a session from timing out and canceling orders
        if the require heartbeat flag has been set when creating the
        sessions API key. Note that this is only required if no other
        private API requests have been made. The arrival of any message
        resets the heartbeat timer.

        Response
        ========
        result : bool
            Will always be True if the response from the Gemini
            server is 200 OK.
        """
        method = 'heartbeat'
        params = {'request': '/v1/heartbeat'}

        res = self.send_private_request(method, params)

        return res

        # Public request

    def get_symbols(self):
        """Returns a list of all available symbols for trading"""
        return self.send_public_request('symbols')

    def get_ticker(self, symbol):
        """
        Returns information about recent trading activity for the symbol.

        Parameters:
        symbol (string): The symbol to retrieve trading activities for.

        Response:
        bid : str
            The highest bid currently available.
        asks : str
            The lowest ask currently available.
        last : str
            The price of the last executed trade.
        volume : dict
            Information about the last 24 hour volume
            on the exchange. Information is updated every five minutes.
            It will have three fields:

            timestamp : int
                The end of the 24-hour period over which
                volume was measured in milliseconds since UNIX epoch.
            (price symbol, e.g. 'USD') : str
                The volume denominated in the price currency.
            (quantity symbol, e.g. 'BTC') : str
                The volume denominated in the quantity currency.
        """
        method = 'pubticker/' + symbol
        kwargs = dict()

        return self.send_public_request(method, **kwargs)

    def get_current_order_book(self, symbol, limit_bids=50, limit_asks=50):
        """
        This will return the current order book as a dictionary
        of two lists, one of bids, and one of asks.

        Parameters
        ==========
        If a limit is specified on a side, then the orders closest to the
        midpoint of the book will be the ones returned.

        symbol : str
            The symbol to retrieve the order book for.
        limit_bids : int
            Limit the number of bids (offers to buy) returned. Default is 50. May be 0 to
            return the full order book on this side.
        limit_asks : int
            Limit the number of asks (offers to sell) returned.
            Default is 50. May be 0 to return the full order book on this
            side.

        Response
        ========
        The response will be a dicitionary of two dictionaries:

        bids : dict
            The bids currently on the book. These are offers to buy
            at a given price.
        asks : dict
            The asks currently on the book. These are offers to sell
            at a given price

        The bids and the asks are grouped by price, so each entry may represent
        multiple orders at that price. Each element of the list is a dictionary
        with fields:

        price : str
            The price.
        amount : str
            The total quantity remaining at the price.
        timestamp : str
            DO NOT USE - this field is included for
            compatibility reasons only and is just populated with
            a dummy value.
        """
        method = 'book/' + symbol

        try:
            limit_bids = int(limit_bids)
        except:
            raise TypeError('limit_bids must be an interger')
        try:
            limit_asks = int(limit_asks)
        except:
            raise TypeError('limit_asks must be an interger')

        return self.send_public_request(method, limit_bids=limit_bids,
                                        limit_asks=limit_asks)

    def get_trades_history(self, symbol, since=None, limit_trades=50,
                           include_breaks=False, dataframe=True):
        """
        This will return the executed trades. Each request will show
        at most 500 records.

        If no 'since' is specified, then it will show the most recent
        trades; otherwise, it will show the most recent trades that
        occurred after that timestamp.

        Parameters
        ==========
        symbol : str
            The symbol to retrieve the trades for.
        since : int or datetime.datetime (optional)
            Only returns trades after the specified timestamp. If not
            present or empty, will show the most recent orders.
        limit_trades : int
            The maximum number of trades to return. The
            default is 50.
        include_breaks : bool
            Whether to display broken trades.
            False by default.

        Response
        ========
        The response will be a list of dictionaries, sorted by timestamp,
        with the newest trade shown first.

        timestamp : int
            The time that the trade was executed.
        timestampms : int
            The time that the trade was executed in milliseconds.
        tid : int
            The trade ID number.
        price : float
            The price the trade was executed at.
        amount : float
            The amount that was traded.
        exchange : str
            Will always be 'gemini'.
        type : str
            'buy' means that an ask was removed from the book by an
                incoming buy order.
            'sell' means that a bid was removed from the book by an
                incoming sell order.
            'auction' indicates a bulk trade from an auction.

        broken : bool
            Whether the trade was broken or not. Broken
            trades will not be displayed by default; use the
            include_breaks to display them.
        """
        method = 'trades/' + symbol

        try:
            limit_trades = int(limit_trades)
        except:
            raise TypeError('limit_trades must be an interger')
        if include_breaks:
            include_breaks = 'true'
        else:
            include_breaks = 'false'
        if since is None:
            since = ''
        elif isinstance(since, dt.date) or isinstance(since, dt.datetime):
            since = self.make_timestamp(since)
        else:
            try:
                since = int(since)
            except:
                raise TypeError('since must be of type datetime.date, \
                                   datetime.datetime or an integer')

        data = self.send_public_request(method, since=since,
                                        limit_trades=limit_trades,
                                        include_breaks=include_breaks)

        if dataframe is True:
            data = pd.DataFrame(data)
            if len(data) > 0:
                data['amount'] = data['amount'].astype(float)
                data['price'] = data['price'].astype(float)
                data['datetime'] = data['timestamp'].apply(
                    lambda x: dt.datetime.fromtimestamp(x))
                data.set_index('datetime', drop=True, inplace=True)
                data.sort_index(inplace=True)

        return data

    def get_current_auction(self, symbol):
        """
        Returns the current or next action.

        Parameter
        s========
        symbol (string): The symbol to retrieve the auction for.

        Response
        ========
        A dictionary with the following fields:

        closed_until_ms : int
            If the auction is not currently open, show the time at which the
            next auction opens. Not present if the auction has already opened.
        last_auction_eid : int
            After an auction opens, the unique event ID for last specific auction
            event. Changes when an auction event occurs: the auction opens,
            an indicative price is published, and the auction itself runs.
            Not present before the auction opens.
        last_auction_price : str
            If available, show the auction price from the last successful auction
            for this trading pair. Not present after current auction begins publishing indicative prices.
        last_auction_quantity  : str
            If available, show the auction quantity from the last successful auction
            for this trading pair. Not present after current auction begins publishing indicative prices.
        last_highest_bid_price : str
            If available, show the highest bid price from the continuous trading
            order book at the time of the last successful auction for this trading
            pair. Not present after current auction begins publishing indicative prices.
        last_lowest_ask_price : str
            If available, show the lowest ask price from the continuous trading
            order book at the time of the last successful auction for this trading
            pair. Not present after current auction begins publishing indicative prices.
        most_recent_indicative_price : str
            The most recently published indicative price for the auction. Not
            present before the current auction begins publishing indicatives.
        most_recent_indicative_quantity : str
            The most recently published indicative quantity for the auction. Not
            present before the current auction begins publishing indicatives.
        most_recent_highest_bid_price : str
            The most recent highest bid at the time of the indicative price for the auction. Not
            present before the current auction begins publishing indicatives.
        most_recent_lowest_ask_price : str
            The most recent lowest ask at the time of the indicative price for the auction. Not
            present before the current auction begins publishing indicatives.
        next_update_ms : int
            Timestamp in milliseconds of the next event in this auction, either the
            publication of an indicative price/quantity or the auction itself.
        next_auction_ms : int
            Timestamp in milliseconds of when the next auction will run.
        """
        method = 'auction/' + symbol
        return self.send_public_request(method)

    def get_auction_history(self, symbol, since=None, limit_auction_results=50,
                            include_indicative=False):
        """
        This will return the auction events, optionally including publications
        of indicative prices, since the specific timestamp.

        Timestamps are either seconds or milliseconds since the
        epoch (1970-01-01). Each request will show at most 500 records.

        If no since is specified, then it will show the most recent events.
        Otherwise, it will show the oldest auctions that occurred after that
        timestamp.

        Parameters
        ==========
        symbol : str
            The symbol to retrieve the auction for.
        since : int or datetime.datetime (optional)
            Only returns auction events after the specified timestamp. If not
            present or empty, will show the most recent auction events.
        limit_auction_results : int
            The maximum number of auction events to return. The default is 50.
        include_indicative : bool
            Whether to include publication of indicative prices and quantities.
            True by default, True to explicitly enable and False to disable.

        Response
        ========
        The response will be a list of dictionaries, sorted by timestamp, with
        the newest event shown first.

        timestamp : int
            The time that the auction event ran.
        timestampms : int
            The time that the auction event ran in milliseconds.
        auction_id : int
            The auction ID number.
        eid : int
            Unique event ID for this specific auction event.
        event_type : str
            Indicative for the publication of an indicative price or auction for the auction result.
        auction_result : str
            'success' or 'failure', indicating whether the auction has found a price.
        auction_price : str
            If auction_result is success, the price at which orders were filled. Zero if result is failure.
        auction_quantity : str
            If auction_result is success, the quantity that was filled. Zero if result is failure.
        highest_bid_price : str
            Highest bid price from the continuous trading order book at the time of the auction event, if available.
        lowest_ask_price : str
            Lowest ask price from the continuous trading order book at the time of the auction event, if available.
        """
        method = 'auction/%s/history' % symbol

        try:
            limit_auction_results = int(limit_auction_results)
        except:
            raise TypeError('limit_auction_results must be an interger')
        if not include_indicative:
            include_indicative = 'false'
        else:
            include_indicative = 'true'

        if since is None:
            since = '0'
        elif isinstance(since, dt.date) or isinstance(since, dt.datetime):
            since = self.make_timestamp(since)
        else:
            try:
                since = int(since)
            except:
                raise TypeError('since must be of type datetime.date, \
                                    datatime.datetime or an integer')

        return self.send_public_request(
            method,
            since=since,
            limit_auction_results=limit_auction_results,
            include_indicative=include_indicative)

        # Helper functions

    def make_timestamp(self, date):
        """
        Helper function, generates a timestamp in milliseconds from UNIX epoch
        from a datetime.datetime or datetime.date object.
        """
        if isinstance(date, dt.date) and not isinstance(date, dt.datetime):
            delta = date - dt.date(1970, 1, 1)
        elif isinstance(date, dt.date) and isinstance(date, dt.datetime):
            delta = date - dt.datetime(1970, 1, 1, 0, 0, 0, 0)
        else:
            raise TypeError('date must be of type datetime.date \
                               or datetime.datetime')
        return int(delta.total_seconds() * 1000)

