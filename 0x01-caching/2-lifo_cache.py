#!/usr/bin/env python3
"""LIFO caching"""

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """LIFO Caching"""

    def put(self, key, item):
        """ Add a new item to the cache"""
        keys = self.cache_data.keys()

        if key and item:
            if key in keys:
                self.cache_data[key] = item
            elif len(keys) >= BaseCaching.MAX_ITEMS:
                key_l, val_l = self.cache_data.popitem()
                print("DISCARD: {}".format(key_l))

            self.cache_data[key] = item

    def get(self, key):
        """ Get an item from the cache by key"""
        if not key or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
