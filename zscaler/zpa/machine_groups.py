from box import Box, BoxList
from requests import Response

from . import ZPAClient


class MachineGroupsAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client
        self.customer_id = client.customer_id

    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured machine groups.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`list`: A list of all configured machine groups.

        Examples:
            >>> for machine_group in zpa.machine_groups.list_groups():
            ...    pprint(machine_group)

        """
        list, _ = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/machineGroup" % (self.customer_id),
            data_key_name="list",
        )
        return list

    def get_group(self, group_id: str) -> Box:
        """
        Returns information on the specified machine group.

        Args:
            group_id (str):
                The unique identifier for the machine group.

        Returns:
            :obj:`Box`: The resource record for the machine group.

        Examples:
            >>> pprint(zpa.machine_groups.get_group('99999'))

        """
        response = self.rest.get("/mgmtconfig/v1/admin/customers/%s/machineGroup/%s" % (self.customer_id, group_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def get_machine_group_by_name(self, name):
        apps = self.list_groups()
        for app in apps:
            if app.get("name") == name:
                return app
        return None
