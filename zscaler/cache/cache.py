from urllib.parse import parse_qs, urlencode, urlparse


class Cache:
    """
    This is the ABSTRACT class that defines a Cache object for the ZPA Client
    """

    def __init__(self):
        pass

    def get(self, key):
        """
        A method which retrieves the desired value from the cache.

        Arguments:
            key {str} -- The key used to find the desired value

        Raises:
            NotImplementedError: If the subclass inheriting this class
            has not implemented this function
        """
        raise NotImplementedError

    def contains(self, key):
        """
        A method which checks if the cache contains the desired value.

        Arguments:
            key {str} -- The key used to check the desired value

        Raises:
            NotImplementedError: If the subclass inheriting this class
            has not implemented this function
        """
        raise NotImplementedError

    def add(self, key, value):
        """
        A method which adds a key-value pair to the cache.

        Arguments:
            key {str} -- The key used to identify the entry.
            value {[type]} -- The value in the pair

        Raises:
            NotImplementedError: If the subclass inheriting this class
            has not implemented this function
        """
        raise NotImplementedError

    def delete(self, key):
        """
        A method which deletes a key-value pair from the cache.

        Arguments:
            key {str} -- The key used to identify the entry

        Raises:
            NotImplementedError: If the subclass inheriting this class
            has not implemented this function
        """
        raise NotImplementedError

    def clear(self):
        """
        A method used to empty the cache.

        Raises:
            NotImplementedError: If the subclass inheriting this class
            has not implemented this function
        """
        raise NotImplementedError

    def create_key(self, request, params):
        """
        A method used to create a unique key for an entry in the cache.
        Used with URLs that requests fire at.

        Arguments:
            request {str} -- The key to use to produce a unique key

        Returns:
            str -- Unique key based on the input URL without query parameters
        """
        # Validate URL and return URL string without query parameters
        # Parse the original URL
        url_object = urlparse(request)

        # Extract the query parameters from the URL
        original_query_params = parse_qs(url_object.query)

        # Update the query parameters with the provided `params` dictionary
        if params is not None and len(params) > 0:
            original_query_params.update(params)

        # Create a new query string with the updated parameters
        updated_query_string = urlencode(original_query_params, doseq=True)

        # Combine the netloc, path, and the updated query string to form the new URL
        base_url = f"{url_object.netloc}{url_object.path}"
        if updated_query_string != "":
            base_url = f"{base_url}?{updated_query_string}"

        return base_url
