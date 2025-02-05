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
from zscaler.zpa.models.application_segment_pra import ApplicationSegmentPRA
from zscaler.utils import add_id_groups, format_url


class AppSegmentsPRAAPI(APIClient):
    """
    A client object for Application Segments PRA (Privileged Remote Access).
    """

    reformat_params = [
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_segments_pra(self, query_params=None, **kwargs) -> tuple:
        """
        Enumerates application segment pra in your organization with pagination.
        A subset of application segment pra can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {str}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            tuple: A tuple containing (list of AppSegmentsPRA instances, Response, error)
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

        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

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
                result.append(ApplicationSegmentPRA(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_segment_pra(self, segment_id: str, query_params=None) -> tuple:
        """
        Get details of an application segment by its ID.

        Args:
            segment_id (str): The unique ID for the application segment.

        Returns:
            tuple: A tuple containing (ApplicationSegment, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{segment_id}
        """
        )

        query_params = query_params or {}

        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, ApplicationSegmentPRA)
        if error:
            return (None, response, error)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = ApplicationSegmentPRA(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_segment_pra(self, **kwargs) -> tuple:
        """
        Add a new application segment.

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
            tuple: A tuple containing (ApplicationSegment, Response, error)

        Examples:
            Add a new application segment for example.com, ports 8080-8085.

            >>> zpa.app_segments_pra.add_segment('new_app_segment',
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

        # Check if microtenant_id is set in kwargs or the body, and use it to set query parameter
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

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
            .create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, ApplicationSegmentPRA)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegmentPRA(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_segment_pra(self, segment_id: str, **kwargs) -> tuple:
        """
        Update an existing application segment.

        Args:
            segment_id (str): The unique identifier of the application segment.

        Keyword Args:
            microtenant_id (str, optional): ID of the microtenant, if applicable.

        Returns:
            tuple: A tuple containing (ApplicationSegment, Response, error)
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

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

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
            .create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, ApplicationSegmentPRA)
        if error:
            return (None, response, error)

        if response is None:
            return (ApplicationSegmentPRA({"id": segment_id}), None, None)
        
        try:
            result = ApplicationSegmentPRA(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_segment_pra(
        self,
        segment_id: str, 
        force_delete: bool = False, 
        microtenant_id: str = None
    ) -> tuple:
        """
        Delete an PRA application segment.

        Args:
            segment_id (str):
                The unique identifier for the PRA application segment.
            force_delete (bool):
                Setting this field to true deletes the mapping between PRA Application Segment and Segment Group.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

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

        # Handle microtenant_id in URL params if provided
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if force_delete:
            params["forceDelete"] = "true"

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
