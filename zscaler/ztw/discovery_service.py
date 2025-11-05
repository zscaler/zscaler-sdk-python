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

from zscaler.request_executor import RequestExecutor
from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.types import APIResult
from zscaler.ztw.models.discovery_service import DiscoveryService
from zscaler.ztw.models.discovery_service import DiscoveryServicePermissions
from zscaler.utils import format_url


class DiscoveryServiceAPI(APIClient):

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_discovery_settings(self) -> APIResult[DiscoveryService]:
        """
        Retrieves the workload discovery service settings.

        Returns:
            tuple: A tuple containing (DiscoveryService instance, Response, error)

        Examples:
            Get the workload discovery service settings:

            >>> discovery_settings, _, error = client.ztw.discovery_service.get_discovery_settings()
            ... if error:
            ...     print(f"Error getting discovery settings: {error}")
            ...     return
            ... print(f"Discovery settings: {discovery_settings.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /discoveryService/workloadDiscoverySettings
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
            result = DiscoveryService(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_discovery_service_permissions(
        self, account_group_id: int, **kwargs
    ) -> APIResult[DiscoveryServicePermissions]:
        """
        Verifies the specified AWS account permissions using the discovery role and external ID.

            >>> updated_discovery_service_permissions, _, error = (
            ...     client.ztw.discovery_settings.update_discovery_service_permissions(
            ...     discovery_role="arn:aws:iam::123456789012:role/DiscoveryRole",
            ...     external_id="123456789012"
            ... )
            ... if error:
            ...     print(f"Error updating discovery service permissions: {error}")
            ...     return
            ... print(f"Discovery service permissions updated: {updated_discovery_service_permissions.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /discoveryService/{account_group_id}/permissions
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DiscoveryServicePermissions)
        if error:
            return (None, response, error)

        try:
            result = DiscoveryServicePermissions(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
