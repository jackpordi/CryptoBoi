#!/usr/bin/python

import datetime
import numpy as np
import csv as csv
import pandas as pd
import tkinter
from dateutil.parser import parse
from matplotlib import pyplot as plt
from matplotlib import style

style.use('ggplot')


def main():
    with open("../Crypto_Data/BTC-ETH.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        time = []
        usd_price = []
        volume = []
        for row in readCSV:
            time.append(datetime.datetime.strptime( row[0].split('.')[0], "%Y-%m-%dT%H:%M:%S" ))
            print(row[0]) 
            usd_price.append(float(row[6]))
            volume.append(float(row[7]))

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(time, usd_price, 'b-')
    ax1.set_ylabel("USD Price of ETH", color='b')
    ax2 = ax1.twinx()
    ax2.plot(time, volume, 'r-')
    ax2.set_ylabel("24Hr Trading Volume of ETH", color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.title("XMR-USD Prices")
    plt.show()



if __name__ == "__main__":
    main()
