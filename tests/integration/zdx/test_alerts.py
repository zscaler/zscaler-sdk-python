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


class TestAlerts:
    """
    Integration Tests for the alerts
    """

    def test_list_ongoing(self, fs):
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

            ongoing_alerts = client.alerts.list_ongoing(**kwargs)
            alerts = list(ongoing_alerts)

            if not alerts:
                print("No ongoing alerts found within the specified time range.")
            else:
                print(f"Retrieved {len(alerts)} ongoing alerts")
                for alert in alerts:
                    pprint(alert)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_historical(self, fs):
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

            historical_alerts = client.alerts.list_historical(**kwargs)
            alerts = list(historical_alerts)

            if not alerts:
                print("No historical alerts found within the specified time range.")
            else:
                print(f"Retrieved {len(alerts)} historical alerts")
                for alert in alerts:
                    pprint(alert)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_get_alert(self, fs):
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

            # List ongoing alerts to get an alert ID
            ongoing_alerts = client.alerts.list_ongoing(**kwargs)
            alerts = list(ongoing_alerts)

            if not alerts:
                print("No ongoing alerts found within the specified time range.")
            else:
                alert_id = alerts[0].id
                print(f"Using alert ID {alert_id} for get_alert test")

                # Get alert information using the retrieved alert ID
                alert_info = client.alerts.get_alert(alert_id=alert_id, **kwargs)
                pprint(alert_info)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_affected_devices(self, fs):
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

            # List ongoing alerts to get an alert ID
            ongoing_alerts = client.alerts.list_ongoing(**kwargs)
            alerts = list(ongoing_alerts)

            if not alerts:
                print("No ongoing alerts found within the specified time range.")
            else:
                alert_id = alerts[0].id
                print(f"Using alert ID {alert_id} for list_affected_devices test")

                # List affected devices using the retrieved alert ID
                affected_devices = client.alerts.list_affected_devices(alert_id=alert_id, **kwargs)
                devices = list(affected_devices)

                if not devices:
                    print("No affected devices found within the specified time range.")
                else:
                    print(f"Retrieved {len(devices)} affected devices")
                    for device in devices:
                        pprint(device)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
