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
from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAccessPolicyReorderRule:
    """
    Integration Tests for the Access Policy Reorder Rules.
    """

    def test_reorder_access_rules(self, fs):
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

            # Step 2: Reorder the created rules
            try:
                for index, rule in enumerate(created_rules):
                    rule_id = rule["id"]
                    rule_order = index + 1
                    _, response, err = client.zpa.policies.reorder_rule(
                        policy_type="access",
                        rule_id=rule_id,
                        rule_order=str(rule_order)
                    )
                    assert err is None, f"Error reordering rule {rule_id}: {err}"
                    print(f"Reordered Rule ID: {rule_id}, Response: {response}")
            except Exception as exc:
                errors.append(f"Reordering rules failed: {exc}")

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
            assert len(errors) == 0, f"Errors occurred during the test: {errors}"
