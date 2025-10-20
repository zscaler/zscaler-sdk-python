from typing import Dict, Any, List, Union, Optional
import json
import requests


class ZscalerAPIError(Exception):
    def __init__(
        self, 
        url: str, 
        response_details: requests.Response, 
        response_body: Union[Dict[str, Any], str], 
        service_type: str = ""
    ) -> None:
        self.status_code: int = response_details.status_code
        self.url: str = url
        self.service_type: str = service_type.lower()
        self.headers: Dict[str, Any] = response_details.headers
        self.stack: str = ""

        if not isinstance(response_body, dict):
            response_body = {"message": str(response_body)}

        self.error_code: Optional[Union[str, int]] = response_body.get("code") or response_body.get("id")
        self.error_message: Optional[str] = response_body.get("message") or response_body.get("reason")
        self.params: List[Any] = response_body.get("params", [])
        self.path: Optional[str] = response_body.get("path")

        message_parts: List[str] = [f"HTTP {self.status_code}"]
        if self.error_code:
            message_parts.append(str(self.error_code))
        if self.error_message:
            message_parts.append(self.error_message)
        if self.params:
            # Handle mixed types in params (lists and strings) safely
            param_strings: List[str] = []
            for param in self.params:
                if isinstance(param, list):
                    # Flatten lists and join with commas
                    param_strings.append(', '.join(str(item) for item in param))
                else:
                    # Convert non-list items to strings
                    param_strings.append(str(param))
            message_parts.append(f"Parameters: {', '.join(param_strings)}")

        self.message: str = " ".join(message_parts)
        super().__init__(self.message)  # ✅ This is what makes it raise-able

    def __str__(self) -> str:
        error_payload: Dict[str, Any] = {
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

    def __repr__(self) -> str:
        return self.__str__()
