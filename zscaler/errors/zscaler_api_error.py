from zscaler.errors.error import Error
import json


class ZscalerAPIError(Error):
    def __init__(self, url, response_details, response_body, service_type=""):
        self.status_code = response_details.status_code
        self.url = url
        self.headers = response_details.headers
        self.stack = ""
        self.service_type = service_type.lower()

        # Initialize all possible fields to None
        self.error_code = None
        self.error_message = None
        self.params = None
        self.path = None

        # Populate based on service type
        if self.service_type == "zpa":
            self.error_code = response_body.get("id")
            self.error_message = response_body.get("reason")
            self.params = response_body.get("params")
        else:  # default to ZIA/others
            self.error_code = response_body.get("code") or response_body.get("id")
            self.error_message = response_body.get("message") or response_body.get("reason")

        # Always fallback to raw keys if something's missing
        self.params = self.params or []
        self.path = response_body.get("path")

        # Construct message string (for human-readable log line)
        message_parts = [f"HTTP {self.status_code}"]
        if self.error_code:
            message_parts.append(self.error_code)
        if self.error_message:
            message_parts.append(self.error_message)
        if self.params:
            message_parts.append(f"Parameters: {', '.join(self.params)}")

        self.message = " ".join(message_parts)

    def __str__(self):
        # Compact JSON-like output with only populated fields
        error_payload = {
            "status": self.status_code,
            "code": self.error_code,
            "message": self.error_message,
            "url": self.url
        }
        if self.params:
            error_payload["params"] = self.params
        if self.path:
            error_payload["path"] = self.path
        return json.dumps(error_payload, indent=2)

    def __repr__(self):
        return self.__str__()
