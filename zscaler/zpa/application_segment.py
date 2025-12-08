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

from typing import List, Optional, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.application_segment import ApplicationSegments
from zscaler.zpa.models.application_segment_lb import WeightedLBConfig
from zscaler.zpa.app_segment_by_type import ApplicationSegmentByTypeAPI
from zscaler.zpa.models.application_segment import MultiMatchUnsupportedReferences
from zscaler.utils import format_url, add_id_groups
import logging

logger = logging.getLogger(__name__)


class ApplicationSegmentAPI(APIClient):
    """
    A client object for the Application Segments resource.
    """

    reformat_params = [
        ("clientless_app_ids", "clientlessApps"),
        ("server_group_ids", "serverGroups"),
    ]

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self.config = config
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_segments(self, query_params: Optional[dict] = None) -> List[ApplicationSegments]:
        """
        Enumerates application segments in your organization with pagination.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[ApplicationSegments]: A list of ApplicationSegment instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     segments = client.zpa.application_segment.list_segments()
            ...     for segment in segments:
            ...         print(segment.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ApplicationSegments)

        return [ApplicationSegments(self.form_response_body(item)) for item in response.get_results()]

    def get_segment(self, segment_id: str, query_params: Optional[dict] = None) -> ApplicationSegments:
        """
        Retrieve an application segment by its ID.

        Args:
            segment_id (str): The unique identifier of the application segment.
            query_params (dict, optional): Map of query parameters.

        Returns:
            ApplicationSegments: The application segment object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     segment = client.zpa.application_segment.get_segment('999999')
            ...     print(segment.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, ApplicationSegments)

        return ApplicationSegments(self.form_response_body(response.get_body()))

    def add_segment(self, **kwargs) -> ApplicationSegments:
        """
        Create a new application segment.

        Args:
            name (str): Name of the application segment.
            domain_names (list): Domain names or IP addresses for the segment.
            segment_group_id (str): Unique identifier for the segment group.
            server_group_ids (list): List of server group IDs.
            tcp_port_ranges (list, optional): Legacy TCP port range pairs.
            tcp_port_range (list, optional): New format TCP port ranges.

        Returns:
            ApplicationSegments: The created application segment.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If conflicting port range formats are used.

        Examples:
            >>> try:
            ...     segment = client.zpa.application_segment.add_segment(
            ...         name="NewSegment",
            ...         domain_names=["test.example.com"],
            ...         segment_group_id="12345",
            ...         server_group_ids=["67890"],
            ...         tcp_port_ranges=["8081", "8081"]
            ...     )
            ...     print(segment.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/application")

        body = kwargs
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": gid} for gid in body.pop("server_group_ids")]

        # Prevent mixed legacy + structured port range usage
        if "tcp_port_ranges" in body and "tcp_port_range" in body:
            raise ValueError("Cannot use both 'tcp_port_ranges' and 'tcp_port_range' in the same request.")
        if "udp_port_ranges" in body and "udp_port_range" in body:
            raise ValueError("Cannot use both 'udp_port_ranges' and 'udp_port_range' in the same request.")

        if "tcp_port_ranges" in body:
            body["tcpPortRanges"] = body.pop("tcp_port_ranges")
        elif "tcp_port_range" in body:
            body["tcpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("tcp_port_range")]

        if "udp_port_ranges" in body:
            body["udpPortRanges"] = body.pop("udp_port_ranges")
        elif "udp_port_range" in body:
            body["udpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("udp_port_range")]

        if "clientless_app_ids" in body:
            body["clientlessApps"] = body.pop("clientless_app_ids")

        add_id_groups(self.reformat_params, kwargs, body)

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, ApplicationSegments)

        return ApplicationSegments(self.form_response_body(response.get_body()))

    def update_segment(self, segment_id: str, **kwargs) -> ApplicationSegments:
        """
        Update an existing application segment.

        Args:
            segment_id (str): The unique identifier of the application segment.
            **kwargs: Fields to update.

        Returns:
            ApplicationSegments: The updated application segment.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If conflicting port range formats are used.

        Examples:
            >>> try:
            ...     segment = client.zpa.application_segment.update_segment(
            ...         "999999",
            ...         name="UpdatedSegment",
            ...         enabled=True
            ...     )
            ...     print(segment.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}")

        body = kwargs

        # Prevent mixed legacy + structured port range usage
        if "tcp_port_ranges" in body and "tcp_port_range" in body:
            raise ValueError("Cannot use both 'tcp_port_ranges' and 'tcp_port_range' in the same request.")
        if "udp_port_ranges" in body and "udp_port_range" in body:
            raise ValueError("Cannot use both 'udp_port_ranges' and 'udp_port_range' in the same request.")

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": gid} for gid in body.pop("server_group_ids")]

        if "clientless_app_ids" in body:
            clientless_apps = body.pop("clientless_app_ids")
            app_segment_api = ApplicationSegmentByTypeAPI(self._request_executor, self.config)
            segments_list = app_segment_api.get_segments_by_type(application_type="BROWSER_ACCESS")
            matched_segment = next((app for app in segments_list if app.get("appId") == segment_id), None)

            if not matched_segment:
                raise ValueError(f"No matching clientless App found with appId '{segment_id}' in existing segments.")

            clientless_app_id = matched_segment["id"]
            body["clientlessApps"] = []
            for app in clientless_apps:
                app["appId"] = segment_id
                app["id"] = clientless_app_id
                body["clientlessApps"].append(app)

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
            body["udpPortRanges"] = []

        if "udp_port_range" in body:
            body["udpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("udp_port_range")]
        else:
            body["udpPortRange"] = []

        add_id_groups(self.reformat_params, kwargs, body)

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, ApplicationSegments)

        if response is None:
            return ApplicationSegments({"id": segment_id})

        return ApplicationSegments(self.form_response_body(response.get_body()))

    def delete_segment(
        self,
        segment_id: str,
        force_delete: bool = False,
        microtenant_id: Optional[str] = None
    ) -> None:
        """
        Deletes the specified Application Segment from ZPA.

        Args:
            segment_id (str): The unique identifier for the Application Segment.
            force_delete (bool): Setting this to true deletes mapping between segment and group.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.application_segment.delete_segment('999999')
            ...     print("Segment deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}
        if force_delete:
            params["forceDelete"] = "true"

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)

    def app_segment_move(self, application_id: str, **kwargs) -> dict:
        """
        Moves application segments from one microtenant to another.

        Args:
            application_id (str): The unique identifier of the Application Segment.
            target_segment_group_id (str): Target segment group ID.
            target_server_group_id (str): Target server group ID.
            target_microtenant_id (str): Target microtenant ID.

        Returns:
            dict: Result of the move operation.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     result = client.zpa.application_segment.app_segment_move(
            ...         '216199618143373016',
            ...         target_segment_group_id='216199618143373010',
            ...         target_server_group_id='216199618143373012',
            ...         target_microtenant_id='216199618143372994'
            ...     )
            ...     print(result)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{application_id}/move")

        payload = {
            "targetSegmentGroupId": kwargs.pop("target_segment_group_id", None),
            "targetMicrotenantId": kwargs.pop("target_microtenant_id", None),
            "targetServerGroupId": kwargs.pop("target_server_group_id", None),
        }

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=payload, params=params
        )
        response = self._request_executor.execute(request)

        if response and response.status_code == 204:
            logger.debug("Move operation completed successfully with 204 No Content.")
            return {"message": "Move operation completed successfully."}

        return response.get_body() if response else {}

    def app_segment_share(self, application_id: str, **kwargs) -> dict:
        """
        Shares the application segment to the Microtenant.

        Args:
            application_id (str): The unique identifier of the Application Segment.
            share_to_microtenants (list): List of microtenant IDs to share to.

        Returns:
            dict: Result of the share operation.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     result = client.zpa.application_segment.app_segment_share(
            ...         '216199618143373016',
            ...         share_to_microtenants=['216199618143373010']
            ...     )
            ...     print(result)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{application_id}/share")

        payload = {"shareToMicrotenants": kwargs.pop("share_to_microtenants", None)}

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=payload, params=params
        )
        response = self._request_executor.execute(request)

        if response and response.status_code == 204:
            logger.debug("Sharing operation completed successfully with 204 No Content.")
            return {"message": "Sharing operation completed successfully."}

        return response.get_body() if response else {}

    def add_segment_provision(self, **kwargs) -> ApplicationSegments:
        """
        Provision a new application segment with all related objects.

        Args:
            name (str): Name of the application segment.
            domain_names (list): List of domain names.
            segment_group_id (str): ID of the segment group.
            server_group_ids (list): List of server group IDs.

        Returns:
            ApplicationSegments: The provisioned application segment.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     segment = client.zpa.application_segment.add_segment_provision(
            ...         name="app02",
            ...         domain_names=["app02.acme.com"],
            ...         server_group_ids=["72058304855116228"]
            ...     )
            ...     print(segment.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/provision")

        body = kwargs
        microtenant_id = kwargs.get("microtenant_id") or body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "server_group_ids" in body:
            body["serverGroups"] = [{"id": gid} for gid in body.pop("server_group_ids")]

        if "tcp_port_ranges" in body:
            body["tcpPortRanges"] = body.pop("tcp_port_ranges")
        elif "tcp_port_range" in body:
            body["tcpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("tcp_port_range")]

        if "udp_port_ranges" in body:
            body["udpPortRanges"] = body.pop("udp_port_ranges")
        elif "udp_port_range" in body:
            body["udpPortRange"] = [{"from": pr["from"], "to": pr["to"]} for pr in body.pop("udp_port_range")]

        if "clientless_app_ids" in body:
            body["clientlessApps"] = body.pop("clientless_app_ids")

        add_id_groups(self.reformat_params, kwargs, body)

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, ApplicationSegments)

        return ApplicationSegments(self.form_response_body(response.get_body()))

    def get_weighted_lb_config(self, segment_id: str, query_params: Optional[dict] = None) -> WeightedLBConfig:
        """
        Get Weighted Load Balancer Config for AppSegment.

        Args:
            segment_id (str): The unique identifier of the application segment.
            query_params (dict, optional): Map of query parameters.

        Returns:
            WeightedLBConfig: The load balancer configuration.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     config = client.zpa.application_segment.get_weighted_lb_config('999999')
            ...     print(config.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}/weightedLbConfig")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, WeightedLBConfig)

        return WeightedLBConfig(self.form_response_body(response.get_body()))

    def update_weighted_lb_config(
        self,
        segment_id: str,
        query_params: Optional[dict] = None,
        **kwargs
    ) -> WeightedLBConfig:
        """
        Updates the Weighted Load Balancing configuration.

        Args:
            segment_id (str): The unique identifier of the Application Segment.
            weighted_load_balancing (bool): Enable/disable weighted load balancing.
            application_to_server_group_mappings (list): List of server group mappings.

        Returns:
            WeightedLBConfig: The updated configuration.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     config = client.zpa.application_segment.update_weighted_lb_config(
            ...         '72058304855090129',
            ...         weighted_load_balancing=True,
            ...         application_to_server_group_mappings=[
            ...             {"id": "72058304855090128", "weight": "10", "passive": True}
            ...         ]
            ...     )
            ...     print(config.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}/weightedLbConfig")

        body = dict(kwargs)

        query_params = query_params.copy() if query_params else {}
        if microtenant_id := query_params.pop("microtenant_id", None):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, body, {}, params=query_params)
        response = self._request_executor.execute(request, WeightedLBConfig)

        if response is None:
            return WeightedLBConfig({"id": segment_id})

        return WeightedLBConfig(self.form_response_body(response.get_body()))

    def bulk_update_multimatch(self, **kwargs) -> Union[MultiMatchUnsupportedReferences, dict]:
        """
        Update multimatch feature in multiple application segments.

        Args:
            application_ids (list): List of application segment IDs.
            match_style (str): The match style ('EXCLUSIVE', 'INCLUSIVE').

        Returns:
            MultiMatchUnsupportedReferences or dict: Result of the update.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     result = client.zpa.application_segment.bulk_update_multimatch(
            ...         application_ids=["216196257331372697"],
            ...         match_style="INCLUSIVE"
            ...     )
            ...     print(result)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/bulkUpdateMultiMatch")

        body = kwargs
        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request)

        if response is None:
            return {"message": "Bulk update multimatch operation completed successfully."}

        return MultiMatchUnsupportedReferences(self.form_response_body(response.get_body()))

    def get_multimatch_unsupported_references(self, domains, **kwargs) -> List[MultiMatchUnsupportedReferences]:
        """
        Get unsupported feature references for multimatch domains.

        Args:
            domains (list): List of domain names to check.

        Returns:
            List[MultiMatchUnsupportedReferences]: List of unsupported references.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     refs = client.zpa.application_segment.get_multimatch_unsupported_references(
            ...         ["app2.securitygeek.io"]
            ...     )
            ...     for ref in refs:
            ...         print(ref.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/multimatchUnsupportedReferences")

        body = domains
        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, MultiMatchUnsupportedReferences)

        return [MultiMatchUnsupportedReferences(self.form_response_body(item)) for item in response.get_results()]

    def get_current_and_max_limit(self) -> dict:
        """
        Get current applications count and maxLimit for the customer.

        Returns:
            dict: Dictionary with currentAppsCount and maxAppsLimit.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     limits = client.zpa.application_segment.get_current_and_max_limit()
            ...     print(f"Current: {limits.get('currentAppsCount')}")
            ...     print(f"Max: {limits.get('maxAppsLimit')}")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/count/currentAndMaxLimit")

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)

        return self.form_response_body(response.get_body())

    def get_application_segment_count(self) -> List[dict]:
        """
        Returns the count of configured application segments.

        Returns:
            List[dict]: List of count records.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     counts = client.zpa.application_segment.get_application_segment_count()
            ...     for count in counts:
            ...         print(count)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/configured/count")

        request = self._request_executor.create_request(http_method, api_url)
        response = self._request_executor.execute(request)

        return [self.form_response_body(item) for item in response.get_results()]

    def get_application_segment_mappings(self, segment_id: str, query_params: Optional[dict] = None) -> List[dict]:
        """
        Get the Application Segment Mapping details.

        Args:
            segment_id (str): The unique identifier of the application segment.
            query_params (dict, optional): Map of query parameters.

        Returns:
            List[dict]: List of mapping dictionaries.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     mappings = client.zpa.application_segment.get_application_segment_mappings('999999')
            ...     for mapping in mappings:
            ...         print(mapping)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/{segment_id}/mappings")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request)

        return [self.form_response_body(item) for item in response.get_results()]

    def application_segment_export(self, query_params: Optional[dict] = None) -> str:
        """
        Export application segments as a CSV document.

        Args:
            query_params (dict, optional): Map of query parameters.

        Returns:
            str: The CSV content as a string.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     csv_content = client.zpa.application_segment.application_segment_export()
            ...     print(csv_content)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/application/export")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        headers = {"Accept": "text/csv"}

        request = self._request_executor.create_request(http_method, api_url, params=query_params, headers=headers)
        response = self._request_executor.execute(request)

        return response.get_body()
