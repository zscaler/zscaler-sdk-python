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
import os
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.app_connector_schedule import AppConnectorSchedule
from zscaler.utils import format_url


class AppConnectorScheduleAPI(APIClient):
    """
    A Client object for the App Connector Schedule resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self.customer_id = config["client"].get("customerId") or os.getenv("ZPA_CUSTOMER_ID")
        if not self.customer_id:
            raise ValueError("customer_id is required either in the config or as an environment variable ZPA_CUSTOMER_ID")

        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{self.customer_id}"

    def get_connector_schedule(self, customer_id: str = None) -> AppConnectorSchedule:
        """
        Returns the configured App Connector Schedule frequency.

        Args:
            customer_id (str, optional): Unique identifier of the ZPA tenant.

        Returns:
            AppConnectorSchedule: The schedule configuration.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     schedule = client.zpa.app_connector_schedule.get_connector_schedule()
            ...     print(schedule.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/connectorSchedule")

        customer_id = customer_id or self.customer_id
        microtenant_id = os.getenv("ZPA_MICROTENANT_ID")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=None, headers={}, params=params)
        response = self._request_executor.execute(request)

        return AppConnectorSchedule(self.form_response_body(response.get_body()))

    def add_connector_schedule(self, **kwargs) -> AppConnectorSchedule:
        """
        Configure an App Connector schedule frequency.

        Args:
            frequency (str): Frequency at which disconnected App Connectors are deleted.
            frequency_interval (str): Interval for the frequency value.
            delete_disabled (bool, optional): Whether to include disconnected connectors.
            enabled (bool, optional): Whether the deletion setting is enabled.

        Returns:
            AppConnectorSchedule: The created schedule configuration.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If customer_id is not provided.

        Examples:
            >>> try:
            ...     schedule = client.zpa.app_connector_schedule.add_connector_schedule(
            ...         frequency="days",
            ...         frequency_interval="5",
            ...         enabled=True
            ...     )
            ...     print(schedule.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/connectorSchedule")

        customer_id = kwargs.get("customer_id") or os.getenv("ZPA_CUSTOMER_ID")
        if not customer_id:
            raise ValueError("customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID")

        body = kwargs
        payload = {
            "customerId": customer_id,
            "frequency": body.get("frequency"),
            "frequencyInterval": body.get("frequency_interval"),
        }
        if "delete_disabled" in body:
            payload["deleteDisabled"] = body["delete_disabled"]
        if "enabled" in body:
            payload["enabled"] = body["enabled"]

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        response = self._request_executor.execute(request, AppConnectorSchedule)

        return AppConnectorSchedule(self.form_response_body(response.get_body()))

    def update_connector_schedule(self, scheduler_id: str, **kwargs) -> AppConnectorSchedule:
        """
        Updates App Connector schedule frequency.

        Args:
            scheduler_id (str): Unique identifier for the schedule.
            frequency (str): Frequency at which disconnected App Connectors are deleted.
            frequency_interval (str): Interval for the frequency value.
            delete_disabled (bool): Whether to include disconnected connectors.
            enabled (bool): Whether the deletion setting is enabled.

        Returns:
            AppConnectorSchedule: The updated schedule configuration.

        Raises:
            ZscalerAPIException: If the API request fails.
            ValueError: If customer_id is not provided.

        Examples:
            >>> try:
            ...     schedule = client.zpa.app_connector_schedule.update_connector_schedule(
            ...         "12345",
            ...         frequency="days",
            ...         frequency_interval="7",
            ...         enabled=True
            ...     )
            ...     print(schedule.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/connectorSchedule/{scheduler_id}")

        customer_id = kwargs.get("customer_id") or os.getenv("ZPA_CUSTOMER_ID")
        if not customer_id:
            raise ValueError("customer_id is required either as a function argument or as an environment variable ZPA_CUSTOMER_ID")

        body = dict(kwargs)
        payload = {
            "customerId": customer_id,
            "frequency": body.get("frequency"),
            "frequencyInterval": body.get("frequency_interval"),
        }
        if "delete_disabled" in body:
            payload["deleteDisabled"] = body["delete_disabled"]
        if "enabled" in body:
            payload["enabled"] = body["enabled"]

        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, AppConnectorSchedule)

        if response is None:
            return AppConnectorSchedule({"id": scheduler_id})

        return AppConnectorSchedule(self.form_response_body(response.get_body()))
