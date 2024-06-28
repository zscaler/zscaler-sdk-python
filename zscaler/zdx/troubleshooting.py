from box import BoxList

from zscaler.utils import ZDXIterator, CommonFilters
from zscaler.zdx.zdx_client import ZDXClientHelper


class TroubleshootingAPI:
    def __init__(self, client: ZDXClientHelper):
        self.rest = client

    def list_deeptraces(self, device_id: str, **kwargs):
        """
        Returns a list of all deep traces for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`BoxList`: The list of deep traces for the device.

        Examples:
            Print a list of deep traces for a device.

            >>> for trace in zdx.troubleshooting.list_deep_traces('123456789'):
            ...     print(trace)

        """
        filters = CommonFilters(**kwargs).to_dict()
        devices = []
        for device in ZDXIterator(self.rest, f"devices/{device_id}/deeptraces", filters=filters):
            devices.append(device)
        return BoxList(devices)

    def start_deeptrace(self, device_id: str, app_id: str, session_name: str, **kwargs):
        """
        Starts a deep trace for a specific device and application.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            session_name (str): The name of the deeptrace session.

        Keyword Args:
            web_probe_id (str): The unique ID for the Web probe.
            cloudpath_probe_id (str): The unique ID for the Cloudpath probe.
            session_length_minutes (int): The duration of the deeptrace session in minutes. Defaults to 5.
            probe_device (bool): Whether to probe the device.

        Returns:
            :obj:`Box`: The deeptrace resource record.

        Examples:
            Start a deeptrace for a device.

            >>> trace = zdx.troubleshooting.start_deeptrace(device_id='123456789', app_id='1', session_name='My Deeptrace')
            ... print(trace)

        """
        payload = {
            "session_name": session_name,
            "app_id": app_id,
        }
        payload.update(kwargs)

        return self.rest.post(f"devices/{device_id}/deeptraces", json=payload)

    def get_deeptrace(self, device_id: str, trace_id: str):
        """
        Returns information on a single deeptrace for a specific device.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace resource record.

        Examples:
            Print a single deeptrace for a device.

            >>> trace = zdx.troubleshooting.get_deeptrace('123456789', '987654321')
            ... print(trace)

        """
        return self.rest.get(f"devices/{device_id}/deeptraces/{trace_id}")

    def delete_deeptrace(self, device_id: str, trace_id: str):
        """
        Deletes a single deeptrace session and associated data for a specific device.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`str`: The trace ID that was deleted.

        Examples:
            Delete a single deeptrace for a device.

            >>> trace = zdx.troubleshooting.delete_deeptrace('123456789', '987654321')
            ... print(trace)

        """
        return self.rest.delete(f"devices/{device_id}/deeptraces/{trace_id}")

    def list_top_processes(self, device_id: str, trace_id: str, **kwargs):
        """
        Returns a list of all deep traces for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`BoxList`: The list of deep traces for the device.

        Examples:
            Print a list of deep traces for a device.

            >>> for processes in zdx.troubleshooting.list_top_processes('123456789'):
            ...     print(processes)

        """
        return self.rest.get(f"devices/{device_id}/deeptraces/{trace_id}/top-processes", params=kwargs)
