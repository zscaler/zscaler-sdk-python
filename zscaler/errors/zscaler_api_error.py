from zscaler.errors.error import Error


class ZscalerAPIError(Error):
    def __init__(self, url, response_details, response_body):
        self.status_code = response_details.status_code
        self.error_id = response_body.get("id", "")
        self.reason = response_body.get("reason", "")
        self.params = response_body.get("params", [])
        self.error = response_body.get("error", "")
        self.path = response_body.get("path", "")

        # Constructing the message dynamically based on available fields
        message_parts = [f"HTTP {self.status_code}"]

        if self.error_id:
            message_parts.append(self.error_id)
        if self.reason:
            message_parts.append(self.reason)
        if self.params:
            params_string = ", ".join(self.params)
            message_parts.append(f"Parameters: {params_string}")

        self.message = " ".join(message_parts)

        self.url = url
        self.headers = response_details.headers
        self.stack = ""

