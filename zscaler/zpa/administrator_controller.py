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

    def list_administrators(self, query_params: Optional[dict] = None) -> List[AdministratorController]:
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
            :obj:`Tuple`: A tuple containing List[AdministratorController]

        Examples:
            >>> try:
            ...     admin_list = client.zpa.administrator_controller.list_administrators()
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request)
        result = []
        for item in response.get_results():
            result.append(AdministratorController(self.form_response_body(item)))
        return result

    def get_administrator(self, admin_id: str, query_params: Optional[dict] = None) -> AdministratorController:
        """
        Fetches a specific administrator details by ID.

        Args:
            admin_id (str): The unique identifier for the administrator.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing AdministratorController.

        Examples:
            >>> try:
            ...     fetched_admin = client.zpa.administrator_controller.get_administrator('999999')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, AdministratorController)
        result = AdministratorController(self.form_response_body(response.get_body()))
        return result

    def add_administrator(self, **kwargs) -> AdministratorController:
        """
        Adds a new ZPA admministrator.

        Args:
            name (str): The name of the Administrator.

        Keyword Args:

        Returns:
            :obj:`Tuple`: A tuple containing AdministratorController

        Examples:
            Adding a new local administrator account

            >>> try:
            ...     added_admin = client.zpa.administrator_controller.add_administrator(
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

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, AdministratorController)
        result = AdministratorController(self.form_response_body(response.get_body()))
        return result

    def update_administrator(self, admin_id: str, **kwargs) -> AdministratorController:
        """
        Updates an existing ZPA c.

        Args:
            admin_id (str): The unique id for the Administrator in ZPA.

        Keyword Args:

        Returns:

        Examples:
            Updating a new local administrator account

            >>> try:
            ...     updated_admin = client.zpa.administrator_controller.add_administrator(
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

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, AdministratorController)
        if response is None:
            return AdministratorController({"id": admin_id})

        result = AdministratorController(self.form_response_body(response.get_body()))
        return result

    def delete_administrator(self, admin_id: str, microtenant_id: str = None) -> None:
        """
        Deletes the specified Administrator from ZPA.

        Args:
            admin_id (str): The unique identifier for the Administrator
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:

        Examples:
            >>> try:
            ...     _ = client.zpa.administrator_controller.delete_administrator(
            ...     admin_id='999999'
            ... )
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
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

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
