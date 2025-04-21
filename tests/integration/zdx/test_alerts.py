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


class TestAlerts:
    """
    Integration Tests for the alerts
    """

    def test_list_ongoing(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            ongoing_alerts = client.zdx.alerts.list_ongoing(query_params={"since": 2})
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
            historical_alerts = client.zdx.alerts.list_historical(query_params={"since": 2})
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
            ongoing_alerts, _, error = client.zdx.alerts.list_ongoing(query_params={"since": 2})

            if error:
                errors.append(f"Error listing ongoing alerts: {error}")
                return

            if not ongoing_alerts or not isinstance(ongoing_alerts, list):
                print("No ongoing alerts found within the specified time range.")
                return

            first_alert = ongoing_alerts[0]
            alert_id = getattr(first_alert, "id", None)

            if not alert_id:
                raise ValueError(f"Alert ID not found in response: {first_alert.as_dict()}")

            print(f"Using Alert ID: {alert_id}")

            alert_info, _, error = client.zdx.alerts.get_alert(alert_id=alert_id)

            if error:
                errors.append(f"Error retrieving alert details: {error}")
            else:
                print(f"Successfully retrieved alert {alert_id}:")
                pprint(alert_info.as_dict() if hasattr(alert_info, "as_dict") else alert_info)

        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    def test_list_affected_devices(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            ongoing_alerts, _, error = client.zdx.alerts.list_ongoing(query_params={"since": 2})

            if error:
                errors.append(f"Error listing ongoing alerts: {error}")
                return

            if not ongoing_alerts or not isinstance(ongoing_alerts, list):
                print("No ongoing alerts found within the specified time range.")
                return

            first_alert = ongoing_alerts[0]
            alert_id = getattr(first_alert, "id", None)

            if not alert_id:
                raise ValueError(f"Alert ID not found in response: {first_alert.as_dict()}")

            print(f"Using Alert ID: {alert_id}")

            # List affected devices using the retrieved alert ID
            affected_devices = client.zdx.alerts.list_affected_devices(alert_id=alert_id)
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
