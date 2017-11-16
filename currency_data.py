import json
import csv
import os
import requests
from datetime import datetime
from baseCurr import BaseCurrency


class Asset(object):

    def __init__(self, asset_name):
        self.asset = asset_name
        self.markets = set()
    def __str__(self):
        return self.asset
    def __add__(self, other):
        return str(self) + other
    def __radd__(self, other):
        return other + str(self)

    def add_pairs(self, *pairs):
        for pair in pairs:
            self.markets.add(pair)

class Pair_Groups(object):

    def __init__(self, rawjson):
        self.btc_pairs = Pair_Group(BaseCurrency.BTC)
        self.eth_pairs = Pair_Group(BaseCurrency.ETH)
        self.usdt_pairs = Pair_Group(BaseCurrency.USDT)
        self.allpairs = [self.btc_pairs, self.eth_pairs, self.usdt_pairs]
        #print(rawjson)
        for pair in rawjson:
            market_name = pair['MarketName']
            print(market_name)
            base_quote= market_name.split("-")
            base = base_quote[0]
            quote= base_quote[1]
            if base == 'BTC':
                #print(market_name + " is a BTC Pair")
                self.btc_pairs.add_pairs([pair, base, quote])
            elif base == 'ETH':
                #print(market_name + " is an ETH Pair")
                self.eth_pairs.add_pairs([pair, base, quote])
            elif base == 'USDT':
                #print(market_name + " is a USDT Pair")
                self.usdt_pairs.add_pairs([pair, base, quote])
            else:
                print("Error! Not a BTC, ETH, or USDT Pair:" + pair['MarketName'])

    def show_all_base_currs(self):
        for pair in self.allpairs:
           pair.update_base_curr_price()
           print(pair.base_curr.value + "-$ = " + pair.base_curr_price)

    def update_all(self, data):
        self.btc_pairs.update_group(data)
        self.eth_pairs.update_group(data)
        self.usdt_pairs.update_group(data)

    def log_all(self):
        self.btc_pairs.log_group()
        self.eth_pairs.log_group()
        self.usdt_pairs.log_group()

    def initialize_all_logs(self):
        self.btc_pairs.initialize_logs()
        self.eth_pairs.initialize_logs()
        self.usdt_pairs.initialize_logs()

    def show_all(self):
            self.btc_pairs.show_members()
            self.eth_pairs.show_members()
            self.usdt_pairs.show_members()


class Pair_Group(object):

    def __init__(self, base_curr):
        self.base_curr = base_curr
        self.pairs = []
        self.update_base_curr_price()

    def add_pairs(self, *args):
        self.pairs = []
        for arg in args:
            new_trading_pair = Trading_Pair(arg[1], arg[2])
            self.pairs.append(new_trading_pair)
            new_trading_pair.add_to_group(self)
    
    def update_base_curr_price(self):
        data = requests.get("https://api.coinmarketcap.com/v1/ticker/" + self.base_curr.value).json()
        self.base_curr_price = float(data[0]['price_usd'])

    def get_base_usd_price(self):
        return self.base_curr_price
    def update_group(self, data):
        for pair in self.pairs:
            pair.update(data)

    def log_group(self):
        for pair in self.pairs:
            pair.log()

    def show_members(self):
        for pair in self.pairs:
            print (pair.market_name + " is a member of " + self.base_curr.value)

    def initialize_logs(self):
        for pair in self.pairs:
            pair.initialize_logs()

class Trading_Pair(object):
    
    def __init__(self, base_asset, quote_asset):
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.market_name = base_asset + "-" + quote_asset

    def update(self, data):
        for dataset in data:
            #print(dataset['MarketName'] + " == " + self.market_name)
            if dataset['MarketName'] == self.market_name:
                self.data = dataset
                return

    def add_to_group(self, group):
        self.parent_group = group

    def initialize_log(self):
        log_file_name = "AssetLogs/" + self.market_name + ".csv"
        if not os.path.isfile(log_file_name):
            log_file = open(log_file_name, "a+")
            writer = csv.writer(log_file)
            writer.writerow(["Time", "BasePrice", "USDPrice", "24Hr USD Volume"])
            log_file.close()

    def log(self):    
        log_file = open("AssetLogs/" + self.market_name + ".csv", "a+")
        writer = csv.writer(log_file)
        current_time =  datetime.now() # Time
        price = self.data['Last']
        usd_price = price * self.parent_group.get_base_usd_price()
        usd_volume = self.parent_group.get_base_usd_price() * self.data['BaseVolume']
        print(current_time, price, usd_price, usd_volume)
        # Timestamp, Price, to USD Price, 24Hr Volume
        writer.writerow([current_time, price, usd_price, usd_volume])
        log_file.close()

def main():
    allpairs = Pair_Groups()
    allpairs.show_all_base_currs()

# if __name__ == "__main__":
#     eth_asset = Asset("ETH")
#     btc_asset = Asset("BTC")
#     btc_eth_pair = Trading_Pair(btc_asset, eth_asset)
#     btc_group = Pair_Group(BaseCurrency.BTC)
#     btc_group.add_pairs(btc_eth_pair)
#     btc_eth_pair.log()
#     print(btc_eth_pair.market_name)
#     print(datetime.now())
