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
            try:
                # Prerequisite: Create a Destination IP Group
                dst_group_name = "tests-" + generate_random_string()
                dst_group_description = "tests-" + generate_random_string()
                created_dst_group = client.firewall.add_ip_destination_group(
                    name=dst_group_name,
                    description=dst_group_description,
                    type="DSTN_IP",
                    addresses=["192.168.100.4", "192.168.100.5"],
                )
                dst_group_id = created_dst_group.get("id", None)
                assert dst_group_id is not None, "Destination IP Group creation failed"
            except Exception as exc:
                errors.append(f"Destination IP Group creation failed: {exc}")

            try:
                # Prerequisite: Create a Source IP Group
                src_group_name = "tests-" + generate_random_string()
                created_src_group = client.firewall.add_ip_source_group(
                    name=src_group_name,
                    description="Integration test source group",
                    ip_addresses=["192.168.100.1", "192.168.100.2", "192.168.100.3"],
                )
                src_group_id = created_src_group.get("id", None)
                assert src_group_id is not None, "Source IP Group creation failed"
            except Exception as exc:
                errors.append(f"Source IP Group creation failed: {exc}")

            try:
                # Create a Firewall Rule
                rule_name = "tests-" + generate_random_string()
                created_rule = client.forwarding_control.add_rule(
                    name=rule_name,
                    description='Integration test Forwarding Control Rule',
                    state=True,
                    order=1,
                    rank=7,
                    type='FORWARDING',
                    forward_method='DIRECT',
                    groups=['76662385'],
                    src_ip_groups=[src_group_id],
                    dest_ip_groups=[dst_group_id],
                )
                rule_id = created_rule.get("id", None)
                assert rule_id is not None, "Forwarding Control Rule creation failed"
            except Exception as exc:
                errors.append(f"Forwarding Control Rule creation failed: {exc}")

            try:
                # Verify the rule by retrieving it
                retrieved_rule = client.forwarding_control.get_rule(rule_id)
                assert retrieved_rule["id"] == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Forwarding Control Rule failed: {exc}")

            try:
                # Update the Forwarding Control Rule
                updated_description = "Updated integration test Forwarding Control Rule"
                client.forwarding_control.update_rule(
                    rule_id,
                    description=updated_description,
                )
                updated_rule = client.forwarding_control.get_rule(rule_id)
                assert updated_rule["description"] == updated_description, "Forwarding Control Rule update failed"
            except Exception as exc:
                errors.append(f"Updating Forwarding Control Rule failed: {exc}")

            try:
                # Retrieve the list of all rules
                rules = client.forwarding_control.list_rules()
                # Check if the newly created location is in the list of rules
                found_rule = any(rule["id"] == rule_id for rule in rules)
                assert found_rule, "Newly created rule not found in the list of rules."
            except Exception as exc:
                errors.append(f"Listing rules failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                # Attempt to delete resources created during the test
                if rule_id:
                    delete_status = client.forwarding_control.delete_rule(rule_id)
                    assert delete_status == 204, "Forwarding Control Rule deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Forwarding Control Rule failed: {exc}")

            try:
                if dst_group_id:
                    client.firewall.delete_ip_destination_group(dst_group_id)
            except Exception as exc:
                cleanup_errors.append(f"Deleting Destination IP Group failed: {exc}")

            try:
                if src_group_id:
                    client.firewall.delete_ip_source_group(src_group_id)
            except Exception as exc:
                cleanup_errors.append(f"Deleting Source IP Group failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the firewall rule lifecycle test: {errors}"