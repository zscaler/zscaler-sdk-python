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
from zscaler.zeasm.models.lookalike_domains import LookALikeDomains, LookalikeDomainDetails
from zscaler.utils import format_url
from zscaler.types import APIResult


class LookALikeDomainsAPI(APIClient):
    """
    A Client object for the ZEASM Lookalike Domains resource.

    This class provides methods to interact with ZEASM lookalike domains,
    allowing you to retrieve and manage lookalike domains detected for
    an organization's assets.
    """

    _zeasm_base_endpoint = "/easm/easm-ui/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_lookalike_domains(self, org_id: str) -> APIResult[LookALikeDomains]:
        """
        Retrieves the list of lookalike domains for an organization.

        Args:
            org_id (str): The unique identifier for the organization.

        Returns:
            tuple: A tuple containing:
                - LookALikeDomains: Object containing results list and total_results count
                - Response: The raw API response object
                - error: Any error that occurred, or None if successful

        Examples:
            List all lookalike domains for an organization::

                >>> domains, _, err = client.zeasm.lookalike_domains.list_lookalike_domains(
                ...     org_id="3f61a446-1a0d-11f0-94e8-8a5f4d45e80c"
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> if domain:
                ...     print(domain.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zeasm_base_endpoint}
            /organizations/{org_id}/lookalike-domains
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

        try:
            result = LookALikeDomains(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_lookalike_domain(self, org_id: str, lookalike_raw: str) -> APIResult[LookalikeDomainDetails]:
        """
        Retrieves details for a lookalike domain based on the specified domain name.

        Args:
            org_id (str): The unique identifier for the organization.
            lookalike_raw (str): The lookalike domain name (e.g., "assuredartners.com").

        Returns:
            tuple: A tuple containing:
                - LookalikeDomainDetails: Object containing the domain details
                - Response: The raw API response object
                - error: Any error that occurred, or None if successful

        Examples:
            Get details for a specific lookalike domain::

                >>> domain, _, err = client.zeasm.lookalike_domains.get_lookalike_domain(
                ...     org_id="3f61a446-1a0d-11f0-94e8-8a5f4d45e80c",
                ...     lookalike_raw="assuredartners.com"
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> print(domain.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zeasm_base_endpoint}
            /organizations/{org_id}/lookalike-domains/{lookalike_raw}/details
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LookalikeDomainDetails)
        if error:
            return (None, response, error)

        try:
            result = LookalikeDomainDetails(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
