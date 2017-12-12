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
    data = load_data('../Crypto_Data/ETH-LTC.csv')[:-650]
    sets = [5, 10, 15, 20, 30, 45, 60, 90 ] #300, 720, 3600, 7200]
    #sets = [20, 25, 30, 40, 55, 75, 100, 130, 150]
    # for i in sets:
    #     last = data['USD Price'][-i:]
    #     print("For the last", i, "entries:")
    #     print("    Mean:")
    #     print("   ",last.mean())
    #     print("    Standard Deviations:")
    #     print("   ", last.std())
    #     print("    Standard Deviation Relative to Means:")
    #     print("   ", last.std() / last.mean())
    #     print("")
    # diffs = data.pct_change()
    # diffs = diffs.applymap(lambda x: 100 * x)
    # price_changes = diffs['USD Price']
    # for i in sets:
    #     last = diffs['USD Price'][-i:]
    #     print("For the last", i, "entries percentage difference:")
    #     print("    Mean:")
    #     print("   ",last.mean())
    #     print("    Standard Deviations:")
    #     print("   ", last.std())
    #print(price_changes.std())
    #print(price_changes.mean())
    #lm_originals = np.polyfit([x for x in range(1, len(data) + 1)], data['Last'], 1)
    #print(lm_originals)
    eth_wallet = 1
    ltc_wallet = 0
    history = []
    for j in range(5000, 6000): #len(data) - 90):
        current_data = data[j:j+90]
        current_stat = {}
        current_stat['Price'] = current_data['Last'][-1]
        for i in sets:
            istat = {}
            data_set = current_data['Last'][-i:]
            result = sm.OLS(data_set, statsmodels.tools.add_constant([x for x in range(1, i + 1)])).fit()
            istat['RegressionCoefficient'] = result.rsquared
            istat['RegressionCoefficientSquared'] = result.rsquared ** 2
            istat['Gradient'] = result.params[1]
            current_stat['Last' + str(i)] = istat
            #print("\nFor the last", i, "entries:")
            #print("   R Squared Correlation Coefficient:    ", result.rsquared ** 2)
            #print("   R Squared Correlation Coefficient:    ", result.rsquared )
            #print("   Linear Regression Gradient:           ", result.params[0])
            # best_fit_values = [(result.params[1] * x) + result.params[0] for x in range(1, i + 1)]
            # plt.plot(data_set)
            # plt.plot(data_set.index, best_fit_values)
        if current_stat['Last10']['Gradient'] * current_stat['Last10']['RegressionCoefficientSquared'] > 0.00001:
            if eth_wallet != 0:
                print("Buying ETH, round =", j)
                print(eth_wallet)
                print(ltc_wallet)
                print(current_stat['Price'])
                ltc_wallet == eth_wallet / current_stat['Price']
                eth_wallet = 0
                print(eth_wallet)
                print(ltc_wallet)
        elif current_stat['Last10']['Gradient'] * current_stat['Last10']['RegressionCoefficientSquared'] < -0.00001:
            if ltc_wallet != 0:
                print("Selling ETH, round =", j)
                eth_wallet = ltc_wallet * current_stat['Price']
                ltc_wallet == 0
        history.append(current_stat)
        if j % 100 == 0:
            print("At Round: ", j)
            print("Current ETH Value:", eth_wallet)
            print("Current LTC Value:", ltc_wallet)
    #print_json(history)
    plt.show()
