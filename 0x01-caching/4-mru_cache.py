#!/usr/bin/env python3
"""MRU caching"""

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """MRU Caching"""

    def __init__(self):
        """Initialize
        """
        super().__init__()
        self.__usedItems = []

    def put(self, key, item):
        """ Add a new item to the cache"""

        if key and item:
            if key not in self.__usedItems:
                self.__usedItems.append(key)
            else:
                used_key = self.__usedItems.pop(self.__usedItems.index(key))
                self.__usedItems.append(used_key)

            self.cache_data[key] = item
            if len(self.__usedItems) > BaseCaching.MAX_ITEMS:
                key_l = self.__usedItems.pop(-2)
                del self.cache_data[key_l]
                print("DISCARD: {}".format(key_l))

    def get(self, key):
        """ Get an item from the cache by key"""
        if not key or key not in self.cache_data.keys():
            return None
        key_l = self.__usedItems.pop(self.__usedItems.index(key))
        self.__usedItems.append(key_l)
        return self.cache_data[key]
