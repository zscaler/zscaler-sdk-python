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
from zscaler.zpa.models.user_portal_aup import UserPortalAUP
from zscaler.utils import format_url
from zscaler.types import APIResult


class UserPortalAUPAPI(APIClient):
    """
    A client object for the User Portal AUP resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_user_portal_aup(self, query_params: Optional[dict] = None) -> APIResult[List[UserPortalAUP]]:
        """
        Retrieve all Acceptable Use Policy (AUP) configurations for a given customer.

        This endpoint retrieves a list of all AUPs configured for the customer's user portals.
        AUPs define the terms and conditions that users must accept when accessing the portal.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (list of UserPortalAUP instances, Response, error).

        Examples:
            List all AUPs without filtering:

            >>> aup_list, _, err = client.zpa.user_portal_aup.list_user_portal_aup()
            ... if err:
            ...     print(f"Error listing AUPs: {err}")
            ...     return
            ... print(f"Total AUPs found: {len(aup_list)}")
            ... for aup in aup_list:
            ...     print(aup.as_dict())

            List AUPs with query parameters and microtenant ID:

            >>> aup_list, _, err = client.zpa.user_portal_aup.list_user_portal_aup(
            ...     query_params={'search': 'Standard AUP', 'page': '1', 'page_size': '100', 'microtenant_id': '1234567890'}
            ... )
            ... if err:
            ...     print(f"Error listing AUPs: {err}")
            ...     return
            ... print(f"Total AUPs found: {len(aup_list)}")
            ... for aup in aup_list:
            ...     print(f"Name: {aup.name}, Enabled: {aup.enabled}, Description: {aup.description}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userportal/aup
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalAUP)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(UserPortalAUP(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_user_portal_aup(self, portal_id: str, query_params: Optional[dict] = None) -> APIResult[UserPortalAUP]:
        """
        Get information about a specific Acceptable Use Policy (AUP) configuration.

        This endpoint retrieves the details of a specific AUP by its unique identifier.

        Args:
            portal_id (str): The unique identifier of the AUP configuration.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (UserPortalAUP instance, Response, error).

        Examples:
            Get AUP details by ID:

            >>> aup, _, err = client.zpa.user_portal_aup.get_user_portal_aup('999999')
            ... if err:
            ...     print(f"Error fetching AUP by ID: {err}")
            ...     return
            ... print(f"AUP Name: {aup.name}")
            ... print(f"AUP Content: {aup.aup}")
            ... print(f"Enabled: {aup.enabled}")

            Get AUP details with microtenant ID:

            >>> aup, _, err = client.zpa.user_portal_aup.get_user_portal_aup(
            ...     '999999',
            ...     query_params={'microtenant_id': '1234567890'}
            ... )
            ... if err:
            ...     print(f"Error fetching AUP by ID: {err}")
            ...     return
            ... print(f"Fetched AUP: {aup.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userportal/aup/{portal_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalAUP)
        if error:
            return (None, response, error)

        try:
            result = UserPortalAUP(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_user_portal_aup(self, **kwargs) -> APIResult[UserPortalAUP]:
        """
        Add a new Acceptable Use Policy (AUP) configuration.

        This endpoint creates a new AUP configuration for user portals. The AUP defines
        the terms and conditions that users must accept when accessing the portal.

        Keyword Args:
            name (str): The name of the AUP configuration.
            description (str): A description of the AUP configuration.
            aup (str): The Acceptable Use Policy text content that users must accept.
            enabled (bool): Whether the AUP is enabled. Defaults to True.
            email (str): Contact email address for the AUP.
            phone_num (str): Contact phone number for the AUP.
            microtenant_id (str): The unique identifier of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (UserPortalAUP instance, Response, error).

        Examples:
            Add a new AUP configuration:

            >>> aup, _, err = client.zpa.user_portal_aup.add_user_portal_aup(
            ...     name="Standard AUP",
            ...     description="Standard Acceptable Use Policy for all users",
            ...     aup="By accessing this portal, you agree to comply with all company policies...",
            ...     enabled=True,
            ...     email="admin@example.com",
            ...     phone_num="+1-555-123-4567"
            ... )
            ... if err:
            ...     print(f"Error adding AUP: {err}")
            ...     return
            ... print(f"AUP added successfully: {aup.as_dict()}")

            Add a new AUP configuration with microtenant ID:

            >>> aup, _, err = client.zpa.user_portal_aup.add_user_portal_aup(
            ...     name="Microtenant AUP",
            ...     description="AUP for specific microtenant",
            ...     aup="Custom AUP text for microtenant users...",
            ...     enabled=True,
            ...     email="admin@example.com",
            ...     microtenant_id="1234567890"
            ... )
            ... if err:
            ...     print(f"Error adding AUP: {err}")
            ...     return
            ... print(f"AUP ID: {aup.id}, Name: {aup.name}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userportal/aup
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalAUP)
        if error:
            return (None, response, error)

        try:
            result = UserPortalAUP(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_user_portal_aup(self, portal_id: str, **kwargs) -> APIResult[UserPortalAUP]:
        """
        Update an existing Acceptable Use Policy (AUP) configuration.

        This endpoint updates the specified AUP configuration with new values.
        Only the attributes provided in kwargs will be updated.

        Args:
            portal_id (str): The unique identifier of the AUP configuration to update.

        Keyword Args:
            name (str): The name of the AUP configuration.
            description (str): A description of the AUP configuration.
            aup (str): The Acceptable Use Policy text content that users must accept.
            enabled (bool): Whether the AUP is enabled.
            email (str): Contact email address for the AUP.
            phone_num (str): Contact phone number for the AUP.
            microtenant_id (str): The unique identifier of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (UserPortalAUP instance, Response, error).

        Examples:
            Update an AUP configuration:

            >>> updated_aup, _, err = client.zpa.user_portal_aup.update_user_portal_aup(
            ...     portal_id='25456654',
            ...     name="Updated AUP Name",
            ...     description="Updated description",
            ...     enabled=True,
            ...     aup="Updated AUP text content..."
            ... )
            ... if err:
            ...     print(f"Error updating AUP: {err}")
            ...     return
            ... print(f"AUP updated successfully: {updated_aup.as_dict()}")

            Update an AUP configuration with microtenant ID:

            >>> updated_aup, _, err = client.zpa.user_portal_aup.update_user_portal_aup(
            ...     portal_id='25456654',
            ...     enabled=False,
            ...     microtenant_id="1234567890"
            ... )
            ... if err:
            ...     print(f"Error updating AUP: {err}")
            ...     return
            ... print(f"AUP ID: {updated_aup.id}, Enabled: {updated_aup.enabled}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userportal/aup/{portal_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UserPortalAUP)
        if error:
            return (None, response, error)

        if response is None:
            return (UserPortalAUP({"id": portal_id}), None, None)

        try:
            result = UserPortalAUP(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_user_portal_aup(self, portal_id: str, microtenant_id: str = None) -> APIResult[None]:
        """
        Delete an Acceptable Use Policy (AUP) configuration.

        This endpoint permanently deletes the specified AUP configuration.
        Once deleted, the AUP cannot be recovered.

        Args:
            portal_id (str): The unique identifier of the AUP configuration to delete.

        Keyword Args:
            microtenant_id (str, optional): The unique identifier of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (None, Response, error).

        Examples:
            Delete an AUP configuration:

            >>> _, _, err = client.zpa.user_portal_aup.delete_user_portal_aup('513265')
            ... if err:
            ...     print(f"Error deleting AUP: {err}")
            ...     return
            ... print(f"AUP with ID 513265 deleted successfully.")

            Delete an AUP configuration with microtenant ID:

            >>> _, _, err = client.zpa.user_portal_aup.delete_user_portal_aup(
            ...     '513265',
            ...     microtenant_id='1234567890'
            ... )
            ... if err:
            ...     print(f"Error deleting AUP: {err}")
            ...     return
            ... print(f"AUP deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /userportal/aup/{portal_id}
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
