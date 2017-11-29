
from pandas import read_csv
from pandas import datetime, DataFrame, concat, Series
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

# load dataset
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

def timeseries_to_supervised(data, lag=1):
    df = DataFrame(data)
    columns = [df.shift(i) for i in range (1, lag+1)]
    columns.append(df)
    df = concat(columns,axis=1)
    df.fillna(0, inplace=True)
    return df

# create a differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
            value = dataset[i] - dataset[i - interval]
            diff.append(value)
    return Series(diff)

# invert differenced value
def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]

def fit_lstm(train, batch_size, nb_epoch, neurons):
	X, y = train[:, 0:-1], train[:, -1]
	X = X.reshape(X.shape[0], 1, X.shape[1])
	model = Sequential()
	model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
		model.reset_states()
	return model

def forecast(model, batch_size, row):
	X = row[0:-1]
	X = X.reshape(1, 1, len(X))
	yhat = model.predict(X, batch_size=batch_size)
	return yhat[0,0]

def main():
    series = read_csv('shampoo_sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    # summarize first few rows
    print(series.head())
    # line plot
    X = series.values
    differenced = difference(series,1)
    print(differenced.head())
    inverted = []
    for i in range(len(differenced)):
        value = inverse_difference(series,differenced[i],len(series)-i)
        inverted.append(value)
    inverted = Series(inverted)
    print(inverted.head())
    #supervised = timeseries_to_supervised(X,1)
    #print(supervised.head())
    # train, test = X[0:-12], X[-12:]

    # history = [x for x in train]
    # predictions = list()
    # for i in range(len(test)):
    #     #Make prediction
    #     predictions.append(history[-1])
    #     #observation
    #     history.append(test[i])
    # rmse = sqrt(mean_squared_error(test, predictions))
    # print('RMSE: %.f' % rmse)
    # plt.plot(test)
    # plt.plot(predictions)
    # plt.show()

if __name__ == "__main__":
    main()
