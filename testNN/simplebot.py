from matplotlib import pyplot as plt
from pandas import datetime, read_csv, Series, DataFrame, date_range
from keras.layers import Dense, Dropout, Activation, LSTM, TimeDistributed, Flatten
from keras.models import Sequential
import numpy as np
import time

def load_data(csvname):
    data = read_csv(csvname, parse_dates=[0], header=0, names=['Date', 'x'], index_col=0)
    start_data = data[0:1]
    differenced_values = [0]
    for i in range(1, len(data) - 1):
        value = ((data['x'][i] - data['x'][i-1]) / data['x'][i]) * 100
        differenced_values.append(value)

    data = data.iloc[1:]
    data['diff'] = Series(differenced_values).values
    #print(data)
    return start_data, data.dropna(axis=0, how='any')

def load_data_max(csvname):
    data = read_csv(csvname, parse_dates=[0], header=0, names=['Date', 'x'], index_col=0)
    start_data = data[0:1]
    differenced_values = []
    for i in range(0, len(data) - 1):
        value = ((data['x'][i + 1] - data['x'][i]) / data['x'][i]) * 100
        differenced_values.append(value)
    differenced_values.append(0)

    data['diff'] = Series(differenced_values).values
    #print(data)
    return start_data, data.dropna(axis=0, how='any')

def main2():
    start_data, data = load_data("simple-prices2.csv")
    print(data.values[-15:])
    btc_wallet = 1
    usd_wallet = 0
    round = 0
    print(data.values[0])
    print("Current OMG: ", btc_wallet, "Current USD: ", usd_wallet)
    for price, delta in data.values:
        #print("Price: ", price, "Delta: ", delta)
        if btc_wallet > 0:
            if delta < 0:
                #print("Selling ETH for USD")
                usd_wallet = btc_wallet * price
                btc_wallet = 0
        elif usd_wallet > 0:
            if delta > 0:
                #print("ETH Price is rising, buying BTC")
                btc_wallet = (usd_wallet / price)
                usd_wallet = 0
        round += 1
        if round % 10 == 0:
            print("Current OMG: ", btc_wallet, "Current USD: ", usd_wallet)
    print("Current OMG: ", btc_wallet, "Current USD: ", usd_wallet)


def main():
    # Loads data from CSV file
    start_data, data = load_data("simple-prices2.csv")
    train_data = data[:-100]
    test_data = data[-100:]
    print(data.shape)
    small_data = data[:10]
    '''
    # Create test and training X and Y data
    train_x = []
    train_y = []
    for i in range(0,50):
        train_x.append(train_data['x/' + str(i)].values)
        train_y.append(train_data['y/' + str(i)].values)
    #print(train_x)
    '''
    # Build model
    model = build_model()
    #print(model.input_shape)
    model.summary()
    # Fit model
    train_x = train_data.values
    print(train_x.shape)
    train_x = np.reshape(train_x, (1, 629, 1))
    print(train_x.shape)
    # #print(train_x)
    train_y = train_data.values
    train_y = np.reshape(train_y, (1, 629, 1))
    # print("shape of training input: ", train_x.shape)
    model.fit(
            train_x,
            train_y,
            batch_size=10,
            epochs=10
            )
    # # Use model for prediction
    # pred = model.predict(np.reshape(test_x[1], (1,50)))
    # print(pred)
    # print(test_y[1])
    # #print(data)
    # ax = data.plot(legend='BTC Prices')
    # plt.ylabel("Price in USD")
    # plt.xlabel("Date")
    # ax.legend(["BTC"])
    # plt.show()

if __name__ == '__main__':
    main2()
