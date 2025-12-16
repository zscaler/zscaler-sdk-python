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
from zscaler.zinsights.web_traffic import WebTrafficAPI
from zscaler.zinsights.saas_security import SaasSecurityAPI
from zscaler.zinsights.cyber_security import CyberSecurityAPI
from zscaler.zinsights.firewall import FirewallAPI
from zscaler.zinsights.iot import IotAPI
from zscaler.zinsights.shadow_it import ShadowItAPI


class ZInsightsService:
    """Z-Insights Service client, exposing various Z-Insights Analytics APIs."""

    def __init__(self, request_executor: RequestExecutor) -> None:
        self._request_executor = request_executor

    @property
    def web_traffic(self) -> WebTrafficAPI:
        """
        The interface object for the :ref:`Z-Insights Web Traffic API <zinsights-web_traffic>`.

        """
        return WebTrafficAPI(self._request_executor)

    @property
    def saas_security(self) -> SaasSecurityAPI:
        """
        The interface object for the :ref:`Z-Insights SaaS Security (CASB) API <zinsights-saas_security>`.

        """
        return SaasSecurityAPI(self._request_executor)

    @property
    def cyber_security(self) -> CyberSecurityAPI:
        """
        The interface object for the :ref:`Z-Insights Cyber Security API <zinsights-cyber_security>`.

        """
        return CyberSecurityAPI(self._request_executor)

    @property
    def firewall(self) -> FirewallAPI:
        """
        The interface object for the :ref:`Z-Insights Zero Trust Firewall API <zinsights-firewall>`.

        """
        return FirewallAPI(self._request_executor)

    @property
    def iot(self) -> IotAPI:
        """
        The interface object for the :ref:`Z-Insights IoT Device Visibility API <zinsights-iot>`.

        """
        return IotAPI(self._request_executor)

    @property
    def shadow_it(self) -> ShadowItAPI:
        """
        The interface object for the :ref:`Z-Insights Shadow IT Discovery API <zinsights-shadow_it>`.

        """
        return ShadowItAPI(self._request_executor)
