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
from zscaler.zpa.models.application_segment import ApplicationSegment
from zscaler.zpa.app_segment_by_type import ApplicationSegmentByTypeAPI
from zscaler.utils import format_url, add_id_groups
import logging

logger = logging.getLogger(__name__)


class ApplicationSegmentAPI(APIClient):
    reformat_params = [
        ("clientless_app_ids", "clientlessApps"),
        ("server_group_ids", "serverGroups"),
    ]
    """
    A client object for the Application Segments resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self.config = config
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_segments(self, query_params=None) -> tuple:
        """
        Enumerates application segments in your organization with pagination.
        A subset of application segments can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of ApplicationSegment instances, Response, error)

        Examples:
            >>> segment_list, _, err = client.zpa.application_segment.list_segments(
            ... query_params={'search': 'AppSegment01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing application segments: {err}")
            ...     return
            ... print(f"Total application segments found: {len(segment_list)}")
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

        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegment)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ApplicationSegment(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_segment(self, segment_id: str, query_params=None) -> tuple:
        """
        Retrieve an application segment by its ID.

        Args:
            segment_id (str): The unique identifier of the application segment.

        Keyword Args:
            microtenant_id (str, optional): ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing the `ApplicationSegment` instance, response object, and error if any.

        Examples:
            >>> fetched_segment, _, err = client.zpa.application_segment.get_segment('999999')
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

        response, error = self._request_executor.execute(request, ApplicationSegment)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegment(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_segment(self, **kwargs) -> tuple:
        """
        Create a new application segment.

        Args:
            name (str): **Required**. Name of the application segment (user-defined).
            domain_names (list of str): **Required**. Domain names or IP addresses for the segment.
            segment_group_id (str): **Required**. Unique identifier for the segment group.
            server_group_ids (list of str): **Required**. List of server group IDs this segment belongs to.
            tcp_port_ranges (list of str, optional): **Legacy format**. TCP port range pairs (e.g., `['22', '22']`).
            udp_port_ranges (list of str, optional): **Legacy format**. UDP port range pairs (e.g., `['35000', '35000']`).
            tcp_port_range (list of dict, optional): **New format**. TCP port range pairs `[{"from": "8081", "to": "8081"}]`.
            udp_port_range (list of dict, optional): **New format**. UDP port range pairs `[{"from": "8081", "to": "8081"}]`.

        Keyword Args:
            bypass_type (str): Bypass type for the segment. Values: `ALWAYS`, `NEVER`, `ON_NET`.
            clientless_app_ids (list): IDs for associated clientless apps.
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

        Returns:
            :obj:`Tuple`: A tuple containing the `ApplicationSegment` instance, response object, and error if any.

        Examples:

            Create an application segment using **legacy TCP port format** (`tcp_port_ranges`):

            >>> added_segment, _, err = client.zpa.application_segment.add_segment(
            ...     name=f"NewAppSegment_{random.randint(1000, 10000)}",
            ...     description=f"NewAppSegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["test.example.com", "test1.example.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_ranges=["8081", "8081"],
            ... )
            ... if err:
            ...     print(f"Error creating segment: {err}")
            ...     return
            ... print(f"segment created successfully: {added_segment.as_dict()}")

           Create an application segment using **new TCP port format** (`tcp_port_range`):

            >>> added_segment, _, err = client.zpa.application_segment.add_segment(
            ...     name=f"NewAppSegment_{random.randint(1000, 10000)}",
            ...     description=f"NewAppSegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["test.example.com", "test1.example.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "8081", "to": "8081"}],  # Single port range using 'from' and 'to'
            ... )
            ... if err:
            ...     print(f"Error creating segment: {err}")
            ...     return
            ... print(f"segment created successfully: {added_segment.as_dict()}")

           Create an Browser Access application segment:

            >>> added_segment, _, err = client.zpa.application_segment.add_segment(
            ...     name=f"NewAppSegment_{random.randint(1000, 10000)}",
            ...     description=f"NewAppSegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["test.example.com", "test1.example.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "8081", "to": "8081"}],
            ...     clientless_app_ids=[
            ...         {
            ...             "name": "jenkins.securitygeek.io",
            ...             "enabled": True,
            ...             "certificate_id": "72058304855021564",
            ...             "application_port": "4443",
            ...             "application_protocol": "HTTPS",
            ...             "domain": "jenkins.securitygeek.io",
            ...         }
            ...     ]
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

        # Check if microtenant_id is set in kwargs or the body, and use it to set query parameter
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Reformat server_group_ids to match the expected API format (serverGroups)
        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": group_id} for group_id in body.pop("server_group_ids")]

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

        # Convert clientless_app_ids to clientlessApps if present
        if "clientless_app_ids" in body:
            body["clientlessApps"] = body.pop("clientless_app_ids")

        # Apply add_id_groups to reformat params based on self.reformat_params
        add_id_groups(self.reformat_params, kwargs, body)

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ApplicationSegment)
        if error:
            return (None, response, error)

        try:
            result = ApplicationSegment(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_segment(self, segment_id: str, **kwargs) -> tuple:
        """
        Update an existing application segment.

        Args:
            segment_id (str): The unique identifier of the application segment.

        Keyword Args:
            microtenant_id (str, optional): ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing the updated `ApplicationSegment` instance, response object, and error if any.

        Examples:

            Update an application segment using **legacy TCP port format** (`tcp_port_ranges`):

            >>> update_segment, _, err = client.zpa.application_segment.add_segment(
            ...     name=f"UpdateAppSegment_{random.randint(1000, 10000)}",
            ...     description=f"UpdateAppSegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["test.example.com", "test1.example.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_ranges=["8081", "8081"],
            ... )
            ... if err:
            ...     print(f"Error updating segment: {err}")
            ...     return
            ... print(f"segment updated successfully: {update_segment.as_dict()}")

            Update an application segment using **new TCP port format** (`tcp_port_range`):

            >>> update_segment, _, err = client.zpa.application_segment.add_segment(
            ...     name=f"UpdateAppSegment_{random.randint(1000, 10000)}",
            ...     description=f"UpdateAppSegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["test.example.com", "test1.example.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "8081", "to": "8081"}],
            ... )
            ... if err:
            ...     print(f"Error updating segment: {err}")
            ...     return
            ... print(f"segment updated successfully: {update_segment.as_dict()}")

            Update an Browser Access application segment

            >>> update_segment, _, err = client.zpa.application_segment.add_segment(
            ...     segment_id='99999',
            ...     name=f"UpdateAppSegment_{random.randint(1000, 10000)}",
            ...     description=f"UpdateAppSegment_{random.randint(1000, 10000)}",
            ...     enabled=True,
            ...     domain_names=["test.example.com", "test1.example.com"],
            ...     segment_group_id="72058304855089379",
            ...     server_group_ids=["72058304855090128"],
            ...     tcp_port_range=[{"from": "8081", "to": "8081"}],
            ...     clientless_app_ids=[
                        {
                            "name": "jenkins.securitygeek.io",
                            "enabled": True,
                            "certificate_id": "72058304855021564",
                            "application_port": "4443",
                            "application_protocol": "HTTPS",
                            "domain": "jenkins.securitygeek.io",
                        }
                    ]
            ... )
            ... if err:
            ...     print(f"Error updating segment: {err}")
            ...     return
            ... print(f"segment updated successfully: {update_segment.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}")

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Reformat server_group_ids to match the expected API format (serverGroups)
        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": group_id} for group_id in body.pop("server_group_ids")]

        # Step 1: Fetch BROWSER_ACCESS apps for `clientless_app_ids`
        if "clientless_app_ids" in body:
            clientless_apps = body.pop("clientless_app_ids")

            # Instantiate ApplicationSegmentByTypeAPI to fetch data
            app_segment_api = ApplicationSegmentByTypeAPI(self._request_executor, self.config)

            # Fetch all `BROWSER_ACCESS` apps
            segments_list, _, err = app_segment_api.get_segments_by_type(application_type="BROWSER_ACCESS")

            if err:
                return (None, None, f"Error fetching application segment data: {err}")

            # Step 2: Find the correct entry where `appId == segment_id`
            matched_segment = next((app for app in segments_list if app.get("appId") == segment_id), None)

            if not matched_segment:
                return (None, None, f"Error: No matching clientless App found with appId '{segment_id}' in existing segments.")

            clientless_app_id = matched_segment["id"]  # Extract correct `id`

            # Step 3: Assign `appId` and `id`
            body["clientlessApps"] = []
            for app in clientless_apps:
                app["appId"] = segment_id  # Auto-assign appId (segment_id)
                app["id"] = clientless_app_id  # Auto-assign id from API response

                body["clientlessApps"].append(app)  # Append updated app config

        # Process TCP and UDP port attributes
        if "tcp_port_ranges" in body:
            body["tcpPortRanges"] = body.pop("tcp_port_ranges")
        elif "tcp_port_range" in body:
            body["tcpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("tcp_port_range")]

        if "udp_port_ranges" in body:
            body["udpPortRanges"] = body.pop("udp_port_ranges")
        elif "udp_port_range" in body:
            body["udpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("udp_port_range")]

        add_id_groups(self.reformat_params, kwargs, body)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ApplicationSegment)
        if error:
            return (None, response, error)

        if response is None:
            return (ApplicationSegment({"id": segment_id}), None, None)

        try:
            result = ApplicationSegment(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_segment(self, segment_id: str, force_delete: bool = False, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified Application Segment from ZPA.

        Args:
            segment_id (str): The unique identifier for the Application Segment.
            force_delete (bool):
                Setting this field to true deletes the mapping between Application Segment and Segment Group.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            tuple: A tuple containing the response and error (if any).

        Examples:
            >>> _, _, err = client.zpa.application_segment.delete_segment(
            ...     segment_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting application segment: {err}")
            ...     return
            ... print(f"Application segment with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{segment_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if force_delete:
            params["forceDelete"] = "true"

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    def app_segment_move(self, application_id: str, **kwargs) -> tuple:
        """
        Moves application segments from one microtenant to another
        Note: Application segments can only be moved from a Default Microtenant microtenant_id as 0 to a child tenant

        Args:
            application_id (str):
                The unique identifier of the Application Segment.
            target_segment_group_id (str):
                The unique identifier of the target segment group that the application segment is being moved to.
            target_server_group_id (str):
                The unique identifier of the target server group that the application segment is being moved to.
            target_microtenant_id (str):
                The unique identifier of the Microtenant that the application segment is being moved to.

        Keyword Args:
            ...

        Returns:
            :obj:`Tuple`: The resource record for the moved application segment.

        Examples:
            Moving an application segment to another microtenant:

            >>> zpa.app_segments.app_segment_move(
            ...    application_id='216199618143373016',
            ...    target_segment_group_id='216199618143373010',
            ...    target_server_group_id='216199618143373012',
            ...    target_microtenant_id='216199618143372994'
            ... )

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{application_id}/move
        """
        )

        payload = {
            "targetSegmentGroupId": kwargs.pop("target_segment_group_id", None),
            "targetMicrotenantId": kwargs.pop("target_microtenant_id", None),
            "targetServerGroupId": kwargs.pop("target_server_group_id", None),
        }

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=payload, params=params
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        if response and response.status_code == 204:
            logger.debug("Move operation completed successfully with 204 No Content.")
            return ({"message": "Move operation completed successfully."}, response, None)

        try:
            result = response.get_body() if response else {}
        except Exception as error:
            logger.debug(f"Error retrieving response body: {error}")
            return (None, response, error)

        return (result, response, None)

    def app_segment_share(self, application_id: str, **kwargs) -> tuple:
        """
        Moves application segments from one microtenant to another
        Note: Application segments can only be shared between child tenants.

        Args:
            application_id (str):
                The unique identifier of the Application Segment.
            share_to_microtenants (:obj:`list` of :obj:`str`):
                The unique identifier of the Microtenant that the application segment is being shared to.
                This field is required if you want to share an application segment.
                To remove the share send the attribute as an empty list.
        Keyword Args:
            ...

        Returns:
            :obj:`Tuple`: An empty Box object if the operation is successful.

        Examples:
            Moving an application segment to another microtenant:

            >>> zpa.app_segments.app_segment_share(
            ...    application_id='216199618143373016',
            ...    share_to_microtenants=['216199618143373010']
            ... )

        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /application/{application_id}/share
        """
        )

        payload = {
            "shareToMicrotenants": kwargs.pop("share_to_microtenants", None),
        }

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=payload, params=params
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        if response and response.status_code == 204:
            logger.debug("Sharing operation completed successfully with 204 No Content.")
            return ({"message": "Shareing operation completed successfully."}, response, None)

        try:
            result = response.get_body() if response else {}
        except Exception as error:
            logger.debug(f"Error retrieving response body: {error}")
            return (None, response, error)

        return (result, response, None)
