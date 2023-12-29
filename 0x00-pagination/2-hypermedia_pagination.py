#!/usr/bin/env python3
"""Hypermedia pagination"""
import csv
import math
from typing import List, Tuple
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Return a tuple containing a start and end index
    corresponding to the range of indexes to return in a list
    for those particular pagination parameters"""

    start_index = (page - 1) * page_size
    end_index = page * page_size

    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return the appropriate page of the dataset
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()
        n = len(dataset)
        if start_index >= n or end_index > n:
            return []
        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """Returns a dictionary with the following keys:
        page_size: the length of the returned dataset page
        page: the current page number
        data: the dataset page (equivalent to return from previous task)
        next_page: number of the next page, None if no next page
        prev_page: number of the previous page, None if no previous page
        total_pages: the total number of pages in the dataset as an integer
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0
        dic = {}
        data = self.get_page(page, page_size)
        dic['page_size'] = len(data)
        dic['page'] = page
        dic['data'] = data
        dic['next_page'] = None if len(data) == 0 else page + 1
        dic['prev_page'] = None if page == 1 else page - 1
        dic['total_page'] = math.ceil(len(self.dataset()) / page_size)
        return dic
