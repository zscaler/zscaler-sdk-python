import logging

from zscaler import __version__
from zscaler.zdx.admin import AdminAPI
from zscaler.zdx.alerts import AlertsAPI
from zscaler.zdx.apps import AppsAPI
from zscaler.zdx.devices import DevicesAPI
from zscaler.zdx.inventory import InventoryAPI
from zscaler.zdx.troubleshooting import TroubleshootingAPI
from zscaler.zdx.users import UsersAPI

from zscaler.logger import setup_logging
from .zdx_client import ZDXClientHelper  # Import ZDXClientHelper from zdx_client.py

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class ZDX:
    """
    A Controller to access Endpoints in the Zscaler Digital Experience (ZDX) API.

    The ZDX object stores the session token and simplifies access to CRUD options within the ZDX Portal.

    Attributes:
        client_id (str): The ZDX Client ID generated from the ZDX Portal.
        client_secret (str): The ZDX Client Secret generated from the ZDX Portal.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are below. Defaults to ``zdxcloud``.

            * ``zdxcloud``
            * ``zdxbeta``

        override_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.
    """

    def __init__(self, **kw):
        self.client = ZDXClientHelper(**kw)

    @property
    def admin(self):
        """The interface object for the :ref:`ZDX Admin interface <zdx-admin>`."""
        return AdminAPI(self.client)

    @property
    def alerts(self):
        """The interface object for the :ref:`ZDX Alerts interface <zdx-alerts>`."""
        return AlertsAPI(self.client)

    @property
    def apps(self):
        """The interface object for the :ref:`ZDX Apps interface <zdx-apps>`."""
        return AppsAPI(self.client)

    @property
    def devices(self):
        """The interface object for the :ref:`ZDX Devices interface <zdx-devices>`."""
        return DevicesAPI(self.client)

    @property
    def inventory(self):
        """The interface object for the :ref:`ZDX Inventory interface <zdx-inventory>`."""
        return InventoryAPI(self.client)

    @property
    def troubleshooting(self):
        """The interface object for the :ref:`ZDX Troubleshooting interface <zdx-troubleshooting>`."""
        return TroubleshootingAPI(self.client)

    @property
    def users(self):
        """The interface object for the :ref:`ZDX Users interface <zdx-users>`."""
        return UsersAPI(self.client)
