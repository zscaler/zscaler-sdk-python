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
from zscaler.zpa.models.microtenants import Microtenant
from zscaler.zpa.models.microtenants import MicrotenantSearch
from zscaler.utils import format_url


class MicrotenantsAPI(APIClient):
    """
    A client object for the Microtenants resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_microtenants(self, query_params=None) -> tuple:
        """
        Enumerates microtenants in your organization with pagination.
        A subset of microtenants can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.include_roles]`` {bool}: Include roles information in the API response. Default value: False

        Returns:
            :obj:`Tuple`: A tuple containing (list of Microtenants instances, Response, error)

            >>> microtenant_list, _, err = client.zpa.microtenants.list_microtenants(
            ... query_params={'search': 'Microtenant_A', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing microtenants: {err}")
            ...     return
            ... print(f"Total certificates found: {len(microtenant_list)}")
            ... for tenant in microtenant_list:
            ...     print(tenant.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /microtenants
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Microtenant)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(Microtenant(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_microtenant(
        self,
        microtenant_id: str,
    ) -> tuple:
        """
        Returns information on the specified microtenant.

        Args:
            microtenant_id (str): The unique identifier for the microtenant.

        Returns:
            :obj:`Tuple`: Microtenant: The resource record for the microtenant.

        Examples:
            >>> fetched_microtenant, _, err = client.zpa.microtenants.get_microtenant('999999')
            ... if err:
            ...     print(f"Error fetching microtenant by ID: {err}")
            ...     return
            ... print(fetched_microtenant.id)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /microtenants/{microtenant_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Microtenant)
        if error:
            return (None, response, error)

        try:
            result = Microtenant(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_microtenant_summary(self) -> tuple:
        """
        Returns the name and ID of the configured Microtenant.

        Returns:
            :obj:`Tuple`: Microtenant: The resource record for the microtenant.

        Examples:
            >>> microtenants_list, err = client.zpa.microtenants.get_microtenant_summary()
            ... if err:
            ...     print(f"Error listing microtenants: {err}")
            ...     return
            ... print(f"Total microtenants found: {len(microtenants_list)}")
            ... for microtenant in microtenants_list:
            ...     print(microtenant.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /microtenants/summary
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, error)

        microtenant_list = []
        response_body = response.get_body()

        if isinstance(response_body, list):
            for item in response_body:
                microtenant_list.append(Microtenant(item))

        return (microtenant_list, None)

    def get_microtenant_search(self, **kwargs) -> tuple:
        """
        Gets all configured Microtenants for the specified customer based on given filters.

        Args:
            **kwargs: Keyword arguments that define search filters, pagination, and sorting criteria.

        Keyword Args:
            filter_and_sort_dto (dict): A dictionary containing filtering, pagination, and sorting information.

                - **filter_by** (list): A list of filter condition dictionaries.

                    - **filter_name** (str): The name of the field to filter on (e.g., `name`, `criteria_attribute_values`).
                    - **operator** (str): The logical operator (e.g., `EQUALS`, `LIKE`).
                    - **values** (list): A list of values to match.
                    - **comma_sep_values** (str, optional): Optional comma-separated string version of values.

                - **page_by** (dict, optional): Dictionary containing pagination configuration.

                    - **page** (int): The current page number.
                    - **page_size** (int): The number of records per page.
                    - **valid_page** (int, optional): Optional page validation flag.
                    - **valid_page_size** (int, optional): Optional page size validation flag.

                - **sort_by** (dict, optional): Dictionary defining sorting options.

                    - **sort_name** (str): The name of the field to sort by (e.g., `name`).
                    - **sort_order** (str): Sorting direction (e.g., `ASC` or `DESC`).

        Returns:
            tuple: A tuple containing:

                - **MicrotenantSearch**: The parsed response object containing filter results, paging, and sorting.
                - **Response**: The raw response object returned by the request executor.
                - **Error**: An exception if one occurred, otherwise `None`.

        Example:
            >>> search_payload = {
            ...     "filter_and_sort_dto": {
            ...         "filter_by": [
            ...             {
            ...                 "filter_name": "criteria_attribute_values",
            ...                 "operator": "LIKE",
            ...                 "values": ["Test"]
            ...             }
            ...         ],
            ...         "page_by": {
            ...             "page": 1,
            ...             "page_size": 20
            ...         },
            ...         "sort_by": {
            ...             "sort_name": "name",
            ...             "sort_order": "ASC"
            ...         }
            ...     }
            ... }
            >>> result, _, err = client.zpa.microtenants.get_microtenant_search(**search_payload)
            >>> if err:
            ...     print(f"Error searching microtenants: {err}")
            ... else:
            ...     for item in result.filter_by:
            ...         print(item.request_format())
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /microtenants/search
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, MicrotenantSearch)
        if error:
            return (None, response, error)

        try:
            result = MicrotenantSearch(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_microtenant(self, **kwargs) -> tuple:
        """
        Add a new microtenant.

        Args:
            name (str): The name of the microtenant.
            criteria_attribute (str): The criteria attribute for the microtenant.
            criteria_attribute_values (list): The values for the criteria attribute.

        Keyword Args:
            description (str): A description for the microtenant.
            enabled (bool): Whether the microtenant is enabled. Defaults to True.
            privileged_approvals_enabled (bool): Whether privileged approvals are enabled. Defaults to True.

        Returns:
            Microtenant: The resource record for the newly created microtenant.

        Examples:
            >>> microtenant = zpa.microtenants.add_microtenant(
                    name="Microtenant_A",
                    criteria_attribute="AuthDomain",
                    criteria_attribute_values=["acme.com"]
                )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /microtenants
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Microtenant)
        if error:
            return (None, response, error)

        try:
            result = Microtenant(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_microtenant(self, microtenant_id: str, **kwargs) -> tuple:
        """
        Updates the specified microtenant.

        Args:
            microtenant_id (str): The unique identifier for the microtenant being updated.

        Keyword Args:
            name (str): The name of the microtenant.
            description (str): A description for the microtenant.
            enabled (bool): Whether the microtenant is enabled. Defaults to True.
            privileged_approvals_enabled (bool): Whether privileged approvals are enabled. Defaults to True.
            criteria_attribute (str): The criteria attribute for the microtenant.
            criteria_attribute_values (list): The values for the criteria attribute.

        Returns:
            Microtenant: The updated resource record for the microtenant.

        Examples:
            >>> updated_microtenant = zpa.microtenants.update_microtenant(
                    microtenant_id="216199618143368569",
                    name="Microtenant_A",
                    enabled=False
                )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /microtenants/{microtenant_id}
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
        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, Microtenant)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (Microtenant({"id": microtenant_id}), None, None)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = Microtenant(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_microtenant(self, microtenant_id: str) -> int:
        """
        Deletes the specified microtenant.

        Args:
            microtenant_id (str): The unique identifier for the microtenant to be deleted.

        Returns:
            int: Status code of the delete operation.

        Examples:
            >>> zpa.microtenants.delete_microtenant('99999')
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /microtenants/{microtenant_id}
        """
        )

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
