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
from zscaler.zia.models.cloud_to_cloud_ir import CloudToCloudIR
from zscaler.utils import format_url


class CloudToCloudIRAPI(APIClient):
    """
    A Client object for the Cloud-to-Cloud Incident Forwarding resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_cloud_to_cloud_ir(self, query_params=None) -> tuple:
        """
        Retrieves the list of DLP Incident Receivers configured for Cloud-to-Cloud Incident Forwarding.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.page]`` (int): Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size.
                    The default size is 50.

                ``[query_params.search]`` (str): The search string used to match against the names of Cloud-to-Cloud Incident
                    Forwarding tenants and their configurations

        Returns:
            tuple: A tuple containing (Retries the Cloud-to-Cloud Incident Forwarding instances, Response, error)

        Examples:
            List the Cloud-to-Cloud Incident Forwarding:

            >>> c2c_list, response, error = client.zia.cloud_to_cloud_ir.list_cloud_to_cloud_ir()
            ... if error:
            ...    print(f"Error listing c2c incident receiver: {error}")
            ...    return
            ... print(f"Total c2c incident receiver found: {len(c2c_list)}")
            ... for c2c in c2c_list:
            ...    print(c2c.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudToCloudIR
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CloudToCloudIR(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cloud_to_cloud_ir(self, receiver_id: int) -> tuple:
        """
        Retrieves information about a DLP Incident Receiver configured for
        Cloud-to-Cloud DLP Incident Forwarding based on the specified ID

        Args:
            receiver_id (str): System-generated unique ID of the Cloud-to-Cloud Incident Receiver.

        Returns:
            :obj:`Tuple`: The ZIA DLP Incident Receiver resource record.

        Examples:
            >>> fetched_receiver, _, error = client.zia.cloud_to_cloud_ir.get_cloud_to_cloud_ir('5865456')
            >>> if error:
            ...     print(f"Error fetching c2c receiver by ID: {error}")
            ...     return
            ... print(f"Fetched c2c receiver by ID: {fetched_receiver.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudToCloudIR/{receiver_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = CloudToCloudIR(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_cloud_to_cloud_ir_lite(self, query_params=None) -> tuple:
        """
        Retrieves the list of DLP Incident Receivers configured for Cloud-to-Cloud DLP Incident Forwarding,
        with a subset of information for each Incident Receiver

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.page]`` (int): Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size.
                    The default size is 50.

                ``[query_params.search]`` (str): The search string used to match against the names of Cloud-to-Cloud Incident
                    Forwarding tenants and their configurations

        Returns:
            :obj:`Tuple`: The ZIA DLP Incident Receiver resource record.

        Examples:
            List the Cloud-to-Cloud Incident Forwarding:

            >>> c2c_list, response, error = client.zia.cloud_to_cloud_ir.list_cloud_to_cloud_ir_lite()
            ... if error:
            ...    print(f"Error listing c2c incident receiver: {error}")
            ...    return
            ... print(f"Total c2c incident receiver found: {len(c2c_list)}")
            ... for c2c in c2c_list:
            ...    print(c2c.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudToCloudIR/lite
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CloudToCloudIR(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_c2c_count(self, query_params=None) -> tuple:
        """
        Retrieves the number of DLP Incident Receivers configured for Cloud-to-Cloud Incident Forwarding

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: The search string used to match against the names of

                    Cloud-to-Cloud Incident Forwarding tenants and their configurations

        Returns:
            :obj:`Tuple`: A list of c2c receiver resource records.

        Examples:
            Gets the list of c2c receiver for your organization:

            >>> count, _, error = client.zia.cloud_to_cloud_ir.list_c2c_count()
            >>> if error:
            ...     print(f"Error fetching c2c receivers count: {error}")
            ...     return
            ... print(f"Total c2c receivers found: {count}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudToCloudIR/count
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            body = response.get_body()
            if isinstance(body, int):
                return (body, response, None)
            elif isinstance(body, str) and body.strip().isdigit():
                return (int(body.strip()), response, None)
            else:
                raise ValueError(f"Unexpected response format: {body}")
        except Exception as error:
            return (None, response, error)

    def c2c_validate_delete(self, receiver_id: int) -> tuple:
        """
        Validates the specified cloud storage configuration e.g. Amazon S3 bucket configuration
        of a Cloud-to-Cloud DLP Incident Receiver by verifying he configuration's current association
        status with policy rules.
        Configurations cannot be deleted while being associated with policy rules.

        Args:
            receiver_id (int):
                System-generated unique ID of a Cloud-to-Cloud Incident Receiver's storage

        Returns:
            :obj:`int`: Response code for the operation.

        Examples:
            >>> _, _, err = client.zia.cloud_to_cloud_ir.c2c_validate_delete('123454')
            >>> if err:
            ...     print(f"Error validating c2c deletion: {err}")
            ...     return
            ... print(f"C2C Deletion with ID {'123454'} validated successfully.")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cloudToCloudIR/config/{receiver_id}/validateDelete
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
