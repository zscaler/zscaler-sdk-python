from typing import Any, Dict
import requests


class HTTPError(Exception):
    def __init__(self, url: str, response_details: requests.Response, response_body: str) -> None:
        self.status_code: int = response_details.status_code
        self.url: str = url
        self.response_headers: Dict[str, Any] = response_details.headers
        self.message: str = f"HTTP {self.status_code} {response_body}"
        super().__init__(self.message)  # ✅ important

    def __str__(self) -> str:
        return self.message
