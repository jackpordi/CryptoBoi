#!/usr/bin/env python3

import json
import requests

class API(object):
    
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.api_version = "v1.1"
        self.api_url = "https://bittrex.com/api/"
        self.all_markets = self.update_all_markets()
        self.btc_price = self.update_btc_price()

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
    
    def update_all_markets(self):
        self.all_markets = self.public_query("getmarketsummaries")
        return self.all_markets

    def display_all_markets(self):
        for currency in self.update_all_markets()['result']:
            price_in_btc = currency['Last']
            price_in_usd = price_in_btc * self.btc_price
            to_print = '{:<9} {:<6} {:<13} {:<6} {:<10}'.format(currency['MarketName'],"price:",str(price_in_btc), "USD price =", price_in_usd)
            print(to_print)
            
    
def main():
    api = API("cfa2fe7b52fc446a8c02baed2df9ae32", "80e19ec06bb54a639ff403b2a63d36f4",)
    api.display_all_markets()

if __name__ == '__main__':
    main()

        
