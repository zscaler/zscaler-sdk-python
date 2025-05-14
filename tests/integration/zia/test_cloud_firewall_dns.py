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


class TestCloudFirewallDNSRules:
    """
    Integration Tests for the ZIA Cloud Firewall DNS Rules
    """

    def test_firewall_dns_rule(self, fs):
        client = MockZIAClient(fs)
        errors = []
        rule_id = None

        try:

            # Step 3: Create a Firewall Rule
            try:
                rule_name = "tests-" + generate_random_string()
                created_rule, _, error = client.zia.cloud_firewall_dns.add_rule(
                    name=rule_name,
                    description="Integration test firewall rule",
                    enabled=True,
                    order=1,
                    rank=7,
                    action='REDIR_REQ',
                    redirect_ip='8.8.8.8',
                    dest_countries=["COUNTRY_CA", "COUNTRY_MX", "COUNTRY_AU", "COUNTRY_GB"],
                    source_countries=["COUNTRY_CA", "COUNTRY_MX", "COUNTRY_AU", "COUNTRY_GB"],
                    protocols=["ANY_RULE"],
                )
                assert error is None, f"Firewall Rule creation failed: {error}"
                assert created_rule is not None, "Firewall Rule creation returned None"
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Firewall Rule creation failed: {exc}")

            # Step 4: Retrieve the Firewall Rule by ID
            try:
                retrieved_rule, _, error = client.zia.cloud_firewall_dns.get_rule(rule_id)
                assert error is None, f"Error retrieving Firewall Rule: {error}"
                assert retrieved_rule is not None, "Retrieved Firewall Rule is None"
                assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Firewall Rule failed: {exc}")

            # Step 5: Update the Firewall Rule
            try:
                updated_description = "Updated integration test firewall dns rule"
                updated_rule, _, error = client.zia.cloud_firewall_dns.update_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    enabled=True,
                    order=1,
                    rank=7,
                    action='REDIR_REQ',
                    redirect_ip='8.8.8.8',
                    dest_countries=["COUNTRY_CA", "COUNTRY_MX", "COUNTRY_AU", "COUNTRY_GB"],
                    source_countries=["COUNTRY_CA", "COUNTRY_MX", "COUNTRY_AU", "COUNTRY_GB"],
                    protocols=["ANY_RULE"],
                )
                assert error is None, f"Error updating Firewall DNS Rule: {error}"
                assert updated_rule is not None, "Updated Firewall DNS Rule is None"
                assert (
                    updated_rule.description == updated_description
                ), f"Firewall DNS Rule update failed: {updated_rule.as_dict()}"
            except Exception as exc:
                errors.append(f"Updating Firewall DNS Rule failed: {exc}")

            # Step 6: List Firewall DNS Rules and verify the rule is present
            try:
                rules, _, error = client.zia.cloud_firewall_dns.list_rules()
                assert error is None, f"Error listing Firewall DNS Rules: {error}"
                assert rules is not None, "Firewall DNS Rules list is None"
                assert any(rule.id == rule_id for rule in rules), "Newly created rule not found in the list of rules."
            except Exception as exc:
                errors.append(f"Listing Firewall DNS Rules failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                if rule_id:
                    # Delete the firewall rule
                    _, _, error = client.zia.cloud_firewall_dns.delete_rule(rule_id)
                    assert error is None, f"Error deleting Firewall DNS Rule: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Firewall DNS Rule failed: {exc}")

            errors.extend(cleanup_errors)

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
