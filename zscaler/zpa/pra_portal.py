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
                ``[query_params.page_size]`` {int}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: A list of `PrivilegedRemoteAccessPortal` instances.
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

        # Prepare request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivilegedRemoteAccessPortal(
                    self.form_response_body(item)))
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
            PrivilegedRemoteAccessPortal: The corresponding portal object.
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

        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, PrivilegedRemoteAccessPortal)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessPortal(
                self.form_response_body(response.get_body())
            )
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
            PrivilegedRemoteAccessPortal: The newly created portal object.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /praPortal
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, PrivilegedRemoteAccessPortal)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessPortal(
                self.form_response_body(response.get_body())
            )
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
            PrivilegedRemoteAccessPortal: The updated portal object.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praPortal/{portal_id}
        """
        )

        # Start with an empty body or an existing resource's current data
        body = {}

        # Update the body with the fields passed in kwargs
        body.update(kwargs)

        # Use get instead of pop to keep microtenant_id in the body
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, PrivilegedRemoteAccessPortal)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (PrivilegedRemoteAccessPortal({"id": portal_id}), None, None)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = PrivilegedRemoteAccessPortal(
                self.form_response_body(response.get_body())
            )
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
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /praPortal/{portal_id}
        """
        )

        # Handle microtenant_id in URL params if provided
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
