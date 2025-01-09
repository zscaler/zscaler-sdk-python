import logging
import time
from urllib.parse import urlparse

from zscaler.cache.cache import Cache

logger = logging.getLogger("zscaler-sdk-python")


class ZscalerCache(Cache):
    """
    This is a base class implementing a Cache using TTL and TTI.
    Implementing the zscaler.cache.cache.Cache abstract class.
    """

    def __init__(self, ttl, tti):
        """
        Constructor.

        Arguments:
            ttl {float} -- Time to Live: for cache entries
            tti {float} -- Time to Idle: for cache entries
        """
        super()  # Inherit from parent class
        self._store = {}  # key -> {value, TTI, TTL}
        self._time_to_live = ttl
        self._time_to_idle = tti

    def get(self, key):
        """
        Retrieves value from cache using key

        Arguments:
            key {str} -- Desired key

        Returns:
            str -- Corresponding value to given key
            None -- Unable to find value for this key
        """
        logger.debug(f'Attempting to retrieve key "{key}" from cache.')
        # Get current time
        now = self._get_current_time()
        # Check if key is in cache and valid
        if self.contains(key):
            entry = self._store[key]
            # Reset TTI
            entry["tti"] = now + self._time_to_idle
            # Return desired value and update cache
            self._clean_cache()
            logger.debug(f'Cached value for key {key}: {entry["value"]}')
            return entry["value"]

        # Return None if key isn't in cache and update cache
        self._clean_cache()
        logger.warning(f'Key "{key}" not found in cache.')
        return None

    def contains(self, key):
        """
        Returns existence of key in cache, as boolean

        Arguments:
            key {str} -- Desired key

        Returns:
            bool -- Existence of key in cache
        """
        return key in self._store and self._is_valid_entry(self._store[key])

    def add(self, key: str, value: tuple):
        """
        Adds a key-value pair to the cache.

        Arguments:
            key {str} -- Key in pair
            value {tuple} -- Tuple of response and response body
        """
        logger.debug(f'Attempting to add key "{key}" to cache with value: {value}.')
        # Update cache
        self._clean_cache()
        if isinstance(key, str) and (not isinstance(value, list) or not isinstance(value[1], list)):
            # Get current time
            now = self._get_current_time()

            # Add new entry to cache with timers
            self._store[key] = {
                "value": value,
                "tti": now + self._time_to_idle,
                "ttl": now + self._time_to_live,
            }
            logger.info(f'Successfully added key "{key}" to cache.')
            logger.debug(f"Cached value for key {key}: {value}.")
        else:
            logger.error(f'Failed to add key "{key}" to cache. Invalid key or value type.')

    def delete(self, key):
        """
        Delete a key-value pair from the cache.

        Arguments:
            key {str} -- Desired key
        """
        logger.debug(f'Attempting to delete key "{key}" from cache.')
        # Make sure key is in cache
        if key in self._store:
            # Delete entry
            del self._store[key]
            logger.info(f'Successfully deleted key "{key}" from cache.')
        else:
            logger.warning(f'Key "{key}" not found in cache. Nothing to delete.')
        url_object = urlparse(key)
        base_url = f"{url_object.netloc}{url_object.path}"
        for other_key in self._store.keys():
            other_url_object = urlparse(other_key)
            other_base_url = f"{other_url_object.netloc}{other_url_object.path}"
            if not self._is_valid_entry(self._store[other_key]) and other_base_url.startswith(base_url):
                del self._store[other_key]
                logger.info(f'Removed also value from cache for key "{other_key}".')

    def clear(self):
        """
        Clear the cache.
        """
        logger.debug("Attempting to clear the entire cache.")
        self._store.clear()
        logger.info("Cache cleared successfully.")

    def _clean_cache(self):
        """
        Updates cache by removing expired entries at time of call
        """
        logger.debug("Cleaning cache by removing expired entries.")
        expired = []
        # Check every entry
        for key in self._store.keys():
            # If not valid, delete
            if not self._is_valid_entry(self._store[key]):
                expired.append(key)
        # Delete keys
        for expired_key in expired:
            self.delete(expired_key)
        if expired:
            logger.info(f"Removed expired keys from cache: {expired}")
        else:
            logger.debug("No expired entries found during cache cleaning.")

    def _is_valid_entry(self, entry):
        """
        Determines if a given cache entry is not expired.

        Args:
            entry (dict): An entry from the cache composed of value,
            TTI, and TTL

        Returns:
            bool: Boolean value representing if entry is expired
        """
        # Get Current time
        now = self._get_current_time()
        # Check timers and compare against current time
        timers = [entry["tti"], entry["ttl"]]
        return not any(timer <= now for timer in timers)

    def _get_current_time(self):
        """
        Helper function to get current time

        Returns:
            float: value representing the number of seconds since the epoch
        """
        return time.time()
