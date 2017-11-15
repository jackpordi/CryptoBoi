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
        return

    def print_currency(self, coin):
        coin_balance = self.btrx.get_balance(coin.value)
        market = 'BTC-' + coin.value + ' price ='
        output = line_new = '{:>6} {:>4} {:>10}{:>12} {:>12} {:>16}'.format("Current", coin.value, "Balance = ",float(coin_balance['result']['Balance']), market, self.get_market_price(coin))
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
                #print('failed, exchange returned ', marketData['result']['MarketName'])


if __name__ == '__main__' :
    bot = Bot()
    bot.runbot()
    #print(bot.get_market_price(Currencies.ETH))
    exit()
