from sklearn import linear_model
import numpy as np
import math
import time
import json
import statsmodels.formula.api as sm
import statsmodels
import datetime
from pandas import read_csv
from matplotlib import pyplot as plt
from matplotlib import ticker as mtick

def load_data(csvname):
    parser = lambda x : datetime.datetime.strptime( x.split('.')[0], "%Y-%m-%dT%H:%M:%S" )
    data = read_csv(csvname, parse_dates=['Time'], header=0,
            names=['Time', 'Last', 'Ask', 'Bid', 'Open Buy Orders', 'Open Sell Orders', 'USD Price', 'Volume'], date_parser=parser, index_col=0)
    return data

def print_json(to_print):
    print(json.dumps(to_print, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    name = 'ETH-LTC'
    base_name, alt_name = name.split('-')[0], name.split('-')[1]
    data = load_data('../Crypto_Data/' + name + '.csv')[-15000:-2000]
    sets = [5] #, 10, 15, 20, 30, 45, 60, 90 ] #300, 720, 3600, 7200]
    base_wallet = 1
    alt_wallet = 0
    history = []
    value_history = []
    sell_price_history = []
    sell_time_history = []
    buy_price_history = []
    buy_time_history = []
    buys = 0
    for j in range(0, len(data) -5 ):
        current_data = data[j:j+5]
        current_stat = {}
        current_stat['Price'] = current_data['Last'][-1]
        for i in sets:
            istat = {}
            data_set = current_data['Last'][-i:]
            result = sm.OLS(data_set, statsmodels.tools.add_constant([x for x in range(1, i + 1)])).fit()
            istat['RegressionCoefficient'] = result.rsquared
            istat['RegressionCoefficientSquared'] = result.rsquared ** 2
            istat['Gradient'] = result.params[1]
            istat['STD'] = data_set.std()
            istat['Mean'] = data_set.mean()
            current_stat['Last' + str(i)] = istat
            #print("\nFor the last", i, "entries:")
            #print("   R Squared Correlation Coefficient:    ", result.rsquared ** 2)
            #print("   R Squared Correlation Coefficient:    ", result.rsquared )
            #print("   Linear Regression Gradient:           ", result.params[0])
            # best_fit_values = [(result.params[1] * x) + result.params[0] for x in range(1, i + 1)]
            # plt.plot(data_set)
            # plt.plot(data_set.index, best_fit_values)
        to_use = 'Last5'
        confidence = current_stat[to_use]['Gradient'] * current_stat[to_use]['RegressionCoefficientSquared'] / current_stat['Price']
        if not np.isinf(confidence):
            if confidence < -0.001:
                if base_wallet != 0:
                    # Sell from ETH to Asset
                    alt_wallet = base_wallet * 0.9975 / (current_stat['Price'] * 1.00005)
                    buys += 1
                    base_wallet = 0
                    buy_price_history.append(current_stat['Price'])
                    buy_time_history.append(current_data.index.values[-1])
            elif confidence > 0.001:
                if alt_wallet != 0:
                    # Sell from Asset back to ETH
                    base_wallet = alt_wallet * current_stat['Price'] * 0.9975 * 0.99995
                    #print("Selling ETH, round =", j)
                    buys += 1
                    alt_wallet = 0
                    sell_price_history.append(current_stat['Price'])
                    sell_time_history.append(current_data.index.values[-1])
            if j % 1440 == 0:
                print("Buy/Sell Confidence: ", confidence)
                print("   At Round:         ", j)
                print("   Mean:             ", current_stat['Last5']['Mean'])
                print("   STD:              ", current_stat['Last5']['STD'])
                print("   No of buys :      ", buys)
                print("   Current " + base_name + " Value:", base_wallet if base_wallet != 0 else alt_wallet * current_stat['Price'])
                print("   Current " + alt_name + " Value:", alt_wallet if alt_wallet != 0 else base_wallet / current_stat['Price'])
                print()
            value_history.append(base_wallet if base_wallet != 0 else alt_wallet * current_stat['Price'])
        else:
            value_history.append(base_wallet if base_wallet != 0 else alt_wallet * current_stat['Price'])
        history.append(current_stat)
    print("No of buys:", buys)
    fig, ax1 = plt.subplots()
    ax1.plot(data['Last'][:-5], 'b', buy_time_history, buy_price_history, 'og', sell_time_history, sell_price_history, 'oy')
    ax2 = ax1.twinx()
    ax2.plot(data[:-5].index, value_history, 'r')
    #ax3 = ax2.twinx()
    #ax3.plot(buy_time_history, buy_price_history, 'og')
    #ax3.plot(sell_time_history, sell_price_history, 'oy')
    #ax4 = ax1.twinx()
    #plt.savefig('test_graphs/' + name + '.png')
    
    plt.show()
