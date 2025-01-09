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
from pprint import pprint
from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAccessPolicyBulkReorderRule:
    """
    Integration Tests for the Access Policy Bulk Reorder Rules.
    """

    def test_bulk_reorder_access_rules(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        created_rules = []  # Store created rule objects

        try:
            # Step 1: Add 5 access rules with distinct names
            try:
                for i in range(5):
                    rule_name = f"tests-{generate_random_string()}"
                    rule_description = f"tests-{generate_random_string()}"
                    created_rule, _, err = client.zpa.policies.add_access_rule(
                        name=rule_name,
                        description=rule_description,
                        action="allow"
                    )
                    assert err is None, f"Error creating access rule: {err}"
                    assert created_rule is not None, "Created rule is None"
                    created_rules.append(created_rule.as_dict())  # Store as dictionaries for consistency
                    print(f"Created Rule: {created_rule.as_dict()}")
            except Exception as exc:
                errors.append(f"Failed to create access rules: {exc}")

            # Step 2: List all access rules
            all_rule_ids = []
            try:
                all_rules, _, err = client.zpa.policies.list_rules(policy_type="access")
                assert err is None, f"Error listing access rules: {err}"
                assert all_rules is not None, "No rules returned from list_rules"
                all_rules = [rule.as_dict() if hasattr(rule, "as_dict") else rule for rule in all_rules]
                all_rule_ids = [rule["id"] for rule in all_rules]
                print(f"All Rules: {all_rules}")
            except Exception as exc:
                errors.append(f"Listing Access Rules failed: {exc}")

            # Step 3: Reverse the order of the created rules within the full list of rule IDs
            try:
                created_rule_ids = [rule["id"] for rule in created_rules]
                reversed_rule_ids = created_rule_ids[::-1]

                # Update the full list of rule IDs to reflect the reversed order
                for rule_id in created_rule_ids:
                    if rule_id in all_rule_ids:
                        all_rule_ids.remove(rule_id)
                    else:
                        raise ValueError(f"Rule ID {rule_id} not found in all_rule_ids.")
                new_rule_order = reversed_rule_ids + all_rule_ids
            except Exception as exc:
                errors.append(f"Reversing rule order failed: {exc}")

            # Step 4: Bulk reorder the rules
            try:
                _, _, err = client.zpa.policies.bulk_reorder_rules(
                    policy_type="access",
                    rules_orders=new_rule_order
                )
                assert err is None, f"Error reordering access rules: {err}"
                print(f"Rules reordered successfully: {reversed_rule_ids}")
            except Exception as exc:
                errors.append(f"Bulk reordering rules failed: {exc}")

            # Step 5: Verify the order by listing the rules again
            try:
                reordered_rules, _, err = client.zpa.policies.list_rules(policy_type="access")
                assert err is None, f"Error listing reordered rules: {err}"
                reordered_rules = [
                    rule.as_dict() if hasattr(rule, "as_dict") else rule for rule in reordered_rules
                ]
                reordered_rule_ids = [rule["id"] for rule in reordered_rules]

                # Validate if the top N rule IDs match the reversed order of the created rules
                assert reordered_rule_ids[:5] == reversed_rule_ids, (
                    "Rules were not reordered correctly"
                )
                print(f"Reordered Rules: {reordered_rules[:5]}")
            except Exception as exc:
                errors.append(f"Reordered rules validation failed: {exc}")

        finally:
            # Clean up: Delete the created rules
            for rule in created_rules:
                try:
                    _, _, err = client.zpa.policies.delete_rule(policy_type="access", rule_id=rule["id"])
                    assert err is None, f"Error deleting rule {rule['id']}: {err}"
                    print(f"Rule deleted successfully with ID: {rule['id']}")
                except Exception as exc:
                    errors.append(f"Cleanup failed for rule ID {rule['id']}: {exc}")

            # Assert that no errors occurred during the process
            assert len(errors) == 0, f"Errors occurred during the bulk reorder test: {errors}"
