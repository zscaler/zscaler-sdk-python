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

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zidentity.models.user_entitlement import Entitlement, Entitlements
from zscaler.zidentity.models.user_entitlement import Service
from zscaler.utils import format_url


class EntitlementAPI(APIClient):
    """
    A Client object for the Entitlement API resource.
    """

    _zidentity_base_endpoint = "/admin/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_admin_entitlement(self, user_id: str) -> tuple:
        """
        Retrieves the administrative entitlements for a specific user by their user ID.

        Args:
            user_id (str): The user ID of the individual whose admin entitlements are being retrieved.

        Returns:
            tuple: A tuple containing Entitlements collection, Response, error).

        Examples:
            Print a specific User

            >>> fetched_entitlements, _, error = client.zidentity.user_entitlement.get_admin_entitlement(
                'ihlmch6ikg7m1')
            >>> if error:
            ...     print(f"Error fetching Entitlement for User by ID: {error}")
            ...     return
            ... print(f"Fetched Entitlements by User ID: {fetched_entitlements.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /users/{user_id}/admin-entitlements
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Entitlements)
        if error:
            return (None, response, error)

        try:
            result = Entitlements(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_service_entitlement(self, user_id: str) -> tuple:
        """
        Retrieves service entitlements for a specified user ID.

        Args:
            user_id (str): The user ID of the individual for whom the service entitlements are to be retrieved.

        Returns:
            tuple: A tuple containing Service Entitlement instance, Response, error).

        Examples:
            Print a specific User

            >>> fetched_entitlement, _, error = client.zidentity.users.get_service_entitlement(
                'ihlmch6ikg7m1')
            >>> if error:
            ...     print(f"Error fetching Entitlement for User by ID: {error}")
            ...     return
            ... print(f"Fetched Entitlement by User ID: {fetched_entitlement.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zidentity_base_endpoint}
            /users/{user_id}/service-entitlements
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Service)
        if error:
            return (None, response, error)

        try:
            result = Service(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
