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

from typing import Dict, Any, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.ransomware_kill import (
    RansomwareKillEmailTemplate,
    RansomwareKillErrorPayload,
    RansomwareKillState,
)


class RansomwareKillAPI(APIClient):
    """
    Client for the ZTB Ransomware Kill resource.

    Provides operations for managing ransomware kill state and email
    templates in the Zero Trust Branch API.

    Endpoints live under ``/api/v3/ransomware-kill``.
    """

    _ztb_base_endpoint = "/ztb/api/v3"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_email_template(self, site_id: str) -> APIResult:
        """
        Get Ransomware email template by site id.

        Args:
            site_id (str): The unique identifier of the site.

        Returns:
            tuple: (RansomwareKillEmailTemplate instance, Response, error).

        Examples:
            Get email template for a site::

                >>> template, _, error = client.ztb.ransomware_kill.get_email_template("site-123")
                >>> if error:
                ...     print(f"Error fetching template: {error}")
                ...     return
                >>> print(template.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /ransomware-kill/email-template/{site_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RansomwareKillEmailTemplate)

        if error:
            return (None, response, error)

        try:
            result = RansomwareKillEmailTemplate(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def save_email_template(
        self,
        site_id: str,
        *,
        cluster_token: Optional[str] = None,
        email_body: Optional[str] = None,
        recipients: Optional[str] = None,
        token: Optional[str] = None,
        **kwargs: Any,
    ) -> APIResult:
        """
        Save email template message for a site.

        Args:
            site_id (str): The unique identifier of the site.
            cluster_token (str, optional): Cluster token.
            email_body (str, optional): The body of the notification email.
            recipients (str, optional): Comma-separated list of recipient emails.
            token (str, optional): Authentication token.
            **kwargs: Additional fields (snake_case) passed to the API.

        Returns:
            tuple: (RansomwareKillEmailTemplate instance, Response, error).

        Examples:
            Save email template::

                >>> template, _, error = client.ztb.ransomware_kill.save_email_template(
                ...     site_id="site-123",
                ...     email_body="Ransomware detected. Please investigate.",
                ...     recipients="admin@example.com,security@example.com",
                ... )
                >>> if error:
                ...     print(f"Error saving template: {error}")
                ...     return
                >>> print(template.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /ransomware-kill/email-template/{site_id}
        """
        )

        body: Dict[str, Any] = {
            "cluster_token": cluster_token,
            "email_body": email_body,
            "recipients": recipients,
            "token": token,
        }
        body = {k: v for k, v in body.items() if v is not None}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RansomwareKillEmailTemplate)

        if error:
            return (None, response, error)

        try:
            result = RansomwareKillEmailTemplate(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_state(self) -> APIResult:
        """
        Get Ransomware kill state.

        Returns:
            tuple: (RansomwareKillState or RansomwareKillErrorPayload, Response, error).
                On 200 Success: RansomwareKillState (cluster_token, token, result).
                On error/default: RansomwareKillErrorPayload (detail, errorCode,
                message, requestKey, statusCode).

        Examples:
            Get ransomware kill state::

                >>> state, _, error = client.ztb.ransomware_kill.get_state()
                >>> if error:
                ...     print(f"Error fetching state: {error}")
                ...     return
                >>> if hasattr(state, "error_code") and state.error_code is not None:
                ...     print(f"API error: {state.message}")
                ... else:
                ...     print(state.cluster_token, state.token)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /ransomware-kill/state/
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        body_data = response.get_body() if response else {}
        if not body_data:
            return (None, response, None)

        try:
            if "errorCode" in body_data or "statusCode" in body_data or "detail" in body_data:
                result = RansomwareKillErrorPayload(body_data)
            else:
                result = RansomwareKillState(body_data)
        except Exception as parse_error:
            return (None, response, parse_error)
        return (result, response, None)

    def update_state(self, site_id: str, color: str) -> APIResult:
        """
        Update Ransomware kill state for a site.

        Args:
            site_id (str): The unique identifier of the site.
            color (str): The kill state color. One of: ``green``, ``yellow``,
                ``orange``, ``red``.

        Returns:
            tuple: (None, Response, error).

        Examples:
            Update ransomware kill state::

                >>> _, _, error = client.ztb.ransomware_kill.update_state(
                ...     site_id="site-123",
                ...     color="yellow",
                ... )
                >>> if error:
                ...     print(f"Error updating state: {error}")
                ...     return
                >>> print("State updated successfully.")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /ransomware-kill/state/{site_id}/{color}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (None, response, None)
