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


class TestCloudFirewallRules:
    """
    Integration Tests for the Cloud Firewall Rules API.
    """

    @pytest.mark.vcr()
    def test_cloud_firewall_rules(self, fs):
        client = MockZIAClient(fs)
        errors = []

        rule_id = None
        rule_name = "tests-" + generate_random_string()
        rule_description = "tests-" + generate_random_string()

        try:
            # Step 1: List all firewall rules
            try:
                all_rules, _, error = client.zia.cloud_firewall_rules.list_rules()
                assert error is None, f"Error listing all firewall rules: {error}"
                assert all_rules is not None, "Firewall rules list is None"
            except Exception as exc:
                errors.append(f"Failed to list all firewall rules: {exc}")

            # Step 2: List firewall rules with query params
            try:
                filtered_rules, _, error = client.zia.cloud_firewall_rules.list_rules(
                    query_params={'rule_action': 'ALLOW'}
                )
                assert error is None, f"Error listing firewall rules with filter: {error}"
            except Exception as exc:
                errors.append(f"Failed to list firewall rules with filter: {exc}")

            # Step 3: Create a firewall rule
            try:
                created_rule, _, error = client.zia.cloud_firewall_rules.add_rule(
                    name=rule_name,
                    description=rule_description,
                    enabled=True,
                    order=1,
                    rank=7,
                    action="ALLOW",
                    enable_full_logging=True,
                    src_ips=["192.168.100.0/24", "192.168.200.1"],
                    dest_addresses=["3.217.228.0-3.217.231.255"],
                    dest_countries=["COUNTRY_US"],
                    device_trust_levels=["UNKNOWN_DEVICETRUSTLEVEL", "LOW_TRUST", "MEDIUM_TRUST", "HIGH_TRUST"],
                )
                assert error is None, f"Error adding firewall rule: {error}"
                assert created_rule is not None, "Failed to create firewall rule"
                rule_id = created_rule.id
                assert created_rule.name == rule_name, "Rule name mismatch in creation"
            except Exception as exc:
                errors.append(f"Failed to add firewall rule: {exc}")

            # Step 4: Retrieve the created rule by ID
            try:
                if rule_id:
                    fetched_rule, _, error = client.zia.cloud_firewall_rules.get_rule(rule_id=rule_id)
                    assert error is None, f"Error retrieving firewall rule: {error}"
                    assert fetched_rule is not None, "Retrieved firewall rule is None"
                    assert fetched_rule.id == rule_id, "Incorrect firewall rule retrieved"
            except Exception as exc:
                errors.append(f"Failed to retrieve firewall rule: {exc}")

            # Step 5: Update the firewall rule
            try:
                if rule_id:
                    updated_name = "updated-" + generate_random_string()
                    updated_description = "updated-" + generate_random_string()
                    updated_rule, _, error = client.zia.cloud_firewall_rules.update_rule(
                        rule_id=rule_id,
                        name=updated_name,
                        description=updated_description,
                        enabled=True,
                        order=1,
                        rank=7,
                        action="ALLOW",
                        enable_full_logging=True,
                        src_ips=["192.168.100.0/24"],
                        dest_addresses=["3.217.228.0-3.217.231.255"],
                        dest_countries=["COUNTRY_US", "COUNTRY_CA"],
                        device_trust_levels=["UNKNOWN_DEVICETRUSTLEVEL", "LOW_TRUST", "MEDIUM_TRUST", "HIGH_TRUST"],
                    )
                    assert error is None, f"Error updating firewall rule: {error}"
                    assert updated_rule.name == updated_name, "Rule name mismatch after update"
            except Exception as exc:
                errors.append(f"Failed to update firewall rule: {exc}")

            # Step 6: List rules again to verify the update
            try:
                rules_after_update, _, error = client.zia.cloud_firewall_rules.list_rules()
                assert error is None, f"Error listing firewall rules after update: {error}"
                if rule_id:
                    assert any(r.id == rule_id for r in rules_after_update), "Updated rule not found in list"
            except Exception as exc:
                errors.append(f"Failed to list firewall rules after update: {exc}")

            # Step 7: List rules with pagination
            try:
                paginated_rules, _, error = client.zia.cloud_firewall_rules.list_rules(
                    query_params={'page': 1, 'page_size': 10}
                )
                assert error is None, f"Error listing firewall rules with pagination: {error}"
            except Exception as exc:
                errors.append(f"Failed to list firewall rules with pagination: {exc}")

        finally:
            # Step 8: Cleanup
            try:
                if rule_id:
                    _, _, error = client.zia.cloud_firewall_rules.delete_rule(rule_id=rule_id)
                    assert error is None, f"Error deleting firewall rule: {error}"
            except Exception as exc:
                errors.append(f"Deleting firewall rule failed: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")

