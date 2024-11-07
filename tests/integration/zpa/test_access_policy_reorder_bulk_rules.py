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
from pprint import pprint
from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAccessPolicyBulkReorderRule:
    """
    Integration Tests for the Rule Reorder
    """

    def test_bulk_reorder_access_rules(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        created_rules = []

        try:
            # Step 1: Add 5 access rules with distinct names
            for i in range(5):
                rule_name = f"tests-{generate_random_string()}"
                rule_description = f"tests-{generate_random_string()}"
                response = client.policies.add_access_rule(name=rule_name, description=rule_description, action="allow")
                created_rules.append(response)
                pprint(response)

            # Step 2: List the created rules
            all_rules = client.policies.list_rules(policy_type="access")
            all_rule_ids = [rule.id for rule in all_rules]

            # Identify the IDs of the newly created rules
            created_rule_ids = [rule.id for rule in created_rules]

            # Step 3: Reverse the order of the created rules within the full list of rule IDs
            reversed_rule_ids = created_rule_ids[::-1]

            # Step 4: Update the full list of rule IDs to reflect the reversed order of the newly created rules
            for rule_id in created_rule_ids:
                all_rule_ids.remove(rule_id)

            new_rule_order = reversed_rule_ids + all_rule_ids

            # Step 5: Bulk reorder the rules
            client.policies.bulk_reorder_rules(policy_type="access", rules_orders=new_rule_order)

            # Verify the order by listing the rules again
            reordered_rules = client.policies.list_rules(policy_type="access")
            reordered_rule_ids = [rule.id for rule in reordered_rules]

            # Check if the top N rule IDs match the reversed order of the created rules
            assert reordered_rule_ids[:5] == reversed_rule_ids, "Rules were not reordered correctly"

        except Exception as exc:
            errors.append(f"Error during rule creation or reordering: {exc}")

        finally:
            # Clean up: delete the created rules
            for rule in created_rules:
                try:
                    client.policies.delete_rule(policy_type="access", rule_id=rule.id)
                except Exception as exc:
                    errors.append(f"Deleting rule {rule.id} failed: {exc}")

            # Assert that no errors occurred during the process
            assert len(errors) == 0, f"Errors occurred during the test: {errors}"
