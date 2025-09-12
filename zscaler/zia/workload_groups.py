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
from zscaler.zia.models.workload_groups import WorkloadGroups
from zscaler.utils import format_url


class WorkloadGroupsAPI(APIClient):
    """
    A Client object for the Workload Groups API resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns the list of workload groups configured in the ZIA Admin Portal.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 250, but the maximum size is 1000.

        Returns:
            tuple: A tuple containing (list of WorkloadGroups instances, Response, error)


        Examples:
            List users using default settings:

            >>> group_list, _, err = client.zia.workload_groups.list_groups()
            ... if err:
            ...     print(f"Error listing groups: {err}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}/workloadGroups
        """
        )

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
                result.append(WorkloadGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group(self, group_id: int) -> tuple:
        """
        Fetches a specific workload group by ID.

        Args:
            group_id (int): The unique identifier for the workload group.

        Returns:
            tuple: A tuple containing (WorkloadGroup instance, Response, error).

        Examples:
            Print a specific Workload Group

            >>> fetched_group, _, error = client.zia.workload_groups.get_group(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Workload Group by ID: {error}")
            ...     return
            ... print(f"Fetched Workload Group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /workloadGroups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WorkloadGroups)
        if error:
            return (None, response, error)

        try:
            result = WorkloadGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_group(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Workload Group.

        Args:
            name (str): The name of the workload group.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional notes or information about the workload group.
            expression (str): The expression string for the workload group.
            expression_json (dict): JSON object containing the expression configuration with the following structure:

                - expression_containers (list): List of expression containers, each containing:

                    - tag_type (str): Type of tag (e.g., "ATTR", "ENI", "VPC", "VM").
                    - operator (str): Logical operator for the expression (e.g., "AND", "OR").
                    - tag_container (dict): Container for tags with:

                        - tags (list): List of tag objects, each containing:

                            - key (str): The tag key identifier.
                            - value (str): The tag value.
                        - operator (str): Logical operator for tags within the container.

        Returns:
            tuple: A tuple containing the newly added Workload Group, response, and error.

        Examples:
            Add a new Workload Group with basic information:

            >>> added_group, _, error = client.zia.workload_groups.add_group(
            ...     name="Test Group",
            ...     description="Test Group Description"
            ... )
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")

            Add a new Workload Group with complex expression configuration:

            >>> added_group, _, error = client.zia.workload_groups.add_group(
            ...     name="Test Group",
            ...     description="Test Group",
            ...     expression_json={
            ...         "expression_containers": [
            ...             {
            ...                 "tag_type": "ATTR",
            ...                 "operator": "AND",
            ...                 "tag_container": {
            ...                     "tags": [
            ...                         {
            ...                             "key": "GroupName",
            ...                             "value": "example"
            ...                         }
            ...                     ],
            ...                     "operator": "AND"
            ...                 }
            ...             },
            ...             {
            ...                 "tag_type": "VPC",
            ...                 "operator": "AND",
            ...                 "tag_container": {
            ...                     "tags": [
            ...                         {
            ...                             "key": "Vpc-id",
            ...                             "value": "vpcid12344"
            ...                         }
            ...                     ],
            ...                     "operator": "AND"
            ...                 }
            ...             }
            ...         ]
            ...     }
            ... )
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /workloadGroups
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

        response, error = self._request_executor.execute(request, WorkloadGroups)
        if error:
            return (None, response, error)

        try:
            result = WorkloadGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Workload Group.

        Args:
            group_id (int): The unique ID for the Workload Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the workload group.
            description (str): Additional notes or information about the workload group.
            expression (str): The expression string for the workload group.
            expression_json (dict): JSON object containing the expression configuration with the following structure:

                - expression_containers (list): List of expression containers, each containing:

                    - tag_type (str): Type of tag (e.g., "ATTR", "ENI", "VPC", "VM").
                    - operator (str): Logical operator for the expression (e.g., "AND", "OR").
                    - tag_container (dict): Container for tags with:

                        - tags (list): List of tag objects, each containing:

                            - key (str): The tag key identifier.
                            - value (str): The tag value.
                        - operator (str): Logical operator for tags within the container.

        Returns:
            tuple: A tuple containing the updated Workload Group, response, and error.

        Examples:
            Update an existing Workload Group with basic information:

            >>> updated_group, _, error = client.zia.workload_groups.update_group(
            ...     group_id=1524566,
            ...     name="Updated Test Group",
            ...     description="Updated Test Group Description"
            ... )
            >>> if error:
            ...     print(f"Error updating Workload Group: {error}")
            ...     return
            ... print(f"Workload Group updated successfully: {updated_group.as_dict()}")

            Update an existing Workload Group with complex expression configuration:

            >>> updated_group, _, error = client.zia.workload_groups.update_group(
            ...     group_id=1524566,
            ...     name="Updated Test Group",
            ...     description="Updated Test Group",
            ...     expression_json={
            ...         "expression_containers": [
            ...             {
            ...                 "tag_type": "ATTR",
            ...                 "operator": "AND",
            ...                 "tag_container": {
            ...                     "tags": [
            ...                         {
            ...                             "key": "GroupName",
            ...                             "value": "updated_example"
            ...                         }
            ...                     ],
            ...                     "operator": "AND"
            ...                 }
            ...             },
            ...             {
            ...                 "tag_type": "ENI",
            ...                 "operator": "AND",
            ...                 "tag_container": {
            ...                     "tags": [
            ...                         {
            ...                             "key": "GroupId",
            ...                             "value": "987654321"
            ...                         }
            ...                     ],
            ...                     "operator": "AND"
            ...                 }
            ...             }
            ...         ]
            ...     }
            ... )
            >>> if error:
            ...     print(f"Error updating Workload Group: {error}")
            ...     return
            ... print(f"Workload Group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /workloadGroups/{group_id}
        """
        )
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, WorkloadGroups)
        if error:
            return (None, response, error)

        try:
            result = WorkloadGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: int) -> tuple:
        """
        Deletes the specified Workload Group.

        Args:
            group_id (str): The unique identifier of the Workload Group.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Workload Group:

            >>> _, _, error = client.zia.workload_groups.delete_group('73459')
            >>> if error:
            ...     print(f"Error deleting Workload Group: {error}")
            ...     return
            ... print(f"Workload Group with ID {'73459'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /workloadGroups/{group_id}
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
