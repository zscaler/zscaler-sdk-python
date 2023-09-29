import logging

from zscaler.cache.cache import Cache

# Setting up the logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Get the custom logger you've defined in logger.py
logger = logging.getLogger("zscaler-sdk-python")


class NoOpCache(Cache):
    """
    This class represents a no-operation (NoOp) cache.
    It implements the Cache interface but does not actually store any data.
    It is useful for testing and debugging scenarios.
    """

    def get(self, key):
        """
        Simulates retrieval of key from the cache.

        Args:
            key (str): Key to look for.

        Returns:
            None: Always returns None since no data is stored in the cache.
        """
        logger.debug("NoOpCache in use. No data retrieved from cache for key: %s", key)
        return None

    def contains(self, key):
        """
        Always returns False since no data is stored in the cache.

        Args:
            key (str): Key to check for existence in cache.

        Returns:
            bool: Always returns False.
        """
        return False

    def add(self, key, value):
        """
        Simulates adding a key-value pair to the cache.

        Args:
            key (str): Key to add to the cache.
            value (Any): Value to associate with the key.
        """
        logger.debug("NoOpCache in use. Not adding key-value pair to cache: %s - %s", key, value)

    def delete(self, key):
        """
        Simulates deletion of key from the cache.

        Args:
            key (str): Key to delete from the cache.
        """
        logger.debug("NoOpCache in use. No key deleted from cache: %s", key)

    def clear(self):
        """
        Simulates clearing the cache.
        """
        logger.debug("NoOpCache in use. Cache cleared (no actual operation performed).")
