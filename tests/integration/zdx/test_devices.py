# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import pytest
import time
from pprint import pprint
from tests.integration.zdx.conftest import MockZDXClient


@pytest.fixture
def fs():
    yield


class TestDevices:
    """
    Integration Tests for the devices
    """

    def test_list_devices(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                print(f"Retrieved {len(devices)} devices")
                for device in devices:
                    pprint(device)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_device(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                device_id = devices[0].id
                print(f"Using device ID {device_id} for get_device_apps test")

                # Get device information using the retrieved device ID
                device_info = client.devices.get_device_apps(device_id=device_id, **kwargs)
                pprint(device_info)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_device_apps(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                device_id = devices[0].id
                print(f"Using device ID {device_id} for get_device_apps test")

                # Get device applications using the retrieved device ID
                device_apps = client.devices.get_device_apps(device_id=device_id, **kwargs)
                pprint(device_apps)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_web_probes(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices and apps to get a device ID and app ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not devices or not apps:
                print("No devices or apps found within the specified time range.")
            else:
                device_id = devices[0].id
                app_id = apps[0].id
                print(f"Using device ID {device_id} and app ID {app_id} for get_web_probes test")

                # Get web probes using the retrieved device ID and app ID
                web_probes = client.devices.get_web_probes(device_id=device_id, app_id=app_id)
                pprint(web_probes)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_cloudpath_probes(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices and apps to get a device ID and app ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not devices or not apps:
                print("No devices or apps found within the specified time range.")
            else:
                device_id = devices[0].id
                app_id = apps[0].id
                print(f"Using device ID {device_id} and app ID {app_id} for list_cloudpath_probes test")

                # List cloudpath probes using the retrieved device ID and app ID
                cloudpath_probes = client.devices.list_cloudpath_probes(device_id=device_id, app_id=app_id, **kwargs)
                pprint(cloudpath_probes)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_call_quality_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices and apps to get a device ID and app ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not devices or not apps:
                print("No devices or apps found within the specified time range.")
            else:
                device_id = devices[0].id
                app_id = apps[0].id
                print(f"Using device ID {device_id} and app ID {app_id} for get_call_quality_metrics test")

                # Get call quality metrics using the retrieved device ID and app ID
                call_quality_metrics = client.devices.get_call_quality_metrics(device_id=device_id, app_id=app_id, **kwargs)
                pprint(call_quality_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_health_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                device_id = devices[0].id
                print(f"Using device ID {device_id} for get_health_metrics test")

                # Get health metrics using the retrieved device ID
                health_metrics = client.devices.get_health_metrics(device_id=device_id, **kwargs)
                pprint(health_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_events(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                device_id = devices[0].id
                print(f"Using device ID {device_id} for get_events test")

                # Get events using the retrieved device ID
                events = client.devices.get_events(device_id=device_id)
                pprint(events)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_webprobe_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                # Ensure that devices[0] is a Box object and not a list
                device = devices[0]
                device_id = device.get("id", None) if isinstance(device, dict) else device.id
                print(f"Using device ID {device_id} to list deeptraces")

                # List deeptraces to get a trace ID
                deeptraces_iterator = client.troubleshooting.list_deeptraces(device_id=device_id, **kwargs)
                deeptraces = list(deeptraces_iterator)

                if not deeptraces:
                    print("No deeptraces found within the specified time range.")
                else:
                    # Ensure that deeptraces[0] is a Box object and not a list
                    deeptrace = deeptraces[0]
                    trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                    print(f"Using trace ID {trace_id} for get_deeptrace_webprobe_metrics test")

                    # Get deeptrace webprobe metrics using the retrieved device ID and trace ID
                    webprobe_metrics = client.devices.get_deeptrace_webprobe_metrics(device_id=device_id, trace_id=trace_id)
                    pprint(webprobe_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_cloudpath_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                # Ensure that devices[0] is a Box object and not a list
                device = devices[0]
                device_id = device.get("id", None) if isinstance(device, dict) else device.id
                print(f"Using device ID {device_id} to list deeptraces")

                # List deeptraces to get a trace ID
                deeptraces_iterator = client.troubleshooting.list_deeptraces(device_id=device_id, **kwargs)
                deeptraces = list(deeptraces_iterator)

                if not deeptraces:
                    print("No deeptraces found within the specified time range.")
                else:
                    # Ensure that deeptraces[0] is a Box object and not a list
                    deeptrace = deeptraces[0]
                    trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                    print(f"Using trace ID {trace_id} for get_deeptrace_cloudpath_metrics test")

                    # Get deeptrace cloudpath metrics using the retrieved device ID and trace ID
                    cloudpath_metrics = client.devices.get_deeptrace_cloudpath_metrics(device_id=device_id, trace_id=trace_id)
                    pprint(cloudpath_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_health_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                # Ensure that devices[0] is a Box object and not a list
                device = devices[0]
                device_id = device.get("id", None) if isinstance(device, dict) else device.id
                print(f"Using device ID {device_id} to list deeptraces")

                # List deeptraces to get a trace ID
                deeptraces_iterator = client.troubleshooting.list_deeptraces(device_id=device_id, **kwargs)
                deeptraces = list(deeptraces_iterator)

                if not deeptraces:
                    print("No deeptraces found within the specified time range.")
                else:
                    # Ensure that deeptraces[0] is a Box object and not a list
                    deeptrace = deeptraces[0]
                    trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                    print(f"Using trace ID {trace_id} for get_deeptrace_health_metrics test")

                    # Get deeptrace health metrics using the retrieved device ID and trace ID
                    health_metrics = client.devices.get_deeptrace_health_metrics(device_id=device_id, trace_id=trace_id)
                    pprint(health_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_events(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                # Ensure that devices[0] is a Box object and not a list
                device = devices[0]
                device_id = device.get("id", None) if isinstance(device, dict) else device.id
                print(f"Using device ID {device_id} to list deeptraces")

                # List deeptraces to get a trace ID
                deeptraces_iterator = client.troubleshooting.list_deeptraces(device_id=device_id, **kwargs)
                deeptraces = list(deeptraces_iterator)

                if not deeptraces:
                    print("No deeptraces found within the specified time range.")
                else:
                    # Ensure that deeptraces[0] is a Box object and not a list
                    deeptrace = deeptraces[0]
                    trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                    print(f"Using trace ID {trace_id} for get_deeptrace_events test")

                    # Get deeptrace events using the retrieved device ID and trace ID
                    events = client.devices.get_deeptrace_events(device_id=device_id, trace_id=trace_id)
                    pprint(events)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_top_processes(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            # List devices to get a device ID
            devices_iterator = client.devices.list_devices(**kwargs)
            devices = list(devices_iterator)

            if not devices:
                print("No devices found within the specified time range.")
            else:
                # Ensure that devices[0] is a Box object and not a list
                device = devices[0]
                device_id = device.get("id", None) if isinstance(device, dict) else device.id
                print(f"Using device ID {device_id} to list deeptraces")

                # List deeptraces to get a trace ID
                deeptraces_iterator = client.troubleshooting.list_deeptraces(device_id=device_id, **kwargs)
                deeptraces = list(deeptraces_iterator)

                if not deeptraces:
                    print("No deeptraces found within the specified time range.")
                else:
                    # Ensure that deeptraces[0] is a Box object and not a list
                    deeptrace = deeptraces[0]
                    trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                    print(f"Using trace ID {trace_id} for get_deeptrace_top_processes test")

                    # Get deeptrace top processes using the retrieved device ID and trace ID
                    top_processes = client.devices.get_deeptrace_top_processes(device_id=device_id, trace_id=trace_id)
                    pprint(top_processes)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_geolocations(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            geolocations_iterator = client.devices.list_geolocations(**kwargs)
            geolocations = list(geolocations_iterator)

            if not geolocations:
                print("No geolocations found within the specified time range.")
            else:
                print(f"Retrieved {len(geolocations)} geolocations")
                for geolocation in geolocations:
                    pprint(geolocation)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
