import json

raise_exception = False

# Zscaler Base Exceptions
class ZscalerBaseException(Exception):
    def __init__(self, url, response, response_body):
        self.status_code = response.status_code
        self.url = url
        self.response_body = json.dumps(response_body)
        self.message = f"ZSCALER HTTP {url} {self.status_code} {self.response_body}"

    def __repr__(self):
        return str({"message": self.message})

    def __str__(self):
        return self.message


class HTTPException(ZscalerBaseException):
    pass


class ZscalerAPIException(ZscalerBaseException):
    def __init__(self, error):
        # error is a ZscalerAPIError
        super().__init__(error.url, error, error.message)


# Other exceptions (unchanged)
class ZpaBaseException(Exception):
    pass


class ZpaAPIException(ZpaBaseException):
    pass


class RateLimitExceededError(Exception):
    pass


class RetryLimitExceededError(Exception):
    pass


class CacheError(Exception):
    pass


class BadRequestError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class NotFoundError(Exception):
    pass


class APIClientError(Exception):
    pass


class InvalidCloudEnvironmentError(Exception):
    def __init__(self, cloud: str):
        self.cloud = cloud
        super().__init__(f"Unrecognized cloud environment: {self.cloud}")


class TokenExpirationError(Exception):
    pass


class TokenRefreshError(Exception):
    pass


class HeaderUpdateError(Exception):
    pass
