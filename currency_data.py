import json
import requests
from baseCurr import BaseCurrency


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

    def add_pairs(*args):
        self.pairs = []
        for arg in args:
            self.pairs.append(arg)
    
    def update_base_curr_price(self):
        data = requests.get("https://api.coinmarketcap.com/v1/ticker/" + self.base_curr.value).json()
        self.base_curr_price = data[0]['price_usd']

def main():
    allpairs = Pair_Groups()
    allpairs.show_all_base_currs()

#if __name__ == "__main__":
    #main()
