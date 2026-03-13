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

from __future__ import annotations

from typing import TYPE_CHECKING

from zscaler.ztb.alarms import AlarmsAPI
from zscaler.ztb.api_key import APIKeyAuthRouterAPI
from zscaler.ztb.app_connector_config import AppConnectorConfigAPI
from zscaler.ztb.devices import DevicesAPI
from zscaler.ztb.groups_router import GroupsRouterAPI
from zscaler.ztb.logs import LogsAPI
from zscaler.ztb.policy_comments import PolicyCommentsAPI
from zscaler.ztb.ransomware_kill import RansomwareKillAPI
from zscaler.ztb.site import SiteAPI
from zscaler.ztb.site2site_vpn import Site2SiteVPNAPI
from zscaler.ztb.template_router import TemplateRouterAPI

if TYPE_CHECKING:
    from zscaler.oneapi_client import Client


class ZTBService:
    """
    ZTB Service client, exposing Zero Trust Branch API resources.

    This service is used via the OneAPI authentication path
    (``ZscalerClient`` / ``Client``).  For standalone / legacy token-based
    access, use ``LegacyZTBClient`` or ``LegacyZTBClientHelper`` directly.
    """

    def __init__(self, client: "Client") -> None:
        self._request_executor = client.get_request_executor()

    @property
    def alarms(self) -> AlarmsAPI:
        """
        The interface object for the :ref:`ZTB Alarms interface <ztb-alarms>`.

        """
        return AlarmsAPI(self._request_executor)

    @property
    def api_keys(self) -> APIKeyAuthRouterAPI:
        """
        The interface object for the :ref:`ZTB API Key Auth interface <ztb-api_keys>`.

        """
        return APIKeyAuthRouterAPI(self._request_executor)

    @property
    def app_connector_config(self) -> AppConnectorConfigAPI:
        """
        The interface object for the :ref:`ZTB App Connector Config interface <ztb-app_connector_config>`.

        """
        return AppConnectorConfigAPI(self._request_executor)

    @property
    def devices(self) -> DevicesAPI:
        """
        The interface object for the :ref:`ZTB Devices interface <ztb-devices>`.

        """
        return DevicesAPI(self._request_executor)

    @property
    def groups_router(self) -> GroupsRouterAPI:
        """
        The interface object for the :ref:`ZTB Groups Router interface <ztb-groups_router>`.

        """
        return GroupsRouterAPI(self._request_executor)

    @property
    def logs(self) -> LogsAPI:
        """
        The interface object for the :ref:`ZTB Logs interface <ztb-logs>`.

        """
        return LogsAPI(self._request_executor)

    @property
    def policy_comments(self) -> PolicyCommentsAPI:
        """
        The interface object for the :ref:`ZTB Policy Comments interface <ztb-policy_comments>`.

        """
        return PolicyCommentsAPI(self._request_executor)

    @property
    def ransomware_kill(self) -> RansomwareKillAPI:
        """
        The interface object for the :ref:`ZTB Ransomware Kill interface <ztb-ransomware_kill>`.

        """
        return RansomwareKillAPI(self._request_executor)

    @property
    def site(self) -> SiteAPI:
        """
        The interface object for the :ref:`ZTB Site interface <ztb-site>`.

        """
        return SiteAPI(self._request_executor)

    @property
    def site2site_vpn(self) -> Site2SiteVPNAPI:
        """
        The interface object for the :ref:`ZTB Site2Site VPN interface <ztb-site2site_vpn>`.

        """
        return Site2SiteVPNAPI(self._request_executor)

    @property
    def template_router(self) -> TemplateRouterAPI:
        """
        The interface object for the :ref:`ZTB Template Router interface <ztb-template_router>`.

        """
        return TemplateRouterAPI(self._request_executor)
