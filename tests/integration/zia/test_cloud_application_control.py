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

from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestCloudApplicationRules:
    """
    Integration Tests for the ZIA Cloud Application Rules
    """

    def test_cloud_application_rule(self, fs):
        client = MockZIAClient(fs)
        errors = []
        rule_id = None
        duplicate_rule_id = None
        rule_type = "WEBMAIL"  # Define the rule type

        try:
            try:
                # Create a Cloud Application Rule
                rule_name = "tests-" + generate_random_string()
                created_rule, _, error = client.zia.cloudappcontrol.add_rule(
                    rule_type=rule_type,
                    name=rule_name,
                    description="Integration test Cloud Application Rule",
                    order=1,
                    rank=7,
                    enabled=True,
                    actions=["ALLOW_WEBMAIL_VIEW", "ALLOW_WEBMAIL_ATTACHMENT_SEND", "ALLOW_WEBMAIL_SEND"],
                    applications=["GOOGLE_WEBMAIL", "YAHOO_WEBMAIL"],
                    device_trust_levels=["UNKNOWN_DEVICETRUSTLEVEL", "LOW_TRUST", "MEDIUM_TRUST", "HIGH_TRUST"],
                    user_agent_types=["OPERA", "FIREFOX", "MSIE", "MSEDGE", "CHROME", "SAFARI", "MSCHREDGE"],
                )
                assert error is None, f"Error creating Cloud App Rule: {error}"
                rule_id = created_rule.id
                assert rule_id is not None, "Cloud Application Rule creation failed"
            except Exception as exc:
                errors.append(f"Cloud Application Rule creation failed: {exc}")

            try:
                # Duplicate the Cloud Application Rule
                duplicate_rule_name = "tests-" + generate_random_string()
                duplicate_rule, _, error = client.zia.cloudappcontrol.add_duplicate_rule(
                    rule_type=rule_type, rule_id=rule_id, name=duplicate_rule_name
                )
                assert error is None, f"Error duplicating Cloud App Rule: {error}"
                duplicate_rule_id = duplicate_rule.id
                assert duplicate_rule_id is not None, "Duplicate Cloud Application Rule creation failed"
            except Exception as exc:
                errors.append(f"Duplicating Cloud Application Rule failed: {exc}")

            try:
                # Verify the rule by retrieving it
                retrieved_rule, _, error = client.zia.cloudappcontrol.get_rule(rule_type, rule_id)
                assert error is None, f"Error retrieving Cloud App Rule: {error}"
                assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Cloud Application Rule failed: {exc}")

            try:
                # Update the Cloud Application Rule
                updated_description = "Updated integration test Cloud Application Rule"
                _, _, error = client.zia.cloudappcontrol.update_rule(
                    rule_type, rule_id, description=updated_description
                )
                assert error is None, f"Error updating Cloud App Rule: {error}"

                updated_rule, _, error = client.zia.cloudappcontrol.get_rule(rule_type, rule_id)
                assert error is None, f"Error retrieving updated Cloud App Rule: {error}"
                assert updated_rule.description == updated_description, "Cloud Application Rule update failed"
            except Exception as exc:
                errors.append(f"Updating Cloud Application Rule failed: {exc}")

            try:
                rules, _, error = client.zia.cloudappcontrol.list_rules(rule_type)
                assert error is None, f"Error listing rules: {error}"
                assert isinstance(rules, list), "Expected a list of rules"
                assert len(rules) > 0, "No rules found for the specified rule type"
            except Exception as exc:
                errors.append(f"Listing rules failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                if rule_id:
                    delete_status, _ = client.zia.cloudappcontrol.delete_rule(rule_type, rule_id)
                    assert delete_status == 204, "Cloud Application Rule deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Cloud Application Rule failed: {exc}")

            try:
                if duplicate_rule_id:
                    delete_status, _ = client.zia.cloudappcontrol.delete_rule(rule_type, duplicate_rule_id)
                    assert delete_status == 204, "Duplicate rule deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting duplicate rule failed: {exc}")

            errors.extend(cleanup_errors)

    def test_list_available_actions(self, fs):
        client = MockZIAClient(fs)
        rule_type = "STREAMING_MEDIA"  # Define the rule type
        cloud_apps = ["DROPBOX"]
        errors = []

        try:
            actions, response, error = client.zia.cloudappcontrol.list_available_actions(rule_type, cloud_apps)

            # Check for errors
            assert error is None, f"API returned an error: {error}"
            assert actions is not None, f"Failed to list available actions: {actions}"
            assert isinstance(actions, list), f"Response is not a list: {actions}"
            assert len(actions) > 0, "No actions returned"
        except Exception as exc:
            errors.append(f"Listing available actions failed: {exc}")

        # Assert no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the test: {errors}"
