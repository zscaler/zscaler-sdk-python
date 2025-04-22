import json

from zscaler.errors.error import Error


class HTTPError(Error):
    def __init__(self, url, response_details, response_body):
        self.status_code = response_details.status_code
        self.url = url
        self.response_headers = response_details.headers
        self.stack = ""
        self.message = f"HTTP {self.status_code} {response_body}"


class ZscalerAPIError(Error):
    def __init__(self, url, response, response_body):
        self.status_code = response.status_code
        self.url = url
        self.response_body = json.dumps(response_body)
        self.message = f"ZSCALER HTTP {url} {self.status_code} {self.response_body}"
