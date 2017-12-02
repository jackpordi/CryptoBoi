from matplotlib import pyplot as plt
from pandas import datetime, read_csv, Series, DataFrame, date_range
from keras.layers import Dense, Dropout, Activation, LSTM
from keras.models import Sequential
import numpy as np
import time

def load_data(csvname):
    data = read_csv(csvname, parse_dates=[0], header=None, names=['Date', 'x'], index_col=0)
    start_data = data[0:1]
    differenced_values = []
    for i in range(0, len(data) - 1):
        value = ((data['x'][i + 1] - data['x'][i]) / data['x'][i]) * 100
        differenced_values.append(value)
    #print(differenced_values)

    data = data.iloc[1:]
    data['t'] = Series(differenced_values).values
    #print(data)
    for i in range(1,51):
        data['x/' + str(i)] = data['t'].shift(-i)
    for i in range(51,101):
       data['y/' + str(i - 50)] = data['t'].shift(-i)
    return start_data, data.dropna(axis=0, how='any')

def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_shape=(None, layers[0]),
        units=layers[1],
        return_sequences=True
        ))

    model.add(Dropout(0.1))

    model.add(LSTM(
        layers[2],
        return_sequences=False
        ))

    model.add(Dropout(0.1))

    model.add(Dense(
        units=layers[3]
        ))

    model.add(Activation('tanh'))

    start=time.time()
    model.compile(loss='mse', optimizer='rmsprop')
    print("Model Compilation time:", time.time() - start, 'seconds')

    return model

def main():
    # Loads data from CSV file
    start_data, data = load_data("market-price.csv")
    train_data = data[:-100]
    test_data = data[-100:]
    print(test_data['x'])
    '''
    # Build model
    model = build_model([1, 50, 100, 1])
    # Fit model
    model.fit(
            train_data['Date'],
            train_data['t'],
            batch_size=50,
            nb_epochs=1,
            validation_split=0.05
            )
    # Use model for prediction
    #print(data)
    ax = data.plot(legend='BTC Prices')
    plt.ylabel("Price in USD")
    plt.xlabel("Date")
    ax.legend(["BTC"])
    plt.show()
    '''


if __name__ == '__main__':
    main()
