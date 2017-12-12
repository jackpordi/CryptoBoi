from matplotlib import pyplot as plt
from pandas import datetime, read_csv, Series, DataFrame, date_range
from keras.layers import Dense, Dropout, Activation, LSTM, TimeDistributed, Flatten
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
    data['x'] = Series(differenced_values).values
    #print(data)
    for i in range(0,50):
        data['x/' + str(i)] = data['x'].shift(-i)
    for i in range(0,50):
       data['y/' + str(i)] = data['x'].shift(-(i + 50))
    data = data.drop('x', 1)
    return start_data, data.dropna(axis=0, how='any')

def build_model():
    model = Sequential()

    model.add(LSTM(
        50,
        input_shape=(530, 50),
        activation='sigmoid',
        return_sequences=True
        ))

    #model.add(Dense(50))

    # model.add(LSTM(
    #     50,
    #     input_shape=(530,50),
    #     return_sequences=True
    #     ))

    # model.add(Dropout(0.1))

    model.add(LSTM(
        50,
        return_sequences=True
        ))

    # model.add(Dropout(0.1))
    

    #model.add(Dense(
    #    input_shape=(530,50),
    #    units=50,
    #    activation='sigmoid'
    #    ))


    start=time.time()
    model.compile(loss='mse', optimizer='rmsprop')
    print("Model Compilation time:", time.time() - start, 'seconds')

    return model

def main():
    # Loads data from CSV file
    start_data, data = load_data("market-price.csv")
    train_data = data[:-100]
    test_data = data[-100:]
    test_x = test_data.values[:,:50]
    test_y = test_data.values[:,-50:]
    #print(test_x.shape)
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
    train_x = train_data.values[:,:50]
    #print(train_x.shape)
    train_x = np.reshape(train_x, (1, 1, 530, 50))
    #print(train_x.shape)
    #print(train_x)
    train_y = train_data.values[:,-50:]
    train_y = np.reshape(train_y, (1, 530, 50))
    print("shape of training input: ", train_x.shape)
    model.fit(
            train_x,
            train_y,
            batch_size=10,
            epochs=100,
            validation_split=0
            )
    # Use model for prediction
    #pred = model.predict(np.reshape(test_x[1], (1,1,50)))
    #print(pred)
    print(test_y[1])
    #print(data)
    ax = data.plot(legend='BTC Prices')
    # plt.ylabel("Price in USD")
    # plt.xlabel("Date")
    # ax.legend(["BTC"])
    # plt.show()

if __name__ == '__main__':
    main()
