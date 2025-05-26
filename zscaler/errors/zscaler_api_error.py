import json


class ZscalerAPIError(Exception):
    def __init__(self, url, response_details, response_body, service_type=""):
        self.status_code = response_details.status_code
        self.url = url
        self.service_type = service_type.lower()
        self.headers = response_details.headers
        self.stack = ""

        if not isinstance(response_body, dict):
            response_body = {"message": str(response_body)}

        self.error_code = response_body.get("code") or response_body.get("id")
        self.error_message = response_body.get("message") or response_body.get("reason")
        self.params = response_body.get("params", [])
        self.path = response_body.get("path")

        message_parts = [f"HTTP {self.status_code}"]
        if self.error_code:
            message_parts.append(str(self.error_code))
        if self.error_message:
            message_parts.append(self.error_message)
        if self.params:
            message_parts.append(f"Parameters: {', '.join(self.params)}")

        self.message = " ".join(message_parts)
        super().__init__(self.message)  # ✅ This is what makes it raise-able

    def __str__(self):
        error_payload = {
            "status": self.status_code,
            "code": self.error_code,
            "message": self.error_message,
            "url": self.url,
        }
        if self.params:
            error_payload["params"] = self.params
        if self.path:
            error_payload["path"] = self.path
        return json.dumps(error_payload, indent=2)

    def __repr__(self):
        return self.__str__()
