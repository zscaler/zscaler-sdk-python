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

from zscaler.request_executor import RequestExecutor
from zscaler.api_client import APIClient
from zscaler.zia.models.cloud_firewall_destination_groups import IPDestinationGroups
from zscaler.zia.models.cloud_firewall_source_groups import IPSourceGroup
from zscaler.zia.models.cloud_firewall_nw_application_groups import NetworkApplicationGroups
from zscaler.zia.models.cloud_firewall_nw_applications import NetworkApplications
from zscaler.zia.models.cloud_firewall_nw_service_groups import NetworkServiceGroups
from zscaler.zia.models.cloud_firewall_nw_service import NetworkServices
from zscaler.zia.models.cloud_firewall_time_windows import TimeWindows
from zscaler.utils import format_url, transform_common_id_fields, reformat_params


class FirewallResourcesAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_ip_destination_groups(self, exclude_type: str = None, query_params=None) -> tuple:
        """
        Returns a list of IP Destination Groups.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.exclude_type]`` (str):
                    Exclude all groups that match the specified IP destination group's type.
                    Accepted values: ``DSTN_IP``, ``DSTN_FQDN``, ``DSTN_DOMAIN``, ``DSTN_OTHER``.

        Returns:
            tuple:
                A tuple containing (list of IPDestinationGroups instances, Response, error)

        Examples:
            Gets a list of all IP destination groups.

            >>> group_list, response, error = zia.cloud_firewall.list_ip_destination_groups():
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP destination groups by excluding specific type.

            >>> group_list, response, error = zia.cloud_firewall.list_ip_destination_groups(
                query_params={"exclude_type": 'DSTN_DOMAIN'}):
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """

        valid_exclude_types = {"DSTN_IP", "DSTN_FQDN", "DSTN_DOMAIN", "DSTN_OTHER"}

        if exclude_type and exclude_type not in valid_exclude_types:
            raise ValueError(
                f"Invalid exclude_type: {exclude_type}. \
                Supported values are: {', '.join(valid_exclude_types)}"
            )

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups
        """
        )

        query_params = query_params or {}

        if exclude_type:
            query_params["excludeType"] = exclude_type

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
                result.append(IPDestinationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ipv6_destination_groups(self, exclude_type: str = None, query_params=None) -> tuple:
        """
        Lists IPv6 Destination Groups name and ID  all IPv6 Source Groups.
        `Note`: User-defined groups for IPv6 addresses are currently not supported,
        so this endpoint retrieves only the predefined group that includes all IPv6 addresses.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.exclude_type]`` (str):
                    Exclude all groups that match the specified IP destination group's type.
                    Accepted values: ``DSTN_IP``, ``DSTN_FQDN``, ``DSTN_DOMAIN``, ``DSTN_OTHER``.

        Returns:
            tuple:
                A tuple containing (list of IPDestinationGroups instances, Response, error)

        Examples:
            Gets a list of all IP destination groups.

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_destination_groups():
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP destination groups by excluding specific type.

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_destination_groups(
                query_params={"exclude_type": 'DSTN_DOMAIN'}):
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """

        valid_exclude_types = {"DSTN_IP", "DSTN_FQDN", "DSTN_DOMAIN", "DSTN_OTHER"}

        if exclude_type and exclude_type not in valid_exclude_types:
            raise ValueError(
                f"Invalid exclude_type: {exclude_type}. \
                Supported values are: {', '.join(valid_exclude_types)}"
            )

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/ipv6DestinationGroups
        """
        )

        query_params = query_params or {}

        if exclude_type:
            query_params["excludeType"] = exclude_type

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
                result.append(IPDestinationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ip_destination_groups_lite(self, exclude_type: str = None, query_params=None) -> tuple:
        """
        Lists IP Destination Groups name and ID  all IP Destination Groups.
        This endpoint retrieves only IPv4 destination address groups.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.exclude_type]`` (str):
                    Exclude all groups that match the specified IP destination group's type.
                    Accepted values: ``DSTN_IP``, ``DSTN_FQDN``, ``DSTN_DOMAIN``, ``DSTN_OTHER``.

        Returns:
            tuple: List of IP Destination Groups resource records.

        Examples:
            Gets a list of all IP destination groups.

            >>> group_list, response, error = zia.cloud_firewall.list_ip_destination_groups_lite():
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP destination groups by excluding specific type.

            >>> group_list, response, error = zia.cloud_firewall.list_ip_destination_groups_lite(
                query_params={"exclude_type": 'DSTN_DOMAIN'}):
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/lite
        """
        )

        valid_exclude_types = {"DSTN_IP", "DSTN_FQDN", "DSTN_DOMAIN", "DSTN_OTHER"}

        if exclude_type and exclude_type not in valid_exclude_types:
            raise ValueError(
                f"Invalid exclude_type: {exclude_type}. \
                Supported values are: {', '.join(valid_exclude_types)}"
            )

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups
        """
        )

        query_params = query_params or {}

        if exclude_type:
            query_params["excludeType"] = exclude_type

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
                result.append(IPDestinationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ipv6_destination_groups_lite(self, exclude_type: str = None, query_params=None) -> tuple:
        """
        Lists IPv6 Destination Groups name and ID  all IPv6 Source Groups.
        `Note`: User-defined groups for IPv6 addresses are currently not supported,
        so this endpoint retrieves only the predefined group that includes all IPv6 addresses.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.exclude_type]`` (str):
                    Exclude all groups that match the specified IP destination group's type.
                    Accepted values: ``DSTN_IP``, ``DSTN_FQDN``, ``DSTN_DOMAIN``, ``DSTN_OTHER``.

        Returns:
            tuple: List of IP Destination Groups resource records.

        Examples:
            Gets a list of all IP destination groups.

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_destination_groups_lite():
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP destination groups by excluding specific type.

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_destination_groups_lite(
                query_params={"exclude_type": 'DSTN_DOMAIN'}):
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/ipv6DestinationGroups/lite
        """
        )

        valid_exclude_types = {"DSTN_IP", "DSTN_FQDN", "DSTN_DOMAIN", "DSTN_OTHER"}

        if exclude_type and exclude_type not in valid_exclude_types:
            raise ValueError(
                f"Invalid exclude_type: {exclude_type}. \
                Supported values are: {', '.join(valid_exclude_types)}"
            )

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups
        """
        )

        query_params = query_params or {}

        if exclude_type:
            query_params["excludeType"] = exclude_type

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
                result.append(IPDestinationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ip_destination_group(self, group_id: int) -> tuple:
        """
        Returns information on the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.

        Returns:
            tuple: The IP Destination Group resource record.

        Examples:
            >>> fetched_group, response, error = client.zia.cloud_firewall.get_ip_destination_group('18382907')
            ... if error:
            ...     print(f"Error fetching group by ID: {error}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPDestinationGroups)

        if error:
            return (None, response, error)

        try:
            result = IPDestinationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_ip_destination_group(self, **kwargs) -> tuple:
        """
        Adds a new IP Destination Group.

        Args:
            name (str): The name of the IP Destination Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the destination IP group.
            type (str): Destination IP group type. Allowed values are DSTN_IP and DSTN_FQDN, DSTN_DOMAIN, DSTN_OTHER.
            addresses (list): Destination IP addresses or FQDNs within the group.
            ip_categories (list): Destination IP address URL categories. Note: Only Custom categories allowed.
            countries (list): Destination IP address counties. i.e COUNTRY_CA, COUNTRY_US.

        Returns:
            :obj:`Tuple`: The newly created IP Destination Group resource record.

        Examples:
            Add a Destination IP Group with IP addresses:

            >>> added_group, _, error = client.zia.cloud_firewall.add_ip_destination_group(
            ...     name=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...     description=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...     addresses=["192.168.1.1", "192.168.1.2"],
            ...     type='DSTN_IP',
            ... )
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")

            Add a Destination IP Group with FQDN:

            >>> added_group, _, error = client.zia.cloud_firewall.add_ip_destination_group(
            ...    name=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...    description='Covers domains for Example Inc.',
            ...    addresses=['example.com', 'example.edu'],
            ...    type='DSTN_FQDN',
            ... )
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")

            Add a Destination IP Group with country and url category for the US:

            >>> added_group, _, error = client.zia.cloud_firewall.add_ip_destination_group(
            ...    name=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...    description='Covers domains for Example Inc.',
            ...    type='DSTN_OTHER',
            ...    countries=['COUNTRY_US']),
            ...    ip_categories=['CUSTOM_01']),
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups
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

        response, error = self._request_executor.execute(request, IPDestinationGroups)

        if error:
            return (None, response, error)

        try:
            result = IPDestinationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_ip_destination_group(self, group_id: str, **kwargs) -> tuple:
        """
        Updates the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the IP Destination Group.
            description (str): Additional information about the destination IP group.
            type (str): Destination IP group type. Allowed values are DSTN_IP and DSTN_FQDN, DSTN_DOMAIN, DSTN_OTHER.
            addresses (list): Destination IP addresses or FQDNs within the group.
            ip_categories (list): Destination IP address URL categories. Note: Only Custom URL categories allowed.
            countries (list): Destination IP address counties. i.e COUNTRY_CA, COUNTRY_US.

        Returns:
            :obj:`Tuple`: The updated IP Destination Group resource record.

        Examples:
            Update the name of an IP Destination Group:

            >>> updated_group, _, error = client.zia.cloud_firewall.update_ip_destination_group(
            ...     group_id='452125',
            ...     name=f"UpdateGroup {random.randint(1000, 10000)}",
            ...     description=f"UpdateGroup {random.randint(1000, 10000)}",
            ...     addresses=["192.168.1.1", "192.168.1.2"],
            ...     type="DSTN_IP"
            ... )
            >>> if error:
            ...     print(f"Error updating group: {error}")
            ...     return
            ... print(f"Group updated successfully: {updated_group.as_dict()}")

            Update the description and FQDNs for an IP Destination Group:

            >>> updated_group, _, error = client.zia.cloud_firewall.update_ip_destination_group(
            ...     group_id='452125',
            ...     name=f"UpdateGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdateGroup {random.randint(1000, 10000)}",
            ...     addresses=['arstechnica.com', 'slashdot.org'],
            ...     type="DSTN_FQDN",
            ... )
            >>> if error:
            ...     print(f"Error updating group: {error}")
            ...     return
            ... print(f"Group updated successfully: {updated_group.as_dict()}")

            Update a Destination IP Group with country and url category for the US:

            >>> updated_group, _, error = client.zia.cloud_firewall.update_ip_destination_group(
            ...    group_id='452125',
            ...    name=f"UpdateGroup_{random.randint(1000, 10000)}",
            ...    description=f"UpdateGroup_{random.randint(1000, 10000)}",
            ...    type='DSTN_OTHER',
            ...    countries=['COUNTRY_CA']),
            ...    ip_categories=['CUSTOM_01']),
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/{group_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPDestinationGroups)
        if error:
            return (None, response, error)

        try:
            result = IPDestinationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ip_destination_group(self, group_id: int) -> tuple:
        """
        Deletes the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            >>> _, _, error = client.zia.cloud_firewall.delete_ip_destination_group('18382907')
            >>> if error:
            ...     print(f"Error deleting group: {error}")
            ...     return
            ... print(f"Group with ID {updated_group.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipDestinationGroups/{group_id}
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

    def list_ip_source_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        List IP Source Groups in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple: A tuple containing (list of IP Source Groups instances, Response, error)

        Examples:
            List all IP Source Groups:

            >>> group_list, response, error = zia.cloud_firewall.list_ip_source_groups():
            ... if error:
            ...     print(f"Error listing IP Source Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP Source Groups.

            >>> group_list, response, error = zia.cloud_firewall.list_ip_source_groups(
                query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing IP Source Groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups
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
                result.append(IPSourceGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ipv6_source_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        List IPv6 Source Groups in your organization.
        `Note`: User-defined groups for IPv6 addresses are currently not supported,
        so this endpoint retrieves only the predefined group that includes all IPv6 addresses.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple: A tuple containing (list of IPv6 Source Groups instances, Response, error)

        Examples:
            List all IPv6 Source Groups:

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_source_groups():
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Use search parameter to find IP Source Groups with `fiji` in the name:

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_source_groups('fiji'):
            ... if error:
            ...     print(f"Error listing ip destination groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/ipv6SourceGroups
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
                result.append(IPSourceGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ip_source_groups_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists IP Source Groups name and ID  all IP Source Groups.
        This endpoint retrieves only IPv4 source address groups.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against a group's name or description attributes.

        Returns:
            tuple: List of IP Source Groups resource records.

        Examples:
            Gets a list of all IP source groups.

            >>> group_list, response, error = zia.cloud_firewall.list_ip_source_groups_lite():
            ... if error:
            ...     print(f"Error listing IP source groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP source groups name and ID.

            >>> group_list, response, error = zia.cloud_firewall.list_ip_source_groups_lite(
                query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing IP source groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/lite
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(IPSourceGroup(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def list_ipv6_source_groups_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists IPv6 Source Groups name and ID all IPv6 Source Groups.
        `Note`: User-defined groups for IPv6 addresses are currently not supported,
        so this endpoint retrieves only the predefined group that includes all IPv6 addresses.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against a group's name or description attributes.

        Returns:
            tuple: List of IPv6 Source Groups resource records.

        Examples:
            Gets a list of all IP source groups.

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_source_groups_lite():
            ... if error:
            ...     print(f"Error listing IP source groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all IP source groups name and ID.

            >>> group_list, response, error = zia.cloud_firewall.list_ipv6_source_groups_lite(
                query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing IP source groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/ipv6SourceGroups/lite
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(IPSourceGroup(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_ip_source_group(
        self,
        group_id: int,
    ) -> tuple:
        """
        Returns information for the specified IP Source Group.

        Args:
            group_id (str): The unique identifier for the source group.

        Examples:
            >>> fetched_group, response, error = client.zia.cloud_firewall.get_ip_source_group('18382907')
            ... if error:
            ...     print(f"Error fetching group by ID: {error}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPSourceGroup)

        if error:
            return (None, response, error)

        try:
            result = IPSourceGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_ip_source_group(self, **kwargs) -> tuple:
        """
        Adds a new IP Source Group.

        Args:
            name (str): The name of the IP Source Group.
            ip_addresses (list): The list of IP addresses for the IP Source Group.
            description (str): Additional information for the IP Source Group.

        Returns:
            tuple: The new IP Source Group resource record.

        Examples:
            Add a new IP Source Group:

            >>> added_group, _, error = client.zia.cloud_firewall.add_ip_source_group(
            ...     name=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...     description=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...     ip_addresses=["192.168.1.1", "192.168.1.2"],
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
            /ipSourceGroups
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

        response, error = self._request_executor.execute(request, IPSourceGroup)
        if error:
            return (None, response, error)

        try:
            result = IPSourceGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_ip_source_group(self, group_id: int, **kwargs) -> tuple:
        """
        Update an IP Source Group.

        This method supports updating individual fields in the IP Source Group resource record.

        Args:
            group_id (str): The unique ID for the IP Source Group to update.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the IP Source Group.
            ip_addresses (list): The list of IP addresses for the IP Source Group.
            description (str): Additional information for the IP Source Group.

        Returns:
            :obj:`Tuple`: The updated IP Source Group resource record.

        Examples:

            Update ip_addresses list of the IP Source Group:

            >>> update_group, _, error = client.zia.cloud_firewall.add_ip_source_group(
            ...     name=f"UpdateNewGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdateNewGroup_{random.randint(1000, 10000)}",
            ...     ip_addresses=["192.168.1.1", "192.168.1.2", "192.168.1.4"],
            ... )
            >>> if error:
            ...     print(f"Error updating group: {error}")
            ...     return
            ... print(f"Group updated successfully: {update_group.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/{group_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IPSourceGroup)
        if error:
            return (None, response, error)

        try:
            result = IPSourceGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ip_source_group(self, group_id: int) -> tuple:
        """
        Deletes an IP Source Group.

        Args:
            group_id (str): The unique ID of the IP Source Group to be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, error = client.zia.cloud_firewall.delete_ip_source_group('18382907')
            >>> if error:
            ...     print(f"Error deleting group: {error}")
            ...     return
            ... print(f"Group with ID 18382907 deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /ipSourceGroups/{group_id}
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

    def list_network_app_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        List Network Application Groups in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results by rule name.

        Returns:
            tuple:
                A tuple containing (list of NetworkApplicationGroups instances, Response, error).

        Examples:
            Gets a list of all network app groups.

            >>> group_list, response, error = zia.cloud_firewall.list_network_app_groups():
            ... if error:
            ...     print(f"Error listing network app groupss: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all network app groups by excluding specific type.

            >>> group_list, response, error = zia.cloud_firewall.list_network_app_groups(
                query_params={"search": 'AppGroup01'}):
            ... if error:
            ...     print(f"Error listing network app groups: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups
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
                result.append(NetworkApplicationGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_network_app_group(
        self,
        group_id: int,
    ) -> tuple:
        """
        Returns information for the specified Network Application Group.

        Args:
            group_id (str):
                The unique ID for the Network Application Group.

        Returns:
             :obj:`FirewallRule`: The Network Application Group resource record.

        Examples:
            >>> fetched_group, response, error = client.zia.cloud_firewall.get_network_app_group('18382907')
            ... if error:
            ...     print(f"Error fetching group by ID: {error}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups/{group_id}
        """
        )
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkApplicationGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_network_app_group(self, **kwargs) -> tuple:
        """
        Adds a new Network Application Group.

        Args:
            name (str): The name of the Network Application Group.
            description (str): Additional information about the Network Application Group.
            network_applications (list): A list of Application IDs to add to the group.

        Returns:
            :obj:`Tuple`: The newly created Network Application Group resource record.

        Examples:
            Add a new Network Application Group:

            >>> added_group, _, error = client.zia.cloud_firewall.add_network_app_group(
            ...     name=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...     description=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...     network_applications=['SALESFORCE', 'GOOGLEANALYTICS', 'OFFICE365'],
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
            /networkApplicationGroups
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

        response, error = self._request_executor.execute(request, NetworkApplicationGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_network_app_group(self, group_id: int, **kwargs) -> tuple:
        """
        Update an Network Application Group.

        This method supports updating individual fields in the Network Application Group resource record.

        Args:
            group_id (str): The unique ID for the Network Application Group to update.

        Keyword Args:
            name (str): The name of the Network Application Group.
            network_applications (list): The list of applications for the Network Application Group.
            description (str): Additional information for the Network Application Group.

        Returns:
            :obj:`Tuple`: The updated Network Application Group resource record.

        Examples:
            Update the name of an Network Application Group:

            >>> update_group, _, error = client.zia.cloud_firewall.add_network_app_group(
            ...     name=f"UpdateNewGroup_{random.randint(1000, 10000)}",
            ...     description=f"UpdateNewGroup_{random.randint(1000, 10000)}",
            ...     network_applications=['SALESFORCE', 'GOOGLEANALYTICS'],
            ... )
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {update_group.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups/{group_id}
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response, error = self._request_executor.execute(request, NetworkApplicationGroups)
        if error:
            return (None, response, error)

        try:
            result = NetworkApplicationGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_network_app_group(
        self,
        group_id: int,
    ) -> tuple:
        """
        Deletes the specified Network Application Group.

        Args:
            group_id (str): The unique identifier for the Network Application Group.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> _, _, error = client.zia.cloud_firewall.delete_network_app_group('18382907')
            >>> if error:
            ...     print(f"Error deleting group: {error}")
            ...     return
            ... print(f"Group with ID {updated_group.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplicationGroups/{group_id}
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

    def list_network_apps(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists Network Applications in your organization with pagination.
        A subset of Network Applications can be returned that match a supported
        filter expression or query.

        Args:
            query_params (dict): Map of query parameters for the request.
                ``[query_params.search]`` (str): Search string for filtering results.

                ``[query_params.locale]`` (str): When set to one of the supported locales (e.g., ``en-US``, ``de-DE``,
                    ``es-ES``, ``fr-FR``, ``ja-JP``, ``zh-CN``), the network application
                    description is localized into the requested language.

        Returns:
            tuple:
                A tuple containing (list of firewall rules instances, Response, error).

        Examples:
            Gets a list of all network apps.

            >>> app_list, response, error = zia.cloud_firewall.list_network_apps():
            ... if error:
            ...     print(f"Error listing ip network apps : {error}")
            ...     return
            ... print(f"Total apps found: {len(app_list)}")
            ... for app in app_list:
            ...     print(app.as_dict())

            Gets a list of all of specific network apps.

            >>> app_list, response, error = zia.cloud_firewall.list_network_apps(
                query_params={'search': 'ICMP_ANY',"locale": 'fr-FR'}):
            ... if error:
            ...     print(f"Error listing network apps : {error}")
            ...     return
            ... print(f"Total apps found: {len(app_list)}")
            ... for app in app_list:
            ...     print(app.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplications
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
                result.append(NetworkApplications(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_network_app(self, app_id: int) -> tuple:
        """
        Returns information for the specified Network Application.

        Args:
            app_id (str): The unique ID for the Network Application.

        Examples:
            >>> fetched_app, response, error = client.zia.cloud_firewall.get_network_app('18382907')
            ... if error:
            ...     print(f"Error fetching app by ID: {error}")
            ...     return
            ... print(f"Fetched app by ID: {fetched_app.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkApplications/{app_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkApplications)
        if error:
            return (None, response, error)

        try:
            result = NetworkApplications(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_network_svc_groups(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists network service groups in your organization with pagination.
        A subset of network service groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string used to match against a group's name or description attributes.

        Returns:
            tuple: List of Network Service Group resource records.

        Examples:
            Gets a list of all network services group.

            >>> group_list, response, error = zia.cloud_firewall.list_network_svc_groups():
            ... if error:
            ...     print(f"Error listing network services group: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all network services group.

            >>> group_list, response, error = zia.cloud_firewall.list_network_svc_groups(
                query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing network services group: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups
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
                result.append(NetworkServiceGroups(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_network_svc_groups_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists Network Service Groups name and ID  all network service groups.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params (dict): Map of query parameters for the request.
                ``[query_params.search]`` (str): Search string for filtering results.

        Returns:
            tuple:
                A tuple containing (list of network service groups instances, Response, error).

        Examples:
            Gets a list of all network services group.

            >>> group_list, response, error = zia.cloud_firewall.list_network_svc_groups():
            ... if error:
            ...     print(f"Error listing network services group: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

            Gets a list of all network services group.

            >>> group_list, response, error = zia.cloud_firewall.list_network_svc_groups(
                query_params={"search": 'Group01'}):
            ... if error:
            ...     print(f"Error listing network services group: {error}")
            ...     return
            ... print(f"Total groups found: {len(group_list)}")
            ... for group in group_list:
            ...     print(group.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups/lite
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(NetworkServiceGroups(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_network_svc_group(self, group_id: int) -> tuple:
        """
        Returns information for the specified Network Service Group.

        Args:
            group_id (str): The unique ID for the Network Service Group.

        Examples:
            >>> fetched_group, response, error = client.zia.cloud_firewall.get_network_svc_group('18382907')
            ... if error:
            ...     print(f"Error fetching group by ID: {error}")
            ...     return
            ... print(f"Fetched group by ID: {fetched_group.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkServiceGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkServiceGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_network_svc_group(self, **kwargs) -> tuple:
        """
        Adds a new Network Service Group.

        Args:
            name (str): The name of the Network Service Group.
            service_ids (list): A list of Network Service IDs to add to the group.
            description (str): Additional information about the Network Service Group.

        Returns:
            :obj:`Tuple`: The newly created Network Service Group resource record.

        Examples:
            Add a new Network Service Group:

            >>> added_group, _, error = client.zia.cloud_firewall.add_network_svc_group(
            ...    name=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...    description=f"AddNewGroup_{random.randint(1000, 10000)}",
            ...    service_ids=['159143', '159144', '159145'],
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {added_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups
        """
        )

        body = kwargs

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkServiceGroups)

        if error:
            return (None, response, error)

        try:
            result = NetworkServiceGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_network_svc_group(self, group_id: int, **kwargs) -> tuple:
        """
        Update a Network Service Group.

        Args:
            group_id (str): The unique ID of the Network Service Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the Network Service Group.
            service_ids (list): A list of Network Service IDs to add to the group.
            description (str): Additional information about the Network Service Group.

        Returns:
            :obj:`Tuple`: The updated Network Service Group resource record.

        Examples:
            Update the name Network Service Group:

            >>> update_group, _, error = client.zia.cloud_firewall.update_network_svc_group(
            ...    name=f"UpdateNewGroup_{random.randint(1000, 10000)}",
            ...    description=f"UpdateNewGroup_{random.randint(1000, 10000)}",
            ...    service_ids=['159143', '159144'],
            >>> if error:
            ...     print(f"Error adding group: {error}")
            ...     return
            ... print(f"Group added successfully: {update_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups/{group_id}
        """
        )

        body = kwargs

        transform_common_id_fields(reformat_params, body, body)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response, error = self._request_executor.execute(request, NetworkServiceGroups)
        if error:
            return (None, response, error)

        try:
            result = NetworkServiceGroups(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_network_svc_group(
        self,
        group_id: int,
    ) -> tuple:
        """
        Deletes the specified Network Service Group.

        Args:
            group_id (str): The unique identifier for the Network Service Group.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> _, _, error = client.zia.cloud_firewall.delete_network_svc_group('18382907')
            >>> if error:
            ...     print(f"Error deleting group: {error}")
            ...     return
            ... print(f"Group with ID {updated_group.id} deleted successfully.")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServiceGroups/{group_id}
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

    def list_network_services(self, query_params=None) -> tuple:
        """
        Lists network services in your organization with pagination.
        A subset of network services  can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.protocol]`` {str}: Filter based on the network service protocol.
                Supported Values: `ICMP`, `TCP`, `UDP`, `GRE`, `ESP`, `OTHER`,

                ``[query_params.search]`` {str}: Search string used to match against a service's name or description attributes

                ``[query_params.locale]`` (str): When set to one of the supported locales (e.g., ``en-US``, ``de-DE``,
                    ``es-ES``, ``fr-FR``, ``ja-JP``, ``zh-CN``), the network application
                    description is localized into the requested language.
        Returns:
            tuple: A tuple containing (list of network services instances, Response, error)

        Examples:
            Gets a list of all network services.

            >>> service_list, response, error = zia.cloud_firewall.list_network_services():
            >>> if error:
            ...     print(f"Error listing network services: {error}")
            ...     return
            ... print(f"Total network services found: {len(service_list)}")
            ... for service in service_list:
            ...     print(service.as_dict())

            Gets a list of all network services.

            >>> service_list, response, error = zia.cloud_firewall.list_network_services(query_params={"search": 'FTP'}):
            ... if error:
            ...     print(f"Error listing network services: {error}")
            ...     return
            ... print(f"Total services found: {len(service_list)}")
            ... for service in service_list:
            ...     print(service.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices
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
                result.append(NetworkServices(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_network_services_lite(
        self,
        query_params=None,
    ) -> tuple:
        """
        Lists network services name and ID all network services.
        A subset of network service groups can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}:  Search string used to match against a group's name or description attributes.

                ``[query_params.locale]`` (str): When set to one of the supported locales (e.g., ``en-US``, ``de-DE``,
                    ``es-ES``, ``fr-FR``, ``ja-JP``, ``zh-CN``), the network application
                    description is localized into the requested language.

        Returns:
            tuple: List of Network Services resource records.

        Examples:
            Gets a list of all network services.

            >>> service_list, response, error = zia.cloud_firewall.list_network_services_lite():
            ... if error:
            ...     print(f"Error listing network services: {error}")
            ...     return
            ... print(f"Total network services found: {len(service_list)}")
            ... for service in service_list:
            ...     print(service.as_dict())

            Gets a list of all network services.

            >>> service_list, response, error = zia.cloud_firewall.list_network_services_lite(
                query_params={"search": 'FTP'}):
            ... if error:
            ...     print(f"Error listing network services: {error}")
            ...     return
            ... print(f"Total services found: {len(service_list)}")
            ... for service in service_list:
            ...     print(service.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices/lite
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(NetworkServices(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def get_network_service(self, service_id: int) -> tuple:
        """
        Returns information for the specified Network Service.

        Args:
            service_id (str): The unique ID for the Network Service.

        Returns:
            :obj:`Tuple`: The Network Service resource record.

        Examples:
            >>> fetched_service, response, error = client.zia.cloud_firewall.get_network_service('18382907')
            ... if error:
            ...     print(f"Error fetching service by ID: {error}")
            ...     return
            ... print(f"Fetched service by ID: {fetched_service.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices/{service_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_network_service(self, ports: list = None, **kwargs) -> tuple:
        """
        Adds a new Network Service

        Args:
            name: The name of the Network Service
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`,
                `start port`, `end port`. If this is a single port and not a port range then `end port` can be omitted.
                E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`Tuple`: The newly created Network Service resource record.

        Examples:

            Add Network Services:

            >>> added_service, _, error = client.zia.cloud_firewall.add_network_service(
            ...     name=f"NewService {random.randint(1000, 10000)}",
            ...     description=f"NewService {random.randint(1000, 10000)}",
            ...     ports=[
            ...         ('dest', 'tcp', '389'),
            ...         ('dest', 'udp', '389'),
            ...         ('dest', 'tcp', '636'),
            ...         ('dest', 'tcp', '3268', '3269')])
            >>> if error:
            ...     print(f"Error adding network services: {error}")
            ...     return
            ... print(f"Service added successfully: {added_service.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices
        """
        )

        body = kwargs

        if ports is not None:
            for items in ports:
                port_dict = {"start": int(items[2])}
                if len(items) == 4:
                    port_dict["end"] = int(items[3])
                body.setdefault(f"{items[0]}{items[1].title()}Ports", []).append(port_dict)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_network_service(self, service_id: str, ports: list = None, **kwargs) -> tuple:
        """
        Updates the specified Network Service.

        If ports aren't provided then no changes will be made to the ports already defined. If ports are provided then
        the existing ports will be overwritten.

        Args:
            service_id (str): The unique ID for the Network Service.
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`, `start port`,
                `end port`. If this is a single port and not a port range then `end port` can be omitted. E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`dict`: The updated Network Service resource record.

        Examples:
            Update the name and description for a Network Service:

            >>> update_service, _, error = client.zia.cloud_firewall.update_network_service(
            ...     name=f"UpdateNewService_{random.randint(1000, 10000)}",
            ...     description=f"UpdateNewService_{random.randint(1000, 10000)}",
            ...     ports=[
            ...         ('dest', 'tcp', '389'),
            ...         ('dest', 'udp', '389'),
            ...         ('dest', 'tcp', '636'),
            ...         ('dest', 'tcp', '3268', '3269')])
            >>> if error:
            ...     print(f"Error updating network services: {error}")
            ...     return
            ... print(f"Service updated successfully: {added_service.as_dict()}")

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices/{service_id}
        """
        )

        body = {}

        body.update(kwargs)

        if ports is not None:
            for items in ports:
                port_dict = {"start": int(items[2])}
                if len(items) == 4:
                    port_dict["end"] = int(items[3])
                body.setdefault(f"{items[0]}{items[1].title()}Ports", []).append(port_dict)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NetworkServices)

        if error:
            return (None, response, error)

        try:
            result = NetworkServices(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_network_service(self, service_id: int) -> tuple:
        """
        Deletes the specified Network Service.

        Args:
            service_id (str): The unique ID for the Network Service.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, error = client.zia.cloud_firewall.delete_network_service('18382907')
            >>> if error:
            ...     print(f"Error deleting network service: {error}")
            ...     return
            ... print(f"Network service with ID 18382907 deleted successfully.")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /networkServices/{service_id}
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

    def list_time_windows(self) -> tuple:
        """
        Returns a list of time intervals used by the Firewall policy or the URL Filtering policy.

        Returns:
            tuple: A list of TimeWindow model instances, the response object, and any error encountered.

        Examples:
            >>> result, response, error = zia.cloud_firewall.list_time_windows()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeWindows
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
            result = []
            for item in response.get_body():
                result.append(TimeWindows(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_time_windows_lite(self) -> tuple:
        """
        Returns name and ID dictionary of time intervals used by the Firewall policy or the URL Filtering policy.

        Returns:
            tuple: A list of TimeWindowLite model instances, the response object, and any error encountered.

        Examples:
            >>> result, response, error = zia.cloud_firewall.list_time_windows_lite()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /timeWindows/lite
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
            result = []
            for item in response.get_results():
                result.append(TimeWindows(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
