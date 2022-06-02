"""
This library contains all of our unit tests for our functions.
"""
import datetime
import pytest
from generate_results import str_to_list
from graphing.graph_stock_info import (
    days_since_epoch,
    date_from_epoch_time
)
from reddit.pmaw_api import (
    find_tickers,
    find_qmarks,
    find_long,
    find_short,
    str_create_timestamp,
    remove_dupes
)

# Scraping and analyzing Alpaca data

from stock_info.pull_stock_info import get_datetime

find_tickers_cases = [
    # Check that a string with no tickers returns an empty list.
    ("something with words", []),
    # Check that capital letters without a dollar sign are not counted.
    ("CAPITAL LETTERS", []),
    # Check that a valid ticker symbol is recorded
    ("Words$TSLA more wWORds", ['TSLA']),
    # Check that multiple ticker symbols are recorded
    ("Long $TSLA & $AAPLto be cool", ['TSLA', 'AAPL']),
]

find_qmarks_cases = [
    # Check that any string with a question mark returns True.
    ('????!!??', True),
    # Check that any string without a question mark returns False.
    ('Hello!', False),
]

find_long_cases = [
    # Check that any string with the word "long" returns True as long as it is
    # not the last word or part of another word.
    ('This is so long stocking.', True),
    # Check that any string without the word "long" returns False.
    ('This is so short.', False),
]

find_short_cases = [
    # Check that any string that contains the word "short" returns True as long
    # as it is not the last word or part of another word.
    ('I am not short at all.', True),
    # Check that any string without "short" returns False.
    ('I am not tall.', False),
]

str_create_timestamp_cases = [
    # Check that an inputted string in datetime format will be
    # outputted as a datetime date that is an integer.
    ('2018-01-01', 1514782800),
]

remove_dupes_cases = [
    # Check that empty strings in a list are removed.
    (['hello', '', 'hi'], ['hello', 'hi']),
    # Check that repeats in a list are removed.
    (['hello', 'hello', 'hi'], ['hello', 'hi']),
]

days_since_epoch_cases = [
    # Check that the number of days since the beginning of the epoch is correct.
    (datetime.date(1970, 1, 11), 10),
    # Check that if the inputted date is before the beginning of the epoch, a
    # negative integer is returned.
    (datetime.date(1960, 1, 11), -3643),
]

date_from_epoch_time_cases = [
    # Check that the datetime object returned is correct and aligns with the
    # beginning of the epoch and an inputted time difference of days.
    (10, datetime.date(1970, 1, 11)),
    # Check that the correct datetime object is returned when a time difference
    # of over a year is inputted.
    (366, datetime.date(1971, 1, 2)),
]

str_to_list_cases = [
    # Check that an inputted string with one comma is split determining on the
    # comma.
    ("['hello', 'goodbye']", ['hello', 'goodbye']),
    # Check that an inputted string with multiple commas is split correctly.
    ("['hello', 'goodbye', 'see you again']",
     ['hello', 'goodbye', 'see you again']),
    # Check that an inputted string with no commas outputs the original string
    # minus 4 characters.
    ("['hello']", ['hello']),
]

get_datetime_cases = [
    # Check that a simple addition case returns a datetime.date object.
    ("2022-01-01", 10, [datetime.date(2022, 1, 1),
                        datetime.date(2022, 1, 11)]),
    # Check addition for months.
    ("2022-01-01", 31, [datetime.date(2022, 1, 1),
                        datetime.date(2022, 2, 1)]),
    # Check addition for years.
    ("2021-01-01", 365, [datetime.date(2021, 1, 1),
                         datetime.date(2022, 1, 1)]),
]

# Define additional testing lists and functions that check other properties of
# functions in gene_finder.py.


@ pytest.mark.parametrize("string,tickers", find_tickers_cases)
def test_find_tickers(string, tickers):
    """
    Check that the correct tickers are pulled out from a string.

    Args:
        string: A string representing the body or title of a Reddit post.
    """
    assert find_tickers(string) == tickers


@ pytest.mark.parametrize("string,boolean", find_qmarks_cases)
def test_find_qmarks(string, boolean):
    """
    Test that a string is searched for any question marks.

    Args:
        string: A string to be searched.
    """
    assert find_qmarks(string) == boolean


@ pytest.mark.parametrize("string,boolean", find_long_cases)
def test_find_long(string, boolean):
    """
    Tests that a string is searched for the word long.

    Args:
        string: A string to be searched.
    """
    assert find_long(string) == boolean


@ pytest.mark.parametrize("string,boolean", find_short_cases)
def test_find_short(string, boolean):
    """
    Tests that a string is searched for the word short.

    Args:
        string: A string to be searched.
    """
    assert find_short(string) == boolean


@ pytest.mark.parametrize("date_str,timestamp", str_create_timestamp_cases)
def test_str_create_timestamp(date_str, timestamp):
    """
    Tests that a datetime timestamp is obtained from a date.

    Args:
        date_str: A string in format "YXXX-MX-DX" to be converted to a
        timestamp.
    """
    assert str_create_timestamp(date_str) == timestamp


@ pytest.mark.parametrize("str_list, res", remove_dupes_cases)
def test_remove_dupes(str_list, res):
    """
    Tests that empty strings and repeats are removed from a list of strings.

    Args:
        str_list: A list of strings.
    """
    assert remove_dupes(str_list) == res


@ pytest.mark.parametrize("date,days", days_since_epoch_cases)
def test_days_since_epoch(date, days):
    """
    Check that the correct tickers are pulled out from a string.

    Args:
        string: A string representing the body or title of a Reddit post.
    """
    assert days_since_epoch(date) == days


@ pytest.mark.parametrize("num_days,date", date_from_epoch_time_cases)
def test_date_from_epoch_time(num_days, date):
    """
    Tests that the number of days since January 1, 1970 from a given date is
    calculated.

    Args:
        date: The datetime.date object that 1970-1-1 is to be subtracted from.
    """
    assert date_from_epoch_time(num_days) == date


@ pytest.mark.parametrize("list_string,str_list", str_to_list_cases)
def test_str_to_list(list_string, str_list):
    """
    Tests that a string that is formatted like a list of strings is converted to
    a list.

    Args:
        list_string: A string in the format "['item 1', 'item 2'].
    """
    assert str_to_list(list_string) == str_list


@ pytest.mark.parametrize("start_date,time_period,dates", get_datetime_cases)
def test_get_datetime(start_date, time_period, dates):
    """
    Tests that a start date and number of days to a start and end datetime
    results in a date.

    Args:
        start_date: A string containing the first date to pull data for in the
        format YYYY-MM-DD.
        time_period: An integer of the number of days to pull data for.
    """
    assert get_datetime(start_date, time_period) == dates
