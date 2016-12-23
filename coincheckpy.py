# -*- coding: utf-8 -*-
""" COINCHECK API wrapper """

"""
AUTHOR: @jimako1989
GITHUB: github.com/jimako1989/coincheckpy
LICENSE: MIT
"""

import json,time,hmac,hashlib,requests,datetime
import pandas as pd
from decimal import *
getcontext().prec = 8

"""EndpointsMixin provides a mixin for the API instance """
class EndpointsMixin(object):

    """Public API"""
    def ticker(self, **params):
        """ Get a tick
        Docs: https://coincheck.com/documents/exchange/api#ticker
        """
        endpoint = 'api/ticker'
        return self.request(endpoint, auth=False, params=params)

    def public_trades(self, **params):
        """ Get public trades
        Docs: https://coincheck.com/documents/exchange/api#public-trades
        """
        endpoint = 'api/trades'
        return self.request(endpoint, auth=False, params=params)

    def order_book(self, **params):
        """ Get order books
        Docs: https://coincheck.com/documents/exchange/api#order-book
        """
        endpoint = 'api/order_books'
        return self.request(endpoint, auth=False, params=params)

    def order_rate(self, order_type, pair, **params):
        """ Get order rate
        Docs: https://coincheck.com/documents/exchange/api#order-rate
        """
        params['order_type'] = order_type
        params['pair'] = pair

        endpoint = 'api/exchange/orders/rate'
        return self.request(endpoint, auth=False, params=params)

    def buy_rate(self, pair, **params):
        """ Get buy rate
        Docs: https://coincheck.com/documents/exchange/api#buy-rate
        """
        params['pair'] = pair

        endpoint = 'api/rate/' + pair
        return self.request(endpoint, auth=False, params=params)        

    """ Private API """
    """ Order """
    def order_new(self, pair, order_type, **params):
        """ Create a new order
        Docs: https://coincheck.com/documents/exchange/api#order-new
        """
        params['pair'] = pair
        params['order_type'] = order_type

        if (order_type == "buy" or order_type == "sell") and 'rate' not in params and 'amount' not in params:
            raise InputError(['rate', 'amount'], order_type)
        if order_type == "market_buy" and 'market_buy_amount' not in params:
            raise InputError('market_buy_amount', order_type)
        if (order_type == "market_sell" or order_type == "leverage_buy" or order_type == "leverage_sell") and 'amount' not in params:
            raise InputError('amount', order_type)
        if (order_type == "close_long" or order_type == "close_short") and 'amount' not in params and 'positions' not in params:
            raise InputError(['amount', 'positions'], order_type)

        endpoint = 'api/exchange/orders'
        return self.request(endpoint, method='POST', params=params)

    def order_opens(self, **params):
        """ Get open orders
        Docs: https://coincheck.com/documents/exchange/api#order-opens
        """
        endpoint = 'api/exchange/orders/opens'
        return self.request(endpoint, params=params)

    def order_cancel(self, order_id, **params):
        """ Cancel an order
        Docs: https://coincheck.com/documents/exchange/api#order-cancel
        """
        params['id'] = order_id
        endpoint = 'api/exchange/orders/'+str(order_id)
        return self.request(endpoint, method='DELETE', params=params)

    def order_transactions(self, **params):
        """ Get your transactions
        Docs: https://coincheck.com/documents/exchange/api#order-transactions
        """
        endpoint = 'api/exchange/orders/transactions'
        return self.request(endpoint, params=params)

    def order_positions(self, **params):
        """ Get your leverage position list
        Docs: https://coincheck.com/documents/exchange/api#order-positions
        """
        endpoint = 'api/exchange/leverage/positions'
        return self.request(endpoint ,params=params)

    """ Account """
    def account_balance(self, **params):
        """ Check your balance
        Docs: https://coincheck.com/documents/exchange/api#account-balance
        """
        endpoint = 'api/accounts/balance'
        return self.request(endpoint, params=params)

    def account_leverage_balance(self, **params):
        """ Check your leverage balance
        Docs: https://coincheck.com/documents/exchange/api#account-leverage-balance
        """
        endpoint = 'api/accounts/leverage_balance'
        return self.request(endpoint, params=params)

    def account_sendmoney(self, address, amount, **params):
        """ Send money
        Docs: https://coincheck.com/documents/exchange/api#account-sendmoney
        """
        params['address'] = address
        params['amount'] = amount
        endpoint = 'api/send_money'
        return self.request(endpoint,method='POST', params=params)

    def account_sends(self, currency, **params):
        """ Get the history of sent money
        Docs: https://coincheck.com/documents/exchange/api#account-sends
        """
        params['currency'] = currency
        endpoint = 'api/send_money'
        return self.request(endpoint, params=params)

    def account_deposits(self, currency, **params):
        """ Get the history of deposit money
        Docs: https://coincheck.com/documents/exchange/api#account-deposits
        """
        params['currency'] = currency
        endpoint = 'api/deposit_money'
        return self.request(endpoint, params=params)

    def account_deposits_fast(self, order_id, **params):
        """ Fast withdrawal
        Docs: https://coincheck.com/documents/exchange/api#account-deposits-fast
        """
        params['id'] = order_id
        endpoint = 'api/deposit_money/'+str(order_id)+'/fast'
        return self.request(endpoint, method='POST', params=params)

    def account_info(self, **params):
        """ Get account info.
        Docs: https://coincheck.com/documents/exchange/api#account-info
        """
        endpoint = 'api/accounts'
        return self.request(endpoint, params=params)

    """ Withdrawal """
    def bank_accounts(self, **params):
        """ Get bank accounts
        Docs: https://coincheck.com/documents/exchange/api#bank-accounts
        """
        endpoint = 'api/bank_accounts'
        return self.request(endpoint, params=params)

    def bank_accounts_create(self, bank_name, branch_name, bank_account_type, number, name, **params):
        """ Create a bank account
        Docs: https://coincheck.com/documents/exchange/api#bank-accounts-create
        """
        endpoint = 'api/bank_accounts'
        return self.request(endpoint, method='POST', params=params)

    def bank_accounts_destroy(self, bank_id, **params):
        """ Destroy a bank account
        Docs: https://coincheck.com/documents/exchange/api#bank-accounts-destroy
        """
        endpoint = 'api/bank_accounts/'+str(bank_id)
        return self.request(endpoint, method='DELETE', params=params)

    def withdraws(self, **params):
        """ Get the history of withdraws
        Docs: https://coincheck.com/documents/exchange/api#withdraws
        """
        endpoint = 'api/withdraws'
        return self.request(endpoint, params=params)

    def withdraws_create(self, bank_account_id, amount, currency, is_fast=False, **params):
        """ Apply the withdrawal
        Docs: https://coincheck.com/documents/exchange/api#withdraws-create
        """
        params['bank_account_id'] = bank_account_id
        params['amount'] = amount
        params['currency'] = currency
        params['is_fast'] = is_fast
        endpoint = 'api/withdraws'
        return self.request(endpoint, method='POST', params=params)

    def withdraws_destroy(self, withdrawal_id, **params):
        """ Destroy a withdrawal
        Docs: https://coincheck.com/documents/exchange/api#withdraws-destroy
        """
        params['id'] = withdrawal_id
        endpoint = 'api/withdraws'+str(withdrawal_id)
        return self.request(endpoint, method='DELETE', params=params)

    """ Borrow """
    def create_borrow(self, amount, currency, **params):
        """ Create a borrow
        Docs: https://coincheck.com/documents/exchange/api#create-borrow
        """
        params['amount'] = amount
        params['currency'] = currency
        endpoint = 'api/lending/borrows'
        return self.request(endpoint, method='POST', params=params)

    def read_borrow_matches(self, **params):
        """ Get the list of borrows
        Docs: https://coincheck.com/documents/exchange/api#read-borrow-matches
        """
        endpoint = 'api/lending/borrows/matches'
        return self.request(endpoint, params=params)

    def create_repay(self, repay_id, **params):
        """ Repayment
        Docs: https://coincheck.com/documents/exchange/api#create-repay
        """
        params['id'] = repay_id
        endpoint = 'api/lending/borrows/'+str(repay_id)+'/repay'
        return self.request(endpoint, method='POST', params=params)

    """ Transfer """
    def transfers_to_leverage(self, amount, currency, **params):
        """ Transfers to your leverage account from your spot account.
        Docs: https://coincheck.com/documents/exchange/api#transfers-to-leverage
        """
        params['amount'] = amount
        params['currency'] = currency
        endpoint = 'api/exchange/transfers/to_leverage'
        return self.request(endpoint, method='POST', params=params)

    def transfers_from_leverage(self, amount, currency, **params):
        """ Transfers to your spot account from your leverage account.
        Docs: https://coincheck.com/documents/exchange/api#transfers-from-leverage
        """
        params['amount'] = amount
        params['currency'] = currency
        endpoint = 'api/exchange/transfers/from_leverage'
        return self.request(endpoint, method='POST', params=params)

    """ Get the historical prices of JPY/BTC """
    def get_prices(self, term):
        response = requests.get("https://coincheck.com/exchange/chart.json?line=true&term="+str(term)).json()['chart']
        datetimeIndex = [pd.Timestamp(datetime.datetime.fromtimestamp(r[0]/1000.0)) for r in response]
        rates = [int(r[1]) for r in response]
        series = pd.Series(rates, index=datetimeIndex)
        return(series)

    """ Get the depth of BTC trading """
    def get_depth(self):
        response = requests.get("https://coincheck.com/exchange/depth_chart.json").json()['chart']
        return(response['buy'], response['sell'])

