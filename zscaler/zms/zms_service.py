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
from zscaler.zms.agents import AgentsAPI
from zscaler.zms.agent_groups import AgentGroupsAPI
from zscaler.zms.nonces import NoncesAPI
from zscaler.zms.resources import ResourcesAPI
from zscaler.zms.resource_groups import ResourceGroupsAPI
from zscaler.zms.policy_rules import PolicyRulesAPI
from zscaler.zms.app_zones import AppZonesAPI
from zscaler.zms.app_catalog import AppCatalogAPI
from zscaler.zms.tags import TagsAPI


class ZMSService:
    """ZMS (Zscaler Microsegmentation) Service client, exposing various ZMS GraphQL APIs."""

    def __init__(self, request_executor: RequestExecutor) -> None:
        self._request_executor = request_executor

    @property
    def agents(self) -> AgentsAPI:
        """
        The interface object for the :ref:`ZMS Agents API <zms-agents>`.

        """
        return AgentsAPI(self._request_executor)

    @property
    def agent_groups(self) -> AgentGroupsAPI:
        """
        The interface object for the :ref:`ZMS Agent Groups API <zms-agent_groups>`.

        """
        return AgentGroupsAPI(self._request_executor)

    @property
    def nonces(self) -> NoncesAPI:
        """
        The interface object for the :ref:`ZMS Nonces (Provisioning Keys) API <zms-nonces>`.

        """
        return NoncesAPI(self._request_executor)

    @property
    def resources(self) -> ResourcesAPI:
        """
        The interface object for the :ref:`ZMS Resources API <zms-resources>`.

        """
        return ResourcesAPI(self._request_executor)

    @property
    def resource_groups(self) -> ResourceGroupsAPI:
        """
        The interface object for the :ref:`ZMS Resource Groups API <zms-resource_groups>`.

        """
        return ResourceGroupsAPI(self._request_executor)

    @property
    def policy_rules(self) -> PolicyRulesAPI:
        """
        The interface object for the :ref:`ZMS Policy Rules API <zms-policy_rules>`.

        """
        return PolicyRulesAPI(self._request_executor)

    @property
    def app_zones(self) -> AppZonesAPI:
        """
        The interface object for the :ref:`ZMS App Zones API <zms-app_zones>`.

        """
        return AppZonesAPI(self._request_executor)

    @property
    def app_catalog(self) -> AppCatalogAPI:
        """
        The interface object for the :ref:`ZMS App Catalog API <zms-app_catalog>`.

        """
        return AppCatalogAPI(self._request_executor)

    @property
    def tags(self) -> TagsAPI:
        """
        The interface object for the :ref:`ZMS Tags API <zms-tags>`.

        """
        return TagsAPI(self._request_executor)
