from matplotlib import pyplot as plt
from pandas import datetime, read_csv, Series, DataFrame, date_range
import numpy as np





def load_data(csvname):
    return read_csv(csvname, parse_dates=[0], header=None, index_col=0)

def split_data(data):
    return data

def main():
    # Load data from CSV file
    # Transform data
    # Build model
    # Fit model
    # Use model for prediction
    data = load_data("market-price.csv")
    ax = data.plot(legend='BTC Prices')
    plt.ylabel("Price in USD")
    plt.xlabel("Date")
    ax.legend(["BTC"])
    plt.show()


if __name__ == '__main__':
    main()
