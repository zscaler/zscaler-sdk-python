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

from typing import List, Optional
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.pra_portal import PrivilegedRemoteAccessPortal
from zscaler.utils import format_url


class PRAPortalAPI(APIClient):
    """
    A Client object for the Privileged Remote Access Portal resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_portals(self, query_params: Optional[dict] = None) -> List[PrivilegedRemoteAccessPortal]:
        """
        Returns a list of all configured PRA portals.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[PrivilegedRemoteAccessPortal]: A list of PRA portal instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     portals = client.zpa.pra_portal.list_portals()
            ...     for portal in portals:
            ...         print(portal.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/praPortal")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)

        return [PrivilegedRemoteAccessPortal(self.form_response_body(item)) for item in response.get_results()]

    def get_portal(self, portal_id: str, query_params: Optional[dict] = None) -> PrivilegedRemoteAccessPortal:
        """
        Provides information on the specified PRA portal.

        Args:
            portal_id (str): The unique identifier of the portal.
            query_params (dict, optional): Map of query parameters.

        Returns:
            PrivilegedRemoteAccessPortal: The portal object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     portal = client.zpa.pra_portal.get_portal('999999')
            ...     print(portal.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/praPortal/{portal_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)

        return PrivilegedRemoteAccessPortal(self.form_response_body(response.get_body()))

    def add_portal(self, **kwargs) -> PrivilegedRemoteAccessPortal:
        """
        Adds a new PRA portal.

        Args:
            name (str): The name of the PRA portal.
            certificate_id (str): The unique identifier of the certificate.
            domain (str): The domain of the PRA portal.
            enabled (bool): Whether the PRA portal is enabled.

        Returns:
            PrivilegedRemoteAccessPortal: The newly created portal object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     portal = client.zpa.pra_portal.add_portal(
            ...         name="PRA Portal",
            ...         domain="portal.acme.com",
            ...         certificate_id="72058304855021564",
            ...         enabled=True
            ...     )
            ...     print(portal.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/praPortal")

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)

        return PrivilegedRemoteAccessPortal(self.form_response_body(response.get_body()))

    def update_portal(self, portal_id: str, **kwargs) -> PrivilegedRemoteAccessPortal:
        """
        Updates the specified PRA portal.

        Args:
            portal_id (str): The unique identifier of the portal.
            **kwargs: Fields to update.

        Returns:
            PrivilegedRemoteAccessPortal: The updated portal object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     portal = client.zpa.pra_portal.update_portal(
            ...         "999999",
            ...         name="Updated Portal",
            ...         enabled=True
            ...     )
            ...     print(portal.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/praPortal/{portal_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)

        if response is None:
            return PrivilegedRemoteAccessPortal({"id": portal_id})

        return PrivilegedRemoteAccessPortal(self.form_response_body(response.get_body()))

    def delete_portal(self, portal_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified PRA portal.

        Args:
            portal_id (str): The unique identifier of the portal.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.pra_portal.delete_portal('999999')
            ...     print("Portal deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/praPortal/{portal_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
