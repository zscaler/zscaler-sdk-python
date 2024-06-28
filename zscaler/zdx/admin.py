from box import BoxList
from zscaler.utils import zdx_params
from zscaler.utils import ZDXIterator, CommonFilters
from zscaler.zdx.zdx_client import ZDXClientHelper


class AdminAPI:
    def __init__(self, client: ZDXClientHelper):
        self.rest = client

    @zdx_params
    def list_departments(self, filters=None, **kwargs) -> BoxList:
        """
        Returns a list of departments that are configured within ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            search (str): The search string to filter by name or department ID.

        Returns:
            :obj:`BoxList`: The list of departments in ZDX.

        Examples:
            List all departments in ZDX for the past 2 hours:

            >>> for department in zdx.admin.list_departments():
            ...     print(department)

        """
        filters = CommonFilters(**kwargs).to_dict()
        return ZDXIterator(self.rest, "administration/departments", filters)

    @zdx_params
    def list_locations(self, filters=None, **kwargs) -> BoxList:
        """
        Returns a list of locations that are configured within ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            search (str): The search string to filter by name or location ID.

        Returns:
            :obj:`BoxList`: The list of locations in ZDX.

        Examples:
            List all locations in ZDX for the past 2 hours:

            >>> for location in zdx.admin.list_locations():
            ...     print(location)

        """
        if filters is None:
            filters = CommonFilters(**kwargs).to_dict()
        else:
            filters.update(kwargs)

        iterator = ZDXIterator(self.rest, "administration/locations", filters)
        return BoxList(iterator)
