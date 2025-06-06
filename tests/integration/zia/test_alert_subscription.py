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

from tests.integration.zia.conftest import MockZIAClient
import random


@pytest.fixture
def fs():
    yield


class TestAlertSubscription:
    """
    Integration Tests for the Alert Subscription
    """

    def test_alert_subscription(self, fs):
        client = MockZIAClient(fs)
        errors = []
        subscription_id = None
        update_subscription = None

        try:
            try:
                create_alert, _, error = client.zia.alert_subscriptions.add_alert_subscription(
                    description =f"AddedAlertSubscription_{random.randint(1000, 10000)}",
                    email = 'alert@acme.com',
                    pt0_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    secure_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    manage_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    comply_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    system_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                )
                assert error is None, f"Add Alert Subscription Error: {error}"
                assert create_alert is not None, "Subscription creation failed."
                subscription_id = create_alert.id
            except Exception as e:
                errors.append(f"Exception during add_alert_subscription: {str(e)}")

            try:
                if subscription_id:
                    update_subscription, _, error = client.zia.alert_subscriptions.update_alert_subscription(
                        subscription_id=subscription_id,
                        description =f"UpdateAlertSubscription_{random.randint(1000, 10000)}",
                        email = 'alert@acme.com',
                        pt0_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        secure_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        manage_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        comply_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        system_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    )
                    assert error is None, f"Update Alert Subscription Error: {error}"
                    assert update_subscription is not None, "Subscription update returned None."
            except Exception as e:
                errors.append(f"Exception during update_alert_subscription: {str(e)}")

            try:
                if update_subscription:
                    subscription, _, error = client.zia.alert_subscriptions.get_alert_subscription(update_subscription.id)
                    assert error is None, f"Get Alert Subscription Error: {error}"
                    assert subscription.id == subscription_id, "Retrieved subscription ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_alert_subscription: {str(e)}")

            try:
                subscriptions, _, error = client.zia.alert_subscriptions.list_alert_subscriptions()
                assert error is None, f"Error listing Alert Subscriptions: {error}"
                assert subscriptions is not None, "Alert Subscriptions list is None"
                assert any(alert.id == subscription_id for alert in subscriptions), "Newly created alert not found in the list of subscriptions."
            except Exception as exc:
                errors.append(f"Listing Alert Subscriptions failed: {exc}")


        finally:
            try:
                if update_subscription:
                    _, _, error = client.zia.alert_subscriptions.delete_alert_subscription(update_subscription.id)
                    assert error is None, f"Delete Alert Subscription Error: {error}"
            except Exception as e:
                errors.append(f"Exception during delete_alert_subscription: {str(e)}")

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
