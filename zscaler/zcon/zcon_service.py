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
from zscaler.zcon.account_details import AccountDetailsAPI
from zscaler.zcon.activation import ActivationAPI
from zscaler.zcon.admin_roles import AdminRolesAPI
from zscaler.zcon.admin_users import AdminUsersAPI
from zscaler.zcon.ec_groups import ECGroupsAPI
from zscaler.zcon.api_keys import ProvisioningAPIKeyAPI
from zscaler.zcon.provisioning_url import ProvisioningURLAPI
from zscaler.zcon.location_management import LocationManagementAPI
from zscaler.zcon.location_template import LocationTemplateAPI

class ZCONService:
    """ZCON Service client, exposing various ZCON APIs."""

    def __init__(self, request_executor: RequestExecutor):
        # Ensure the service gets the request executor from the Client object
        self._request_executor = request_executor
        
    @property
    def account_details(self):
        """
        The interface object for the :ref:`ZCON Account Details interface <zcon-account_details>`.

        """
        return AccountDetailsAPI(self._request_executor)

    @property
    def activate(self):
        """
        The interface object for the :ref:`ZIA Activation interface <zia-activate>`.

        """
        return ActivationAPI(self._request_executor)
    
    @property
    def admin_roles(self):
        """
        The interface object for the :ref:`ZIA Admin and Role Management interface <zia-admin_roles>`.

        """
        return AdminRolesAPI(self._request_executor)

    @property
    def admin_users(self):
        """
        The interface object for the :ref:`ZIA Admin Users interface <zia-admin_users>`.

        """
        return AdminUsersAPI(self._request_executor)

    @property
    def ec_groups(self):
        """
        The interface object for the :ref:`ZCON EC Groups interface <zcon-ec_groups>`.

        """
        return ECGroupsAPI(self._request_executor)

    @property
    def location_management(self):
        """
        The interface object for the :ref:`ZCON Locations interface <zcon-location_management>`.

        """

        return LocationManagementAPI(self._request_executor)
    
    @property
    def location_template(self):
        """
        The interface object for the :ref:`ZCON Locations interface <zcon-location_template>`.

        """

        return LocationTemplateAPI(self._request_executor)

    @property
    def api_keys(self):
        """
        The interface object for the :ref:`ZCON Provisioning API Key interface <zcon-api_keys>`.

        """

        return ProvisioningAPIKeyAPI(self._request_executor)
    
    @property
    def provisioning_url(self):
        """
        The interface object for the :ref:`ZCON Provisioning URL interface <zcon-provisioning_url>`.

        """

        return ProvisioningURLAPI(self._request_executor)