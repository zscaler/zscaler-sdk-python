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


# import pytest
# from pprint import pprint
# from tests.integration.zpa.conftest import MockZPAClient


# @pytest.fixture
# def fs():
#     yield


# class TestAppConnectorSchedule:
#     """
#     Integration Tests for the App Connector Schedule
#     """

#     def test_app_connector_schedule(self, fs):
#         client = MockZPAClient(fs)
#         errors = []  # Initialize an empty list to collect errors
#         scheduler_id = None

#         try:
#             # Step 1: Get the existing App Connector Schedule
#             try:
#                 schedule, _, err = client.zpa.app_connector_schedule.get_connector_schedule()
#                 assert err is None, f"Error retrieving App Connector Schedule: {err}"
#                 assert schedule is not None, "Failed to retrieve App Connector Schedule"
#                 pprint(schedule.as_dict())
#                 scheduler_id = schedule.id  # Extract scheduler_id
#             except Exception as exc:
#                 errors.append(f"Error during get_connector_schedule: {exc}")

#             # Step 2: Add a new App Connector Schedule
#             try:
#                 _, _, err = client.zpa.app_connector_schedule.add_connector_schedule(
#                     frequency="days",
#                     interval="5",
#                     disabled=False,
#                     enabled=True,
#                 )
#                 if err:
#                     if "resource.already.exist" in str(err):
#                         print("App Connector Schedule already exists. Continuing with the test.")
#                     else:
#                         errors.append(f"Error during add_connector_schedule: {err}")
#                 else:
#                     print("App Connector Schedule added successfully (204 No Content).")
#             except Exception as exc:
#                 errors.append(f"Unexpected error during add_connector_schedule: {exc}")

#             # Step 3: Update the App Connector Schedule
#             try:
#                 assert scheduler_id is not None, "Scheduler ID is None"
#                 _, _, err = client.zpa.app_connector_schedule.update_connector_schedule(
#                     scheduler_id=scheduler_id,
#                     frequency="days",
#                     interval="7",
#                     disabled=True,
#                     enabled=False,
#                 )
#                 if err:
#                     if isinstance(err, ValueError) and str(err) == "Response is None":
#                         print("[INFO] Interpreting 'Response is None' as 204 success.")
#                     else:
#                         errors.append(f"Error during update_connector_schedule: {err}")
#                 else:
#                     print("App Connector Schedule updated successfully (204 No Content).")
#             except Exception as exc:
#                 errors.append(f"Unexpected error during update_connector_schedule: {exc}")

#         except Exception as exc:
#             errors.append(f"Unexpected error during test execution: {exc}")

#         # Final assertion to ensure no errors occurred
#         assert len(errors) == 0, f"Errors occurred: {errors}"

