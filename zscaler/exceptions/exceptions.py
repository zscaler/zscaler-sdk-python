import json


# Zscaler Base Exceptions
class ZscalerBaseException(Exception):
    def __init__(self, url, response, response_body):
        self.status = response.status_code
        self.url = url
        self.response_body = json.dumps(response_body)
        self.message = f"ZSCALER HTTP {url} {self.status} {self.response_body}"

    def __repr__(self):
        return str({"message": self.message})

    def __str__(self):
        return self.message


class HTTPException(ZscalerBaseException):
    pass


class ZscalerAPIException(ZscalerBaseException):
    pass


# Zscaler Private Access specific exceptions (Potential Future Use)
class ZpaBaseException(Exception):
    pass


class ZpaAPIException(ZpaBaseException):
    pass


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
