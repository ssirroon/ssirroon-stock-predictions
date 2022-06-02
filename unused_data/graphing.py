import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import datetime as dt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

def make_stock_plot(path, ticker_symbol):
    """
    [Old function] 
    Graph the price of a given stock over a time interval.

    Args:
        path: A string showing the path to the CSV file created by 
        stock_info.get_stock_info.
        ticker_symbol: A string of 1-4 uppercase letters representing the
        ticker symbol for the desired stock.

    Returns:
        A graph of the price (in USD) of the given stock over time, labeled
        in terms of months.
    """
    dataframe = pd.read_csv(path)
    x_coords = dataframe['timestamp']
    y_coords = dataframe['close']

    x_coords = [dt.datetime.strptime(str(value)[0:10],'%Y-%m-%d').date()
                for value in x_coords]

    plt.figure(facecolor="white")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title(f"{ticker_symbol}")

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_tick_params(rotation = 30)
    plt.plot(x_coords,y_coords)
    plt.gcf().autofmt_xdate()
    plt.show()
    return