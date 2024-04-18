from zscaler.errors.error import Error


# ZPA API Errors
class ZPAAPIError(Error):
    def __init__(self, url, response_details, response_body):
        self.status = response_details.status
        self.error_id = response_body.get("id", "")
        self.reason = response_body.get("reason", "")
        self.params = response_body.get("params", [])

        params_string = ", ".join(self.params)

        self.url = url
        self.headers = response_details.headers
        self.stack = ""

        self.message = f"ZPA HTTP {self.status} {self.error_id} " f"{self.reason}\nParameters: {params_string}"


# ZIA API Errors
