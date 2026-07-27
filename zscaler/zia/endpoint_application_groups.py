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

from typing import List, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.endpoint_application_groups import EndpointApplicationGroups
from zscaler.zia.models.endpoint_applications_policies import EndpointApplicationsPolicies


class EndpointApplicationGroupsAPI(APIClient):
    """
    A Client object for the Endpoint Application Groups resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_groups(self, query_params: Optional[dict] = None) -> APIResult[List[EndpointApplicationGroups]]:
        """
        Lists the endpoint application groups configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of EndpointApplicationGroups instances, Response, error)

        Examples:
            List endpoint application groups:

            >>> group_list, _, error = client.zia.endpoint_application_groups.list_groups()
            >>> if error:
            ...     print(f"Error listing endpoint application groups: {error}")
            ...     return
            ... print(f"Total endpoint application groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplicationGroups
        """)

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
                result.append(EndpointApplicationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_group(self, **kwargs) -> APIResult[EndpointApplicationGroups]:
        """
        Creates a new endpoint application group.

        Args:
            name (str): The name of the endpoint application group.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the endpoint application group.
            mod_uid (int): The mod uid for this endpoint application group.
            end_point_applications (list): The list of end point applications for this endpoint application group.

        Returns:
            tuple: A tuple containing the newly added EndpointApplicationGroups instance, response, and error.

        Examples:
            Add a new endpoint application group:

            >>> added_group, _, error = client.zia.endpoint_application_groups.add_group(
            ...     name=f"NewGroup_{random.randint(1000, 10000)}",
            ...     description=f"NewGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding endpoint application group: {error}")
            ...     return
            ... print(f"Endpoint application group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplicationGroups
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointApplicationGroups)
        if error:
            return (None, response, error)

        try:
            result = EndpointApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: int, **kwargs) -> APIResult[EndpointApplicationGroups]:
        """
        Updates information for the specified endpoint application group.

        Args:
            group_id (int): The unique identifier for the endpoint application group.

        Keyword Args:
            name (str): The name of the endpoint application group.
            description (str): Additional information about the endpoint application group.
            mod_uid (int): The mod uid for this endpoint application group.
            end_point_applications (list): The list of end point applications for this endpoint application group.

        Returns:
            tuple: A tuple containing the updated EndpointApplicationGroups instance, response, and error.

        Examples:
            Update an existing endpoint application group:

            >>> updated_group, _, error = client.zia.endpoint_application_groups.update_group(
            ...     group_id=1013,
            ...     name=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating endpoint application group: {error}")
            ...     return
            ... print(f"Endpoint application group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplicationGroups/{group_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndpointApplicationGroups)
        if error:
            return (None, response, error)

        try:
            result = EndpointApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: int) -> APIResult[None]:
        """
        Deletes the specified endpoint application group.

        Args:
            group_id (int): The unique identifier for the endpoint application group.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a endpoint application group:

            >>> _, _, error = client.zia.endpoint_application_groups.delete_group(1013)
            >>> if error:
            ...     print(f"Error deleting endpoint application group: {error}")
            ...     return
            ... print(f"Endpoint application group deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplicationGroups/{group_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def update_application_group_resources(self, group_id: int, **kwargs) -> APIResult[dict]:
        """
        Associates endpoint applications with, or removes them from, the specified application group. Pass ``resources_to_be_added`` and/or ``resources_to_be_deleted`` lists of application resource IDs.

        Args:
            group_id (int): The unique identifier for the endpoint application group.

        Returns:
            tuple: A tuple containing (result, Response, error).

        Examples:
            >>> result, _, error = client.zia.endpoint_application_groups.update_application_group_resources(
            ...     1013,
            ... )
            >>> if error:
            ...     print(f"Error calling update_application_group_resources: {error}")
            ...     return
            ... print(f"Result: {result}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplicationGroups/{group_id}/resources
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_application_group_policies(
        self, query_params: Optional[dict] = None
    ) -> APIResult[List[EndpointApplicationsPolicies]]:
        """
        Lists the policy rules currently associated with the endpoint application group(s) identified by the given resource IDs.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.resourceId]`` {list}: One or more application group resource IDs (repeated query parameter).

        Returns:
            tuple: A tuple containing (list of EndpointApplicationsPolicies instances, Response, error)

        Examples:
            List endpoint application groups:

            >>> group_list, _, error = client.zia.endpoint_application_groups.get_application_group_policies()
            >>> if error:
            ...     print(f"Error listing endpoint application groups: {error}")
            ...     return
            ... print(f"Total endpoint application groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            List endpoint application groups using filters:

            >>> group_list, _, error = client.zia.endpoint_application_groups.get_application_group_policies(
            ...     query_params={'resourceId': 'VALUE'})
            >>> if error:
            ...     print(f"Error listing endpoint application groups: {error}")
            ...     return
            ... print(f"Total endpoint application groups found: {len(group_list)}")

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointApplicationGroups/policies
        """)

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
                result.append(EndpointApplicationsPolicies(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