""" Provides functionality for access to core COINCHECK API calls """

class API(EndpointsMixin, object):
    def __init__(self, environment='live', key=None, secret_key=None):
        """ Instantiates an instance of CoincheckPy's API wrapper """

        if environment == 'live':
            self.api_url = 'https://coincheck.com'
        else:
            # for future, access to a demo account.
            pass

        self.key = key
        self.secret_key = bytes(secret_key, 'ascii')

        self.client = requests.Session()

    def request(self, endpoint, method='GET', auth=True, params=None):
        """ Returns dict of response from Coincheck's open API """

        self.nonce = str(int(time.time() * 10000))

        url = '%s/%s' % ( self.api_url, endpoint)

        request_args = {}

        method = method.lower()
        params = params or {}

        if 'amount' in params:
            params['amount'] = str(params['amount'])
        if 'rate' in params:
            params['rate'] = str(params['rate'])

        request_args['headers'] = params
        if method == 'get' or method == 'post':
            if type(params) is dict:
                url_endpoint = "?"
            for (key, value) in params.items():
                url_endpoint += str(key) + "=" + str(value) + "&"
            url += url_endpoint[:-1]
        elif method == 'delete':
            pass

        if auth:
            message = bytes(self.nonce + url, 'ascii')
            signature = hmac.new(self.secret_key, msg=message, digestmod=hashlib.sha256).hexdigest()
            headers = {
                "Content-Type":"application/json",\
                "ACCESS-KEY":self.key,\
                "ACCESS-NONCE":self.nonce,\
                "ACCESS-SIGNATURE":signature
            }
            request_args['headers'].update(headers)

        func = getattr(self.client, method)
        try:
            response = func(url, **request_args)
        except requests.RequestException as e:
            print (str(e))

        content = response.json()

        # error message
        if response.status_code >= 400:
            raise CoincheckError(response.status_code,content)

        return content


