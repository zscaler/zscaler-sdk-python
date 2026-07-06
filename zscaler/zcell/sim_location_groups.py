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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zcell.models.sim_location_groups import (
    GetSimLocationGroup,
    ResponseMessage,
    SimLocationGroups,
    UpdateSimLocationGroup,
)


class SimLocationGroupsAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor", config: dict = None) -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcell_customer_id = (config or {}).get("client", {}).get("zcellCustomerId")

    def list_sim_location_groups(self, id: str = None, query_params=None) -> APIResult[List[SimLocationGroups]]:
        """
        Get all Sim Location Groups for a customer.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.name]`` {str}
                ``[query_params.page]`` {int}: Page number (0-based)
                ``[query_params.size]`` {int}: Page size (1-100)
                ``[query_params.sort_by]`` {str}: Field to sort by. Default: name. Sortable fields: id, name
                ``[query_params.sort_dir]`` {str}: ASC or DESC. Default: ASC

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_location_groups.list_sim_location_groups(id='...')
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "get".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim-location-groups")

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
                result.append(SimLocationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_sim_location_group(self, id: str = None, group_id: str = None) -> APIResult[GetSimLocationGroup]:
        """
        Get a Sim Location Group by ID.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            group_id (str): Path parameter.
        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_location_groups.get_sim_location_groups(
            ...     id='...',
            ...     group_id='...',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "get".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim-location-groups/{group_id}")
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, GetSimLocationGroup)
        if error:
            return (None, response, error)
        try:
            result = GetSimLocationGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_location_group(self, id: str = None, query_params=None, **kwargs) -> APIResult[List[ResponseMessage]]:
        """
        Creates new Sim Location Groups (bulk create).

        This endpoint accepts a JSON array of group objects. The fields passed via
        ``**kwargs`` describe a single group and are wrapped into a one-element list.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            **kwargs: Request body fields for a single group (e.g. name, geo_fence_details).
            query_params (dict): Map of query parameters for the request.

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            >>> results, response, error = client.zcell.sim_location_groups.add_location_group(
            ...     id='...',
            ...     name='NewLocationGroup',
            ...     geo_fence_details={'lat': '37.3382082', 'lng': '-121.8863286', 'radius': '1'},
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> for item in results:
            ...     print(item.as_dict())
        """
        http_method = "post".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim-location-groups")

        query_params = query_params or {}

        # Bulk-create endpoint: the body is a JSON array of group objects. The model
        # builds one array item and emits the camelCase wire shape via request_format().
        body = [SimLocationGroups(kwargs).request_format()]
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
                result.append(ResponseMessage(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sim_location_group(self, id: str = None, group_id: str = None, **kwargs) -> APIResult[UpdateSimLocationGroup]:
        """
        Updates an existing Sim Location Group.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            group_id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            >>> result, response, error = client.zcell.sim_location_groups.update_sim_location_groups(
            ...     id='...',
            ...     group_id='...',
            ...     name='example',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
            ...     return
            >>> print(result.as_dict())
        """
        http_method = "put".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim-location-groups/{group_id}")

        # The model maps the user-facing fields to the wire shape (geoFenceData) via
        # request_format(), so the geo-fence isn't sent under the wrong key.
        body = UpdateSimLocationGroup(kwargs).request_format()

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, UpdateSimLocationGroup)
        if error:
            return (None, response, error)
        try:
            result = UpdateSimLocationGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_sim_location_group(self, id: str = None, group_id: str = None) -> APIResult[None]:
        """
        Deletes an existing Sim Location Group.

        Args:
            id (str): Optional. The ZCell customer ID. Defaults to the ``zcellCustomerId`` config value
                or the ``ZCELL_CUSTOMER_ID`` environment variable when omitted.
            group_id (str): Path parameter.
        Returns:
            tuple: (None, Response, error)

        Examples:
            >>> _, response, error = client.zcell.sim_location_groups.delete_sim_location_groups(
            ...     id='...',
            ...     group_id='...',
            ... )
            >>> if error:
            ...     print(f"Error: {error}")
        """
        http_method = "delete".upper()
        id = id or self._zcell_customer_id
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/sim-location-groups/{group_id}")

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
