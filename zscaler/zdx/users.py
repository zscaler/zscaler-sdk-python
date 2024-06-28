from box import BoxList
from zscaler.utils import ZDXIterator, CommonFilters, zdx_params
from zscaler.zdx.zdx_client import ZDXClientHelper


class UsersAPI:
    def __init__(self, client: ZDXClientHelper):
        self.rest = client

    @zdx_params
    def list_users(self, **kwargs) -> BoxList:
        """
        Returns a list of all active users configured within the ZDX tenant.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.

        Returns:
            :obj:`BoxList`: The list of users in ZDX.

        Examples:
            List all users in ZDX for the past 2 hours:

            >>> for user in zdx.users.list_users():
            ...     print(user)

        """
        filters = CommonFilters(**kwargs).to_dict()
        devices = []
        for device in ZDXIterator(self.rest, "users", filters=filters):
            devices.append(device)
        return BoxList(devices)

    @zdx_params
    def get_user(self, user_id: str, **kwargs):
        """
        Returns information on the specified user configured within the ZDX tenant.

        Args:
            user_id (str): The unique ID for the ZDX user.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.

        Returns:
            :obj:`Box`: The user information.

        Examples:
            Return information on the user with the ID of 999999999:

            >>> zia.users.get_user(user_id='999999999')

        """
        return self.rest.get(f"users/{user_id}", **kwargs)
