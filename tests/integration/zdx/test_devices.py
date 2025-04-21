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

import pytest
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
            devices_iterator = client.zdx.devices.list_devices(query_params={"since": 2})
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
            devices, _, error = client.zdx.devices.list_devices(query_params={"since": 2})

            if error:
                errors.append(f"Error listing devices: {error}")
                return

            if not devices or not isinstance(devices, list):
                print("No devices found within the specified time range.")
                return

            first_device = devices[0]
            device_id = getattr(first_device, "id", None)

            if not device_id:
                raise ValueError(f"Device ID not found in response: {first_device.as_dict()}")

            print(f"Using Device ID: {device_id}")

            device_info, _, error = client.zdx.devices.get_device_apps(device_id=device_id)

            if error:
                errors.append(f"Error retrieving device details: {error}")
            else:
                print(f"Successfully retrieved device {device_id}:")
                pprint(device_info.as_dict() if hasattr(device_info, "as_dict") else device_info)

        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_device_apps(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            devices, _, error = client.zdx.devices.list_devices(query_params={"since": 2})

            if error:
                errors.append(f"Error listing devices: {error}")
                return

            if not devices or not isinstance(devices, list):
                print("No devices found within the specified time range.")
                return

            first_device = devices[0]
            device_id = getattr(first_device, "id", None)

            if not device_id:
                raise ValueError(f"Device ID not found in response: {first_device.as_dict()}")

            print(f"Using Device ID: {device_id}")

            device_info, _, error = client.zdx.devices.get_device_apps(device_id=device_id)

            if error:
                errors.append(f"Error retrieving device details: {error}")
            else:
                print(f"Successfully retrieved device {device_id}:")
                pprint(device_info.as_dict() if hasattr(device_info, "as_dict") else device_info)

        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_device_apps(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            devices, _, error = client.zdx.devices.list_devices(query_params={"since": 2})

            if error:
                errors.append(f"Error listing devices: {error}")
                return

            if not devices or not isinstance(devices, list):
                print("No devices found within the specified time range.")
                return

            first_device = devices[0]
            device_id = getattr(first_device, "id", None)

            if not device_id:
                raise ValueError(f"Device ID not found in response: {first_device.as_dict()}")

            print(f"Using Device ID: {device_id}")
            
            apps, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

            if error:
                errors.append(f"Error listing apps: {error}")
                return

            if not apps or not isinstance(apps, list):
                print("No apps found within the specified time range.")
                return

            first_app = apps[0]
            app_id = getattr(first_app, "id", None)

            if not app_id:
                raise ValueError(f"App ID not found in response: {first_app.as_dict()}")

            print(f"Using Device ID: {app_id}")
            
            if not devices or not apps:
                print("No devices or apps found within the specified time range.")
            else:
                device_id = devices[0].id
                app_id = apps[0].id
                print(f"Using device ID {device_id} and app ID {app_id} for get_web_probes test")

                # Get web probes using the retrieved device ID and app ID
                web_probes = client.zdx.devices.get_web_probes(device_id=device_id, app_id=app_id)
                pprint(web_probes)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_cloudpath_probes(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            devices, _, error = client.zdx.devices.list_devices(query_params={"since": 2})

            if error:
                errors.append(f"Error listing devices: {error}")
                return

            if not devices or not isinstance(devices, list):
                print("No devices found within the specified time range.")
                return

            first_device = devices[0]
            device_id = getattr(first_device, "id", None)

            if not device_id:
                raise ValueError(f"Device ID not found in response: {first_device.as_dict()}")

            print(f"Using Device ID: {device_id}")
            
            apps, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

            if error:
                errors.append(f"Error listing apps: {error}")
                return

            if not apps or not isinstance(apps, list):
                print("No apps found within the specified time range.")
                return

            first_app = apps[0]
            app_id = getattr(first_app, "id", None)

            if not app_id:
                raise ValueError(f"App ID not found in response: {first_app.as_dict()}")

            print(f"Using Device ID: {app_id}")
            
            if not devices or not apps:
                print("No devices or apps found within the specified time range.")
            else:
                device_id = devices[0].id
                app_id = apps[0].id
                print(f"Using device ID {device_id} and app ID {app_id} for list_cloudpath_probes test")

                # Get web probes using the retrieved device ID and app ID
                cloudpath_probes = client.zdx.devices.list_cloudpath_probes(device_id=device_id, app_id=app_id)
                pprint(cloudpath_probes)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_call_quality_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            devices, _, error = client.zdx.devices.list_devices(query_params={"since": 2})

            if error:
                errors.append(f"Error listing devices: {error}")
                return

            if not devices or not isinstance(devices, list):
                print("No devices found within the specified time range.")
                return

            first_device = devices[0]
            device_id = getattr(first_device, "id", None)

            if not device_id:
                raise ValueError(f"Device ID not found in response: {first_device.as_dict()}")

            print(f"Using Device ID: {device_id}")
            
            apps, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

            if error:
                errors.append(f"Error listing apps: {error}")
                return

            if not apps or not isinstance(apps, list):
                print("No apps found within the specified time range.")
                return

            first_app = apps[0]
            app_id = getattr(first_app, "id", None)

            if not app_id:
                raise ValueError(f"App ID not found in response: {first_app.as_dict()}")

            print(f"Using Device ID: {app_id}")
            
            if not devices or not apps:
                print("No devices or apps found within the specified time range.")
            else:
                device_id = devices[0].id
                app_id = apps[0].id
                print(f"Using device ID {device_id} and app ID {app_id} for get_call_quality_metrics test")

                # Get web probes using the retrieved device ID and app ID
                cloudpath_probes = client.zdx.devices.get_call_quality_metrics(device_id=device_id, app_id=app_id)
                pprint(cloudpath_probes)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_health_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            devices, _, error = client.zdx.devices.list_devices(query_params={"since": 2})

            if error:
                errors.append(f"Error listing devices: {error}")
                return

            if not devices or not isinstance(devices, list):
                print("No devices found within the specified time range.")
                return

            first_device = devices[0]
            device_id = getattr(first_device, "id", None)

            if not device_id:
                raise ValueError(f"Device ID not found in response: {first_device.as_dict()}")

            print(f"Using Device ID: {device_id}")
            health_metrics = client.zdx.devices.get_health_metrics(device_id=device_id)
            pprint(health_metrics)
            
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_events(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            devices, _, error = client.zdx.devices.list_devices(query_params={"since": 2})

            if error:
                errors.append(f"Error listing devices: {error}")
                return

            if not devices or not isinstance(devices, list):
                print("No devices found within the specified time range.")
                return

            first_device = devices[0]
            device_id = getattr(first_device, "id", None)

            if not device_id:
                raise ValueError(f"Device ID not found in response: {first_device.as_dict()}")

            print(f"Using Device ID: {device_id}")

            device_info, _, error = client.zdx.devices.get_events(device_id=device_id)

            if error:
                errors.append(f"Error retrieving device details: {error}")
            else:
                print(f"Successfully retrieved device {device_id}:")
                pprint(device_info.as_dict() if hasattr(device_info, "as_dict") else device_info)

        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_geolocations(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            geolocations_iterator = client.zdx.devices.list_geolocations(query_params={"since": 2})
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
