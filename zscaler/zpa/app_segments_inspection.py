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
from zscaler.zpa.app_segment_by_type import ApplicationSegmentByTypeAPI
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
        self.config = config
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

        query_params = query_params or {}
        query_params.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ApplicationSegmentInspection(self.form_response_body(item)))
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

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegmentInspection)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegmentInspection(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_segment_inspection(self, **kwargs) -> tuple:
        """
        Create an AppProtection application segment.

        Args:
            name (str): **Required**. Name of the application segment (user-defined).
            domain_names (list of str): **Required**. Domain names or IP addresses for the segment.
            segment_group_id (str): **Required**. Unique identifier for the segment group.
            server_group_ids (list of str): **Required**. List of server group IDs this segment belongs to.
            tcp_port_ranges (list of str, optional): **Legacy format**. TCP port range pairs (e.g., `['22', '22']`).
            udp_port_ranges (list of str, optional): **Legacy format**. UDP port range pairs (e.g., `['35000', '35000']`).
            tcp_port_range (list of dict, optional): **New format**. TCP port range pairs `[{"from": "8081", "to": "8081"}]`.
            udp_port_range (list of dict, optional): **New format**. UDP port range pairs `[{"from": "8081", "to": "8081"}]`.
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

            common_apps_dto (dict, optional): Dictionary containing application-specific configurations.

                - **apps_config** (list[dict], optional): List of application configuration blocks.

                - **application_port** (str): The port used by the application.
                - **application_protocol** (str): The protocol used (e.g., `HTTP`, `HTTPS`).
                - **enabled** (bool): Whether the application is enabled.
                - **domain** (str): The domain name of the application.
                - **name** (str): The name of the application.

        Returns:
            :obj:`tuple`: The newly created application segment resource record.

        Examples:

           Create an application segment using **new TCP port format** (`tcp_port_range`):

            >>> added_segment, _, err = client.zpa.app_segments_pra.add_segment_pra(
            ...     name=f"NewInspectionSegment_{random.randint(1000, 10000)}",
            ...     description=f"NewInspectionSegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["server.acme.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "443", "to": "443"}],
            ...     udp_port_range=[{"from": "443", "to": "443"}],
            ...     common_apps_dto={
            ...         "apps_config": [
            ...             {
            ...                 "application_port": "443",
            ...                 "application_protocol": "HTTPS",
            ...                 "certificate_id": "72058304855021564",
            ...                 "enabled": True,
            ...                 "domain": "server.acme.com",
            ...                 "name": "server.acme.com",
            ...             }
            ...         ]
            ...     },
            ... )
            ... if err:
            ...     print(f"Error creating segment: {err}")
            ...     return
            ... print(f"segment created successfully: {added_segment.as_dict()}")
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

        # Auto-add `"app_types": ["SECURE_REMOTE_ACCESS"]` if missing
        common_apps_dto = kwargs.get("common_apps_dto")
        if common_apps_dto and "apps_config" in common_apps_dto:
            for app_config in common_apps_dto["apps_config"]:
                if "app_types" not in app_config:  # Only add if missing
                    app_config["app_types"] = ["INSPECT"]

        body["commonAppsDto"] = common_apps_dto  # Update the request payload

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
        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ApplicationSegmentInspection)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegmentInspection(self.form_response_body(response.get_body()))
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

            common_apps_dto (dict, optional): Dictionary containing application-specific configurations.

                - **apps_config** (list[dict], optional): List of application configuration blocks.

                - **application_port** (str): The port used by the application.
                - **application_protocol** (str): The protocol used (e.g., `HTTP`, `HTTPS`).
                - **enabled** (bool): Whether the application is enabled.
                - **domain** (str): The domain name of the application.
                - **name** (str): The name of the application.

        Returns:
            :obj:`tuple`: The updated AppProtection application segment resource record.

        Examples:

           Update an app protection segment using **new TCP port format** (`tcp_port_range`):

            >>> updated_segment, _, err = client.zpa.app_segments_inspection.update_segment_inspection(
            ...     segment_id='9999999'
            ...     name=f"UpdatedAppSegmentInspection_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedAppSegmentInspection_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["server.acme.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "443", "to": "443"}],
            ...     udp_port_range=[{"from": "443", "to": "443"}],
            ...     common_apps_dto={
            ...         "apps_config": [
            ...             {
            ...                 "application_port": "443",
            ...                 "application_protocol": "HTTPS",
            ...                 "certificate_id": "72058304855021564",
            ...                 "enabled": True,
            ...                 "domain": "server.acme.com",
            ...                 "name": "server.acme.com",
            ...             }
            ...         ]
            ...     },
            ... )
            ... if err:
            ...     print(f"Error updating segment: {err}")
            ...     return
            ... print(f"segment updated successfully: {updated_segment.as_dict()}")

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

        # Ensure `app_types` is set in `commonAppsDto.apps_config`
        common_apps_dto = kwargs.get("common_apps_dto")
        if common_apps_dto and "apps_config" in common_apps_dto:
            for app_config in common_apps_dto["apps_config"]:
                if "app_types" not in app_config:  # Only set if missing
                    app_config["app_types"] = ["INSPECT"]

            body["commonAppsDto"] = common_apps_dto  # Update the request payload

        # Fetch Secure Remote Access apps (same logic as before)
        if common_apps_dto and "apps_config" in common_apps_dto:
            app_segment_api = ApplicationSegmentByTypeAPI(self._request_executor, self.config)

            # Fetch all INSPECT apps (no filtering, so we get everything)
            segments_list, _, err = app_segment_api.get_segments_by_type(application_type="INSPECT", query_params={})

            if err:
                return (None, None, f"Error fetching application segment data: {err}")

            # Step 2: Find the correct entry where `appId == segment_id`
            matched_segment = next((app for app in segments_list if app.app_id == segment_id), None)

            if not matched_segment:
                return (None, None, f"Error: No matching Inspetion App found with appId '{segment_id}' in existing segments.")

            inspect_app_id = matched_segment.id

            # Step 3: Assign `appId` and `inspectAppId`
            for app_config in common_apps_dto["apps_config"]:
                app_config["app_id"] = segment_id  # Auto-assign appId (segment_id)
                app_config["inspect_app_id"] = inspect_app_id  # Auto-assign inspectAppId

            body["commonAppsDto"] = common_apps_dto  # Update the request payload

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

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegmentInspection)
        if error:
            return (None, response, error)

        if response is None:
            return (ApplicationSegmentInspection({"id": segment_id}), None, None)

        try:
            result = ApplicationSegmentInspection(self.form_response_body(response.get_body()))
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
            >>> _, _, err = client.zpa.app_segments_inspection.delete_segment_inspection(
            ...     segment_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting application segment: {err}")
            ...     return
            ... print(f"application segment with ID {'999999'} deleted successfully.")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{segment_id}
        """
        )

        params = {}
        if force_delete:
            params["forceDelete"] = "true"

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
