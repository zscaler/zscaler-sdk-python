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

    def list_portals(self, query_params=None) -> tuple:
        """
        Returns a list of all configured PRA portals with pagination support.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A list of `PrivilegedRemoteAccessPortal` instances.

        Examples:
            >>> portals_list, _, err = client.zpa.pra_portal.list_portals(
            ... query_params={'search': 'portal01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing pra portals: {err}")
            ...     return
            ... print(f"Total pra portals found: {len(portals_list)}")
            ... for pra in portals_list:
            ...     print(pra.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praPortal
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivilegedRemoteAccessPortal(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_portal(self, portal_id: str, query_params=None) -> tuple:
        """
        Provides information on the specified PRA portal.

        Args:
            portal_id (str): The unique identifier of the portal.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessPortal: The corresponding portal object.

        Examples:
            >>> fetched_portal, _, err = client.zpa.pra_portal.get_portal('999999')
            ... if err:
            ...     print(f"Error fetching portal by ID: {err}")
            ...     return
            ... print(f"Fetched portal by ID: {fetched_portal.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /praPortal/{portal_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessPortal(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_portal(self, **kwargs) -> tuple:
        """
        Adds a new PRA portal.

        Args:
            name (str): The name of the PRA portal.
            certificate_id (str): The unique identifier of the certificate.
            domain (str): The domain of the PRA portal.
            enabled (bool): Whether the PRA portal is enabled (default is True).

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessPortal: The newly created portal object.

        Examples:
            >>> new_portal, _, err = client.zpa.pra_portal.add_portal(
            ...     name="PRA Portal",
            ...     description="PRA Portal",
            ...     enabled=True,
            ...     domain="portal.acme.com",
            ...     certificate_id="72058304855021564",
            ...     user_notification="PRA Portal",
            ...     user_notification_enabled= True,
            ... )
            ... if err:
            ...     print(f"Error creating portal: {err}")
            ...     return
            ... print(f"portal created successfully: {new_portal.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /praPortal
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessPortal(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_portal(self, portal_id: str, **kwargs) -> tuple:
        """
        Updates the specified PRA portal.

        Args:
            portal_id (str): The unique identifier of the portal being updated.
            microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            :obj:`Tuple`: PrivilegedRemoteAccessPortal: The updated portal object.

        Examples:
            >>> update_portal, _, err = client.zpa.pra_portal.update_portal(
            ...     portal_id="999999",
            ...     name="PRA Portal",
            ...     description="Update PRA Portal",
            ...     enabled=True,
            ...     domain="portal.acme.com",
            ...     certificate_id="72058304855021564",
            ...     user_notification="Update PRA Portal",
            ...     user_notification_enabled= True,
            ... )
            ... if err:
            ...     print(f"Error creating portal: {err}")
            ...     return
            ... print(f"portal created successfully: {new_portal.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praPortal/{portal_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessPortal)
        if error:
            return (None, response, error)

        if response is None:
            return (PrivilegedRemoteAccessPortal({"id": portal_id}), None, None)

        try:
            result = PrivilegedRemoteAccessPortal(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_portal(self, portal_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified PRA portal.

        Args:
            portal_id (str): The unique identifier of the portal to be deleted.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            int: Status code of the delete operation.

        Examples:
            >>> _, _, err = client.zpa.pra_portal.delete_portal(
            ...     portal_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting pra portal: {err}")
            ...     return
            ... print(f"PRA Portal with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praPortal/{portal_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
