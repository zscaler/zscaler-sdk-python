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

from typing import Optional, List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.zinsights.models.inputs import IoTDeviceFilterBy, IoTDeviceOrderBy


class IotAPI(APIClient):
    """
    A Client object for the Z-Insights IOT domain.

    Securing IoT begins with knowing which devices are connected to your network
    and what they're doing. Zscaler IoT Device Visibility extends the power of
    the Zero Trust Exchange™ platform, using AI/ML to automatically detect,
    identify, and classify IoT devices across your estate.
    This domain provides device data and statistics.
    """

    _zinsights_base_endpoint = "/zins/graphql"

    def __init__(self, request_executor: RequestExecutor) -> None:
        super().__init__()
        self._request_executor = request_executor

    def get_device_stats(
        self,
        limit: Optional[int] = None,
        filter_by: Optional[IoTDeviceFilterBy] = None,
        order_by: Optional[List[IoTDeviceOrderBy]] = None,
    ) -> tuple:
        """
        Get IoT device statistics.

        Returns device statistics including:
        - devices_count: Total device count
        - user_devices_count: Unmanaged user devices count
        - iot_devices_count: IoT devices count
        - server_devices_count: Server devices count
        - un_classified_devices_count: Unclassified devices count
        - entries: List of device classifications with totals

        Args:
            limit: Maximum number of entries to return.
            filter_by: Filter options using IoTDeviceFilterBy.
                       Supports filtering by classifications, classification_uuid, category.
            order_by: Ordering options using list of IoTDeviceOrderBy.
                       Supports ordering by classifications, classification_uuid, category, total.

        Returns:
            tuple: (device_stats_dict, response, error)
                   device_stats_dict contains counts and entries list.

        Examples:
            >>> stats, _, err = client.zinsights.iot.get_device_stats(limit=10)
            >>> print(f"Total devices: {stats.get('devices_count')}")
            >>> print(f"IoT devices: {stats.get('iot_devices_count')}")
            >>> for entry in stats.get('entries', []):
            ...     print(f"  {entry['classifications']}: {entry['total']}")
            >>>
            >>> # With filtering
            >>> from zscaler.zinsights.models.inputs import IoTDeviceFilterBy, StringFilter
            >>> filter_by = IoTDeviceFilterBy(category=StringFilter(eq="Camera"))
            >>> stats, _, err = client.zinsights.iot.get_device_stats(
            ...     limit=10,
            ...     filter_by=filter_by
            ... )
        """
        query = """
            query IoTDeviceStats($limit: Int, $filter_by: IoTDeviceFilterBy, $order_by: [IoTDeviceOrderBy]) {
                IOT {
                    device_stats {
                        devices_count
                        user_devices_count
                        iot_devices_count
                        server_devices_count
                        un_classified_devices_count
                        entries(limit: $limit, filter_by: $filter_by, order_by: $order_by) {
                            classifications
                            classification_uuid
                            category
                            total
                        }
                    }
                }
            }
        """

        variables = {
            "limit": limit,
            "filter_by": filter_by.as_dict() if filter_by else None,
            "order_by": [o.as_dict() for o in order_by] if order_by else None,
        }

        body = {
            "query": query,
            "variables": variables,
            "operationName": "IoTDeviceStats",
        }

        http_method = "POST"
        api_url = format_url(self._zinsights_base_endpoint)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            body = response.get_body() if response else {}
            # GraphQL responses have data wrapped in "data" key
            data = body.get("data", {}) if isinstance(body, dict) else {}
            device_stats = data.get("IOT", {}).get("device_stats", {})
            return (device_stats, response, None)
        except Exception as ex:
            return (None, response, ex)
