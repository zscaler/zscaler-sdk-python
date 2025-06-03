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
from zscaler.zia.models.traffic_extranet import TrafficExtranet
from zscaler.utils import format_url


class TrafficExtranetAPI(APIClient):
    """
    A Client object for the Extranet resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_extranets(self, query_params=None) -> tuple:
        """
        Lists extranet in your organization with pagination.
        A subset of extranet  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.order_by]`` {str}: The field used to sort the list in a specific order
                ``[query_params.order]`` {str}: The arrangement of the list in ascending or descending order i.e ASC

        Returns:
            tuple: A tuple containing (list of Extranet instances, Response, error)

        Examples:
            List  all extranets:

            >>> extranet_list, _, error = client.zia.traffic_extranet.list_extranets()
            >>> if error:
            ...     print(f"Error listing extranets: {error}")
            ...     return
            ... print(f"Total extranets found: {len(extranet_list)}")
            ... for extranet in extranet_list:
            ...     print(extranet.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /extranet
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
                result.append(TrafficExtranet(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_extranet(self, extranet_id: int) -> tuple:
        """
        Fetches a specific extranet by ID.

        Args:
            extranet_id (int): The unique identifier for the extranet.

        Returns:
            tuple: A tuple containing (Extranet instance, Response, error).

        Examples:
            Retrieve a specific extranet:

            >>> fetched_extranet, _, error = client.zia.traffic_extranet.get_extranet('125245')
            >>> if error:
            ...     print(f"Error fetching Extranet by ID: {error}")
            ...     return
            ... print(f"Fetched Extranet by ID: {fetched_extranet.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /extranet/{extranet_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficExtranet)
        if error:
            return (None, response, error)

        try:
            result = TrafficExtranet(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_extranet(self, **kwargs) -> tuple:
        """
        Adds a new extranet for the organization.

        Args:
            name (str): The name of the extranet
            description (str): The description of the extranet
            description (str): The description of the extranet

        Returns:
            tuple: A tuple containing the newly added Extranet, response, and error.

        Examples:
            Add a new Extranet

            >>> added_extranet, _, error = client.zia.traffic_extranet.add_extranet(
            ...     name=f"NewExtranet {random.randint(1000, 10000)}",
            ...     description=f"NewExtranet {random.randint(1000, 10000)}",
            ...     extranet_dns_list=[
            ...         {
            ...             "name": f"NewExtranet {random.randint(1000, 10000)}",
            ...             "primary_dns_server": "8.8.8.8",
            ...             "secondary_dns_server": "4.4.2.2",
            ...             "use_as_default": True,
            ...         }
            ...     ],
            ...     extranet_ip_pool_list=[
            ...         {
            ...             "name": f"NewExtranet {random.randint(1000, 10000)}",
            ...             "ip_start": "192.168.200.1",
            ...             "ip_end": "192.168.200.21",
            ...             "use_as_default": True,
            ...         }
            ...     ]
            ... )
            >>> if error:
            ...     print(f"Error adding extranet: {error}")
            ...     return
            ... print(f"Extranet added successfully: {added_extranet.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /extranet
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficExtranet)
        if error:
            return (None, response, error)

        try:
            result = TrafficExtranet(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    # Needs to file a bug as method is returning 405 Error
    def update_extranet(self, extranet_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Extranet.

        Args:
            extranet_id (int): The unique ID for the Extranet.

        Returns:
            tuple: A tuple containing the updated Extranet, response, and error.

        Examples:
            Updated a Extranet

            >>> updated_extranet, _, error = client.zia.traffic_extranet.add_extranet(
            ...     extranet_id='125245'
            ...     name=f"UpdateExtranet_{random.randint(1000, 10000)}",
            ...     description=f"UpdateExtranet_{random.randint(1000, 10000)}",
            ...     extranet_dns_list=[
            ...         {
            ...             "name": f"UpdateExtranet_{random.randint(1000, 10000)}",
            ...             "primary_dns_server": "8.8.8.8",
            ...             "secondary_dns_server": "4.4.2.2",
            ...             "use_as_default": True,
            ...         }
            ...     ],
            ...     extranet_ip_pool_list=[
            ...         {
            ...             "name": f"UpdateExtranet_{random.randint(1000, 10000)}",
            ...             "ip_start": "192.168.200.1",
            ...             "ip_end": "192.168.200.21",
            ...             "use_as_default": True,
            ...         }
            ...     ]
            ... )
            >>> if error:
            ...     print(f"Error updating extranet: {error}")
            ...     return
            ... print(f"Extranet updated successfully: {updated_extranet.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /extranet/{extranet_id}
        """
        )

        body = kwargs
        body["id"] = extranet_id

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TrafficExtranet)
        if error:
            return (None, response, error)

        try:
            result = TrafficExtranet(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_extranet(self, extranet_id: int) -> tuple:
        """
        Deletes the specified Extranet.

        Args:
            extranet_id (str): The unique identifier of the Extranet.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Extranet:

            >>> _, _, error = client.zia.traffic_extranet.delete_extranet('73459')
            >>> if error:
            ...     print(f"Error deleting Extranet: {error}")
            ...     return
            ... print(f"Extranet with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /extranet/{extranet_id}
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
