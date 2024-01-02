#!/usr/bin/env python3
"""LFU caching with tie-breaking using LRU"""

from datetime import datetime
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFU Caching with LRU tie-breaking"""

    def __init__(self):
        """Initialize
        """
        super().__init__()
        self.__frequency = {}
        self.__timestamps = {}

    def put(self, key, item):
        """ Add a new item to the cache"""

        if key and item:
            self.__timestamps[key] = datetime.now()

            if key not in self.__frequency:
                self.__frequency[key] = 1
            else:
                self.__frequency[key] += 1

            self.cache_data[key] = item

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                freq_val = [v for k, v in self.__frequency.items() if k != key]
                min_freq = min(freq_val)
                min_keys = [k for k, freq in self.__frequency.items()
                            if freq == min_freq]
                min_key = min(
                    min_keys,
                    key=lambda k: self.__timestamps[k],
                )
                del self.cache_data[min_key]
                del self.__frequency[min_key]
                del self.__timestamps[min_key]
                print("DISCARD: {}".format(min_key))

    def get(self, key):
        """ Get an item from the cache by key"""
        if not key or key not in self.cache_data.keys():
            return None

        self.__frequency[key] += 1
        self.__timestamps[key] = datetime.now()

        return self.cache_data[key]
