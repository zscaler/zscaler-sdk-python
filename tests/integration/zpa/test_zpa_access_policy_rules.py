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

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAccessPolicyRule:
    """
    Integration Tests for the Access Policy Rules
    """

    @pytest.mark.asyncio
    async def test_access_policy_rules(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        connector_group_id = None
        rule_id = None

        try:
            # Prerequisite: Create an App Connector Group
            connector_group_name = "tests-" + generate_random_string()
            connector_group_description = "Integration test for connector group"
            created_connector_group = client.connectors.add_connector_group(
                name=connector_group_name,
                description=connector_group_description,
                enabled=True,
                latitude="37.3382082",
                longitude="-121.8863286",
                location="San Jose, CA, USA",
                upgrade_day="SUNDAY",
                upgrade_time_in_secs="66600",
                override_version_profile=True,
                version_profile_name="Default",
                version_profile_id="0",
                dns_query_type="IPV4_IPV6",
                pra_enabled=True,
                tcp_quick_ack_app=True,
                tcp_quick_ack_assistant=True,
                tcp_quick_ack_read_assistant=True,
            )
            connector_group_id = created_connector_group.get("id", None)
        except Exception as exc:
            errors.append(f"Creating App Connector Group failed: {exc}")

        try:
            # Create an Access Policy Rule
            rule_name = "tests-" + generate_random_string()
            rule_description = "Integration test for access policy rule"
            created_rule = client.policies.add_access_rule(
                policy_type="access",
                name=rule_name,
                description=rule_description,
                action="allow",
                app_connector_group_ids=[connector_group_id],
            )
            rule_id = created_rule.get("id", None)
        except Exception as exc:
            errors.append(f"Creating Access Policy Rule failed: {exc}")

        try:
            # Test listing access policy rules
            all_access_rules = client.policies.list_rules("access")
            if not any(rule["id"] == rule_id for rule in all_access_rules):
                raise AssertionError("Access Policy rules not found in list")
        except Exception as exc:
            errors.append(f"Listing Access Policy Rules failed: {exc}")

        try:
            # Test retrieving the specific Access Policy Rule
            retrieved_rule = client.policies.get_rule("access", rule_id)
            if retrieved_rule["id"] != rule_id:
                raise AssertionError(
                    "Failed to retrieve the correct Access Policy Rule"
                )
        except Exception as exc:
            errors.append(f"Retrieving Access Policy Rule failed: {exc}")

        try:
            # Update the Access Policy Rule
            updated_rule_description = "Updated " + generate_random_string()
            updated_rule = client.policies.update_access_rule(
                policy_type="access",
                rule_id=rule_id,
                description=updated_rule_description,
            )
            if updated_rule["description"] != updated_rule_description:
                raise AssertionError(
                    "Failed to update description for Access Policy Rule"
                )
        except Exception as exc:
            errors.append(f"Updating Access Policy Rule failed: {exc}")

        # Cleanup
        if rule_id:
            try:
                # Cleanup: Delete the Access Policy Rule
                delete_status_rule = client.policies.delete_rule("access", rule_id)
                if delete_status_rule != 204:
                    raise AssertionError("Failed to delete Access Policy Rule")
            except Exception as exc:
                errors.append(f"Deleting Access Policy Rule failed: {exc}")

        if connector_group_id:
            try:
                client.connectors.delete_connector_group(connector_group_id)
            except Exception as exc:
                errors.append(f"Cleanup failed for Connector Group: {exc}")

        assert (
            len(errors) == 0
        ), f"Errors occurred during the Access Policy Rule operations test: {errors}"
