# -*- coding: utf-8 -*-

import time
from threading import Thread
from collections import defaultdict


class SimpleInMemoryCache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value, ttl=None):
        expires_at = None if ttl is None else time.time() + ttl
        self.cache[key] = {"value": value, "expires_at": expires_at}

    def get(self, key):
        item = self.cache.get(key)
        if item and (item["expires_at"] is None or item["expires_at"] > time.time()):
            return item["value"]
        self.delete(key)
        return None

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]


defaultCache = SimpleInMemoryCache()
# defaultCache.set("product_1", {"name": "Laptop"}, ttl=30)  # 缓存30秒
# print(defaultCache.get("product_1"))  # 输出: {'name': 'Laptop'}
# time.sleep(31)  # 等待超过缓存有效期
# print(defaultCache.get("product_1"))  # 输出: None，因为缓存已过期
