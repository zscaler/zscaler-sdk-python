from box import BoxList

from zscaler.utils import ZDXIterator
from zscaler.zdx.filters import GetSoftwareFilters
from zscaler.zdx.zdx_client import ZDXClientHelper
from zscaler.utils import zdx_params


class InventoryAPI:
    def __init__(self, client: ZDXClientHelper):
        self.rest = client

    @zdx_params
    def list_softwares(self, **kwargs) -> BoxList:
        """
        Returns a list of all software in ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.
            user_ids (list): List of user IDs.
            device_ids (list): List of device IDs.

        Returns:
            :obj:`BoxList`: The list of software in ZDX.

        Examples:
            List all software in ZDX for the past 2 hours:

            >>> for software in zdx.inventory.list_softwares():
            ...     print(software)

            List all software in ZDX for the past 24 hours:

            >>> for software in zdx.inventory.list_softwares(since=24):
            ...     print(software)

        """
        filters = GetSoftwareFilters(**kwargs).to_dict()
        return BoxList(ZDXIterator(self.rest, "inventory/software", filters=filters))

    @zdx_params
    def list_software_keys(self, software_key: str, **kwargs) -> BoxList:
        """
        Returns a list of all users and devices for the given software name and version.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.
            user_ids (list): List of user IDs.
            device_ids (list): List of device IDs.

        Returns:
            :obj:`BoxList`: The list of software in ZDX.

        Examples:
            List all software keys in ZDX for the past 2 hours:

            >>> for software_key in zdx.inventory.list_software_keys("some_software_key"):
            ...     print(software_key)

            List all software keys in ZDX for the past 24 hours:

            >>> for software_key in zdx.inventory.list_software_keys("some_software_key", since=24):
            ...     print(software_key)

        """
        filters = GetSoftwareFilters(**kwargs).to_dict()
        return BoxList(ZDXIterator(self.rest, f"inventory/software/{software_key}", filters=filters))
