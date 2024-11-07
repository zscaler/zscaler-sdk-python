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
        rule_type = "WEBMAIL"  # Define the rule type

        try:
            try:
                # Create a Cloud Application Rule
                rule_name = "tests-" + generate_random_string()
                created_rule = client.cloudappcontrol.add_rule(
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
                rule_id = created_rule.get("id", None)
                assert rule_id is not None, "Cloud Application Rule creation failed"
            except Exception as exc:
                errors.append(f"Cloud Application Rule creation failed: {exc}")

            try:
                # Verify the rule by retrieving it
                retrieved_rule = client.cloudappcontrol.get_rule(rule_type, rule_id)
                assert retrieved_rule["id"] == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Cloud Application Rule failed: {exc}")

            try:
                # Update the Cloud Application Rule
                updated_description = "Updated integration test Cloud Application Rule"
                client.cloudappcontrol.update_rule(
                    rule_type,
                    rule_id,
                    description=updated_description,
                )
                updated_rule = client.cloudappcontrol.get_rule(rule_type, rule_id)
                assert updated_rule["description"] == updated_description, "Cloud Application Rule update failed"
            except Exception as exc:
                errors.append(f"Updating Cloud Application Rule failed: {exc}")

            try:
                # Retrieve the list of all rules
                rules = client.cloudappcontrol.list_rules(rule_type)
                # Check if the newly created location is in the list of rules
                found_rule = any(rule["id"] == rule_id for rule in rules)
                assert found_rule, "Newly created rule not found in the list of rules."
            except Exception as exc:
                errors.append(f"Listing rules failed: {exc}")

            try:
                # Test get_rule_by_name
                first_rule_name = rules[0]["name"] if rules else None
                if first_rule_name:
                    rule_by_name = client.cloudappcontrol.get_rule_by_name(rule_type, first_rule_name)
                    assert rule_by_name is not None, "Failed to retrieve rule by name"
                    assert rule_by_name["name"] == first_rule_name, "Mismatch in rule name"
            except Exception as exc:
                errors.append(f"Retrieving rule by name failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                # Attempt to delete resources created during the test
                if rule_id:
                    delete_status = client.cloudappcontrol.delete_rule(rule_type, rule_id)
                    assert delete_status == 204, "Cloud Application Rule deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Cloud Application Rule failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the Cloud Application Rule lifecycle test: {errors}"

    def test_add_duplicate_rule(self, fs):
        client = MockZIAClient(fs)
        rule_type = "STREAMING_MEDIA"  # Define the rule type
        errors = []
        duplicate_rule_id = None

        try:
            # Step 3: List all rules for the given rule_type
            try:
                rules = client.cloudappcontrol.list_rules(rule_type)
                assert len(rules) > 0, "No rules found for the specified rule type"
                original_rule_id = rules[0]["id"]
            except Exception as exc:
                errors.append(f"Listing rules failed: {exc}")
                raise exc

            # Step 5: Add a duplicate rule using the ID from the first rule
            try:
                duplicate_rule_name = "Duplicate Streaming Media Rule"
                duplicate_rule = client.cloudappcontrol.add_duplicate_rule(
                    rule_type=rule_type,
                    rule_id=original_rule_id,
                    name=duplicate_rule_name,
                )
                duplicate_rule_id = duplicate_rule.get("id", None)
                assert duplicate_rule_id is not None, "Duplicate rule creation failed"
            except Exception as exc:
                errors.append(f"Adding duplicate rule failed: {exc}")
                raise exc

        finally:
            cleanup_errors = []
            try:
                # Attempt to delete resources created during the test
                if duplicate_rule_id:
                    delete_status = client.cloudappcontrol.delete_rule(rule_type, duplicate_rule_id)
                    assert delete_status == 204, "Duplicate rule deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting duplicate rule failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the add duplicate rule test: {errors}"

    def test_list_available_actions(self, fs):
        client = MockZIAClient(fs)
        rule_type = "STREAMING_MEDIA"  # Define the rule type
        cloud_apps = ["DROPBOX"]
        errors = []

        try:
            actions = client.cloudappcontrol.list_available_actions(rule_type, cloud_apps)
            assert actions is not None, "Failed to list available actions"
            assert isinstance(actions, list), "Response is not a list"
            assert len(actions) > 0, "No actions returned"
        except Exception as exc:
            errors.append(f"Listing available actions failed: {exc}")

        # Assert no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the test: {errors}"
