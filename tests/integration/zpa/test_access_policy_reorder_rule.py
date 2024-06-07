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


class TestAccessPolicyReorderRule:
    """
    Integration Tests for the Rule Reorder
    """

    def test_reorder_access_rules(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        created_rules = []

        try:
            # Step 1: Add 5 access rules with distinct names
            for i in range(5):
                rule_name = f"New_Policy_Rule_{generate_random_string()}"
                rule_description = f"New_Policy_Rule_Description_{generate_random_string()}"
                response = client.policies.add_access_rule(name=rule_name, description=rule_description, action="allow")
                created_rules.append(response)
                # pprint(response)

            # Step 2: Reorder the created rules
            for index, rule in enumerate(created_rules):
                try:
                    rule_id = rule.id
                    rule_order = index + 1
                    client.policies.reorder_rule(policy_type="access", rule_id=rule_id, rule_order=str(rule_order))
                except Exception as exc:
                    errors.append(f"Reordering rule {rule_id} failed: {exc}")

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
