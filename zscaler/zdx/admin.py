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
from zscaler.zdx.models.administration import Administration
from zscaler.utils import format_url, zdx_params


class AdminAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    @zdx_params
    def list_departments(self, query_params=None) -> tuple:
        """
        Returns the list of Admin Users enrolled in the Client Connector Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.
                    If not entered, returns the data for the last 2 hours.

                ``[query_params.search]`` {str}: The search string used to support search by name or department ID.

        Returns:
            :obj:`tuple`: A tuple containing configured departments.

        Examples:
            Prints all configured departments.

            >>> dept_list, _, err = client.zdx.admin.list_departments(ss)
            ... if err:
            ...     print(f"Error listing department: {err}")
            ...     return
            ... print(f"Total department found: {len(dept_list)}")
            ...  for dept in dept_list:
            ...     print(dept.as_dict())

            Search specific configured department.

            >>> dept_list, _, err = client.zdx.admin.list_departments(query_params={"search": 'Finance'})
            ... if err:
            ...     print(f"Error listing department: {err}")
            ...     return
            ... print(f"Total department found: {len(dept_list)}")
            ...  for dept in dept_list:
            ...     print(dept.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /administration/departments
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
                result.append(Administration(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zdx_params
    def list_locations(self, query_params=None) -> tuple:
        """
        Returns the list of all configured Zscaler locations if the search filters are not specified.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.
                    If not entered, returns the data for the last 2 hours.

                ``[query_params.search]`` {str}: The search string used to support search by name or location ID.

        Returns:
            :obj:`tuple`: A tuple containing configured locations.

        Examples:
            Prints all configured Zscaler locations.

            >>> locations_list, _, err = client.zdx.admin.list_locations()
            ... if err:
            ...     print(f"Error listing department: {err}")
            ...     return
            ... print(f"Total location found: {len(locations_list)}")
            ...  for location in locations_list:
            ...     print(location.as_dict())

            Search specific configured Zscaler locations.

            >>> locations_list, _, err = client.zdx.admin.list_locations(query_params={"search": 'San Jose'})
            ... if err:
            ...     print(f"Error listing department: {err}")
            ...     return
            ... print(f"Total location found: {len(locations_list)}")
            ...  for location in locations_list:
            ...     print(location.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /administration/locations
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
                result.append(Administration(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
