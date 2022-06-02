"""
Library for pulling and filtering Reddit data.
"""

import re
import datetime
import pandas as pd
from pmaw import PushshiftAPI

api = PushshiftAPI()


def find_tickers(string):
    """
    Searches a string for stock tickers.

    Args:
        string: A string to be searched.

    Returns:
        A list of all the stock tickers in the string.
    """
    return re.findall(r"\$([A-Z]+)", string)


def find_qmarks(string):
    """
    Searches a string for question marks.

    Args:
        string: A string to be searched.

    Returns:
        true if the string contains a question mark, False otherwise.
    """
    q_list = re.findall(r"(\?)", string)
    if q_list:
        return True
    return False


def find_long(string):
    """
    Searches a string for the word long.

    Args:
        string: A string to be searched.

    Returns:
        True if the string contains long, False otherwise.
    """
    long_list = re.findall(r'[Ll]ong ', string)
    if long_list:
        return True
    return False


def find_short(string):
    """
    Searches a string for the word short.

    Args:
        string: A string to be searched.

    Returns:
        True if the string contains short, False otherwise.
    """
    short_list = re.findall(r'[Ss]hort ', string)
    if short_list:
        return True
    return False


def str_create_timestamp(date_str):
    """
    Creates a datetime timestamp from a date.

    Args:
        date_str: A string in format "YXXX-MX-DX" to be converted to a
        timestamp.

    returns:
        An integer timestamp as defined by datetime.
    """
    year = int(date_str[0:4])
    month = int(date_str[5:7])
    day = int(date_str[8:])
    timestamp = int(datetime.datetime(
        year=year, month=month, day=day).timestamp())
    return timestamp


def remove_dupes(str_list):
    """
    Removes empty strings and repeats from a list of strings.

    Args:
        str_list: A list of strings.

    Returns:
        The original list of strings with any repeat elements or empty string
        elements removed.
    """
    res = []
    for string in str_list:
        if string not in res:
            res.append(string)
    if '' in res:
        res.remove('')
    return res


def pull_raw_data(subreddit, limit, beginning_day, end_day):
    """
    Uses PMAW pushshift API wrapper to collect reddit Submission data from a
    specified subreddit.

    Args:
        subreddit: A string that is the name of the subreddit you want to pull
        data from.
        limit: An int representing the maximum amount of reddit submissions you
        want to collect.
        beginning_day: A date represented as a string in "YXXX-MX-DX" format
        that is the beginning of your search time window.
        end_day: A date represented as a string in "YXXX-MX-DX" format
        that is the end of your search time window.

    Returns:
        A dataframe containing the titles, body text, and date written
        of Reddit posts.
    """
    beginning_timestamp = str_create_timestamp(beginning_day)
    end_timestamp = str_create_timestamp(end_day)

    submissions = api.search_submissions(subreddit=subreddit, limit=limit,
                                         before=end_timestamp, after=beginning_timestamp)

    subs_df = pd.DataFrame(submissions)
    subs_df = subs_df[['title', 'selftext', 'created_utc']]
    subs_df = subs_df.sort_values(by='created_utc')
    print(len(subs_df))
    return subs_df


def get_filtered_reddit_data(limit, beginning_day, end_day):
    """
    Pulls data from /r/wallstreetbets over a specified time interval and
    filters out posts that don't meet specific parameters.

    Args:
        limit: An int representing the maximum amount of reddit submissions you
        want to collect.
        Beginning_day: A date represented as a string in "YXXX-MX-DX" format
        that is the beginning of your search time window.
        end_day: A date represented as a string in "YXXX-MX-DX" format
        that is the end of your search time window.

    Returns:
        Creates a csv file containing all key elements of the reddit
        submissions that met our search parameters.
    """

    all_data = pull_raw_data("wallstreetbets", limit, beginning_day, end_day)

    # Init new dataframe
    dataframe = pd.DataFrame()

    # Create a list of exixting tickers to remove posts talking about
    # the same stock. Start with SPY, our S&P500 ETF and baseline
    existing_tickers = ['SPY']

    # Makes each row in the dataframe a tuple
    for post in all_data.itertuples():

        # post[0] is an index added by the itertuples function
        title = str(post.title)
        selftext = str(post.selftext)
        created_utc = post.created_utc

        # Combine the title and text for string searches. Must separate with
        # space to prevent first letter of text being added to ticker in title.
        all_text = title + " " + selftext

        # Removes reddit submissions that don't contain a stock ticker or
        # the word long.
        # Removes reddit submissions that contain a question mark or
        # the word short.
        if find_tickers(all_text) and not find_qmarks(all_text) and \
                find_long(all_text) and not find_short(all_text):

            # Generate a list of all the stock tickers in a post
            #  and remove duplicates
            ticker_list = find_tickers(all_text)
            ticker_list = remove_dupes(ticker_list)

            # filter out all but the first mention of each stock ticker
            new_ticker_list = []
            for ticker in ticker_list:
                if ticker not in existing_tickers:
                    existing_tickers.append(ticker)
                    new_ticker_list.append(ticker)

            if new_ticker_list:
                # censored_title = post['title']  #pf.censor()
                # censored_selftext = post['selftext']
                time = datetime.datetime.fromtimestamp(created_utc)

                # Add specific, relevant information from the reddit submission
                # to our dataframe.
                dataframe = pd.concat(
                    [dataframe, pd.DataFrame({'title': [title],
                                              'selftext': [selftext],
                                              'time': [time],
                                              'tickers': [new_ticker_list]})])
    dataframe.to_csv("reddit/reddit_subs_filtered.csv")
