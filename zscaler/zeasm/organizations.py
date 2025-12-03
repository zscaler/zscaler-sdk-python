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
from zscaler.zeasm.models.organizations import Organizations
from zscaler.utils import format_url
from zscaler.types import APIResult


class OrganizationsAPI(APIClient):
    """
    A Client object for the ZEASM Organizations resource.

    This class provides methods to interact with ZEASM organizations,
    allowing you to retrieve organizations configured for a tenant.
    """

    _zeasm_base_endpoint = "/easm/easm-ui/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_organizations(self) -> APIResult[Organizations]:
        """
        Retrieves all organizations configured for a tenant in the EASM Admin Portal.

        Returns:
            tuple: A tuple containing:
                - Organizations: Object containing results list and total_results count
                - Response: The raw API response object
                - error: Any error that occurred, or None if successful

        Examples:
            List all organizations::

                >>> orgs, _, err = client.zeasm.organizations.list_organizations()
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> print(f"Total organizations: {orgs.total_results}")
                >>> for org in orgs.results:
                ...     print(f"  ID: {org.id}, Name: {org.name}")

            Get the first organization ID for use with other ZEASM APIs::

                >>> orgs, _, err = client.zeasm.organizations.list_organizations()
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> if orgs.results:
                ...     org_id = orgs.results[0].id
                ...     print(f"Using organization: {org_id}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zeasm_base_endpoint}
            /organizations
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
            result = Organizations(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
