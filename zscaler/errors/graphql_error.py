"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
import json
import requests


@dataclass
class GraphQLErrorLocation:
    """Represents a location in a GraphQL query where an error occurred."""
    line: int
    column: int

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> "GraphQLErrorLocation":
        return cls(
            line=data.get("line", 0),
            column=data.get("column", 0)
        )


@dataclass
class GraphQLErrorDetail:
    """Represents a single GraphQL error from the errors array."""
    message: str
    locations: List[GraphQLErrorLocation] = field(default_factory=list)
    path: List[str] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphQLErrorDetail":
        locations = [
            GraphQLErrorLocation.from_dict(loc)
            for loc in data.get("locations", [])
        ]
        return cls(
            message=data.get("message", "Unknown GraphQL error"),
            locations=locations,
            path=data.get("path", []),
            extensions=data.get("extensions", {})
        )

    @property
    def classification(self) -> Optional[str]:
        """Get the error classification from extensions."""
        return self.extensions.get("classification")

    def __str__(self) -> str:
        parts = [self.message]
        if self.path:
            parts.append(f"Path: {'.'.join(str(p) for p in self.path)}")
        if self.classification:
            parts.append(f"Classification: {self.classification}")
        return " | ".join(parts)


class GraphQLAPIError(Exception):
    """
    Exception for GraphQL API errors from Z-Insights.

    GraphQL APIs return errors in a different format than REST:
    {
        "errors": [
            {
                "message": "...",
                "locations": [{"line": 1, "column": 1}],
                "path": ["query", "field"],
                "extensions": {"classification": "BAD_REQUEST"}
            }
        ],
        "data": {...}
    }
    """

    def __init__(
        self,
        url: str,
        response_details: requests.Response,
        response_body: Union[Dict[str, Any], str],
        service_type: str = "zins"
    ) -> None:
        self.url: str = url
        self.status_code: int = response_details.status_code
        self.service_type: str = service_type
        self.headers: Dict[str, Any] = dict(response_details.headers)

        # Parse the response body
        if isinstance(response_body, str):
            try:
                response_body = json.loads(response_body)
            except json.JSONDecodeError:
                response_body = {"errors": [{"message": response_body}]}

        # Extract GraphQL errors
        raw_errors = response_body.get("errors", [])
        self.errors: List[GraphQLErrorDetail] = [
            GraphQLErrorDetail.from_dict(err) for err in raw_errors
        ]

        # Store the data portion (may be partial)
        self.data: Optional[Dict[str, Any]] = response_body.get("data")

        # Build the error message
        if self.errors:
            self.error_message = self.errors[0].message
            self.classification = self.errors[0].classification
            self.path = self.errors[0].path
        else:
            self.error_message = "Unknown GraphQL error"
            self.classification = None
            self.path = []

        # Construct the full message
        message_parts = [f"GraphQL Error"]
        if self.status_code != 200:
            message_parts.append(f"HTTP {self.status_code}")
        if self.classification:
            message_parts.append(f"[{self.classification}]")
        message_parts.append(self.error_message)

        self.message = " - ".join(message_parts)
        super().__init__(self.message)

    @property
    def is_bad_request(self) -> bool:
        """Check if the error is a BAD_REQUEST classification."""
        return self.classification == "BAD_REQUEST"

    @property
    def is_validation_error(self) -> bool:
        """Check if the error is a validation error."""
        return self.classification in ["BAD_REQUEST", "VALIDATION_ERROR"]

    @property
    def is_authorization_error(self) -> bool:
        """Check if the error is an authorization error."""
        return self.classification in ["UNAUTHORIZED", "FORBIDDEN"]

    @property
    def all_error_messages(self) -> List[str]:
        """Get all error messages from the errors array."""
        return [err.message for err in self.errors]

    def __str__(self) -> str:
        error_payload = {
            "service": self.service_type,
            "status": self.status_code,
            "url": self.url,
            "errors": [
                {
                    "message": err.message,
                    "path": err.path,
                    "classification": err.classification
                }
                for err in self.errors
            ]
        }
        return json.dumps(error_payload, indent=2)

    def __repr__(self) -> str:
        return f"GraphQLAPIError({self.message})"


def is_graphql_error_response(response_body: Union[Dict[str, Any], str]) -> bool:
    """
    Check if a response body contains GraphQL errors.

    GraphQL can return HTTP 200 with errors in the body, so we need
    to check the response structure, not just the status code.

    Args:
        response_body: The response body (dict or JSON string)

    Returns:
        True if the response contains GraphQL errors
    """
    if isinstance(response_body, str):
        try:
            response_body = json.loads(response_body)
        except json.JSONDecodeError:
            return False

    if not isinstance(response_body, dict):
        return False

    # GraphQL error responses have an "errors" array
    errors = response_body.get("errors")
    if errors and isinstance(errors, list) and len(errors) > 0:
        return True

    return False

