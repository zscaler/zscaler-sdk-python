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

from tests.integration.zia.conftest import MockZIAClient, NameGenerator


@pytest.fixture
def fs():
    yield


class TestAlertSubscription:
    """
    Integration Tests for the Alert Subscription
    """

    @pytest.mark.vcr()
    def test_alert_subscription(self, fs):
        client = MockZIAClient(fs)
        errors = []
        subscription_id = None
        update_subscription = None
        
        # Use deterministic names for VCR
        names = NameGenerator("alert-subscription")

        try:
            try:
                create_alert = client.zia.alert_subscriptions.add_alert_subscription(
                    description=names.description,
                    email='alert@acme.com',
                    pt0_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    secure_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    manage_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    comply_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    system_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                )
                assert create_alert is not None, "Subscription creation failed."
                subscription_id = create_alert.id
            except Exception as e:
                errors.append(f"Exception during add_alert_subscription: {str(e)}")

            try:
                if subscription_id:
                    update_subscription = client.zia.alert_subscriptions.update_alert_subscription(
                        subscription_id=subscription_id,
                        description=names.updated_description,
                        email='alert@acme.com',
                        pt0_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        secure_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        manage_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        comply_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                        system_severities=["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
                    )
                    assert update_subscription is not None, "Subscription update returned None."
            except Exception as e:
                errors.append(f"Exception during update_alert_subscription: {str(e)}")

            try:
                if update_subscription:
                    subscription = client.zia.alert_subscriptions.get_alert_subscription(update_subscription.id)
                    assert subscription.id == subscription_id, "Retrieved subscription ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_alert_subscription: {str(e)}")

            try:
                subscriptions = client.zia.alert_subscriptions.list_alert_subscriptions()
                assert subscriptions is not None, "Alert Subscriptions list is None"
                assert any(alert.id == subscription_id for alert in subscriptions), "Newly created alert not found in the list of subscriptions."
            except Exception as exc:
                errors.append(f"Listing Alert Subscriptions failed: {exc}")


        finally:
            try:
                if update_subscription:
                    _ = client.zia.alert_subscriptions.delete_alert_subscription(update_subscription.id)
            except Exception as e:
                errors.append(f"Exception during delete_alert_subscription: {str(e)}")

        if errors:
            pytest.fail(f"Test failed with errors: {errors}")
