from pandas import datetime, read_csv, Series, DataFrame, date_range
from sklearn import linear_model
import numpy as np
import math
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
    name = 'ETH-OMG'
    data = load_data('../Crypto_Data/' + name + '.csv')[-20040:-600]
    sets = [5] #, 10, 15, 20, 30, 45, 60, 90 ] #300, 720, 3600, 7200]
    fig, ax1 = plt.subplots()
    ax1.plot(data['Last'][:-5], 'b')
    eth_wallet = 1
    ltc_wallet = 0
    history = []
    value_history = []
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
                if eth_wallet != 0:
                    #print("Buying ETH, round =", j)
                    ltc_wallet = eth_wallet * 0.9975 / (current_stat['Price'] * 1.0005)
                    buys += 1
                    eth_wallet = 0
            elif confidence > 0.001:
                if ltc_wallet != 0:
                    eth_wallet = ltc_wallet * current_stat['Price'] * 0.9975 * 0.9995
                    #print("Selling ETH, round =", j)
                    buys += 1
                    ltc_wallet = 0
            if j % 1440 == 0:
                print("Buy/Sell Confidence: ", confidence)
                print("   At Round:         ", j)
                print("   Mean:             ", current_stat['Last5']['Mean'])
                print("   STD:              ", current_stat['Last5']['STD'])
                print("   No of buys :      ", buys)
                print("   Current ETH Value:", eth_wallet if eth_wallet != 0 else ltc_wallet * current_stat['Price'])
                print("   Current LTC Value:", ltc_wallet if ltc_wallet != 0 else eth_wallet / current_stat['Price'])
                print()
            value_history.append(eth_wallet if eth_wallet != 0 else ltc_wallet * current_stat['Price'])
        else:
            value_history.append(eth_wallet if eth_wallet != 0 else ltc_wallet * current_stat['Price'])
        history.append(current_stat)
    print("No of buys:", buys)
    ax2 = ax1.twinx()
    ax2.plot(data[:-5].index, value_history, 'r')
    plt.savefig('test_graphs/' + name + '.png')
    plt.show()
