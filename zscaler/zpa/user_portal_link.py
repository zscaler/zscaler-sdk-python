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
from zscaler.zpa.models.user_portal_link import UserPortalLink
from zscaler.zpa.models.user_portal_link import UserPortalLinks
from zscaler.utils import format_url, add_id_groups


class UserPortalLinkAPI(APIClient):
    """
    A client object for the user portal link Link resource.
    """

    reformat_params = [
        ("user_portal_ids", "userPortals"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_portal_link(self, query_params=None) -> tuple:
        """
        Enumerates user portal link link in an organization with pagination.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (list of UserPortalLink instances, Response, error)

        Example:
            Fetch all user portal links without filtering

            >>> portal_list, _, err = client.zpa.user_portal_link.list_user_portal_link()
            ... if err:
            ...     print(f"Error listing user portal link link: {err}")
            ...     return
            ... print(f"Total user portal links found: {len(portal_list)}")
            ... for portal in portal_list:
            ...     print(portal.as_dict())

            Fetch user portal links with query_params filters
            >>> portal_list, _, err = client.zpa.user_portal_link.list_user_portal_link(
            ... query_params={'search': 'UserPortal01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing user portal links: {err}")
            ...     return
            ... print(f"Total user portal links found: {len(portal_list)}")
            ... for portal in portal_list:
            ...     print(portal.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortalLink
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalLink)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(UserPortalLink(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_portal_link(self, portal_link_id: str, query_params=None) -> tuple:
        """
        Gets information on the specified user portal link.

        Args:
            portal_link_id (str): The unique identifier of the user portal link.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: UserPortalController: The corresponding user portal link object.

        Example:
            Retrieve details of a specific user portal link

            >>> fetched_portal, _, err = client.zpa.user_portal_link.get_portal_link('999999')
            ... if err:
            ...     print(f"Error fetching user portal link by ID: {err}")
            ...     return
            ... print(f"Fetched user portal link by ID: {fetched_portal.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortalLink/{portal_link_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalLink)
        if error:
            return (None, response, error)

        try:
            result = UserPortalLink(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_portal_link(self, **kwargs) -> tuple:
        """
        Adds a new user portal link.

        Args:
            name (str): The name of the user portal link.
            description (str): The description of the user portal link.
            enabled (bool): Enable the user portal link. Defaults to True.

        Returns:
            :obj:`Tuple`: UserPortalController: The created user portal link object.

        Example:
            Basic example: Add a new user portal link

            >>> added_portal_link, _, err = client.zpa.user_portal_link.add_portal_link(
            ...     name=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     description=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     link="server1.example.com",
            ...     user_notification_enabled=True,
            ...     icon_text='',
            ...     protocol='https://',
            ...     user_portal_link_ids=['72058304855142822']
            ... )
            >>> if err:
            ...     print(f"Error adding user portal link: {err}")
            ...     return
            ... print(f"user portal link added successfully: {added_portal_link.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortalLink
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "user_portal_link_ids" in body:
            body["userPortals"] = [{"id": portal_link_id} for portal_link_id in body.pop("user_portal_link_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalLink)
        if error:
            return (None, response, error)

        try:
            result = UserPortalLink(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_portal_link(self, portal_link_id: str, **kwargs) -> tuple:
        """
        Updates the specified user portal link.

        Args:
            portal_link_id (str): The unique identifier for the user portal link being updated.

        Returns:
            :obj:`Tuple`: UserPortalController: The updated user portal link object.

        Example:
            Updating a user portal link for a specific microtenant

            >>> updated_portal_link, _, err = client.zpa.user_portal_link.update_portal_link(
            ...     portal_link_id='25456654',
            ...     name=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     description=f"Portal01_Dev_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     link="server1.example.com",
            ...     user_notification_enabled=True,
            ...     icon_text='',
            ...     protocol='https://',
            ...     user_portal_link_ids=['72058304855142822']
            ... )
            >>> if err:
            ...     print(f"Error adding user portal link: {err}")
            ...     return
            ... print(f"user portal link added successfully: {added_portal_link.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortalLink/{portal_link_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "user_portal_link_ids" in body:
            body["userPortals"] = [{"id": portal_link_id} for portal_link_id in body.pop("user_portal_link_ids")]

        add_id_groups(self.reformat_params, kwargs, body)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalLink)
        if error:
            return (None, response, error)

        if response is None:
            return (UserPortalLink({"id": portal_link_id}), None, None)

        try:
            result = UserPortalLink(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_portal_link(
        self,
        portal_link_id: str,
        microtenant_id: str = None
    ) -> tuple:
        """
        Deletes the specified user portal link.

        Args:
            portal_link_id (str): The unique identifier for the user portal link to be deleted.

        Returns:
            int: Status code of the delete operation.

        Example:
            # Delete a user portal link by ID
            >>> _, _, err = client.zpa.user_portal_link.delete_portal_link('513265')
            ... if err:
            ...     print(f"Error deleting user portal link: {err}")
            ...     return
            ... print(f"user portal link with ID {'513265'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userPortalLink/{portal_link_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (None, response, error)

    def add_bulk_portal_links(
        self,
        portal_links: list,
        user_portal_link_ids: list = None,
        **kwargs
    ) -> tuple:
        """
        Adds multiple user portal links in bulk.

        Args:
            portal_links (list[dict]): A list of dictionaries, each containing details for a portal link.
                Each dictionary can contain the following keys:
                - **protocol** (str): The protocol for the portal link (e.g., "http://").
                - **description** (str): Description of the portal link.
                - **icon_text** (str): Text for the icon associated with the portal link.
                - **link** (str): The URL or link address for the portal link.
                - **link_path** (str): The path component of the portal link URL.
                - **name** (str): The name of the portal link.
                - **enabled** (bool): Whether the portal link is enabled or not.
            user_portal_link_ids (list[str], optional): A list of user portal IDs to associate with the portal links.
            **kwargs: Additional keyword arguments that may be passed to the function.

        Returns:
            tuple: A tuple containing:
                - **list[UserPortalLinks]**: A list of newly created portal link instances.
                - **Response**: The raw API response object.
                - **Error**: An error message, if applicable.

        Examples:
            >>> added_consoles, _, err = client.zpa.user_portal_link.add_bulk_portal_links(
            ...     portal_links=[
            ...         dict(
            ...             protocol="http://",
            ...             description="server1.example.com",
            ...             icon_text="",
            ...             link="server1.example.com",
            ...             link_path="",
            ...             name="server1.example.com",
            ...             enabled=True,
            ...         ),
            ...         dict(
            ...             protocol="http://",
            ...             description="server3.example.com",
            ...             icon_text="",
            ...             link="server3.example.com",
            ...             link_path="",
            ...             name="server3.example.com",
            ...             enabled=True,
            ...         )
            ...     ],
            ...     user_portal_link_ids=["72058304855142803"]
            ... )
            >>> if err:
            ...     print(f"Error adding bulk consoles: {err}")
            ...     return
            ... print("Bulk PRA Consoles added successfully")
            ... for console in added_consoles:
            ...     print(console.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /userPortalLink/bulk
        """
        )

        user_portal_links = []
        for portal_link in portal_links:
            if isinstance(portal_link, dict):
                portal_link_data = portal_link
            else:
                portal_link_data = portal_link.as_dict()

            user_portal_links.append(
                {
                    "name": portal_link_data.get("name"),
                    "description": portal_link_data.get("description", ""),
                    "enabled": portal_link_data.get("enabled", True),
                    "iconText": portal_link_data.get("icon_text", ""),
                    "link": portal_link_data.get("link", ""),
                    "linkPath": portal_link_data.get("link_path", ""),
                    "protocol": portal_link_data.get("protocol", "")
                }
            )

        user_portals = [{"id": pid} for pid in user_portal_link_ids] if user_portal_link_ids else []

        body = {
            "userPortalLinks": user_portal_links,
            "userPortals": user_portals
        }

        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
            params=params,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [
                UserPortalLinks(self.form_response_body(item))
                for item in response.get_body()
            ]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_user_portal_link(self, portal_link_id: str, query_params=None) -> tuple:
        """
        Returns information on a User Portal Links for Specified Portal.

        Args:
            portal_link_id (str): The unique identifier for the User Portal Link.

        Returns:
            UserPortalLink: The corresponding portal link object.

        Examples:
            >>> fetched_portal_link, _, err = client.zpa.user_portal_link.get_user_portal_link('999999')
            ... if err:
            ...     print(f"Error fetching portal link by ID: {err}")
            ...     return
            ... print(f"Fetched portal link by ID: {fetched_portal_link.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /userPortalLink/userPortal/{portal_link_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalLink)
        if error:
            return (None, response, error)

        try:
            result = UserPortalLink(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
