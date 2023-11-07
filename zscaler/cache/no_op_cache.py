import logging

from zscaler.cache.cache import Cache

# Setting up the logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


class NoOpCache(Cache):
    """
    This is a disabled Cache Class where no operations occur
    in the cache.
    Implementing the zscaler.cache.cache.Cache abstract class.
    """

    def __init__(self):
        super()

    def get(self, key):
        """
        Nothing is returned.

        Arguments:
            key {str} -- Key to look for

        Returns:
            None -- No op cache doesn't contain any data to return
        """
        logging.debug("Serving from cache.")
        return None

    def contains(self, key):
        """
        False is returned

        Arguments:
            key {str} -- Key to look for

        Returns:
            False -- No data to return so key can never be in cache
        """
        return False

    def add(self, key, value):
        """
        This is a void method.

        Arguments:
            key {str} -- Key in pair
            value {str} -- Val in pair
        """
        logging.warning("Saving to cache.")

    def delete(self, key):
        """This is a void method. No need to delete anything not contained.

        Arguments:
            key {str} -- Key to delete
        """
        pass

    def clear(self):
        """
        This is a void method. No need to clear when nothing's stored.
        """
        pass
