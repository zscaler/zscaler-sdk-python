class Error:
    """
    Base Error Class
    """

    def __init__(self):
        self.message = ""

    def __repr__(self):
        return str({"message": self.message})


class HTTPError(Error):
    def __init__(self, url, response, response_body):
        self.status = response.status_code
        self.url = url
        self.message = f"HTTP {self.status} {response_body}"


class ZpaAPIError(Error):
    def __init__(self, url, response, response_body):
        self.status = response.status_code
        self.url = url
        self.response_body = response_body
        self.message = f"ZPA HTTP {self.status} " f"{self.response_body}\n"


class ZpaBaseException(Exception):
    pass


class HTTPException(ZpaBaseException):
    pass


class ZpaAPIException(ZpaBaseException):
    pass
