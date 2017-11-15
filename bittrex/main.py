#!/usr/bin/env python3
from bittrex import Bittrex, API_V2_0
from enum import Enum
import json

class Currencies(Enum):
    ETH="ETH"
    BTC="BTC"
    #BCC="BCC"
    OMG="OMG"
    ARK="ARK"
    LTC="LTC"

class Bot(object):

    def __init__(self):
        self.btrx = Bittrex("cfa2fe7b52fc446a8c02baed2df9ae32", "80e19ec06bb54a639ff403b2a63d36f4", api_version=API_V2_0)

    def runbot(self):
        while True:
            for coin in Currencies:
                self.print_currency(coin)

    def print_currency(self, coin):
        coin_balance = self.btrx.get_balance(coin.value)
        print("Current ", coin.value, "Balance = ",format(coin_balance['result']['Balance'], 'f').rstrip('0'), " perBTC price = ", self.get_market_price(coin))
    
    def get_market_price(self, coin):
        if coin.value == "BTC":
            return "1.0000"
        else:
            return (self.btrx.get_marketsummary('BTC-' + coin.value)['result']['Last'])


if __name__ == '__main__' :
    bot = Bot()
    #bot.runbot()
    print((bot.btrx.get_marketsummary('BTC-ETH')))
    print(bot.get_market_price(Currencies.ETH))
    exit()
