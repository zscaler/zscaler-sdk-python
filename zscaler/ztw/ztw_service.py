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

from typing import Dict, Any
from zscaler.request_executor import RequestExecutor
from zscaler.ztw.account_details import AccountDetailsAPI
from zscaler.ztw.activation import ActivationAPI
from zscaler.ztw.admin_roles import AdminRolesAPI
from zscaler.ztw.admin_users import AdminUsersAPI
from zscaler.ztw.ec_groups import ECGroupsAPI
from zscaler.ztw.api_keys import ProvisioningAPIKeyAPI
from zscaler.ztw.provisioning_url import ProvisioningURLAPI
from zscaler.ztw.location_management import LocationManagementAPI
from zscaler.ztw.location_template import LocationTemplateAPI
from zscaler.ztw.forwarding_gateways import ForwardingGatewaysAPI
from zscaler.ztw.forwarding_rules import ForwardingControlRulesAPI
from zscaler.ztw.ip_destination_groups import IPDestinationGroupsAPI
from zscaler.ztw.ip_source_groups import IPSourceGroupsAPI
from zscaler.ztw.ip_groups import IPGroupsAPI
from zscaler.ztw.nw_service_groups import NWServiceGroupsAPI
from zscaler.ztw.nw_service import NWServiceAPI
from zscaler.ztw.public_cloud_info import PublicCloudInfoAPI
from zscaler.ztw.account_groups import AccountGroupsAPI
from zscaler.ztw.discovery_service import DiscoveryServiceAPI


class ZTWService:
    """ZTW Service client, exposing various ZTW APIs."""

    def __init__(self, request_executor: RequestExecutor):
        # Ensure the service gets the request executor from the Client object
        self._request_executor = request_executor

    @property
    def account_details(self) -> AccountDetailsAPI:
        """
        The interface object for the :ref:`ZTW Account Details interface <ztw-account_details>`.

        """
        return AccountDetailsAPI(self._request_executor)

    @property
    def activate(self) -> ActivationAPI:
        """
        The interface object for the :ref:`ZTW Activation interface <ztw-activate>`.

        """
        return ActivationAPI(self._request_executor)

    @property
    def admin_roles(self) -> AdminRolesAPI:
        """
        The interface object for the :ref:`ZTW Admin and Role Management interface <ztw-admin_roles>`.

        """
        return AdminRolesAPI(self._request_executor)

    @property
    def admin_users(self) -> AdminUsersAPI:
        """
        The interface object for the :ref:`ZTW Admin Users interface <ztw-admin_users>`.

        """
        return AdminUsersAPI(self._request_executor)

    @property
    def ec_groups(self) -> ECGroupsAPI:
        """
        The interface object for the :ref:`ZTW EC Groups interface <ztw-ec_groups>`.

        """
        return ECGroupsAPI(self._request_executor)

    @property
    def location_management(self) -> LocationManagementAPI:
        """
        The interface object for the :ref:`ZTW Locations interface <ztw-location_management>`.

        """

        return LocationManagementAPI(self._request_executor)

    @property
    def location_template(self) -> LocationTemplateAPI:
        """
        The interface object for the :ref:`ZTW Locations interface <ztw-location_template>`.

        """

        return LocationTemplateAPI(self._request_executor)

    @property
    def api_keys(self) -> ProvisioningAPIKeyAPI:
        """
        The interface object for the :ref:`ZTW Provisioning API Key interface <ztw-api_keys>`.

        """

        return ProvisioningAPIKeyAPI(self._request_executor)

    @property
    def provisioning_url(self) -> ProvisioningURLAPI:
        """
        The interface object for the :ref:`ZTW Provisioning URL interface <ztw-provisioning_url>`.

        """

        return ProvisioningURLAPI(self._request_executor)

    @property
    def forwarding_gateways(self) -> ForwardingGatewaysAPI:
        """
        The interface object for the :ref:`ZTW Forwarding Gateway interface <ztw-forwarding_gateways>`.

        """

        return ForwardingGatewaysAPI(self._request_executor)

    @property
    def forwarding_rules(self) -> ForwardingControlRulesAPI:
        """
        The interface object for the :ref:`ZTW Forwarding Control Rules interface <ztw-forwarding_rules>`.

        """

        return ForwardingControlRulesAPI(self._request_executor)

    @property
    def ip_destination_groups(self) -> IPDestinationGroupsAPI:
        """
        The interface object for the :ref:`ZTW IP Destination Groups interface <ztw-ip_destination_groups>`.

        """

        return IPDestinationGroupsAPI(self._request_executor)

    @property
    def ip_source_groups(self) -> IPSourceGroupsAPI:
        """
        The interface object for the :ref:`ZTW IP Source Groups interface <ztw-ip_source_groups>`.

        """

        return IPSourceGroupsAPI(self._request_executor)

    @property
    def ip_groups(self) -> IPGroupsAPI:
        """
        The interface object for the :ref:`ZTW IP Source Groups interface <ztw-ip_groups>`.

        """

        return IPGroupsAPI(self._request_executor)

    @property
    def nw_service_groups(self) -> NWServiceGroupsAPI:
        """
        The interface object for the :ref:`ZTW Network Service Groups interface <ztw-nw_service_groups>`.

        """

        return NWServiceGroupsAPI(self._request_executor)

    @property
    def nw_service(self) -> NWServiceAPI:
        """
        The interface object for the :ref:`ZTW Network Services interface <ztw-nw_service>`.

        """

        return NWServiceAPI(self._request_executor)

    @property
    def public_cloud_info(self) -> PublicCloudInfoAPI:
        """
        The interface object for the :ref:`ZTW Public Cloud Info interface <ztw-public_cloud_info>`.

        """

        return PublicCloudInfoAPI(self._request_executor)

    @property
    def account_groups(self) -> AccountGroupsAPI:
        """
        The interface object for the :ref:`ZTW Account Groups interface <ztw-account_groups>`.

        """

        return AccountGroupsAPI(self._request_executor)

    @property
    def discovery_service(self) -> DiscoveryServiceAPI:
        """
        The interface object for the :ref:`ZTW Discovery Service interface <ztw-discovery_service>`.

        """

        return DiscoveryServiceAPI(self._request_executor)
