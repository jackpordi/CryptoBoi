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

    def __init__(self, *args):
        self.btc_pairs = Pair_Group(BaseCurrency.BTC)
        self.eth_pairs = Pair_Group(BaseCurrency.ETH)
        self.usdt_pairs = Pair_Group(BaseCurrency.USDT)
        self.allpairs = [self.btc_pairs, self.eth_pairs, self.usdt_pairs]

    def show_all_base_currs(self):
        for pair in self.allpairs:
           pair.update_base_curr_price()
           print(pair.base_curr.value + "-$ = " + pair.base_curr_price)

class Pair_Group(object):

    def __init__(self, base_curr):
        self.base_curr = base_curr
        self.pairs = []
        self.update_base_curr_price()

    def add_pairs(self, *pairs):
        self.pairs = []
        for pair in pairs:
            self.pairs.append(pair)
            pair.add_to_group(self)
    
    def update_base_curr_price(self):
        data = requests.get("https://api.coinmarketcap.com/v1/ticker/" + self.base_curr.value).json()
        self.base_curr_price = float(data[0]['price_usd'])

    def get_base_usd_price(self):
        return self.base_curr_price

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
        print(self.data)

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
