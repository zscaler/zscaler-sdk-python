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

from typing import Optional
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zcc.models.application_profiles import ApplicationProfile
from zscaler.utils import format_url, zcc_param_mapper
from zscaler.types import APIResult


class ApplicationProfilesAPI(APIClient):

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zcc_base_endpoint = "/zcc/papi/public/v1"

    @zcc_param_mapper
    def get_application_profiles(self, query_params: Optional[dict] = None) -> APIResult[dict]:
        """
        Retrieves the paginated list of application profiles.

        The ``device_type`` filter accepts a friendly OS name (``ios``,
        ``android``, ``windows``, ``macos``, ``linux``); the
        :func:`zscaler.utils.zcc_param_mapper` decorator converts it to the
        numeric ``deviceType`` value the API expects.

        Args:
            query_params (dict, optional): A dictionary containing supported filters.

                ``[query_params.page]`` {str}: Specifies the page offset.

                ``[query_params.page_size]`` {str}: Specifies the page size. The default size is 50.

                ``[query_params.search]`` {str}: The search string used to match against the policies.

                ``[query_params.search_type]`` {str}: The search string used to match against the search type.
                    This is enabled only for filename, name, policyToken, ruleset, or groups.

                ``[query_params.device_type]`` {str}: Friendly device type filter.
                    One of ``ios``, ``android``, ``windows``, ``macos``, ``linux``.

        Returns:
            :obj:`list`: Retrieves the list of application profile policies.

        Examples:
            Prints all application profile policies:

            >>> profile_list, _, err = client.zcc.application_profiles.get_application_profiles()
            >>> if err:
            ...     print(f"Error listing application profiles: {err}")
            ...     return
            ... for profile in profile_list:
            ...     print(profile.as_dict())

            Filter by device type:

            >>> profile_list, _, err = client.zcc.application_profiles.get_application_profiles(
            ...     query_params={"device_type": "android"}
            ... )
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /application-profiles
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
            response_body = response.get_body() or {}
            items = response_body.get("policies", []) or []
            result = [ApplicationProfile(item) for item in items if isinstance(item, dict)]
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_application_profile(self, profile_id: str) -> APIResult[dict]:
        """
        Retrieves the list of policies for application profiles.

        Args:
            profile_id (str): The unique identifier of the application profile.

        Returns:
            :obj:`list`: Retrieves the list of application profile policies.

        Examples:
            Prints all application profile policies:

            >>> profile, _, err = client.zcc.application_profiles.get_application_profile('1234567890')
            >>> if err:
            ...     print(f"Error listing application profile: {err}")
            ...     return
            ... print(profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /application-profiles/{profile_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = ApplicationProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zcc_param_mapper
    def update_application_profile(self, profile_id: str, **kwargs) -> APIResult[dict]:
        """
        Update the properties of the application profile using profile ID.

        Only the following allowlisted properties can be updated. For array
        or comma-separated string values, include existing values along with
        the new values.

        Args:
            profile_id (str): The unique identifier of the application profile.

        Keyword Args:
            packet_tunnel_exclude_list (str): Hosts/IPs excluded from the packet tunnel.
            packet_tunnel_exclude_list_for_ipv6 (str): IPv6 hosts/IPs excluded.
            packet_tunnel_include_list (str): Hosts/IPs included in the packet tunnel.
            packet_tunnel_include_list_for_ipv6 (str): IPv6 hosts/IPs included.
            vpn_gateways (str): VPN gateways list.
            source_port_based_bypasses (str): Source-port based bypass list.
            disable_parallel_ipv4_and_ipv6 (int): Disable parallel IPv4/IPv6.
            dns_priority_ordering_for_trusted_dns_criteria (int): DNS priority order
                for trusted DNS criteria.
            use_default_adapter_for_dns (str): Use default adapter for DNS.
            update_dns_search_order (int): Update DNS search order.
            disable_dns_route_exclusion (int): Disable DNS route exclusion.
            enforce_split_dns (int): Enforce split DNS.
            bypass_dns_traffic_using_udp_proxy (int): Bypass DNS traffic via UDP proxy.
            truncate_large_udpdns_response (int): Truncate large UDP DNS responses.
            prioritize_dns_exclusions (int): Prioritize DNS exclusions.
            packet_tunnel_dns_exclude_list (str): DNS hosts excluded from packet tunnel.
            packet_tunnel_dns_include_list (str): DNS hosts included in packet tunnel.
            dns_priority_ordering (int): DNS priority ordering.
            custom_dns (str): Custom DNS configuration.
            app_service_ids (list[str]): App service IDs.
            bypass_app_ids (list[str]): Bypass app IDs.
            bypass_custom_app_ids (list[str]): Bypass custom app IDs.
            groups (list): Group objects associated with the profile.
            group_all (int): Apply policy to all groups.
            user_ids (list[str]): User IDs associated with the profile.
            logout_password (str): Logout password.
            uninstall_password (str): Uninstall password.
            disable_password (str): Disable password.
            exit_password (str): Exit password.
            zdx_disable_password (str): ZDX disable password.
            zd_disable_password (str): ZD disable password.
            zpa_disable_password (str): ZPA disable password.
            zdp_disable_password (str): ZDP disable password.
            zcc_revert_password (str): ZCC revert password.
            zcc_fail_close_settings_exit_uninstall_password (str): ZCC fail-close
                exit/uninstall password.
            device_type (str): Device type.

        Returns:
            tuple: A tuple containing the Update Application Profile, response, and error.

        Examples:
            Update an existing Application Profile:

            >>> updated_profile, response, error = (
            ...     client.zcc.application_profiles.update_application_profile(
            ...         profile_id='1234567890',
            ...         enforce_split_dns=1,
            ...         custom_dns='8.8.8.8,1.1.1.1',
            ...         bypass_app_ids=['111', '222'],
            ...         group_all=1,
            ...     )
            ... )
            >>> if error:
            ...     print(f"Error updating application profile: {error}")
            ...     return
            ... print(f"Application profile updated successfully: {updated_profile.as_dict()}")
        """
        http_method = "patch".upper()
        api_url = format_url(f"""
            {self._zcc_base_endpoint}
            /application-profiles/{profile_id}
        """)

        body = {}
        body.update(kwargs)

        # The PATCH endpoint requires the body to identify the policy being
        # updated. Always inject policyId derived from the URL parameter so
        # callers cannot omit it by accident.
        try:
            body["policyId"] = int(profile_id)
        except (TypeError, ValueError):
            body["policyId"] = profile_id

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = ApplicationProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
