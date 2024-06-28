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


class TestApplications:
    """
    Integration Tests for the applications
    """

    def test_list_applications(self, fs):
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

            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not apps:
                print("No applications found within the specified time range.")
            else:
                print(f"Retrieved {len(apps)} applications")
                for app in apps:
                    pprint(app)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_app(self, fs):
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

            # List applications to get an app ID
            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not apps:
                print("No applications found within the specified time range.")
            else:
                app_id = apps[0].id
                print(f"Using app ID {app_id} for get_app test")

                # Get app information using the retrieved app ID
                app_info = client.apps.get_app(app_id=app_id, **kwargs)
                pprint(app_info)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_app_score(self, fs):
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

            # List applications to get an app ID
            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not apps:
                print("No applications found within the specified time range.")
            else:
                app_id = apps[0].id
                print(f"Using app ID {app_id} for get_app_score test")

                # Get app score using the retrieved app ID
                app_score = client.apps.get_app_score(app_id=app_id, **kwargs)
                pprint(app_score)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_app_metrics(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {"from_time": from_time, "to": to_time, "metric_name": "dns"}

            # List applications to get an app ID
            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not apps:
                print("No applications found within the specified time range.")
            else:
                app_id = apps[0].id
                print(f"Using app ID {app_id} for get_app_metrics test")

                # Get app metrics using the retrieved app ID
                app_metrics = client.apps.get_app_metrics(app_id=app_id, **kwargs)
                pprint(app_metrics)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_app_users(self, fs):
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

            # List applications to get an app ID
            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not apps:
                print("No applications found within the specified time range.")
            else:
                app_id = apps[0].id
                print(f"Using app ID {app_id} for list_app_users test")

                # List app users using the retrieved app ID
                app_users = client.apps.list_app_users(app_id=app_id, **kwargs)
                if not app_users:
                    print("No app users found within the specified time range.")
                else:
                    print(f"Retrieved {len(app_users)} app users")
                    for user in app_users:
                        pprint(user)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_app_user(self, fs):
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

            # List applications to get an app ID
            apps_iterator = client.apps.list_apps(**kwargs)
            apps = list(apps_iterator)

            if not apps:
                print("No applications found within the specified time range.")
            else:
                app_id = apps[0].id
                print(f"Using app ID {app_id} for get_app_user test")

                # List app users to get a user ID
                app_users = client.apps.list_app_users(app_id=app_id, **kwargs)
                if not app_users:
                    print("No app users found within the specified time range.")
                else:
                    user_id = app_users[0].id
                    print(f"Using user ID {user_id} for get_app_user test")

                    # Get app user information using the retrieved app and user IDs
                    app_user_info = client.apps.get_app_user(app_id=app_id, user_id=user_id, **kwargs)
                    pprint(app_user_info)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
