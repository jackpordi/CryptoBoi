from pandas import datetime, read_csv, Series, DataFrame, date_range
from sklearn import linear_model
from api_caller import API, get_keys, print_json
import numpy as np
import math
import time
import json
import statsmodels.formula.api as sm
import statsmodels
from matplotlib import pyplot as plt

def load_data(csvname):
    data = read_csv(csvname, parse_dates=[0], header=0,
            names=['Time', 'Last', 'Ask', 'Bid', 'Open Buy Orders', 'Open Sell Orders', 'USD Price', 'Volume'], index_col=0)
    return data

def print_json(to_print):
    print(json.dumps(to_print, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    pubk, privk = get_keys('keys2.txt') 
    api = API(pubk, privk)
    balances = api.get_balances()
    sets = [50] 
    eth_wallet = balances['ETH']['Available']
    try:
        omg_wallet = balances['OMG']['Available']
    except:
        omg_wallet = 0
    name = 'ETH-OMG'
    price_history = []
    value_history = []
    buys = 0
    for i in range(0,49):
        market = api.get_market(name)
        print_json(market)
        price_history.append(market[0]['Last'])
        time.sleep(6)
    print(price_history)
    j = 0
    while True:
        try:
            balances = api.get_balances()
            eth_wallet = balances['ETH']['Available']
            omg_wallet = balances['OMG']['Available']
            market = api.get_market(name)
            api.cancel_all_orders()
            price_history.append(market[0]['Last'])
            current_stat = {}
            current_stat['Price'] = price_history[-1]
            for i in sets:
                istat = {}
                data_set = Series(price_history[-i:])
                result = sm.OLS(DataFrame(data_set), statsmodels.tools.add_constant([x for x in range(1, 50)])).fit()
                #print(result.summary())
                #istat['RegressionCoefficient'] = result.rsquared
                istat['RegressionCoefficientSquared'] = result.rsquared ** 2
                istat['Gradient'] = result.params[1]
                istat['STD'] = data_set.std()
                istat['Mean'] = data_set.mean()
                current_stat['Last' + str(i)] = istat
            to_use = 'Last50'
            confidence = current_stat[to_use]['Gradient'] * current_stat[to_use]['RegressionCoefficientSquared'] / current_stat['Price']
            if not np.isinf(confidence):
                if confidence < -0.001:
                    print("Confidence < -0.001")
                    if eth_wallet > 0.1:
                        print("Selling ETH for OMG, round =", j, "Buy Quantity: ", eth_wallet / current_stat['Price'])
                        order = api.buy_limit(name, eth_wallet * 0.99 / (current_stat['Price'] * 1.00005) , (current_stat['Price'] * 1.005))
                        buys += 1
                        print("Order:  ", order)
                elif confidence > 0.001:
                    print("Confidence > 0.001")
                    if omg_wallet > 0.5 :
                        print("Selling OMG for ETH, round =", j, "Sell Quantity: ", omg_wallet)
                        order = api.sell_limit(name, omg_wallet * 0.99, current_stat['Price'] * 0.99995)
                        buys += 1
                print("Current order UUIDs: ")
                print_json(api.get_open_orders())
                print("Buy/Sell Confidence: ", confidence)
                print("   Price:            ", price_history[-1])
                print("   At Round:         ", j)
                print("   Mean:             ", current_stat['Last5']['Mean'])
                print("   STD:              ", current_stat['Last5']['STD'])
                print("   No of buys :      ", buys)
                print("   Current Actual ETH Count:", eth_wallet)
                print("   Current Actual OMG Count:", omg_wallet)
                print("   Current ETH Value:", eth_wallet if eth_wallet != 0 else omg_wallet * current_stat['Price'])
                print("   Current OMG Value:", omg_wallet if omg_wallet != 0 else eth_wallet / current_stat['Price'])
                print()
                value_history.append(eth_wallet if eth_wallet != 0 else omg_wallet * current_stat['Price'])
            else:
                print("Inf encountered!")
                value_history.append(eth_wallet if eth_wallet != 0 else omg_wallet * current_stat['Price'])
            j += 1
        except:
            pass
        finally:
            time.sleep(6)
    print("No of buys:", buys)
