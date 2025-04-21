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
import time
import random
from pprint import pprint
from tests.integration.zdx.conftest import MockZDXClient


@pytest.fixture
def fs():
    yield


class TestTroubleshooting:
    """
    Integration Tests for the Deep Trace Troubleshooting
    """

    # def test_deep_trace_session(self, fs):
    #     client = MockZDXClient(fs)
    #     errors = []
    #     device_id = None
    #     trace_id = None
    #     deeptrace_session_name = None  # Defined upfront

    #     try:
    #         # Step 1: Get device ID from list_devices, with fallback if none found
    #         try:
    #             devices_iterator = client.zdx.devices.list_devices(query_params={"since": 2})
    #             devices = list(devices_iterator)
    #             if not devices or devices[0] is None:
    #                 # Fallback to a hardcoded device ID, similar to the main script
    #                 device_id = "132559212"
    #                 print(f"No valid devices found; using fallback Device ID: {device_id}")
    #             else:
    #                 first_device = devices[0]
    #                 device_id = getattr(first_device, "id", None)
    #                 if not device_id:
    #                     try:
    #                         device_str = first_device.as_dict()
    #                     except Exception:
    #                         device_str = str(first_device)
    #                     raise ValueError(f"Device ID not found in response: {device_str}")
    #                 print(f"Using Device ID: {device_id}")
    #         except Exception as e:
    #             errors.append(f"Exception occurred while listing devices: {e}")

    #         # Step 3: Start deep trace session (only if device_id is available)
    #         try:
    #             if device_id:
    #                 deeptrace_session_name = f"NewSession_{random.randint(1000, 10000)}"
    #                 deeptrace_response = client.zdx.troubleshooting.start_deeptrace(
    #                     device_id=device_id,
    #                     session_name=deeptrace_session_name,
    #                     session_length_minutes=5,
    #                     probe_device=True
    #                 )
    #                 print(f"Deep trace start response: {deeptrace_response}")
    #                 if deeptrace_response:
    #                     trace_id = deeptrace_response.get("trace_id")
    #                     if not trace_id:
    #                         errors.append("Deep trace response does not contain trace_id")
    #                     else:
    #                         print(f"Deep trace started with trace_id: {trace_id}")
    #                 else:
    #                     errors.append("Deep trace response is None")
    #             else:
    #                 errors.append("Device ID is not defined, skipping deep trace start")
    #         except Exception as e:
    #             errors.append(f"Exception occurred while starting deep trace: {e}")

    #         # Step 4: Wait briefly for the trace to register
    #         time.sleep(5)

    #         # Step 5: Search for the trace by session name (only if deeptrace_session_name is set)
    #         try:
    #             if deeptrace_session_name and device_id:
    #                 traces_list, _, err = client.zdx.troubleshooting.list_deeptraces(
    #                     device_id, query_params={"search": deeptrace_session_name}
    #                 )
    #                 if err:
    #                     errors.append(f"Error listing deep traces: {err}")
    #                 elif not traces_list or not isinstance(traces_list, list):
    #                     errors.append(f"No deep traces found for session '{deeptrace_session_name}'")
    #                 else:
    #                     first_trace = traces_list[0]
    #                     trace_id_from_list = getattr(first_trace, "trace_id", None)
    #                     if not trace_id_from_list:
    #                         errors.append(f"Trace ID not found in trace list: {first_trace.as_dict()}")
    #                     else:
    #                         print(f"Extracted Trace ID from list: {trace_id_from_list}")
    #                         # Use the trace ID from the search result
    #                         trace_id = trace_id_from_list
    #             else:
    #                 errors.append("Deep trace session name is not defined, skipping trace search")
    #         except Exception as e:
    #             errors.append(f"Exception occurred while listing deep traces: {e}")

    #         # Step 6: Get deep trace details using trace_id
    #         try:
    #             if device_id and trace_id:
    #                 fetched_trace, _, err = client.zdx.troubleshooting.get_deeptrace(device_id, trace_id)
    #                 if err:
    #                     errors.append(f"Error fetching deep trace: {err}")
    #                 else:
    #                     print(f"Fetched deep trace details: {fetched_trace}")
    #             else:
    #                 errors.append("Device ID or Trace ID is not defined for fetching deep trace")
    #         except Exception as e:
    #             errors.append(f"Exception occurred while fetching deep trace: {e}")

    #         # Optional: wait briefly before deletion
    #         time.sleep(5)

    #     finally:
    #         # Step 7: Delete the deep trace
    #         try:
    #             if device_id and trace_id:
    #                 # Unpack the tuple returned by delete_deeptrace
    #                 _, _, delete_error = client.zdx.troubleshooting.delete_deeptrace(device_id, trace_id)
    #                 if delete_error:
    #                     errors.append(f"Error deleting deep trace: {delete_error}")
    #                 else:
    #                     print(f"Deep trace with ID {trace_id} deleted successfully.")
    #             else:
    #                 errors.append("Device ID or Trace ID is not defined for deletion")
    #         except Exception as e:
    #             errors.append(f"Exception occurred while deleting deep trace: {e}")

    #     assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_webprobe_metrics(self, fs):
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

            # List deeptraces to get a trace ID
            deeptraces_iterator = client.zdx.troubleshooting.list_deeptraces(device_id=device_id)
            deeptraces = list(deeptraces_iterator)

            if not deeptraces:
                print("No deeptraces found within the specified time range.")
            else:
                # Ensure that deeptraces[0] is a Box object and not a list
                deeptrace = deeptraces[0]
                trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                print(f"Using trace ID {trace_id} for get_deeptrace_webprobe_metrics test")

                # Get deeptrace webprobe metrics using the retrieved device ID and trace ID
                webprobe_metrics = client.zdx.troubleshooting.get_deeptrace_webprobe_metrics(device_id=device_id, trace_id=trace_id)
                pprint(webprobe_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_cloudpath_metrics(self, fs):
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

            # List deeptraces to get a trace ID
            deeptraces_iterator = client.zdx.troubleshooting.list_deeptraces(device_id=device_id)
            deeptraces = list(deeptraces_iterator)

            if not deeptraces:
                print("No deeptraces found within the specified time range.")
            else:
                # Ensure that deeptraces[0] is a Box object and not a list
                deeptrace = deeptraces[0]
                trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                print(f"Using trace ID {trace_id} for get_deeptrace_cloudpath_metrics test")

                # Get deeptrace cloudpath metrics using the retrieved device ID and trace ID
                cloudpath_metrics = client.zdx.troubleshooting.get_deeptrace_cloudpath_metrics(device_id=device_id, trace_id=trace_id)
                pprint(cloudpath_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_health_metrics(self, fs):
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

            # List deeptraces to get a trace ID
            deeptraces_iterator = client.zdx.troubleshooting.list_deeptraces(device_id=device_id)
            deeptraces = list(deeptraces_iterator)

            if not deeptraces:
                print("No deeptraces found within the specified time range.")
            else:
                # Ensure that deeptraces[0] is a Box object and not a list
                deeptrace = deeptraces[0]
                trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                print(f"Using trace ID {trace_id} for get_deeptrace_health_metrics test")

                # Get deeptrace health metrics using the retrieved device ID and trace ID
                health_metrics = client.zdx.troubleshooting.get_deeptrace_health_metrics(device_id=device_id, trace_id=trace_id)
                pprint(health_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_events(self, fs):
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

            # List deeptraces to get a trace ID
            deeptraces_iterator = client.zdx.troubleshooting.list_deeptraces(device_id=device_id)
            deeptraces = list(deeptraces_iterator)

            if not deeptraces:
                print("No deeptraces found within the specified time range.")
            else:
                # Ensure that deeptraces[0] is a Box object and not a list
                deeptrace = deeptraces[0]
                trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                print(f"Using trace ID {trace_id} for get_deeptrace_events test")

                # Get deeptrace events using the retrieved device ID and trace ID
                events = client.zdx.troubleshooting.get_deeptrace_events(device_id=device_id, trace_id=trace_id)
                pprint(events)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_deeptrace_top_processes(self, fs):
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

            # List deeptraces to get a trace ID
            deeptraces_iterator = client.zdx.troubleshooting.list_deeptraces(device_id=device_id)
            deeptraces = list(deeptraces_iterator)

            if not deeptraces:
                print("No deeptraces found within the specified time range.")
            else:
                # Ensure that deeptraces[0] is a Box object and not a list
                deeptrace = deeptraces[0]
                trace_id = deeptrace.get("id", None) if isinstance(deeptrace, dict) else deeptrace.id
                print(f"Using trace ID {trace_id} for get_deeptrace_top_processes test")

                # Get deeptrace top processes using the retrieved device ID and trace ID
                top_processes = client.zdx.troubleshooting.list_top_processes(device_id=device_id, trace_id=trace_id)
                pprint(top_processes)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))