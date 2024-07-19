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


# import pytest
# import time
# from pprint import pprint
# from tests.integration.zdx.conftest import MockZDXClient


# @pytest.fixture
# def fs():
#     yield


# class TestTroubleshooting:
#     """
#     Integration Tests for the Deep Trace Troubleshooting
#     """

#     def test_deep_trace_session(self, fs):
#         client = MockZDXClient(fs)
#         errors = []

#         device_id = None
#         app_id = None
#         probe_id = None
#         trace_id = None

#         try:
#             now = int(time.time())
#             from_time = now - 2 * 60 * 60  # 2 hours ago
#             to_time = now

#             kwargs = {
#                 "from_time": from_time,
#                 "to": to_time,
#             }

#             # List devices to get a device ID
#             try:
#                 devices_iterator = client.devices.list_devices(**kwargs)
#                 devices = list(devices_iterator)

#                 if not devices:
#                     errors.append("No devices found within the specified time range.")
#                 else:
#                     device_id = devices[0].id
#                     print(f"Using device ID {device_id} for deep trace session test")
#             except Exception as e:
#                 errors.append(f"Exception occurred while listing devices: {e}")

#             # List applications to get an app ID
#             try:
#                 apps_iterator = client.apps.list_apps(**kwargs)
#                 apps = list(apps_iterator)

#                 if not apps:
#                     errors.append("No applications found within the specified time range.")
#                 else:
#                     app_id = apps[0].id
#                     print(f"Using app ID {app_id} for deep trace session test")
#             except Exception as e:
#                 errors.append(f"Exception occurred while listing applications: {e}")

#             # List web probes using the retrieved device ID and app ID
#             try:
#                 if device_id and app_id:
#                     probes_iterator = client.devices.get_web_probes(device_id=device_id, app_id=app_id, **kwargs)
#                     probes = list(probes_iterator)

#                     if not probes:
#                         errors.append("No web probes found within the specified time range.")
#                     else:
#                         probe_id = probes[0]["id"]  # Adjusted to match the correct key access
#                         print(f"Using web probe ID {probe_id} for deep trace session test")
#                 else:
#                     errors.append("device_id or app_id is not defined")
#             except Exception as e:
#                 errors.append(f"Exception occurred while listing web probes: {e}")

#             # Invoke the method troubleshooting.start_deeptrace
#             try:
#                 if device_id and app_id and probe_id:
#                     deeptrace_session_name = "Test Deep Trace Session"
#                     deeptrace_response = client.troubleshooting.start_deeptrace(
#                         device_id=device_id, app_id=app_id, session_name=deeptrace_session_name, web_probe_id=probe_id
#                     )
#                     print(f"Deep trace response: {deeptrace_response}")  # Log the response for debugging
#                     if deeptrace_response:
#                         trace_id = deeptrace_response.get("trace_id")  # Adjust the key based on actual response
#                         if trace_id:
#                             print(f"Deep trace started with ID {trace_id}")
#                         else:
#                             errors.append("Deep trace response does not contain an ID")
#                     else:
#                         errors.append("Deep trace response is None")
#                 else:
#                     errors.append("device_id, app_id, or probe_id is not defined")
#             except Exception as e:
#                 errors.append(f"Exception occurred while starting deep trace: {e}")

#             # Pause for 2 seconds
#             time.sleep(2)

#             # Test troubleshooting.list_deeptraces and troubleshooting.get_deeptrace
#             try:
#                 if device_id and trace_id:
#                     deeptraces = client.troubleshooting.list_deeptraces(device_id=device_id)
#                     if not deeptraces:
#                         errors.append("No deep traces found.")
#                     else:
#                         trace_info = client.troubleshooting.get_deeptrace(device_id=device_id, trace_id=trace_id)
#                         pprint(trace_info)
#                 else:
#                     errors.append("device_id or trace_id is not defined")
#             except Exception as e:
#                 errors.append(f"Exception occurred while listing/getting deep trace: {e}")

#             # Pause for 60 seconds
#             time.sleep(30)

#         except Exception as e:
#             errors.append(f"Exception occurred: {e}")

#         finally:
#             # Invoke troubleshooting.delete_deeptrace
#             try:
#                 if device_id and trace_id:
#                     delete_response = client.troubleshooting.delete_deeptrace(device_id=device_id, trace_id=trace_id)
#                     print(f"Deep trace with ID {delete_response} deleted")
#                 else:
#                     errors.append("device_id or trace_id is not defined")
#             except Exception as e:
#                 errors.append(f"Exception occurred while deleting deep trace: {e}")

#         assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
