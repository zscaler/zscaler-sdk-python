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
from zscaler.zia.models.subclouds import TenantSubClouds
from zscaler.zia.models.subclouds import LastDCInCountry
from zscaler.utils import format_url


class SubCloudsAPI(APIClient):
    """
    A Client object for the Tenant Sub Clouds resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_sub_clouds(self, query_params=None) -> tuple:
        """
        Returns the list of all configured Tenant Sub Clouds.

        Keyword Args:
                ``[query_params.page]`` {int, optional}: Page offset.
                ``[query_params.page_size]`` {int, optional}: Specifies the page size. The default size is 100.
                
        Returns:
            :obj:`Tuple`: A list of Sub Clouds configured in ZIA.

        Examples:
            List Sub Clouds with default settings:

            >>> for tunnel in zia.traffic.list_gre_tunnels():
            ...    print(tunnel)

            List GRE tunnels, limiting to a maximum of 10 items:

            >>> for tunnel in zia.traffic.list_gre_tunnels(max_items=10):
            ...    print(tunnel)

            List GRE tunnels, returning 200 items per page for a maximum of 2 pages:

            >>> for tunnel in zia.traffic.list_gre_tunnels(page_size=200, max_pages=2):
            ...    print(tunnel)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /subclouds
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TenantSubClouds(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sub_clouds(self, cloud_id: int, **kwargs) -> tuple:
        """
        Updates information for the subcloud and excluded data centers based on the specified ID.

        Args:
            cloud_id (int): The unique ID for the Sub Clouds.

        Returns:
            tuple: A tuple containing the updated Sub Clouds, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /subclouds/{cloud_id}
        """)
        body = {}

        body.update(kwargs)

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        # Parse the response into a RuleLabels instance
        try:
            result = TenantSubClouds(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_sub_cloud_last_dc_in_country(
        self,
        cloud_id: int,
        query_params=None
    ) -> tuple:
        """
        Returns information for the list of all the excluded data centers in a country.

        Args:
            cloud_id (str): Unique identifier for the country
            dc_id (str): Unique identifier for the country

        Returns:
            :obj:`tuple`: The GRE tunnel resource record.

        Examples:
            >>> gre_tunnel = zia.traffic.get_gre_tunnel('967134')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /subclouds/isLastDcInCountry/{cloud_id}
        """
        )

        query_params = query_params or {}
        
        body = {}
        headers = {}

        request, error = self._request_executor.\
            create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request, LastDCInCountry)

        if error:
            return (None, response, error)

        try:
            result = LastDCInCountry(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)