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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zaiguard.models.policy_detection import (
    ExecuteDetectionsPolicyRequest,
    ExecuteDetectionsPolicyResponse,
    ResolveAndExecuteDetectionsPolicyResponse,
)
from zscaler.utils import format_url
from zscaler.types import APIResult


class PolicyDetectionAPI(APIClient):
    """
    API client for AIGuard Policy Detection operations.
    """

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._base_endpoint = "/v1"

    def execute_policy(
        self,
        content: str,
        direction: str,
        policy_id: Optional[int] = None,
        transaction_id: Optional[str] = None,
    ) -> APIResult[ExecuteDetectionsPolicyResponse]:
        """
        Executes a policy detection with a specific policy ID.

        Args:
            content (str): The content to scan
            direction (str): The direction of the content ('IN' or 'OUT')
            policy_id (int, optional): The policy ID to execute against
            transaction_id (str, optional): Optional transaction ID for tracking

        Returns:
            APIResult[ExecuteDetectionsPolicyResponse]: Tuple of (result, response, error)

        Examples:
            Minimal payload (content + direction):
                >>> result, resp, err = client.zguard.policy_detection.execute_policy(
                ...     content="User prompt or AI response to scan",
                ...     direction="IN"
                ... )

            With optional policy_id and transaction_id:
                >>> result, resp, err = client.zguard.policy_detection.execute_policy(
                ...     content="Content to scan",
                ...     direction="OUT",
                ...     policy_id=12345,
                ...     transaction_id="txn-abc-123"
                ... )
        """
        http_method = "POST"
        api_url = format_url(
            f"""
            {self._base_endpoint}
            /detection/execute-policy
        """
        )

        body = {
            "content": content,
            "direction": direction,
        }

        if policy_id is not None:
            body["policyId"] = policy_id

        if transaction_id is not None:
            body["transactionId"] = transaction_id

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ExecuteDetectionsPolicyResponse)
        if error:
            return (None, response, error)

        try:
            result = ExecuteDetectionsPolicyResponse(self.form_response_body(response.get_body()))

            # Handle rate limiting from response body (AIGuard-specific)
            if result.throttling_details and len(result.throttling_details) > 0:
                # Check if we're using a legacy client with rate limiting
                if hasattr(self._request_executor, 'zguard_legacy_client'):
                    legacy_client = self._request_executor.zguard_legacy_client
                    if legacy_client and hasattr(legacy_client, '_handle_throttling_details'):
                        # Let the client handle throttling
                        legacy_client._handle_throttling_details(result.throttling_details)

        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def resolve_and_execute_policy(
        self,
        content: str,
        direction: str,
        transaction_id: Optional[str] = None,
    ) -> APIResult[ResolveAndExecuteDetectionsPolicyResponse]:
        """
        Resolves and executes a policy detection (automatic policy selection).

        Args:
            content (str): The content to scan
            direction (str): The direction of the content ('IN' or 'OUT')
            transaction_id (str, optional): Optional transaction ID for tracking

        Returns:
            APIResult[ResolveAndExecuteDetectionsPolicyResponse]: Tuple of (result, response, error)

        Examples:
            Minimal payload (content + direction):
                >>> result, resp, err = client.zguard.policy_detection.resolve_and_execute_policy(
                ...     content="User prompt or AI response to scan",
                ...     direction="IN"
                ... )

            With optional transaction_id:
                >>> result, resp, err = client.zguard.policy_detection.resolve_and_execute_policy(
                ...     content="Content to scan",
                ...     direction="OUT",
                ...     transaction_id="txn-abc-123"
                ... )
        """
        http_method = "POST"
        api_url = format_url(
            f"""
            {self._base_endpoint}
            /detection/resolve-and-execute-policy
        """
        )

        body = {
            "content": content,
            "direction": direction,
        }

        if transaction_id is not None:
            body["transactionId"] = transaction_id

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ResolveAndExecuteDetectionsPolicyResponse)
        if error:
            return (None, response, error)

        try:
            result = ResolveAndExecuteDetectionsPolicyResponse(self.form_response_body(response.get_body()))

            # Handle rate limiting from response body (AIGuard-specific)
            if result.throttling_details and len(result.throttling_details) > 0:
                # Check if we're using a legacy client with rate limiting
                if hasattr(self._request_executor, 'zguard_legacy_client'):
                    legacy_client = self._request_executor.zguard_legacy_client
                    if legacy_client and hasattr(legacy_client, '_handle_throttling_details'):
                        # Let the client handle throttling
                        legacy_client._handle_throttling_details(result.throttling_details)

        except Exception as error:
            return (None, response, error)

        return (result, response, None)
