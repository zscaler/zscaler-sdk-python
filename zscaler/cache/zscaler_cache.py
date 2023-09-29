import logging
import os
import threading
import time
from http.client import HTTPResponse
from io import BytesIO

from cachetools import TTLCache

# Setup logger for this module
logger = logging.getLogger("zscaler-cache")  # Changed logger name to avoid conflicts
logger.setLevel(logging.DEBUG)  # This can be adjusted programmatically or using environment variables


class ZPACache:
    _instance = None  # Singleton instance
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not isinstance(cls._instance, cls):
                cls._instance = super(ZPACache, cls).__new__(cls)
                cache_enabled = os.getenv("ZSCALER_CLIENT_CACHE_ENABLED", "true").lower() == "true"
                cls._instance.default_ttl = int(
                    os.getenv("ZSCALER_CLIENT_CACHE_TTL", 600)
                )  # Default to 600 seconds (10 minutes)
                cls._instance.default_tti = int(
                    os.getenv("ZSCALER_CLIENT_CACHE_TTI", 480)
                )  # Default to 480 seconds (8 minutes)
                if cache_enabled:
                    cls._instance._cache = TTLCache(maxsize=100, ttl=cls._instance.default_ttl)
                    logger.info("Cache is enabled with TTL: {}".format(cls._instance.default_ttl))
                else:
                    cls._instance._cache = None  # Cache is disabled
                    logger.info("Cache is disabled")
        return cls._instance

    def __init__(self):
        pass

    def get(self, key):
        with self._lock:
            if self._cache is not None:
                try:
                    entry = self._cache[key]  # Accessing an expired item will raise a `KeyError`
                    logger.debug(f"Cache hit for key: {key}")

                    # Construct a new HTTPResponse object
                    resp = HTTPResponse(BytesIO(entry["content"]))
                    resp.status = entry["status_code"]
                    resp.reason = entry["reason"]
                    resp.headers = entry["headers"]
                    resp.msg = entry["msg"]
                    resp.fp = BytesIO(entry["content"])  # You may need to set the file pointer with the content again
                    logger.debug(f"Getting from cache with key: {key}")
                    resp.begin()  # Consider whether this is necessary based on your use case
                    return resp
                except KeyError:
                    logger.debug(f"Cache miss for key: {key}")
                    return None
                except Exception as e:
                    logger.error(f"Unexpected error while retrieving from cache: {e}")
                    return None

    def add(self, key, response):
        with self._lock:
            if self._cache is not None:
                entry = {
                    "content": response.read(),  # Assuming response has a read method returning bytes
                    "status_code": response.status,
                    "reason": response.reason,
                    "headers": dict(response.getheaders()),  # Assuming response has getheaders method
                    "msg": response.msg
                    # 'timestamp' is not needed as TTLCache handles expiration internally
                }
                logger.debug(f"Adding item to cache with key: {key}")
            else:
                logger.debug("Cache is None, when trying to add key: {key}")
                response.fp = BytesIO(entry["content"])  # Set the file pointer back after reading
                self._cache[key] = entry
                logger.debug(f"Adding item to cache with key: {key}")

    def delete(self, key):
        with self._lock:
            if self._cache is not None and key in self._cache:
                logger.debug(f"Deleting item from cache with key: {key}")
                del self._cache[key]

    def clear(self):
        with self._lock:
            if self._cache is not None:
                logger.debug("Clearing all items from cache")
                self._cache.clear()

    def clear_by_prefix(self, prefix):
        with self._lock:
            if self._cache is not None:
                logger.debug(f"Clearing cache items with prefix: {prefix}")
                keys_to_delete = [k for k in list(self._cache.keys()) if k.startswith(prefix)]
                for key in keys_to_delete:
                    del self._cache[key]
