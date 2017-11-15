#!/usr/bin/env python3
from bittrex import Bittrex, API_V2_0
from enum import Enum
import json
import requests

class Currencies(Enum):
    BTC="BTC"
    ETH="ETH"
    BCC="BCC"
    OMG="OMG"
    ARK="ARK"
    LTC="LTC"

class Bot(object):

    def __init__(self):
        self.btrx = Bittrex("cfa2fe7b52fc446a8c02baed2df9ae32", "80e19ec06bb54a639ff403b2a63d36f4", api_version=API_V2_0)

    def runbot(self):
        while True:
            self.update_btc_price()
            for coin in Currencies:
                self.print_currency(coin)
        return

    def update_btc_price(self):
        data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/").json()
        #print(data[0]['price_usd'])
        self.btc_price = data[0]['price_usd']
        return

    def print_currency(self, coin):
        coin_balance = self.btrx.get_balance(coin.value)
        market = 'BTC-' + coin.value + ' price ='
        marketprice = self.get_market_price(coin)
        usd_price = float(marketprice) * float(self.btc_price)
        output = '{:>6}{:>4} {:>10}{:>12} {:>8} {:>10} {:>8} {:>12}'.format("Current", coin.value, "Balance = ",float(coin_balance['result']['Balance']), market, marketprice, "Price in USD =", usd_price)
        print(output)
        #print("Current", coin.value, "Balance = ",float(coin_balance['result']['Balance']), "perBTC price = ", self.get_market_price(coin))
    
    def get_market_price(self, coin):
        if coin.value == "BTC":
            return "1.0000"
        else:
            while True:
                marketData = self.btrx.get_marketsummary('BTC-' + coin.value)
                if marketData['result']['MarketName'] == 'BTC-' + coin.value:
                    return marketData['result']['Last']
                print('failed, exchange returned ', marketData['result']['MarketName'])


if __name__ == '__main__' :
    bot = Bot()
    bot.runbot()
    #print(bot.get_market_price(Currencies.ETH))
    exit()
