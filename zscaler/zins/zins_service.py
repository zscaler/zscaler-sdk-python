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
from zscaler.zins.web_traffic import WebTrafficAPI
from zscaler.zins.saas_security import SaasSecurityAPI
from zscaler.zins.cyber_security import CyberSecurityAPI
from zscaler.zins.firewall import FirewallAPI
from zscaler.zins.iot import IotAPI
from zscaler.zins.shadow_it import ShadowItAPI


class ZInsService:
    """Z-Ins service client, exposing various Z-Ins analytics APIs."""

    def __init__(self, request_executor: RequestExecutor) -> None:
        self._request_executor = request_executor

    @property
    def web_traffic(self) -> WebTrafficAPI:
        """
        The interface object for the :ref:`Z-Ins Web Traffic API <zins-web_traffic>`.

        """
        return WebTrafficAPI(self._request_executor)

    @property
    def saas_security(self) -> SaasSecurityAPI:
        """
        The interface object for the :ref:`Z-Ins SaaS Security (CASB) API <zins-saas_security>`.

        """
        return SaasSecurityAPI(self._request_executor)

    @property
    def cyber_security(self) -> CyberSecurityAPI:
        """
        The interface object for the :ref:`Z-Ins Cyber Security API <zins-cyber_security>`.

        """
        return CyberSecurityAPI(self._request_executor)

    @property
    def firewall(self) -> FirewallAPI:
        """
        The interface object for the :ref:`Z-Ins Zero Trust Firewall API <zins-firewall>`.

        """
        return FirewallAPI(self._request_executor)

    @property
    def iot(self) -> IotAPI:
        """
        The interface object for the :ref:`Z-Ins IoT Device Visibility API <zins-iot>`.

        """
        return IotAPI(self._request_executor)

    @property
    def shadow_it(self) -> ShadowItAPI:
        """
        The interface object for the :ref:`Z-Ins Shadow IT Discovery API <zins-shadow_it>`.

        """
        return ShadowItAPI(self._request_executor)
