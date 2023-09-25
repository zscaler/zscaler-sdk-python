import logging
import threading
import time

from zscaler.cache.cache import Cache

logger = logging.getLogger("zscaler-sdk-python")


class ZPACache(Cache):
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            # cls._instance = super(ZPACache, cls).__new__(cls, *args, **kwargs)
            cls._instance = super(ZPACache, cls).__new__(cls)
            # Initialize any variables here if required
            cls._instance._store = {}
            cls._instance._time_to_live = args[0] if args else None
            cls._instance._time_to_idle = args[1] if args else None

            # Add a thread lock for thread-safe operations
            cls._instance._lock = threading.Lock()

        return cls._instance

    def __init__(self, ttl, tti):
        # We're deliberately not calling super() here because we don't want
        # to overwrite any variables on repeated instantiation.
        pass

    def get(self, key):
        with self._lock:
            now = self._get_current_time()
            if self.contains(key):
                entry = self._store[key]
                entry["tti"] = now + self._time_to_idle
                self._clean_cache()
                logger.info(f'Got value from cache for key "{key}".')
                logger.debug(f'Cached value for key {key}: {entry["value"]}')
                return entry["value"]

            self._clean_cache()
            return None

    def contains(self, key):
        with self._lock:
            return key in self._store and self._is_valid_entry(self._store[key])

    def add(self, key: str, value: tuple):
        with self._lock:
            if type(key) == str:  # Modified this check to be more flexible
                now = self._get_current_time()
                self._store[key] = {"value": value, "tti": now + self._time_to_idle, "ttl": now + self._time_to_live}
                logger.info(f'Added to cache value for key "{key}".')
                logger.debug(f"Cached value for key {key}: {value}.")
            self._clean_cache()

    def delete(self, key):
        with self._lock:
            if key in self._store:
                del self._store[key]
                logger.info(f'Removed value from cache for key "{key}".')

    def clear(self):
        with self._lock:
            self._store.clear()
            logger.info("Cleared the cache.")

    def _clean_cache(self):
        expired = []
        for key in self._store.keys():
            if not self._is_valid_entry(self._store[key]):
                expired.append(key)
        for expired_key in expired:
            self.delete(expired_key)

    def _is_valid_entry(self, entry):
        now = self._get_current_time()
        timers = [entry["tti"], entry["ttl"]]
        return not any(timer <= now for timer in timers)

    def _get_current_time(self):
        return time.time()

    def clear_by_prefix(self, prefix):
        with self._lock:
            keys_to_delete = [k for k in self._store if k.startswith(prefix)]
            for key in keys_to_delete:
                self.delete(key)
