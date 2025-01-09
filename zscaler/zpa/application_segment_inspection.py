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
from zscaler.zpa.models.application_segment_inspection import ApplicationSegmentInspection
from zscaler.utils import add_id_groups, format_url


class AppSegmentsInspectionAPI(APIClient):
    """
    A client object for the Application Segment Inspection resource.
    """

    reformat_params = [
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_segment_inspection(self, query_params=None, **kwargs) -> tuple:
        """
        Returns all configured application segment inspection with pagination support.

        Keyword Args:
            max_items (int): The maximum number of items to request before stopping iteration.
            max_pages (int): The maximum number of pages to request before stopping iteration.
            pagesize (int): Specifies the page size. The default size is 20, but the maximum size is 500.
            search (str, optional): The search string used to match against features and fields.

        Returns:
            tuple: A tuple containing a list of `AppSegmentsInspection` instances, response object, and error if any.
        Examples:
            >>> app_segments = zpa.app_segments_inspection.list_segments_inspection()

        """
        # Initialize URL and HTTP method
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application
        """
        )

        # Handle optional query parameters
        query_params = query_params or {}
        query_params.update(kwargs)

        # Prepare request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body={}, headers={}, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ApplicationSegmentInspection(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_segment_inspection(self, segment_id: str, query_params: dict = None) -> tuple:
        """
        Get information for an AppProtection application segment.

        Args:
            segment_id (str):
                The unique identifier for the AppProtection application segment.

        Returns:
            :obj:`tuple`: The AppProtection application segment resource record.

        Examples:
            >>> app_segment = zpa.app_segments_inspection.details('99999')

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{segment_id}
        """
        )

        query_params = query_params or {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, ApplicationSegmentInspection)
        if error:
            return (None, response, error)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = ApplicationSegmentInspection(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_segment_inspection(self, **kwargs) -> tuple:
        """
        Create an AppProtection application segment.

        Args:
            segment_group_id (str):
                The unique identifer for the segment group this application segment belongs to.
            udp_ports (:obj:`list` of :obj:`str`):
                List of udp port range pairs, e.g. ['35000', '35000'] for port 35000.
            tcp_ports (:obj:`list` of :obj:`str`):
                List of tcp port range pairs, e.g. ['22', '22'] for port 22-22, ['80', '100'] for 80-100.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the application segment.
            name (str):
                The name of the application segment.
            server_group_ids (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this application segment.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            bypass_type (str):
                The type of bypass for the Application Segment. Accepted values are `ALWAYS`, `NEVER` and `ON_NET`.
            config_space (str):
                The config space for this Application Segment. Accepted values are `DEFAULT` and `SIEM`.
            default_idle_timeout (int):
                The Default Idle Timeout for the Application Segment.
            default_max_age (int):
                The Default Max Age for the Application Segment.
            description (str):
                Additional information about this Application Segment.
            double_encrypt (bool):
                Double Encrypt the Application Segment micro-tunnel.
            enabled (bool):
                Enable the Application Segment.
            health_check_type (str):
                Set the Health Check Type. Accepted values are `DEFAULT` and `NONE`.
            health_reporting (str):
                Set the Health Reporting. Accepted values are `NONE`, `ON_ACCESS` and `CONTINUOUS`.
            ip_anchored (bool):
                Enable IP Anchoring for this Application Segment.
            is_cname_enabled (bool):
                Enable CNAMEs for this Application Segment.
            passive_health_enabled (bool):
                Enable Passive Health Checks for this Application Segment.
            icmp_access_type (str): Sets ICMP access type for ZPA clients.

        Returns:
            :obj:`tuple`: The newly created application segment resource record.

        Examples:
            Add a new AppProtection application segment for example.com, ports 8080-8085.

            >>> zpa.app_segments_inspection.add_segment_inspection('new_app_segment',
            ...    domain_names=['example.com'],
            ...    segment_group_id='99999',
            ...    tcp_ports=['8080', '8085'],
            ...    server_group_ids=['99999', '88888'])

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Reformat server_group_ids to match the expected API format (serverGroups)
        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": group_id} for group_id in body.pop("server_group_ids")]

        # Add common_apps_dto if provided
        common_apps_dto = kwargs.get("common_apps_dto")
        if common_apps_dto:
            body["commonAppsDto"] = common_apps_dto

        # Process TCP and UDP port attributes
        if "tcp_port_ranges" in body:
            # Use format 1 (tcpPortRanges)
            body["tcpPortRanges"] = body.pop("tcp_port_ranges")
        elif "tcp_port_range" in body:
            # Use format 2 (tcpPortRange)
            body["tcpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("tcp_port_range")]

        if "udp_port_ranges" in body:
            # Use format 1 (udpPortRanges)
            body["udpPortRanges"] = body.pop("udp_port_ranges")
        elif "udp_port_range" in body:
            # Use format 2 (udpPortRange)
            body["udpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("udp_port_range")]

        # Apply add_id_groups to reformat params based on self.reformat_params
        add_id_groups(self.reformat_params, kwargs, body)

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, ApplicationSegmentInspection)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegmentInspection(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_segment_inspection(self, segment_id: str, **kwargs) -> tuple:
        """
        Update an AppProtection application segment.

        Args:
            segment_id (str):
                The unique identifier for the AppProtection application segment.
            **kwargs:
                Optional params.

        Keyword Args:
            bypass_type (str): Bypass type for the segment. Values: `ALWAYS`, `NEVER`, `ON_NET`.
            config_space (str): Config space for the segment. Values: `DEFAULT`, `SIEM`.
            default_idle_timeout (int):
                The Default Idle Timeout for the AppProtection Application Segment.
            default_max_age (int):
                The Default Max Age for the AppProtection Application Segment.
            description (str):
                Additional information about this AppProtection Application Segment.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the AppProtection application segment.
            double_encrypt (bool):
                Double Encrypt the AppProtection Application Segment micro-tunnel.
            enabled (bool):
                Enable the AppProtection Application Segment.
            health_check_type (str):
                Set the Health Check Type. Accepted values are `DEFAULT` and `NONE`.
            health_reporting (str):
                Set the Health Reporting. Accepted values are `NONE`, `ON_ACCESS` and `CONTINUOUS`.
            ip_anchored (bool):
                Enable IP Anchoring for this AppProtection Application Segment.
            is_cname_enabled (bool):
                Enable CNAMEs for this AppProtection Application Segment.
            name (str):
                The name of the AppProtection Application Segment.
            passive_health_enabled (bool):
                Enable Passive Health Checks for this AppProtection Application Segment.
            segment_group_id (str):
                The unique identifer for the segment group this AppProtection application segment belongs to.
            server_group_ids (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this AppProtection application segment.
            tcp_ports (:obj:`list` of :obj:`tuple`):
                List of TCP port ranges specified as a tuple pair, e.g. for ports 21-23, 8080-8085 and 443:
                     [(21, 23), (8080, 8085), (443, 443)]
            udp_ports (:obj:`list` of :obj:`tuple`):
                List of UDP port ranges specified as a tuple pair, e.g. for ports 34000-35000 and 36000:
                     [(34000, 35000), (36000, 36000)]
            icmp_access_type (str): Sets ICMP access type for ZPA clients.

        Returns:
            :obj:`tuple`: The updated AppProtection application segment resource record.

        Examples:
            Rename the application segment for example.com.

            >>> zpa.app_segments_inspection.update('99999',
            ...    name='new_app_name',

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{segment_id}
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Reformat server_group_ids to match the expected API format (serverGroups)
        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": group_id} for group_id in body.pop("server_group_ids")]

        # Add common_apps_dto if provided
        common_apps_dto = kwargs.get("common_apps_dto")
        if common_apps_dto:
            body["commonAppsDto"] = common_apps_dto

        # Process TCP and UDP port attributes
        if "tcp_port_ranges" in body:
            # Use format 1 (tcpPortRanges)
            body["tcpPortRanges"] = body.pop("tcp_port_ranges")
        elif "tcp_port_range" in body:
            # Use format 2 (tcpPortRange)
            body["tcpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("tcp_port_range")]

        if "udp_port_ranges" in body:
            # Use format 1 (udpPortRanges)
            body["udpPortRanges"] = body.pop("udp_port_ranges")
        elif "udp_port_range" in body:
            # Use format 2 (udpPortRange)
            body["udpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("udp_port_range")]

        # Apply add_id_groups to reformat params based on self.reformat_params
        add_id_groups(self.reformat_params, kwargs, body)

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, ApplicationSegmentInspection)
        if error:
            return (None, response, error)

        if response is None:
            return (ApplicationSegmentInspection({"id": segment_id}), None, None)

        try:
            result = ApplicationSegmentInspection(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_segment_inspection(self, segment_id: str, force_delete: bool = False) -> int:
        """
        Delete an AppProtection application segment.

        Args:
            force_delete (bool):
                Setting this field to true deletes the mapping between AppProtection Application Segment and Segment Group.
            segment_id (str):
                The unique identifier for the AppProtection application segment.

        Returns:
            :obj:`int`: The operation response code.

        Examples:
            Delete an AppProtection Application Segment with an id of 99999.

            >>> zpa.app_segments_inspection.delete('99999')

            Force deletion of an AppProtection Application Segment with an id of 88888.

            >>> zpa.app_segments_inspection.delete('88888', force_delete=True)

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{segment_id}
        """
        )

        # Initialize params and add forceDelete if needed
        params = {}
        if force_delete:
            params["forceDelete"] = "true"

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
