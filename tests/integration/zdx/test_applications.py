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
from pprint import pprint
from tests.integration.zdx.conftest import MockZDXClient


@pytest.fixture
def fs():
    yield


class TestApplications:
    """
    Integration Tests for the applications
    """

    # def test_list_applications(self, fs):
    #     client = MockZDXClient(fs)
    #     errors = []

    #     try:
    #         apps_iterator = client.zdx.apps.list_apps(query_params={"since": 2})
    #         apps = list(apps_iterator)

    #         if not apps:
    #             print("No applications found within the specified time range.")
    #         else:
    #             print(f"Retrieved {len(apps)} applications")
    #             for app in apps:
    #                 pprint(app)
    #     except Exception as e:
    #         errors.append(f"Exception occurred: {e}")

    #     assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_app(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            app_list, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

            if error:
                errors.append(f"Error listing applications: {error}")
                return

            if not app_list or not isinstance(app_list, list):
                print("No applications found within the specified time range.")
                return

            first_app_id = app_list[0]
            app_id = getattr(first_app_id, "id", None)

            if not app_id:
                raise ValueError(f"App ID not found in response: {first_app_id.as_dict()}")

            print(f"Using App ID: {app_id}")

            app_info, _, error = client.zdx.apps.get_app(app_id=app_id)

            if error:
                errors.append(f"Error retrieving application details: {error}")
            else:
                print(f"Successfully retrieved application {app_id}:")
                pprint(app_info.as_dict() if hasattr(app_info, "as_dict") else app_info)

        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
        
    # def test_get_app_score(self, fs):
    #     client = MockZDXClient(fs)
    #     errors = []

    #     try:
    #         ongoing_alerts, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

    #         if error:
    #             errors.append(f"Error listing applications: {error}")
    #             return

    #         if not ongoing_alerts or not isinstance(ongoing_alerts, list):
    #             print("No applications found within the specified time range.")
    #             return

    #         first_app_id = ongoing_alerts[0]
    #         app_id = getattr(first_app_id, "id", None)

    #         if not app_id:
    #             raise ValueError(f"App ID not found in response: {first_app_id.as_dict()}")

    #         print(f"Using App ID: {app_id}")

    #         app_info, _, error = client.zdx.apps.get_app_score(app_id=app_id)

    #         if error:
    #             errors.append(f"Error retrieving application details: {error}")
    #         else:
    #             print(f"Successfully retrieved application {app_id}:")
    #             pprint(app_info.as_dict() if hasattr(app_info, "as_dict") else app_info)

    #     except Exception as e:
    #         errors.append(f"Exception occurred: {e}")

    #     assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    # def test_get_app_metrics(self, fs):
    #     client = MockZDXClient(fs)
    #     errors = []

    #     try:
    #         ongoing_alerts, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

    #         if error:
    #             errors.append(f"Error listing applications: {error}")
    #             return

    #         if not ongoing_alerts or not isinstance(ongoing_alerts, list):
    #             print("No applications found within the specified time range.")
    #             return

    #         first_app_id = ongoing_alerts[0]
    #         app_id = getattr(first_app_id, "id", None)

    #         if not app_id:
    #             raise ValueError(f"App ID not found in response: {first_app_id.as_dict()}")

    #         print(f"Using App ID: {app_id}")

    #         app_info, _, error = client.zdx.apps.get_app_metrics(app_id=app_id)

    #         if error:
    #             errors.append(f"Error retrieving application details: {error}")
    #         else:
    #             print(f"Successfully retrieved application {app_id}:")
    #             pprint(app_info.as_dict() if hasattr(app_info, "as_dict") else app_info)

    #     except Exception as e:
    #         errors.append(f"Exception occurred: {e}")

    #     assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    # def test_list_app_users(self, fs):
    #     client = MockZDXClient(fs)
    #     errors = []

    #     try:
    #         ongoing_alerts, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

    #         if error:
    #             errors.append(f"Error listing applications: {error}")
    #             return

    #         if not ongoing_alerts or not isinstance(ongoing_alerts, list):
    #             print("No applications found within the specified time range.")
    #             return

    #         first_app_id = ongoing_alerts[0]
    #         app_id = getattr(first_app_id, "id", None)

    #         if not app_id:
    #             raise ValueError(f"App ID not found in response: {first_app_id.as_dict()}")

    #         print(f"Using App ID: {app_id}")

    #         app_info, _, error = client.zdx.apps.list_app_users(app_id=app_id)

    #         if error:
    #             errors.append(f"Error retrieving user details: {error}")
    #         else:
    #             print(f"Successfully retrieved user {app_id}:")
    #             pprint(app_info.as_dict() if hasattr(app_info, "as_dict") else app_info)

    #     except Exception as e:
    #         errors.append(f"Exception occurred: {e}")

    #     assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    # def test_get_app_user(self, fs):
    #     client = MockZDXClient(fs)
    #     errors = []

    #     try:
    #         ongoing_apps, _, error = client.zdx.apps.list_apps(query_params={"since": 2})

    #         if error:
    #             errors.append(f"Error listing applications: {error}")
    #             return

    #         if not ongoing_apps or not isinstance(ongoing_apps, list):
    #             print("No applications found within the specified time range.")
    #             return

    #         print(f"Total applications found: {len(ongoing_apps)}")

    #         first_app = ongoing_apps[0]
    #         app_id = getattr(first_app, "id", None)

    #         if not app_id:
    #             raise ValueError(f"App ID not found in response: {first_app.as_dict()}")

    #         print(f"Using App ID: {app_id}")

    #         app_users, _, error = client.zdx.apps.list_app_users(app_id=app_id)

    #         if error:
    #             errors.append(f"Error listing app users: {error}")
    #             return

    #         if not app_users or not isinstance(app_users, list):
    #             print("No app users found within the specified time range.")
    #             return

    #         print(f"Total app users found: {len(app_users)}")

    #         first_user = app_users[0]
    #         user_id = getattr(first_user, "id", None)

    #         if not user_id:
    #             raise ValueError(f"User ID not found in response: {first_user.as_dict()}")

    #         print(f"Using User ID: {user_id} for get_app_user test")

    #         app_user_info, _, error = client.zdx.apps.get_app_user(app_id=app_id, user_id=user_id)

    #         if error:
    #             errors.append(f"Error retrieving app user details: {error}")
    #         else:
    #             print(f"Successfully retrieved app user {user_id}:")
    #             pprint(app_user_info.as_dict() if hasattr(app_user_info, "as_dict") else app_user_info)

    #     except Exception as e:
    #         errors.append(f"Exception occurred: {e}")

    #     assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