"""HTTPS Streaming"""
class Streamer():
    """ Provides functionality for HTTPS Streaming """

    def __init__(self, environment='live', heartbeat=1.0):
        """ Instantiates an instance of CoincheckPy's streaming API wrapper. """

        if environment == 'live':
            self.api_url = 'https://coincheck.com/api/ticker'
        else:
            # for future, access to a demo account.
            pass

        self.heartbeat = heartbeat

        self.client = requests.Session()


    def start(self, **params):
        """ Starts the stream with the given parameters """
        self.connected = True

        request_args = {}

        content_ = {'last':None,'bid':None,'volume':None,'ask':None,'low':None,'high':None}

        while self.connected:
            response = self.client.get(self.api_url, **request_args)
            content = response.content.decode('ascii')
            content = json.loads(content)

            if response.status_code != 200:
                self.on_error(content)

            self.on_success(content)

            time.sleep(self.heartbeat)

    def on_success(self, content):
        """ Called when data is successfully retrieved from the stream """
        print(content)
        return True

    def on_error(self, content):
        """ Called when stream returns non-200 status code
        Override this to handle your streaming data.
        """
        self.connected = False
        return


""" Contains COINCHECK exception """
class CoincheckError(Exception):
    """ Generic error class, catches coincheck response errors
    """

    def __init__(self, status_code, error_response):
        msg = "COINCHECK API returned error code %s (%s) " % (status_code, error_response['error'])

        super(CoincheckError, self).__init__(msg)

""" Parameter input exception """
class InputError(Exception):
    def __init__(self, must_parameters, order_type):
        self.must_parameters = must_parameters
        self.order_type = order_type
    def __str__(self):
        if type(must_parameters) == str:
            return "Parameter: %s is needed if the order type is %s."%(must_parameters, order_type)
        elif type(must_parameters) == list:
            return "Parameters: %s are needed if the order type is %s."%(str(must_parameters), order_type)
