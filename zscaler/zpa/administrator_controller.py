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
from zscaler.zpa.models.administrator_controller import AdministratorController
from zscaler.utils import format_url


class AdministratorControllerAPI(APIClient):
    """
    A Client object for the administrator controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_administrators(self, query_params=None) -> tuple:
        """
        Get all administrators in a company/customer.
        A mmaximum of 200 administrators are returned per request.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 200.

                ``[query_params.search]`` {str}: Search string for filtering results.

                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of AdministratorController instances, Response, error)

        Examples:
            >>> admin_list, _, err = client.zpa.administrator_controller.list_administrators()
            ... if err:
            ...     print(f"Error listing administrors: {err}")
            ...     return
            ... print(f"Total administrators found: {len(admin_list)}")
            ... for admin in admins:
            ...     print(admin.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /administrators
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(AdministratorController(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_administrator(self, admin_id: str, query_params=None) -> tuple:
        """
        Fetches a specific administrator details by ID.

        Args:
            admin_id (str): The unique identifier for the administrator.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (AdministratorController instance, Response, error).

        Examples:
            >>> fetched_admin, _, err = client.zpa.administrator_controller.get_administrator('999999')
            ... if err:
            ...     print(f"Error fetching admin by ID: {err}")
            ...     return
            ... print(f"Fetched admin by ID: {fetched_admin.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /administrators/{admin_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdministratorController)
        if error:
            return (None, response, error)

        try:
            result = AdministratorController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_administrator(self, **kwargs) -> tuple:
        """
        Adds a new ZPA admministrator.

        Args:
            name (str): The name of the Administrator.

        Keyword Args:

        Returns:
            :obj:`Tuple`: A tuple containing (AdministratorController, Response, error)

        Examples:
            Adding a new local administrator account

            >>> added_admin, _, err = client.zpa.administrator_controller.add_administrator(
            ...     username="jdoe@0000004767847.zpa-customer.com",
            ...     email="jdoe@0000004767847.zpa-customer.com",
            ...     display_name="John Doe",
            ...     password="",
            ...     confirm_password="",
            ...     is_enabled=True,
            ...     role_id="12",
            ...     role={
            ...         "id": "12",
            ...     },
            ...     eula="0"
            ... )
            >>> if err:
            ...     print(f"Error adding administrator: {err}")
            ...     return
            ... print(f"Administrator added successfully: {added_admin.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /administrators
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdministratorController)
        if error:
            return (None, response, error)

        try:
            result = AdministratorController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_administrator(self, admin_id: str, **kwargs) -> tuple:
        """
        Updates an existing ZPA c.

        Args:
            admin_id (str): The unique id for the Administrator in ZPA.

        Keyword Args:

        Returns:
            tuple: A tuple containing (AppConnectorGroup, Response, error)

        Examples:
            Updating a new local administrator account

            >>> updated_admin, _, err = client.zpa.administrator_controller.add_administrator(
            ...     admin_id='876678896',
            ...     username="jdoe@0000004767847.zpa-customer.com",
            ...     email="jdoe@0000004767847.zpa-customer.com",
            ...     display_name="John Doe",
            ...     password="",
            ...     confirm_password="",
            ...     is_enabled=True,
            ...     role_id="12",
            ...     phone_number="+1 408-9899",
            ...     role={
            ...         "id": "12",
            ...     },
            ...     eula="0"
            ... )
            >>> if err:
            ...     print(f"Error updating administrator: {err}")
            ...     return
            ... print(f"Administrator updated successfully: {updated_admin.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /administrators/{admin_id}
        """
        )

        body = {}

        body.update(kwargs)

        # Use get instead of pop to keep microtenant_id in the body
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdministratorController)
        if error:
            return (None, response, error)

        if response is None:
            return (AdministratorController({"id": admin_id}), None, None)

        try:
            result = AdministratorController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_administrator(self, admin_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified Administrator from ZPA.

        Args:
            admin_id (str): The unique identifier for the Administrator
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            tuple: A tuple containing the response and error (if any).

        Examples:
            >>> _, _, err = client.zpa.administrator_controller.delete_administrator(
            ...     admin_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting administrator: {err}")
            ...     return
            ... print(f"administrator with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /administrators/{admin_id}
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
