"""
Library for graphing a stock's price over time.
"""

import datetime as dt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt

def days_since_epoch(date):
    """
    Calculate the number of days since January 1, 1970 from a given date.
    The inverse of date_from_epoch_time.

    Args:
        date: The datetime.date object that 1970-1-1 is to be subtracted from.

    Returns:
        The number of days, in integer form, since January 1, 1970.
    """
    return (date - dt.date(1970, 1, 1)).days


def date_from_epoch_time(num_days):
    """
    Calculate the date that is a given number of days after January 1, 1970.
    The inverse of days_since_epoch.

    Args:
        num_days: The number of days, in integer form, since January 1, 1970.
        The datetime.date object that 1970-1-1 is to be subtracted from.

    Returns:
        The datetime.date object representing the date that is num_days days
        away from January 1, 1970.
    """
    return dt.date(1970, 1, 1) + dt.timedelta(num_days)


def make_color_plot(path, ticker_symbol):
    """
    Create a plot showing the price of a specified stock over time, where
    increases in the price are green and decreases are red.

    Args:
        path: A string containing the path to the CSV file produced by
        stock_info.get_stock_info.
        ticker_symbol: A string of 1-6 uppercase letters representing the
        ticker symbol for the desired stock.

    Returns:
        A colormapped graph of the price (in USD) of the given stock over
        time, labeled in terms of months.
    """
    # Read data from file
    dataframe = pd.read_csv(path)
    x_coords = dataframe['timestamp']

    # Cast to list to use insert function later
    y_coords = list(dataframe['close'])

    # Convert timestamps to date objects
    x_coords = [dt.datetime.strptime(str(value)[0:10], '%Y-%m-%d').date() for
                value in x_coords]

    epoch_offset = days_since_epoch(x_coords[0])

    days_covered = (x_coords[len(x_coords)-1] - x_coords[0]).days

    # Adds data points for weekends where stock prices remain constant
    # but time continues.
    for index in range(days_covered - 1):
        if (days_since_epoch(x_coords[index]) != days_since_epoch(
                x_coords[index+1]) - 1):
            x_coords.insert(index + 1, date_from_epoch_time(
                days_since_epoch(x_coords[index]) + 1))
            y_coords.insert(index + 1, y_coords[index])

    # Make a copy of x_coords that is integers, not date objects
    x_coords_ints = np.linspace(epoch_offset, epoch_offset + days_covered,
                                len(x_coords))

    # Get the first derivative of our data to use when
    # determining the color of the line segment
    slope = np.diff(y_coords)

    # Create colormapping arguments
    colormap = ListedColormap(['r', 'g'])
    norm = BoundaryNorm([-1, 0], colormap.N)

    points = np.array([x_coords_ints, y_coords]).T.reshape((-1, 1, 2))
    segments = np.concatenate((points[:-1], points[1:]), axis=1)

    # Create the line collection object, setting the colormapping parameters.
    # Have to set the actual values used for colormapping separately.
    line_collection = LineCollection(segments, cmap=colormap, norm=norm)
    line_collection.set_array(slope)
    line_collection.set_linewidth(2)

    # Make the background of the graph white so we can read text
    # in dark mode. Must be first.
    plt.figure(figsize=(12, 6), dpi=100, facecolor="white")

    # Add the colored line segments to the graph
    plt.gca().add_collection(line_collection)

    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title(f"{ticker_symbol}")
    plt.plot(x_coords, y_coords, ".", color='black', markersize=1)
    plt.show()
