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
from zscaler.zia.models.dns_application_groups import DnsApplicationGroups


class DNSApplicationGroupsAPI(APIClient):
    """
    A Client object for the DNS Application Groups resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_groups(self, query_params: Optional[dict] = None) -> APIResult[List[DnsApplicationGroups]]:
        """
        Lists the DNS application groups configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of DnsApplicationGroups instances, Response, error)

        Examples:
            List DNS application groups:

            >>> group_list, _, error = client.zia.dns_application_groups.list_groups()
            >>> if error:
            ...     print(f"Error listing DNS application groups: {error}")
            ...     return
            ... print(f"Total DNS application groups found: {len(group_list)}")
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
            /dnsApplicationGroups
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
                result.append(DnsApplicationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_group(self, group_id: int) -> APIResult[DnsApplicationGroups]:
        """
        Fetches a specific DNS application group by ID.

        Args:
            group_id (int): The unique identifier for the DNS application group.

        Returns:
            tuple: A tuple containing (DnsApplicationGroups instance, Response, error).

        Examples:
            Print a specific DNS application group:

            >>> fetched_group, _, error = client.zia.dns_application_groups.get_group(1013)
            >>> if error:
            ...     print(f"Error fetching DNS application group by ID: {error}")
            ...     return
            ... print(f"Fetched DNS application group by ID: {fetched_group.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dnsApplicationGroups/{group_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DnsApplicationGroups)
        if error:
            return (None, response, error)

        try:
            result = DnsApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_group(self, **kwargs) -> APIResult[DnsApplicationGroups]:
        """
        Creates a new DNS application group.

        Args:
            name (str): The name of the DNS application group.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the DNS application group.
            dns_applications (list): The list of dns applications for this DNS application group.

        Returns:
            tuple: A tuple containing the newly added DnsApplicationGroups instance, response, and error.

        Examples:
            Add a new DNS application group:

            >>> added_group, _, error = client.zia.dns_application_groups.add_group(
            ...     name=f"NewGroup_{random.randint(1000, 10000)}",
            ...     description=f"NewGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error adding DNS application group: {error}")
            ...     return
            ... print(f"Dns application group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dnsApplicationGroups
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DnsApplicationGroups)
        if error:
            return (None, response, error)

        try:
            result = DnsApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_group(self, group_id: int, **kwargs) -> APIResult[DnsApplicationGroups]:
        """
        Updates information for the specified DNS application group.

        Args:
            group_id (int): The unique identifier for the DNS application group.

        Keyword Args:
            name (str): The name of the DNS application group.
            description (str): Additional information about the DNS application group.
            dns_applications (list): The list of dns applications for this DNS application group.

        Returns:
            tuple: A tuple containing the updated DnsApplicationGroups instance, response, and error.

        Examples:
            Update an existing DNS application group:

            >>> updated_group, _, error = client.zia.dns_application_groups.update_group(
            ...     group_id=1013,
            ...     name=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedGroup_{random.randint(1000, 10000)}",
            ... )
            >>> if error:
            ...     print(f"Error updating DNS application group: {error}")
            ...     return
            ... print(f"Dns application group updated successfully: {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dnsApplicationGroups/{group_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DnsApplicationGroups)
        if error:
            return (None, response, error)

        try:
            result = DnsApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_group(self, group_id: int) -> APIResult[None]:
        """
        Deletes the specified DNS application group.

        Args:
            group_id (int): The unique identifier for the DNS application group.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a DNS application group:

            >>> _, _, error = client.zia.dns_application_groups.delete_group(1013)
            >>> if error:
            ...     print(f"Error deleting DNS application group: {error}")
            ...     return
            ... print(f"Dns application group deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /dnsApplicationGroups/{group_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
