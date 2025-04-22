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

from zscaler.zdx.admin import AdminAPI
from zscaler.zdx.alerts import AlertsAPI
from zscaler.zdx.apps import AppsAPI
from zscaler.zdx.devices import DevicesAPI
from zscaler.zdx.inventory import InventoryAPI
from zscaler.zdx.troubleshooting import TroubleshootingAPI
from zscaler.zdx.users import UsersAPI


class ZDXService:
    """ZDX Service client, exposing various ZDX APIs."""

    def __init__(self, client):
        self._request_executor = client._request_executor

    @property
    def admin(self):
        """
        The interface object for the :ref:`ZDX Admin interface <zdx-admin>`.

        """
        return AdminAPI(self._request_executor)

    @property
    def alerts(self):
        """
        The interface object for the :ref:`ZDX Alerts interface <zdx-alerts>`.

        """
        return AlertsAPI(self._request_executor)

    @property
    def apps(self):
        """
        The interface object for the :ref:`ZDX Apps interface <zdx-apps>`.

        """
        return AppsAPI(self._request_executor)

    @property
    def devices(self):
        """
        The interface object for the :ref:`ZDX Devices interface <zdx-devices>`.

        """
        return DevicesAPI(self._request_executor)

    @property
    def inventory(self):
        """
        The interface object for the :ref:`ZDX Inventory interface <zdx-inventory>`.

        """
        return InventoryAPI(self._request_executor)

    @property
    def troubleshooting(self):
        """
        The interface object for the :ref:`ZDX Troubleshooting interface <zdx-troubleshooting>`.

        """
        return TroubleshootingAPI(self._request_executor)

    @property
    def users(self):
        """
        The interface object for the :ref:`ZDX Users interface <zdx-users>`.

        """
        return UsersAPI(self._request_executor)
