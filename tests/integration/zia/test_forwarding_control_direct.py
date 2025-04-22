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


class TestForwardingControlRulesDirect:
    """
    Integration Tests for the ZIA Forwarding Control Rules
    """

    def test_forwarding_control_direct(self, fs):
        client = MockZIAClient(fs)
        errors = []
        dst_group_id = None
        src_group_id = None
        rule_id = None

        try:
            # Step 1: Create Destination IP Group
            try:
                dst_group_name = "tests-" + generate_random_string()
                dst_group_description = "tests-" + generate_random_string()
                created_dst_group, _, error = client.zia.cloud_firewall.add_ip_destination_group(
                    name=dst_group_name,
                    description=dst_group_description,
                    type="DSTN_IP",
                    addresses=["192.168.100.4", "192.168.100.5"],
                )
                assert error is None, f"Error creating destination group: {error}"
                dst_group_id = created_dst_group.id
            except Exception as exc:
                errors.append(f"Destination IP Group creation failed: {exc}")

            # Step 2: Create Source IP Group
            try:
                src_group_name = "tests-" + generate_random_string()
                created_src_group, _, error = client.zia.cloud_firewall.add_ip_source_group(
                    name=src_group_name,
                    description="Integration test source group",
                    ip_addresses=["192.168.100.1", "192.168.100.2", "192.168.100.3"],
                )
                assert error is None, f"Error creating source group: {error}"
                src_group_id = created_src_group.id
            except Exception as exc:
                errors.append(f"Source IP Group creation failed: {exc}")

            # Step 3: Create Forwarding Control Rule
            try:
                rule_name = "tests-" + generate_random_string()
                created_rule, _, error = client.zia.forwarding_control.add_rule(
                    name=rule_name,
                    description="Integration test Forwarding Control Rule",
                    enabled=True,
                    order=1,
                    rank=7,
                    type="FORWARDING",
                    forward_method="DIRECT",
                    src_ip_groups=[src_group_id],
                    dest_ip_groups=[dst_group_id],
                )
                assert error is None, f"Error creating Forwarding Control Rule: {error}"
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Forwarding Control Rule creation failed: {exc}")

            # Step 4: Retrieve the Rule by ID
            try:
                retrieved_rule, _, error = client.zia.forwarding_control.get_rule(rule_id)
                assert error is None, f"Error retrieving rule: {error}"
                assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Forwarding Control Rule failed: {exc}")

            # Step 5: Update the Rule
            # Step 5: Update the Rule
            try:
                updated_name = "updated-" + generate_random_string()
                updated_description = "Updated integration test Forwarding Control Rule"

                updated_rule, _, error = client.zia.forwarding_control.update_rule(
                    rule_id=rule_id,
                    name=updated_name,  # ✅ REQUIRED
                    description=updated_description,
                    enabled=True,
                    order=1,
                    rank=7,
                    type="FORWARDING",
                    forward_method="DIRECT",
                )
                assert error is None, f"Error updating rule: {error}"
                assert updated_rule.description == updated_description, "Forwarding Control Rule update failed"
                assert updated_rule.name == updated_name, "Forwarding Control Rule name not updated"
            except Exception as exc:
                errors.append(f"Updating Forwarding Control Rule failed: {exc}")

            # Step 6: List rules and validate presence
            try:
                rules, _, error = client.zia.forwarding_control.list_rules()
                assert error is None, f"Error listing rules: {error}"
                assert rules is not None
                assert any(rule.id == rule_id for rule in rules), "Newly created rule not found in list"
            except Exception as exc:
                errors.append(f"Listing Forwarding Control Rules failed: {exc}")

        finally:
            cleanup_errors = []

            try:
                if rule_id:
                    _, _, error = client.zia.forwarding_control.delete_rule(rule_id)
                    assert error is None, f"Error deleting rule: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Forwarding Control Rule failed: {exc}")

            try:
                if dst_group_id:
                    _, _, error = client.zia.cloud_firewall.delete_ip_destination_group(dst_group_id)
                    assert error is None, f"Error deleting destination group: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Destination IP Group failed: {exc}")

            try:
                if src_group_id:
                    _, _, error = client.zia.cloud_firewall.delete_ip_source_group(src_group_id)
                    assert error is None, f"Error deleting source group: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Source IP Group failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
