class HTTPError(Exception):
    def __init__(self, url, response_details, response_body):
        self.status_code = response_details.status_code
        self.url = url
        self.response_headers = response_details.headers
        self.message = f"HTTP {self.status_code} {response_body}"
        super().__init__(self.message)  # ✅ important

    def __str__(self):
        return self.message
