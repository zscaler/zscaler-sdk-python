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
from zscaler.zpa.models.private_cloud_controller import PrivateCloudController
from zscaler.utils import format_url


class PrivateCloudControllerAPI(APIClient):
    """
    A Client object for the Private Cloud Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_cloud_controllers(self, query_params=None) -> tuple:
        """
        Enumerates Private Cloud Controller in your organization with pagination.
        A subset of Private Cloud Controller can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.sort_by]`` {str}: Indicates the parameter to sort by.

                ``[query_params.sort_dir]`` {(str, optional): Sort results by ascending (`asc`) or descending (`dsc`) order.
                    Default: `dsc`.

                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of Private Cloud Controller instances, Response, error)

        Examples:
            >>> controller_list, _, err = client.zpa.private_cloud_controller.list_cloud_controllers(
            ... query_params={'search': 'PCController01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing Private Cloud Controller: {err}")
            ...     return
            ... print(f"Total Private Cloud Controller found: {len(controller_list)}")
            ... for controller in controller_list:
            ...     print(controller.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /privateCloudController
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloudController)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivateCloudController(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cloud_controller(self, controller_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified Private Cloud Controller.

        Args:
            controller_id (str): The unique id for the ZPA Private Cloud Controller.

        Returns:
            :obj:`Tuple`: The specified Private Cloud Controller resource record.

        Examples:
            >>> fetched_controller, _, err = client.zpa.private_cloud_controller.get_cloud_controller('999999')
            ... if err:
            ...     print(f"Error fetching controller by ID: {err}")
            ...     return
            ... print(f"Fetched controller by ID: {fetched_controller.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /privateCloudController/{controller_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloudController)
        if error:
            return (None, response, error)

        try:
            result = PrivateCloudController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_cloud_controller(self, controller_id: str, **kwargs) -> tuple:
        """
        Updates an existing ZPA Private Cloud Controller.

        Args:
            controller_id (str): The unique id of the ZPA Private Cloud Controller.

        Keyword Args:
            **name (str): The name of the Private Cloud Controller.
            **description (str): Additional information about the Private Cloud Controller.
            **enabled (bool): True if the Private Cloud Controller is enabled.

        Returns:
            :obj:`Tuple`: The updated Private Cloud Controller resource record.

        Examples:
            Update an Private Cloud Controller name, description and disable it.

            >>> update_controller, _, err = client.zpa.private_cloud_controller.update_cloud_controller(
            ...     controller_id='99999'
            ...     name=f"UpdatePrivateController_{random.randint(1000, 10000)}",
            ...     description=f"UpdatePrivateController_{random.randint(1000, 10000)}",
            ...     enabled=False,
            ... )
            ... if err:
            ...     print(f"Error creating private controller: {err}")
            ...     return
            ... print(f"private controller created successfully: {update_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /privateCloudController/{controller_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivateCloudController)
        if error:
            return (None, response, error)

        if response is None:
            return (PrivateCloudController({"id": controller_id}), None, None)

        try:
            result = PrivateCloudController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_cloud_controller(self, controller_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified Private Cloud Controller from ZPA.

        Args:
            controller_id (str): The unique id for the ZPA Private Cloud Controller that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, err = client.zpa.private_cloud_controller.delete_cloud_controller(
            ...     controller_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting Private Cloud Controller: {err}")
            ...     return
            ... print(f"Private Cloud Controller with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /privateCloudController/{controller_id}
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

    def restart_private_controller(
        self,
        controller_id: str,
        microtenant_id: str = None
    ) -> tuple:
        """
        Triggers restart of the Private Cloud Controller

        Args:
            controller_id (str): The unique id for the ZPA Private Cloud Controller that will be restarted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, err = client.zpa.private_cloud_controller.restart_private_controller(
            ...     controller_id='999999'
            ... )
            ... if err:
            ...     print(f"Error restarting Private Cloud Controller: {err}")
            ...     return
            ... print(f"Private Cloud Controller with ID {'999999'} restarted successfully.")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /privateCloudController/{controller_id}/restart
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
