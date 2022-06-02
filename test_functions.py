"""
Test library functions to pull Reddit and Alpaca information, sort for useful
data, and graph the data.
"""
import pytest

from stock_info.pull_stock_info import get_datetime

# Define sets of test cases.
get_datetime_cases = [
    # Check that the complement of A is T.
    ("A", "T"),
]
