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


class TestAccessPolicyTimeoutRule:
    """
    Integration Tests for the Access Policy Timeout Rules
    """

    @pytest.mark.asyncio
    async def test_access_policy_timeout_policy_rules(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        rule_id = None

        try:
            # Create a Timeout Policy Rule
            rule_name = "tests-" + generate_random_string()
            rule_description = "updated-" + generate_random_string()
            created_rule = client.policies.add_timeout_rule(
                policy_type="timeout",
                name=rule_name,
                description=rule_description,
                action="RE_AUTH",
                re_auth_idle_timeout="2592000",
                re_auth_timeout="3456000",
            )
            assert created_rule is not None, "Failed to create Timeout Policy Rule"
            rule_id = created_rule.get("id", None)
        except Exception as exc:
            errors.append(f"Failed to create Timeout Policy Rule: {exc}")

        try:
            # Test listing Timeout Policy Rules
            all_timeout_rules = client.policies.list_rules("timeout")
            assert any(
                rule["id"] == rule_id for rule in all_timeout_rules
            ), "Timeout Policy Rules not found in list"
        except Exception as exc:
            errors.append(f"Failed to list Timeout Policy Rules: {exc}")

        try:
            # Test retrieving the specific Timeout Policy Rule
            retrieved_rule = client.policies.get_rule("timeout", rule_id)
            assert (
                retrieved_rule["id"] == rule_id
            ), "Failed to retrieve the correct Timeout Policy Rule"
        except Exception as exc:
            errors.append(f"Failed to retrieve Timeout Policy Rule: {exc}")

        try:
            # Update the Timeout Policy Rule
            updated_rule_description = "Updated " + generate_random_string()
            updated_rule = client.policies.update_rule(
                policy_type="timeout",
                rule_id=rule_id,
                description=updated_rule_description,
            )
            assert (
                updated_rule["description"] == updated_rule_description
            ), "Failed to update description for Timeout Policy Rule"
        except Exception as exc:
            errors.append(f"Failed to update Timeout Policy Rule: {exc}")

        try:
            # Cleanup: Delete the Timeout Policy Rule
            delete_status_rule = client.policies.delete_rule("timeout", rule_id)
            assert delete_status_rule == 204, "Failed to delete Timeout Policy Rule"
            rule_id = None  # Ensure ID is reset to prevent reattempt in cleanup
        except Exception as exc:
            errors.append(f"Failed to delete Timeout Policy Rule: {exc}")

        # Ensure cleanup is performed even if there are errors
        if rule_id:
            try:
                client.policies.delete_rule("timeout", rule_id)
            except Exception as cleanup_exc:
                errors.append(f"Cleanup failed: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during the timeout policy rule operations test: {errors}"
