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
from zscaler.zpa.models.application_segment import ApplicationSegments
from zscaler.zpa.app_segment_by_type import ApplicationSegmentByTypeAPI
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
        self.config = config
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

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            tuple: A tuple containing (list of AppSegmentsPRA instances, Response, error)

        Examples:
            >>> segment_list, _, err = client.zpa.app_segments_pra.list_segments_pra(
            ... query_params={'search': 'AppSegmentPRA01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing application segment pra: {err}")
            ...     return
            ... print(f"Total application segment pra found: {len(segment_list)}")
            ... for app in segments:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application
        """
        )

        query_params = query_params or {}
        query_params.update(kwargs)

        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegments)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ApplicationSegments(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_segment_pra(self, segment_id: str, query_params=None) -> tuple:
        """
        Get details of an application segment by its ID.

        Args:
            segment_id (str): The unique ID for the application segment.

        Returns:
            :obj:`Tuple`: A tuple containing (ApplicationSegment, Response, error)

        Examples:
            >>> fetched_segment, _, err = client.zpa.app_segments_pra.get_segment_pra('999999')
            ... if err:
            ...     print(f"Error fetching segment by ID: {err}")
            ...     return
            ... print(f"Fetched segment by ID: {fetched_segment.as_dict()}")
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

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegments)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegments(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_segment_pra(self, **kwargs) -> tuple:
        """
        Create a new Privileged Remote Access (PRA) application segment.

        Args:
            name (str): **Required**. Name of the application segment (user-defined).
            domain_names (list[str]): **Required**. Domain names or IP addresses for the segment.
            segment_group_id (str): **Required**. Unique identifier for the segment group.
            server_group_ids (list[str]): **Required**. List of server group IDs this segment belongs to.
            tcp_port_ranges (list[str], optional): **Legacy format**. TCP port range pairs (e.g., `['22', '22']`).
            udp_port_ranges (list[str], optional): **Legacy format**. UDP port range pairs (e.g., `['35000', '35000']`).
            tcp_port_range (list[dict], optional): **New format**. TCP port range pairs `[{"from": "8081", "to": "8081"}]`.
            udp_port_range (list[dict], optional): **New format**. UDP port range pairs `[{"from": "8081", "to": "8081"}]`.

        Keyword Args:
            bypass_type (str): Bypass type for the segment. Values: `ALWAYS`, `NEVER`, `ON_NET`.
            config_space (str): Config space for the segment. Values: `DEFAULT`, `SIEM`.
            description (str): Additional information about the segment.
            double_encrypt (bool): If true, enables double encryption.
            enabled (bool): If true, enables the application segment.
            health_check_type (str): Health Check Type. Values: `DEFAULT`, `NONE`.
            health_reporting (str): Health Reporting mode. Values: `NONE`, `ON_ACCESS`, `CONTINUOUS`.
            ip_anchored (bool): If true, enables IP Anchoring.
            is_cname_enabled (bool): If true, enables CNAMEs for the segment.
            passive_health_enabled (bool): If true, enables Passive Health Checks.
            icmp_access_type (str): Sets ICMP access type for ZPA clients.
            microtenant_id (str, optional): ID of the microtenant, if applicable.

            common_apps_dto (dict, optional): Dictionary containing application-specific configurations.

                - **apps_config** (list[dict], optional): List of application configuration blocks.

                - **application_port** (str): The port used by the application.
                - **application_protocol** (str): The protocol used (e.g., `RDP`, `SSH`).
                - **connection_security** (str): The security mode for connections.
                    Values: `ANY`, `NLA`, `NLA_EXT`, `TLS`, `VM_CONNECT`, `RDP`.
                - **enabled** (bool): Whether the application is enabled.
                - **domain** (str): The domain name of the application.
                - **name** (str): The name of the application.
                - **app_types** (list[str]): The types of applications is optional (i.e., SECURE_REMOTE_ACCESS).

        Returns:
            tuple: A tuple containing:

                - **ApplicationSegment**: The newly created application segment instance.
                - **Response**: The raw API response object.
                - **Error**: An error message, if applicable.

        Examples:

            Create an application segment using **new TCP port format** (`tcp_port_range`):

            >>> added_segment, _, err = client.zpa.app_segments_pra.add_segment_pra(
            ...     name=f"NewPRASegment_{random.randint(1000, 10000)}",
            ...     description=f"NewPRASegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["rdp_pra01.acme.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "3389", "to": "3389"}],
            ...     udp_port_range=[{"from": "3389", "to": "3389"}],
            ...     common_apps_dto={
            ...         "apps_config": [
            ...             {
            ...                 "application_port": "3389",
            ...                 "application_protocol": "RDP",
            ...                 "connection_security": "ANY",
            ...                 "enabled": True,
            ...                 "domain": "rdp_pra01.acme.com",
            ...                 "name": "rdp_pra01.acme.com",
            ...             }
            ...         ]
            ...     },
            ... )
            >>> if err:
            ...     print(f"Error creating segment: {err}")
            ... else:
            ...     print(f"Segment created successfully: {added_segment.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application
        """
        )

        body = kwargs

        # --- Prevent mixed legacy + structured port range usage ---
        if "tcp_port_ranges" in body and "tcp_port_range" in body:
            return None, None, ValueError("Cannot use both 'tcp_port_ranges' and 'tcp_port_range' in the same request.")

        if "udp_port_ranges" in body and "udp_port_range" in body:
            return None, None, ValueError("Cannot use both 'udp_port_ranges' and 'udp_port_range' in the same request.")

        # Check if microtenant_id is set in kwargs or the body, and use it to set query parameter
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Reformat server_group_ids to match the expected API format (serverGroups)
        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": group_id} for group_id in body.pop("server_group_ids")]

        # Auto-add `"app_types": ["SECURE_REMOTE_ACCESS"]` if missing
        common_apps_dto = kwargs.get("common_apps_dto")
        if common_apps_dto and "apps_config" in common_apps_dto:
            for app_config in common_apps_dto["apps_config"]:
                if "app_types" not in app_config:  # Only add if missing
                    app_config["app_types"] = ["SECURE_REMOTE_ACCESS"]

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

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegments)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegments(self.form_response_body(response.get_body()))
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

        Examples:

           Create an application segment using **new TCP port format** (`tcp_port_range`):

            >>> updated_segment, _, err = client.zpa.app_segments_pra.update_segment_pra(
            ...     segment_id='9999999'
            ...     name=f"UpdatePRASegment_{random.randint(1000, 10000)}",
            ...     description=f"UpdatePRASegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["rdp_pra01.acme.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "3389", "to": "3389"}],
            ...     udp_port_range=[{"from": "3389", "to": "3389"}],
            ...     common_apps_dto={
            ...         "apps_config": [
            ...             {
            ...                 "application_port": "3389",
            ...                 "application_protocol": "RDP",
            ...                 "connection_security": "ANY",
            ...                 "enabled": True,
            ...                 "domain": "rdp_pra01.acme.com",
            ...                 "name": "rdp_pra01.acme.com",
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

        body = kwargs

        # --- Prevent mixed legacy + structured port range usage ---
        if "tcp_port_ranges" in body and "tcp_port_range" in body:
            return None, None, ValueError("Cannot use both 'tcp_port_ranges' and 'tcp_port_range'.")
        if "udp_port_ranges" in body and "udp_port_range" in body:
            return None, None, ValueError("Cannot use both 'udp_port_ranges' and 'udp_port_range'.")

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": gid} for gid in body.pop("server_group_ids")]

        common_apps_dto = kwargs.get("common_apps_dto")
        if common_apps_dto and "apps_config" in common_apps_dto:
            for app_config in common_apps_dto["apps_config"]:
                if "app_types" not in app_config:  # Only add if missing
                    app_config["app_types"] = ["SECURE_REMOTE_ACCESS"]

        # --- Handle apps_config ---
        common_apps_dto = kwargs.get("common_apps_dto")
        if common_apps_dto and "apps_config" in common_apps_dto:
            app_segment_api = ApplicationSegmentByTypeAPI(self._request_executor, self.config)

            segments_list, _, err = app_segment_api.get_segments_by_type(
                application_type="SECURE_REMOTE_ACCESS",
                query_params={"microtenant_id": microtenant_id} if microtenant_id else {}
            )

            if err:
                return None, None, f"Error fetching SECURE_REMOTE_ACCESS segments: {err}"

            # Map: domain -> segment
            existing_apps = {s.domain: s for s in segments_list if s.app_id == segment_id}

            # Assign app_id and pra_app_id
            for app in common_apps_dto["apps_config"]:
                domain = app.get("domain")
                app["app_id"] = segment_id
                if domain in existing_apps:
                    app["pra_app_id"] = existing_apps[domain].id
                else:
                    app["pra_app_id"] = ""  # fallback to empty

            # Compute deleted PRA apps
            desired_domains = {a["domain"] for a in common_apps_dto["apps_config"]}
            deleted_ids = [app.id for domain, app in existing_apps.items() if domain not in desired_domains]
            if deleted_ids:
                common_apps_dto["deleted_pra_apps"] = deleted_ids

            body["commonAppsDto"] = common_apps_dto

        if "tcp_port_ranges" in body:
            body["tcpPortRanges"] = body.pop("tcp_port_ranges")
        else:
            body["tcpPortRanges"] = []

        if "tcp_port_range" in body:
            body["tcpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("tcp_port_range")]
        else:
            body["tcpPortRange"] = []

        if "udp_port_ranges" in body:
            body["udpPortRanges"] = body.pop("udp_port_ranges")
        else:
            body["udpPortRanges"] = []  # Explicitly clear if not provided

        if "udp_port_range" in body:
            body["udpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("udp_port_range")]
        else:
            body["udpPortRange"] = []  # Explicitly clear if not provided

        add_id_groups(self.reformat_params, kwargs, body)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegments)
        if error:
            return (None, response, error)

        if response is None:
            return (ApplicationSegments({"id": segment_id}), None, None)

        try:
            result = ApplicationSegments(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_segment_pra(self, segment_id: str, force_delete: bool = False, microtenant_id: str = None) -> tuple:
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
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
