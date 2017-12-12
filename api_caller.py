#!/usr/bin/env python3

import json
import requests
import time
import hmac
import hashlib
try:
    from urllib import urlencode
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlencode
    from urllib.parse import urljoin

from baseCurr import BaseCurrency
from currency_data import Pair_Group, Pair_Groups, Asset, Trading_Pair

class API(object):
    
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.api_version = "v1.1"
        self.api_url = "https://bittrex.com/api/"
        self.all_markets = self.update_and_get_all_markets()
        self.btc_price = self.update_btc_price()
        self.get_balances()

    def public_query(self, query_type, *args):
        url = self.api_url + self.api_version + '/public/' + query_type
        if args:
            url += '?'
            for arg in args:
                url += arg
        return requests.get(url).json()

    def update_btc_price(self):
        data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/").json()
        self.btc_price = float(data[0]['price_usd'])
        return self.btc_price
    
    def update_and_get_all_markets(self):
        self.all_markets = self.public_query("getmarketsummaries")['result']
        return self.all_markets

    def get_market(self, market):
        return self.public_query("getmarketsummary?market=" + market)['result']
#
    def display_all_markets(self):
        for currency in self.update_and_get_all_markets():
            price_in_btc = currency['Last']
            price_in_usd = price_in_btc * self.btc_price
            to_print = '{:<9} {:<6} {:<13} {:<6} {:<10}'.format(currency['MarketName'],"price:",str(price_in_btc), "USD price =", price_in_usd)
            time.sleep(0.05)
            print(to_print)
    
    def private_query(self, ordertype, params={}):
        nonce = int(time.time()) * 1000
        url = "https://bittrex.com/api/v1.1/" + ordertype
        url += "?apikey=" + self.public_key
        url += "&nonce=" + str(nonce) +'&'
        url += urlencode(params)
        apisign = hmac.new(self.private_key.encode(), url.encode(), hashlib.sha512).hexdigest()
        ret = requests.get(url, headers={'apisign': str(apisign)}).json()['result']
        #print(url)
        return ret

    def get_balances(self):
        self.balances = {}
        res = self.private_query("account/getbalances")
        for asset in res:
            self.balances[asset['Currency']] = asset
        return res

    def get_balance(self, asset):
        res = self.private_query("account/getbalance", params={'currency': asset})
        self.balances[res['Currency']] = res
        return res

    def get_order_history(self, market=None):
        if not market:
            return self.private_query("account/getorderhistory")
        else:
            return self.private_query("account/getorderhistory", params={'market': market})

    def buy_limit(self, market, quantity, rate):
        return self.private_query("market/buylimit", params={'market': market, 'quantity': quantity, 'rate': rate})

    def sell_limit(self, market, quantity, rate):
        return self.private_query("market/sell", params={'market': market, 'quantity': quantity, 'rate': rate})

    def get_order(self, uuid):
        return self.private_query("account/getorder", params={'uuid':uuid})

    def cancel_order(self, uuid):
        return self.private_query("market/cancel", params={'uuid':uuid})

    def get_open_orders(self, market=None):
        if not market:
            return self.private_query("market/getopenorders")
        else:
            return self.private_query("market/getopenorders", params={'market': market})
            
def main():
    api = API("cfa2fe7b52fc446a8c02baed2df9ae32", "80e19ec06bb54a639ff403b2a63d36f4",)
    path = "../Crypto_Data"
    all_data = api.update_and_get_all_markets()
    test_groups = Pair_Groups(all_data)
    test_groups.initialize_all_logs(path)
    try: 
        test_groups.update_all(api.update_and_get_all_markets())
        test_groups.log_all(path)
    except:
        print("API Call Error")

def log_asset():
    api = API("cfa2fe7b52fc446a8c02baed2df9ae32", "80e19ec06bb54a639ff403b2a63d36f4",)
    eth_asset = Asset("ETH")
    btc_asset = Asset("BTC")
    btc_eth_pair = Trading_Pair(btc_asset, eth_asset)
    btc_group = Pair_Group(BaseCurrency.BTC)
    btc_group.add_pairs(btc_eth_pair)
    btc_eth_pair.initialize_log()
    while True:
        btc_eth_pair.update(api.update_and_get_all_markets())
        btc_eth_pair.log()
        time.sleep(60)
        btc_group.update_base_curr_price()

def get_keys(f):
    with open(f, 'r') as file:
        lines =file.readlines()
    return lines[0].replace('\n', ''), lines[1].replace('\n', '')

def print_json(to_print):
    print(json.dumps(to_print, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    #main()
    pubk, privk = get_keys('keys2.txt')
    api = API(pubk, privk,)
    result = api.get_balances()
    buy = api.buy_limit('BTC-LTC', 0.05, 0.01)
    print_json(buy)
    uuid = buy['uuid']
    order = api.get_order(uuid)
    print_json(order)
    all_orders = api.get_open_orders()
    print_json(all_orders)
    api.cancel_order(uuid)
    all_orders = api.get_open_orders()
    print_json(all_orders)

