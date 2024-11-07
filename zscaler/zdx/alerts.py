from box import BoxList

from zscaler.utils import ZDXIterator, CommonFilters
from zscaler.zdx.zdx_client import ZDXClientHelper
from zscaler.utils import zdx_params


class AlertsAPI:
    def __init__(self, client: ZDXClientHelper):
        self.rest = client

    @zdx_params
    def list_ongoing(self, **kwargs) -> BoxList:
        """
        Returns a list of all ongoing alert rules across an organization in ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.
            user_ids (list): List of user IDs.
            device_ids (list): List of device IDs.

        Returns:
            :obj:`BoxList`: The list of software in ZDX.

        Examples:
            List all ongoing alerts in ZDX for the past 2 hours:

            >>> for alert in zdx.alerts.list_ongoing():
            ...     print(alert)

            List all ongoing alerts in ZDX for the past 24 hours:

            >>> for alert in zdx.alerts.list_ongoing(since=24):
            ...     print(alert)
        """
        filters = CommonFilters(**kwargs).to_dict()
        return ZDXIterator(self.rest, "alerts/ongoing", filters)

    @zdx_params
    def list_historical(self, **kwargs) -> BoxList:
        """
        Returns a list of all ongoing alert rules across an organization in ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.
            user_ids (list): List of user IDs.
            device_ids (list): List of device IDs.

        Returns:
            :obj:`BoxList`: The list of software in ZDX.

        Examples:
            List all ongoing alerts in ZDX for the past 2 hours:

            >>> for alert in zdx.alerts.list_historical():
            ...     print(alert)

            List all ongoing alerts in ZDX for the past 24 hours:

            >>> for alert in zdx.alerts.list_historical(since=24):
            ...     print(alert)
        """
        filters = CommonFilters(**kwargs).to_dict()
        return ZDXIterator(self.rest, "alerts/historical", filters)

    @zdx_params
    def get_alert(self, alert_id: str, **kwargs):
        """
        Returns a single alert in ZDX.

        Args:
            alert_id (str): The unique ID for the alert.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The ZDX device resource record.

        Examples:
            Get information for the device with an ID of 123456789.
            >>> device = zdx.alerts.get_alert('123456789')

            Get information for the device with an ID of 123456789 for the last 24 hours.
            >>> device = zdx.alerts.get_alert('123456789', since=24)

        """
        return self.rest.get(f"alerts/{alert_id}", params=kwargs)

    @zdx_params
    def list_affected_devices(self, alert_id, **kwargs) -> BoxList:
        """
        Returns a list of all all affected devices associated with
        an alert rule in conjunction with provided filters.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.
            location_groups (list): List of location group IDs.

        Returns:
            :obj:`BoxList`: The list of software in ZDX.

        Examples:
            List all ongoing alerts in ZDX for the past 2 hours:

            >>> for alert in zdx.alerts.list_affected_devices():
            ...     print(alert)

            List all ongoing alerts in ZDX for the past 24 hours:

            >>> for alert in zdx.alerts.list_affected_devices(since=24):
            ...     print(alert)
        """
        filters = CommonFilters(**kwargs).to_dict()
        return ZDXIterator(self.rest, f"alerts/{alert_id}/affected_devices", filters)
