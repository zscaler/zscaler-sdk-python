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

class TestFirewallRules:
    """
    Integration Tests for the ZIA Firewall Rules
    """

    @pytest.mark.asyncio
    async def test_firewall_rule(self, fs):
        client = MockZIAClient(fs)
        errors = []

        dst_group_id = None
        src_group_id = None
        rule_id = None

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

            # Prerequisite: Create a Source IP Group
            src_group_name = "tests-" + generate_random_string()
            src_group_description = "tests-" + generate_random_string()
            created_src_group = client.firewall.add_ip_source_group(
                name=src_group_name,
                description=src_group_description,
                ip_addresses=["192.168.100.1", "192.168.100.2", "192.168.100.3"],
            )
            src_group_id = created_src_group.get("id", None)

            # Create a Firewall Rule
            rule_name = "tests-" + generate_random_string()
            rule_description = "tests-" + generate_random_string()
            created_rule = client.firewall.add_rule(
                name=rule_name,
                description=rule_description,
                state='ENABLED',
                action='BLOCK_DROP',
                order=1,
                rank=7,
                src_ip_groups=[src_group_id],
                dest_ip_groups=[dst_group_id],
            )
            rule_id = created_rule.get("id", None)

            # Retrieve the specific cloud firewall rule
            retrieved_rule = client.firewall.get_rule(rule_id)
            assert retrieved_rule["id"] == rule_id, "Failed to retrieve the correct cloud firewall rule"

            # Update the cloud firewall rule
            updated_description = "Updated " + generate_random_string()
            updated_rule = client.firewall.update_rule(
                rule_id,
                description=updated_description,
            )
            assert updated_rule["description"] == updated_description, "Failed to update description for cloud firewall rule"

            # List static ips and ensure the updated static ip is in the list
            ip_list = client.firewall.list_rules()
            assert any(ip["id"] == rule_id for ip in ip_list), "Updated firewall rule not found in list"

        except Exception as exc:
            errors.append(exc)

        finally:
            # Cleanup
            cleanup_errors = []
            if rule_id:
                try:
                    delete_response_code = client.firewall.delete_rule(rule_id)
                    assert delete_response_code == 204, "Failed to delete cloud firewall rule"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting cloud firewall rule failed: {exc}")

            if dst_group_id:
                try:
                    client.firewall.delete_ip_destination_group(dst_group_id)
                except Exception as exc:
                    cleanup_errors.append(f"Cleanup failed for IP Destination Group: {exc}")

            if src_group_id:
                try:
                    client.firewall.delete_ip_source_group(src_group_id)
                except Exception as exc:
                    cleanup_errors.append(f"Cleanup failed for IP Source Group: {exc}")

            errors.extend(cleanup_errors)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the firewall rule lifecycle test: {errors}"
