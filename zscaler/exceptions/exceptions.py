from zscaler.constants import ZPA_BASE_URLS


# Zscaler Private Access specific exceptions
class RateLimitExceededError(Exception):
    """Raised when the API rate limit is exceeded."""

    pass


class RetryLimitExceededError(Exception):
    """Raised when the maximum number of retries is exceeded."""

    pass


class CacheError(Exception):
    """Raised for errors related to caching operations."""

    pass


class BadRequestError(Exception):
    """Raised when the API responds with a 400 status code."""

    pass


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class NotFoundError(Exception):
    pass


class APIClientError(Exception):
    """General exception related to the API client operations."""

    pass


class InvalidCloudEnvironmentError(Exception):
    """Raised when an unrecognized cloud environment is specified."""

    def __init__(self, cloud: str):
        self.cloud = cloud
        super().__init__(f"Unrecognized cloud environment: {self.cloud}")


class TokenExpirationError(Exception):
    """Raised when the authentication token has expired."""

    pass


class TokenRefreshError(Exception):
    """Raised when there's an issue refreshing the authentication token."""

    pass


class HeaderUpdateError(Exception):
    """Raised if there's a problem updating the session headers."""

    pass
