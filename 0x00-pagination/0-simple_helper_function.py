#!/usr/bin/env python3
"""Simple helper function"""


def index_range(page, page_size):
    """Return a tuple containing a start and end index
    corresponding to the range of indexes to return in a list
    for those particular pagination parameters"""

    start_index = (page - 1) * page_size
    end_index = page * page_size

    return (start_index, end_index)
