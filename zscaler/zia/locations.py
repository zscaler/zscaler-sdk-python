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
from zscaler.zia.models.location_management import LocationManagement
from zscaler.zia.models.location_group import LocationGroup
from zscaler.utils import format_url


class LocationsAPI(APIClient):
    """
    A Client object for the Locations resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_locations(self, query_params=None) -> tuple:
        """
        Returns a list of locations.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.page]`` (int): Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size.
                    The default size is 100, but the maximum size is 1000.

                ``[query_params.search]`` (str): String used to partially match against a location's name and port attributes.

                ``[query_params.ssl_scan_enabled]`` (bool): Parameter was deprecated and no longer has an effect on SSL policy.

                ``[query_params.xff_enabled]`` (bool):
                    Filter based on whether the Enforce XFF Forwarding setting is enabled or disabled
                    for a location.

                ``[query_params.auth_required]`` (bool):
                    Filter based on whether the Enforce Authentication setting is enabled or disabled
                    for a location.

                ``[query_params.bw_enforced]`` (bool):
                    Filter based on whether Bandwidth Control is being enforced for a location.

                ``[query_params.enable_iot]`` (bool):
                    If set to true, the city field (containing IoT-enabled location IDs, names, latitudes,
                    and longitudes) and the iotDiscoveryEnabled filter are included in the response.
                    Otherwise, they are not included.

        Returns:
            tuple:
                List of configured locations as (LocationManagement, Response, error).

        Examples:
            List locations using default settings:

            >>> for location in zia.locations.list_locations():
            ...     print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zia.locations.list_locations(max_items=10):
            ...     print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zia.locations.list_locations(page_size=200, max_pages=2):
            ...     print(location)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations
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
                result.append(LocationManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_location(self, location_id: int) -> tuple:
        """
        Returns information for the specified location based on the location id or location name.

        Args:
            location_id (int): The unique identifier for the location.

        Returns:
           tuple: A tuple containing (Location instance, Response, error).

        Examples:
            >>> location = zia.locations.get_location('97456691')

            >>> location = zia.locations.get_location_name(name='stockholm_office')
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/{location_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LocationManagement)

        if error:
            return (None, response, error)

        try:
            result = LocationManagement(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_location(self, **kwargs) -> tuple:
        """
        Adds a new location.

        Args:
            location (dict or object):
                The label data to be sent in the request.

        Keyword Args:
            parent_id (int, optional):
                Parent Location ID. If this ID does not exist or is 0, it is implied that it is a parent location.
            up_bandwidth (int, optional):
                Upload bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement. Default: 0.
            dn_bandwidth (int, optional):
                Download bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement. Default: 0.
            country (str, optional):
                Country.
            tz (str, optional):
                Timezone of the location. If not specified, it defaults to GMT.
            ip_addresses (list[str], optional):
                For locations: IP addresses of the egress points that are provisioned in the Zscaler Cloud.
                Each entry is a single IP address (e.g., 238.10.33.9).

                For sub-locations: Egress, internal, or GRE tunnel IP addresses. Each entry is either a single
                IP address, CIDR (e.g., 10.10.33.0/24), or range (e.g., 10.10.33.1-10.10.33.10)).
            ports (list[int], optional):
                IP ports that are associated with the location.
            vpn_credentials (list, optional):
                VPN User Credentials that are associated with the location.
            auth_required (bool, optional):
                Enforce Authentication. Required when ports are enabled, IP Surrogate is enabled, or Kerberos
                Authentication is enabled. Default: False.
            ssl_scan_enabled (bool, optional):
                Enable SSL Inspection. Set to true in order to apply your SSL Inspection policy to HTTPS traffic in
                the location and inspect HTTPS transactions for data leakage, malicious content, and viruses.
                Default: False.
            zapp_ssl_scan_enabled (bool, optional):
                Enable Zscaler App SSL Setting. When set to true, the Zscaler App SSL Scan Setting takes effect,
                irrespective of the SSL policy that is configured for the location. Default: False.
            xff_forward_enabled (bool, optional):
                Enable XFF Forwarding for a location. When set to true, traffic is passed to Zscaler Cloud via the
                X-Forwarded-For (XFF) header. Default: False.
            other_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv4 addresses that are not part of any user-defined sub-locations. Default: False.
            other6_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv6 addresses that are not part of any user-defined sub-locations. Default: False.
            surrogate_ip (bool, optional):
                Enable Surrogate IP. When set to true, users are mapped to internal device IP addresses. Default: False.
            idle_time_in_minutes (int, optional):
                Idle Time to Disassociation. The user mapping idle time (in minutes) is required if Surrogate IP is
                enabled.
            display_time_unit (str, optional):
                Display Time Unit. The time unit to display for IP Surrogate idle time to disassociation.
            surrogate_ip_enforced_for_known_browsers (bool, optional):
                Enforce Surrogate IP for Known Browsers. When set to true, IP Surrogate is enforced for all known
                browsers. Default: False.
            surrogate_refresh_time_in_minutes (int, optional):
                Refresh Time for re-validation of Surrogacy. The surrogate refresh time (in minutes) to re-validate
                the IP surrogates.
            surrogate_refresh_time_unit (str, optional):
                Display Refresh Time Unit. The time unit to display for refresh time for re-validation of surrogacy.
            ofw_enabled (bool, optional):
                Enable Firewall. When set to true, Firewall is enabled for the location. Default: False.
            ips_control (bool, optional):
                Enable IPS Control. When set to true, IPS Control is enabled for the location if Firewall is enabled.
                Default: False.
            aup_enabled (bool, optional):
                Enable AUP. When set to true, AUP is enabled for the location. Default: False.
            caution_enabled (bool, optional):
                Enable Caution. When set to true, a caution notification is enabled for the location. Default: False.
            aup_block_internet_until_accepted (bool, optional):
                For First Time AUP Behavior, Block Internet Access. When set, all internet access (including non-HTTP
                traffic) is disabled until the user accepts the AUP. Default: False.
            aup_force_ssl_inspection (bool, optional):
                For First Time AUP Behavior, Force SSL Inspection. When set, Zscaler forces SSL Inspection in order
                to enforce AUP for HTTPS traffic. Default: False.
            ipv6_enabled (bool, optional):
                If set to true, IPv6 is enabled for the location and IPv6 traffic from the location can be forwarded
                to the Zscaler service to enforce security policies.
            ipv6_dns64_prefix (str, optional):
                Name-ID pair of the NAT64 prefix configured as the DNS64 prefix for the location.
            aup_timeout_in_days (int, optional):
                Custom AUP Frequency. Refresh time (in days) to re-validate the AUP.
            managed_by (str, optional):
                SD-WAN Partner that manages the location. If a partner does not manage the location, this is set to
                Self.
            profile (str, optional):
                Profile tag that specifies the location traffic type. If not specified, this tag defaults to
                "Unassigned".
            description (str, optional):
                Additional notes or information regarding the location or sub-location. The description cannot
                exceed 1024 characters.

        Returns:
            :obj:`tuple`: The newly created location resource record

        Examples:
            Add a new location with an IP address.

            >>> zia.locations.add_location(name='new_location',
            ...    ip_addresses=['203.0.113.10'])

            Add a location with VPN credentials.

            >>> zia.locations.add_location(name='new_location',
            ...    vpn_credentials=[{'id': '99999', 'type': 'UFQDN'}])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations
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

        response, error = self._request_executor.execute(request, LocationManagement)

        if error:
            return (None, response, error)

        try:
            result = LocationManagement(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_location(self, location_id: int, **kwargs) -> tuple:
        """
        Update the specified location.

        Note: Changes are not additive and will replace existing values.

        Args:
            location_id (str):
                The unique identifier for the location you are updating.
            **kwargs:
                Optional keyword arguments.

        Keyword Args:
            name (str, optional):
                Location name.
            parent_id (int, optional):
                Parent Location ID. If this ID does not exist or is 0, it is implied that it is a parent location.
            up_bandwidth (int, optional):
                Upload bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement.
            dn_bandwidth (int, optional):
                Download bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement.
            country (str, optional):
                Country.
            tz (str, optional):
                Timezone of the location. If not specified, it defaults to GMT.
            ip_addresses (list[str], optional):
                For locations: IP addresses of the egress points that are provisioned in the Zscaler Cloud.
                Each entry is a single IP address (e.g., 238.10.33.9).

                For sub-locations: Egress, internal, or GRE tunnel IP addresses. Each entry is either a single
                IP address, CIDR (e.g., 10.10.33.0/24), or range (e.g., 10.10.33.1-10.10.33.10)).
            ports (list[int], optional):
                IP ports that are associated with the location.
            vpn_credentials (list, optional):
                VPN User Credentials that are associated with the location.
            auth_required (bool, optional):
                Enforce Authentication. Required when ports are enabled, IP Surrogate is enabled, or Kerberos
                 Authentication is enabled.
            ssl_scan_enabled (bool, optional):
                Enable SSL Inspection. Set to true in order to apply your SSL Inspection policy to HTTPS traffic in the
                location and inspect HTTPS transactions for data leakage, malicious content, and viruses.
            zapp_ssl_scan_enabled (bool, optional):
                Enable Zscaler App SSL Setting. When set to true, the Zscaler App SSL Scan Setting takes effect,
                irrespective of the SSL policy that is configured for the location.
            xff_forward_enabled (bool, optional):
                Enable XFF Forwarding for a location. When set to true, traffic is passed to Zscaler Cloud via the
                X-Forwarded-For (XFF) header.
            other_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv4 addresses that are not part of any user-defined sub-locations.
            other6_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv6 addresses that are not part of any user-defined sub-locations.
            surrogate_ip (bool, optional):
                Enable Surrogate IP. When set to true, users are mapped to internal device IP addresses.
            idle_time_in_minutes (int, optional):
                Idle Time to Disassociation. The user mapping idle time (in minutes) is required if a Surrogate IP is
                enabled.
            display_time_unit (str, optional):
                Display Time Unit. The time unit to display for IP Surrogate idle time to disassociation.
            surrogate_ip_enforced_for_known_browsers (bool, optional):
                Enforce Surrogate IP for Known Browsers. When set to true, IP Surrogate is enforced for all known
                browsers.
            surrogate_refresh_time_in_minutes (int, optional):
                Refresh Time for re-validation of Surrogacy. The surrogate refresh time (in minutes) to re-validate
                the IP surrogates.
            surrogate_refresh_time_unit (str, optional):
                Display Refresh Time Unit. The time unit to display for refresh time for re-validation of surrogacy.
            ofw_enabled (bool, optional):
                Enable Firewall. When set to true, Firewall is enabled for the location.
            ips_control (bool, optional):
                Enable IPS Control. When set to true, IPS Control is enabled for the location if Firewall is enabled.
            aup_enabled (bool, optional):
                Enable AUP. When set to true, AUP is enabled for the location.
            caution_enabled (bool, optional):
                Enable Caution. When set to true, a caution notification is enabled for the location.
            aup_block_internet_until_accepted (bool, optional):
                For First Time AUP Behavior, Block Internet Access. When set, all internet access (including non-HTTP
                traffic) is disabled until the user accepts the AUP.
            aup_force_ssl_inspection (bool, optional):
                For First Time AUP Behavior, Force SSL Inspection. When set, Zscaler forces SSL Inspection in order to
                enforce AUP for HTTPS traffic.
            ipv6_enabled (bool, optional):
                If set to true, IPv6 is enabled for the location and IPv6 traffic from the location can be forwarded
                to the Zscaler service to enforce security policies.
            ipv6_dns64_prefix (str, optional):
                Name-ID pair of the NAT64 prefix configured as the DNS64 prefix for the location.
            aup_timeout_in_days (int, optional):
                Custom AUP Frequency. Refresh time (in days) to re-validate the AUP.
            managed_by (str, optional):
                SD-WAN Partner that manages the location. If a partner does not manage the location, this is set to
                Self.
            profile (str, optional):
                Profile tag that specifies the location traffic type. If not specified, this tag defaults to
                "Unassigned".
            description (str, optional):
                Additional notes or information regarding the location or sub-location. The description cannot exceed
                1024 characters.

        Returns:
            :obj:`tuple`: The updated resource record.

        Examples:
            Update the name of a location:

            >>> zia.locations.update_location('99999',
            ...    name='updated_location_name')

            Update the IP address of a location:

            >>> zia.locations.update_location('99999',
            ...    ip_addresses=['203.0.113.20'])

            Update the VPN credentials of a location:

            >>> zia.locations.update_location('99999',
            ...    vpn_credentials=[{'id': '88888', 'type': 'UFQDN'}])

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/{location_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LocationManagement)
        if error:
            return (None, response, error)

        try:
            result = LocationManagement(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_location(self, location_id: int) -> tuple:
        """
        Deletes the location or sub-location for the specified ID

        Args:
            location_id (int):
                The unique identifier for the location or sub-location.

        Returns:
            :obj:`int`: Response code for the operation.

        Examples:
            >>> zia.locations.delete_location('97456691')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/{location_id}
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

    def bulk_delete_locations(self, location_ids: list) -> tuple:
        """
        Deletes all specified Location Management from ZIA.

        Args:
            location_ids (list): The list of unique ids for the ZIA Locations that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.locations.bulk_delete_locations(['111111', '222222', '333333'])

        """
        # Validate input before making the request
        if not location_ids:
            return (None, ValueError("Empty location_ids list provided"))

        if len(location_ids) > 100:
            return (None, ValueError("Maximum 100 location IDs allowed per bulk delete request"))

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/bulkDelete
        """
        )

        payload = {"ids": location_ids}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=payload, headers={}, params={}
        )
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        # For 204 No Content responses, the executor may return None
        if error:
            return (None, error)
        elif response is None:
            # This is the expected case for 204 No Content
            return (None, None)

        return (response, None)

    def list_sub_locations(self, location_id: int, query_params: dict = None) -> tuple:
        """
        Returns sub-location information for the specified location ID.

        Args:

            location_id (int): The unique identifier for the parent location.
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Keyword Args:
            **auth_required (bool, optional):
                Filter based on whether the Enforce Authentication setting is enabled or disabled for a location.
            **bw_enforced (bool, optional):
                Filter based on whether Bandwith Control is being enforced for a location.
            **enable_firewall (bool, optional):
                Filter based on whether Enable Firewall setting is enabled or disabled for a sub-location.
            **enforce_aup (bool, optional):
                Filter based on whether Enforce AUP setting is enabled or disabled for a sub-location.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.
            **xff_enabled (bool, optional):
                Filter based on whether the Enforce XFF Forwarding setting is enabled or disabled for a location.

        Returns:
            :obj:`Tuple`: A list of sub-locations configured for the parent location.

        Examples:
            >>> for sub_location in zia.locations.list_sub_locations('97456691'):
            ...    pprint(sub_location)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/{location_id}/sublocations
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
                result.append(LocationManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_locations_lite(self, query_params=None) -> tuple:
        """
        Returns only the name and ID of all configured locations.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 100, but the maximum size is 1000.

                ``[query_params.state]`` {str}: Filter based on geographical state for a location.

                ``[query_params.xff_enabled]`` {bool}: Filter based on whether xff_enabled is true for a location.

                ``[query_params.auth_required]`` {bool}: Filter based on whether Enforce Authentication is enabled.

                ``[query_params.bw_enforced]`` {bool}: Filter based on whether Bandwith Control is enforced for a location.

                ``[query_params.partner_id]`` {bool}: Not applicable to Cloud & Branch Connector.

                ``[query_params.enforce_aup]`` {bool}: Filter based on whether Acceptable Use Policy (AUP) is enforced.

                ``[query_params.enable_firewall]`` {bool}: Filter based on whether firewall is enabled for a location.

                ``[query_params.location_type]`` {bool}: Filter based on type of location.
                    Supported values: `NONE`, `CORPORATE`, `SERVER`, `GUESTWIFI`, `IOT`, `WORKLOAD`

        Returns:
            :obj:`Tuple`: A list of configured locations.

        Examples:
            List locations with default settings:

            >>> for location in zia.locations.list_locations_lite():
            ...    print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zia.locations.list_locations_lite(max_items=10):
            ...    print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zia.locations.list_locations_lite(page_size=200, max_pages=2):
            ...    print(location)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/lite
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
                result.append(LocationManagement(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_location_groups(self, query_params=None) -> tuple:
        """
        Return a list of location groups in ZIA.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Page size for pagination.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 100, but the maximum size is 1000.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.group_type]`` {str}: The location group's type (i.e., Static or Dynamic).
                ``[query_params.name]`` {str}: The location group's name.
                ``[query_params.last_mod_user]`` {str}: The location group's name.
                ``[query_params.version]`` {int}: The version parameter is for Zscaler internal use only.
                ``[query_params.comments]`` {str}:  Additional comments or information about the location group.
                ``[query_params.location_id]`` {int}:  The unique identifier for a location within a location group.

        Keyword Args:

        Returns:
            :obj:`Tuple`: A list of location group resource records.

        Examples:
            Get a list of all configured location groups:
            >>> location, _, error = zia.locations.list_location_groups()
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/groups
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
                result.append(LocationGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_location_group(self, group_id: int) -> tuple:
        """
        Fetches a specific location group for the specified ID.

        Args:
            group_id (int): The unique identifier for the location group.

        Returns:
            tuple: A tuple containing (Rule Label instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/groups/{group_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LocationGroup)
        if error:
            return (None, response, error)

        try:
            result = LocationGroup(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_location_groups_lite(self, query_params=None) -> tuple:
        """
        Returns a list of location groups (lite version) by their ID where only name and ID is returned in ZIA.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Page size for pagination.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    The default size is 100, but the maximum size is 1000.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Keyword Args:

        Returns:
            :obj:`Tuple`: A list of location group resource records.

        Examples:
            Get a list of all configured location groups:
            >>> location, _, error = zia.locations.list_location_groups_lite()
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/groups/lite
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
                result.append(LocationGroup(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_location_groups_count(self, query_params=None) -> tuple:
        """
        Returns a list of location groups for your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.group_type]`` {str}: The location group's type (i.e., Static or Dynamic).
                ``[query_params.name]`` {str}: The location group's name.
                ``[query_params.last_mod_user]`` {str}: The location group's name.
                ``[query_params.comments]`` {str}:  Additional comments or information about the location group.
                ``[query_params.location_id]`` {int}:  The unique identifier for a location within a location group.

        Keyword Args:

        Returns:
            :obj:`Tuple`: A list of location group resource records.

        Examples:
            Gets the list of location groups for your organization:
            >>> location = zia.locations.list_location_groups_count(group_type='Static', name='Corporate')
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /locations/groups/count
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
            body = response.get_body()
            if isinstance(body, int):
                return (body, response, None)
            elif isinstance(body, str) and body.strip().isdigit():
                return (int(body.strip()), response, None)
            else:
                raise ValueError(f"Unexpected response format: {body}")
        except Exception as error:
            return (None, response, error)

    def list_region_geo_coordinates(self, latitude: float, longitude: float) -> tuple:
        """
        Retrieves the geographical data of the region or city that is located in the specified latitude and longitude
        coordinates. The geographical data includes the city name, state, country, geographical ID of the city and
        state, etc.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            :obj:`tuple`: The geographical data of the region or city that is located in the specified coordinates.

        Examples:
            Get the geographical data of the region or city that is located in the specified coordinates::

                print(zia.locations.get_geo_by_coordinates(37.3860517, -122.0838511))

        """
        # Validate that both latitude and longitude are provided
        if latitude is None or longitude is None:
            return (None, None, ValueError("Both latitude and longitude must be provided"))

        # Define the HTTP method and API endpoint
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /region/byGeoCoordinates
        """
        )

        # Build query parameters with latitude and longitude
        query_params = {"latitude": latitude, "longitude": longitude}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=body, headers=headers, params=query_params
        )

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

    def get_geo_by_ip(self, ip: str) -> tuple:
        """
        Retrieves the geographical data of the region or city that is located in the specified IP address. The
        geographical data includes the city name, state, country, geographical ID of the city and state, etc.

        Args:
            ip (str): The IP address of the location.

        Returns:
            :obj:`tuple`: The geographical data of the region or city that is located in the specified IP address.

        Examples:
            Get the geographical data of the region or city that is located in the specified IP address::

                print(zia.locations.get_geo_by_ip("8.8.8.8"))
        """
        # Validate that IP is provided
        if not ip:
            return (None, None, ValueError("IP address must be provided"))

        # Define the HTTP method and API endpoint
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /region/byIPAddress/{ip}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=body, headers=headers
        )

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

    def list_cities_by_name(self, query_params=None) -> tuple:
        """
        Retrieves the list of cities (along with their geographical data) that match the prefix search.
        The geographical data includes the latitude and longitude coordinates of the city, geographical
        ID of the city and state, country, postal code, etc.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {int}: Specifies the page offset.
                ``[query_params.page_size]`` {int}: Page size for pagination.

                ``[query_params.prefix]`` {str}: Prefix search of the city or region.

                    It can contain names of city, state, country in the following format: city name,
                    state name, country name.

        Returns:
            :obj:`tuple`: A list of dictionaries containing the cities' geographical data and the raw response.

        Examples:
            Get the list of cities (along with their geographical data) that match the prefix search::

                result, response, error = zia.locations.list_cities_by_name(
                    query_params={"prefix": "San Jose"})
                if not error:
                    for city in result:
                        print(city)

        Notes:
            Very broad or generic search terms may return a large number of results which can take a long time to be
            returned. Ensure you narrow your search result as much as possible to avoid this.

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /region/search
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=body, headers=headers, params=query_params
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(self.form_response_body(item))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
