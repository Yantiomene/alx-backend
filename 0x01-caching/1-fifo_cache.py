#!/usr/bin/env python3
"""FIFO caching"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """FIFO Caching"""

    def put(self, key, item):
        """ Add a new item to the cache"""
        keys = self.cache_data.keys()

        if key and item:
            if key in keys:
                self.cache_data[key] = item
            elif len(keys) >= BaseCaching.MAX_ITEMS:
                key_0 = list(keys)[0]
                print("DISCARD: {}".format(key_0))
                del self.cache_data[key_0]

            self.cache_data[key] = item

    def get(self, key):
        """ Get an item from the cache by key"""
        if not key or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
