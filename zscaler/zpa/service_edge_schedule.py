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

import os
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.service_edge_schedule import ServiceEdgeSchedule
from zscaler.utils import format_url


class ServiceEdgeScheduleAPI(APIClient):
    """
    A Client object for the Service Edge Schedule resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        # Attempt to fetch customer_id from config, else fallback to environment variable
        self.customer_id = config["client"].get("customerId") or os.getenv("ZPA_CUSTOMER_ID")
        if not self.customer_id:
            raise ValueError("customer_id is required either in the config or as an environment variable ZPA_CUSTOMER_ID")

        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{self.customer_id}"

    def get_service_edge_schedule(self, customer_id=None) -> tuple:
        """
        Returns the configured Service Edge Schedule frequency.

        Args:
            customer_id (str, optional): Unique identifier of the ZPA tenant. If not provided, will look up from env var.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (ServiceEdgeSchedule, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serviceEdgeSchedule
        """
        )

        # Use passed customer_id or fallback to initialized customer_id
        customer_id = customer_id or self.customer_id

        # Check if microtenant_id exists in env vars (optional)
        microtenant_id = os.getenv("ZPA_MICROTENANT_ID", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request with headers
        request, error = self._request_executor.create_request(http_method, api_url, body=None, headers={}, params=params)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            # Expect a single object, not a list
            result = ServiceEdgeSchedule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_service_edge_schedule(self, schedule) -> tuple:
        """
        Configure an Service Edge schedule frequency to delete inactive connectors based on the configured frequency.

        Args:
            schedule (dict): Dictionary containing:
                ``frequency`` (str): Frequency at which disconnected Service Edges are deleted.
                ``interval`` (str): Interval for the frequency value.
                ``disabled`` (bool, optional): Whether to include disconnected connectors for deletion.
                ``enabled`` (bool, optional): Whether the deletion setting is enabled.
                ``microtenant_id`` (str): The unique identifier of the Microtenant for the ZPA tenant.
        Returns:
            tuple: A tuple containing (ServiceEdgeSchedule, Response, error)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serviceEdgeSchedule
        """
        )

        customer_id = schedule.get("customer_id") or os.getenv("ZPA_CUSTOMER_ID")
        if not customer_id:
            return (
                None,
                None,
                ValueError(
                    "customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID"
                ),
            )

        # Ensure schedule is a dictionary
        body = schedule if isinstance(schedule, dict) else schedule.as_dict()

        # Construct payload using snake_case to camelCase conversion
        payload = {
            "customerId": customer_id,
            "frequency": body.get("frequency"),
            "frequencyInterval": body.get("frequency_interval"),
        }
        if "delete_disabled" in body:
            payload["deleteDisabled"] = body["delete_disabled"]
        if "enabled" in body:
            payload["enabled"] = body["enabled"]

        # Add microtenant_id to query parameters if set
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ServiceEdgeSchedule)
        if error:
            return (None, response, error)

        try:
            result = ServiceEdgeSchedule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_service_edge_schedule(self, scheduler_id: str, schedule) -> tuple:
        """
        Updates Service Edge schedule frequency to delete inactive connectors based on the configured frequency.

        Args:
            **scheduler_id (str): Unique identifier for the schedule.
            **frequency (str): Frequency at which disconnected Service Edges are deleted.
            **interval (str): Interval for the frequency value.
            **disabled (bool): Whether to include disconnected connectors for deletion.
            **enabled (bool): Whether the deletion setting is enabled.
            **microtenant_id (str): The unique identifier of the Microtenant for the ZPA tenant.

        Returns:
            tuple: A tuple containing (ServiceEdgeSchedule, Response, error)
        """

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /serviceEdgeSchedule/{scheduler_id}
        """
        )

        customer_id = schedule.get("customer_id") or os.getenv("ZPA_CUSTOMER_ID")
        if not customer_id:
            return (
                None,
                None,
                ValueError(
                    "customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID"
                ),
            )

        # Ensure schedule is a dictionary format
        body = schedule if isinstance(schedule, dict) else schedule.as_dict()

        # Construct payload using snake_case to camelCase conversion
        payload = {
            "customerId": customer_id,
            "frequency": body.get("frequency"),
            "frequencyInterval": body.get("frequency_interval"),
        }
        if "delete_disabled" in body:
            payload["deleteDisabled"] = body["delete_disabled"]
        if "enabled" in body:
            payload["enabled"] = body["enabled"]

        # Use get instead of pop to keep microtenant_id in the body
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, ServiceEdgeSchedule)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (ServiceEdgeSchedule({"id": scheduler_id}), None, None)

        # Parse the response into an AppConnectorGroup instance
        try:
            result = ServiceEdgeSchedule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
