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
from zscaler.zpa.models.cloud_connector_groups import CloudConnectorGroup
from zscaler.utils import format_url


class CloudConnectorGroupsAPI(APIClient):
    """
    A Client object for the Cloud Connector Groups resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_cloud_connector_groups(self, query_params=None) -> tuple:
        """
        Returns a list of all configured cloud connector groups.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            list: A list of `CloudConnectorGroup` instances.

        Examples:
            >>> group_list, _, err = client.zpa.cloud_connector_groups.list_cloud_connector_groups(
            ... query_params={'search': 'CloudConnectorGroup01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing connector groups: {err}")
            ...     return
            ... print(f"Total connector groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /cloudConnectorGroup
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CloudConnectorGroup)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CloudConnectorGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cloud_connector_groups(
        self,
        group_id: str,
    ) -> tuple:
        """
        Returns information on the specified cloud connector group.

        Args:
            group_id (str): The unique identifier for the cloud connector group.
            query_params (dict): Optional query parameters.

        Returns:
            dict: The cloud connector group object.

        Examples:
            >>> fetched_group, _, err = client.zpa.cloud_connector_groups.get_cloud_connector_groups('999999')
            ... if err:
            ...     print(f"Error fetching group by ID: {err}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /cloudConnectorGroup/{group_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CloudConnectorGroup)
        if error:
            return (None, response, error)

        try:
            result = CloudConnectorGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
