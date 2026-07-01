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

from zscaler.request_executor import RequestExecutor
from zscaler.zcell.anomaly_policy import AnomalyPolicyAPI
from zscaler.zcell.audit_data_handling import AuditDataHandlingAPI
from zscaler.zcell.customer_data_handling import CustomerDataHandlingAPI
from zscaler.zcell.customer_region_handling import CustomerRegionHandlingAPI
from zscaler.zcell.network_events import NetworkEventsAPI
from zscaler.zcell.sim_analytics import SimAnalyticsAPI
from zscaler.zcell.sim_handling import SimHandlingAPI
from zscaler.zcell.sim_location_groups import SimLocationGroupsAPI
from zscaler.zcell.tag_handling import TagHandlingAPI


class ZCellService:
    """ZCell Service client, exposing various Zscaler Cellular APIs."""

    def __init__(self, request_executor: RequestExecutor) -> None:
        # Ensure the service gets the request executor from the Client object
        self._request_executor = request_executor

    @property
    def anomaly_policy(self) -> AnomalyPolicyAPI:
        """
        The interface object for the :ref:`ZCELL Anomaly Policy interface <zcell-anomaly_policy>`.

        """
        return AnomalyPolicyAPI(self._request_executor)

    @property
    def audit_data_handling(self) -> AuditDataHandlingAPI:
        """
        The interface object for the :ref:`ZCELL Audit Data Handling interface <zcell-audit_data_handling>`.

        """
        return AuditDataHandlingAPI(self._request_executor)

    @property
    def customer_data_handling(self) -> CustomerDataHandlingAPI:
        """
        The interface object for the :ref:`ZCELL Customer Data Handling interface <zcell-customer_data_handling>`.

        """
        return CustomerDataHandlingAPI(self._request_executor)

    @property
    def network_events(self) -> NetworkEventsAPI:
        """
        The interface object for the :ref:`ZCELL Network Events interface <zcell-network_events>`.

        """
        return NetworkEventsAPI(self._request_executor)

    @property
    def sim_analytics(self) -> SimAnalyticsAPI:
        """
        The interface object for the :ref:`ZCELL Sim Analytics interface <zcell-sim_analytics>`.

        """
        return SimAnalyticsAPI(self._request_executor)

    @property
    def sim_handling(self) -> SimHandlingAPI:
        """
        The interface object for the :ref:`ZCELL Sim Handling interface <zcell-sim_handling>`.

        """
        return SimHandlingAPI(self._request_executor)

    @property
    def sim_location_groups(self) -> SimLocationGroupsAPI:
        """
        The interface object for the :ref:`ZCELL Sim Location Groups interface <zcell-sim_location_groups>`.

        """
        return SimLocationGroupsAPI(self._request_executor)

    @property
    def tag_handling(self) -> TagHandlingAPI:
        """
        The interface object for the :ref:`ZCELL Tag Handling interface <zcell-tag_handling>`.

        """
        return TagHandlingAPI(self._request_executor)

    @property
    def customer_region_handling(self) -> CustomerRegionHandlingAPI:
        """
        The interface object for the :ref:`ZCELL Customer Region Handling interface <zcell-customer_region_handling>`.

        """
        return CustomerRegionHandlingAPI(self._request_executor)
