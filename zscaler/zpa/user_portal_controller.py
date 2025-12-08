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
from zscaler.zpa.models.user_portal_controller import UserPortalController
from zscaler.utils import format_url


class UserPortalControllerAPI(APIClient):
    """
    A client object for the User Portal Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_user_portals(self, query_params: Optional[dict] = None) -> List[UserPortalController]:
        """
        Enumerates user portals in an organization with pagination.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.ui_config]`` {str}: Filter by UI Configuration.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing List[UserPortalController]

        Example:
            Fetch all user portals without filtering

            >>> try:
            ...     portal_list = client.zpa.user_portal_controller.list_user_portals()
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Total user portals found: {len(portal_list)}")
            ... for portal in portal_list:
            ...     print(portal.as_dict())

            Fetch user portals with query_params filters
            >>> try:
            ...     portal_list = client.zpa.user_portal_controller.list_user_portals(
            ... query_params={'search': 'UserPortal01', 'page': '1', 'page_size': '100'})
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Total user portals found: {len(portal_list)}")
            ... for portal in portal_list:
            ...     print(portal.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortal
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, UserPortalController)
        result = []
        for item in response.get_results():
            result.append(UserPortalController(self.form_response_body(item)))
        return result

    def get_user_portal(self, portal_id: str, query_params: Optional[dict] = None) -> UserPortalController:
        """
        Gets information on the specified user portal.

        Args:
            portal_id (str): The unique identifier of the user portal.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: UserPortalController: The corresponding user portal object.

        Example:
            Retrieve details of a specific user portal

            >>> try:
            ...     fetched_portal = client.zpa.user_portal_controller.get_user_portal('999999')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"Fetched user portal by ID: {fetched_portal.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortal/{portal_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, UserPortalController)
        result = UserPortalController(self.form_response_body(response.get_body()))
        return result

    def add_user_portal(self, **kwargs) -> UserPortalController:
        """
        Adds a new user portal.

        Args:
            name (str): The name of the user portal.
            description (str): The description of the user portal.
            enabled (bool): Enable the user portal. Defaults to True.
            user_notification (str): The user notification message for the portal.
            user_notification_enabled (bool): Whether user notifications are enabled for the portal.
            managed_by_zs (bool): Whether the portal is managed by Zscaler.
            ext_label (str): The external label for the portal.
            ext_domain (str): The external domain for the portal.
            ext_domain_name (str): The external domain name for the portal.

        Returns:
            :obj:`Tuple`: UserPortalController: The created user portal object.

        Example:
            Basic example: Add a new user portal

            >>> try:
            ...     added_portal = client.zpa.user_portal_controller.add_user_portal(
            ...     name=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     description=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     user_notification=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     user_notification_enabled=True,
            ...     managed_by_zs=True,
            ...     ext_label='portal01',
            ...     ext_domain='acme.com'
            ...     ext_domain_name='-acme.com.b.zscalerportal.net'
            ... )
            >>> if err:
            ...     print(f"Error adding user portal: {err}")
            ...     return
            ... print(f"user portal added successfully: {added_portal.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortal
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, UserPortalController)
        result = UserPortalController(self.form_response_body(response.get_body()))
        return result

    def update_user_portal(self, portal_id: str, **kwargs) -> UserPortalController:
        """
        Updates the specified user portal.

        Args:
            portal_id (str): The unique identifier for the user portal being updated.

        Returns:
            :obj:`Tuple`: UserPortalController: The updated user portal object.

        Example:
            Updating a user portal for a specific microtenant

            >>> try:
            ...     updated_portal = client.zpa.user_portal_controller.update_user_portal(
            ...     portal_id='25456654',
            ...     name=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     description=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     user_notification=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     user_notification_enabled=True,
            ...     managed_by_zs=True,
            ...     ext_label='portal01',
            ...     ext_domain='acme.com'
            ...     ext_domain_name='-acme.com.b.zscalerportal.net'
            ... )
            >>> if err:
            ...     print(f"Error updating user portal: {err}")
            ...     return
            ... print(f"User portal updated successfully: {updated_portal.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortal/{portal_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, UserPortalController)
        if response is None:
            return UserPortalController({"id": portal_id})

        result = UserPortalController(self.form_response_body(response.get_body()))
        return result

    def delete_user_portal(self, portal_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified user portal.

        Args:
            portal_id (str): The unique identifier for the user portal to be deleted.

        Returns:
            int: Status code of the delete operation.

        Example:
            # Delete a user portal by ID
            >>> try:
            ...     _ = client.zpa.user_portal_controller.delete_user_portal('513265')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(f"User Portal with ID {'513265'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortal/{portal_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)

        return None
