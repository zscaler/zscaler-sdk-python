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


class TestAccessPolicyForwardingRule:
    """
    Integration Tests for the Access Policy Forwarding Rules
    """

    @pytest.mark.asyncio
    async def test_access_policy_forwarding_rules(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        rule_id = None

        try:
            # Create a Forwarding Policy Rule
            rule_name = "tests-" + generate_random_string()
            rule_description = "updated-" + generate_random_string()
            created_rule = client.policies.add_client_forwarding_rule(
                policy_type="client_forwarding",
                name=rule_name,
                description=rule_description,
                action="bypass",
            )
            assert created_rule is not None, "Failed to create Forwarding Policy Rule"
            rule_id = created_rule.get("id", None)
        except Exception as exc:
            errors.append(f"Failed to create Forwarding Policy Rule: {exc}")

        try:
            # Test listing Forwarding Policy Rules
            all_timeout_rules = client.policies.list_rules("client_forwarding")
            assert any(
                rule["id"] == rule_id for rule in all_timeout_rules
            ), "Forwarding Policy Rules not found in list"
        except Exception as exc:
            errors.append(f"Failed to list Forwarding Policy Rules: {exc}")

        try:
            # Test retrieving the specific Forwarding Policy Rule
            retrieved_rule = client.policies.get_rule("client_forwarding", rule_id)
            assert (
                retrieved_rule["id"] == rule_id
            ), "Failed to retrieve the correct Forwarding Policy Rule"
        except Exception as exc:
            errors.append(f"Failed to retrieve Forwarding Policy Rule: {exc}")

        try:
            # Update the Forwarding Policy Rule
            updated_rule_description = "Updated " + generate_random_string()
            updated_rule = client.policies.update_rule(
                policy_type="client_forwarding",
                rule_id=rule_id,
                description=updated_rule_description,
            )
            assert (
                updated_rule["description"] == updated_rule_description
            ), "Failed to update description for Forwarding Policy Rule"
        except Exception as exc:
            errors.append(f"Failed to update Forwarding Policy Rule: {exc}")

        try:
            # Cleanup: Delete the Forwarding Policy Rule
            delete_status_rule = client.policies.delete_rule(
                "client_forwarding", rule_id
            )
            assert delete_status_rule == 204, "Failed to delete Forwarding Policy Rule"
            rule_id = None  # Ensure ID is reset to prevent reattempt in cleanup
        except Exception as exc:
            errors.append(f"Failed to delete Forwarding Policy Rule: {exc}")

        # Ensure cleanup is performed even if there are errors
        if rule_id:
            try:
                client.policies.delete_rule("client_forwarding", rule_id)
            except Exception as cleanup_exc:
                errors.append(f"Cleanup failed: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during the Forwarding Policy Rule operations test: {errors}"
