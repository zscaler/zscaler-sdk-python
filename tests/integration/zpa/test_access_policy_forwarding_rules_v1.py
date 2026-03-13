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


class TestAccessPolicyForwardingRuleV1:
    """
    Integration Tests for the Client Forwarding Policy Rules V1
    """

    @pytest.mark.vcr()
    def test_access_policy_forwarding_rules_v1(self, fs):
        client = MockZPAClient(fs)
        errors = []
        rule_id = None

        try:
            # Step 1: Create Access Policy Forwarding Rule
            try:
                rule_name = "tests-apfr1-" + generate_random_string()
                rule_description = "Integration test Client Forwarding Rule V1"
                created_rule, _, err = client.zpa.policies.add_client_forwarding_rule(
                    name=rule_name,
                    description=rule_description,
                    action="intercept",
                    conditions=[
                        ("client_type", "id", "zpn_client_type_exporter"),
                        ("client_type", "id", "zpn_client_type_zapp"),
                    ],
                )
                assert err is None, f"Error creating forwarding rule: {err}"
                assert created_rule is not None
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Access Policy Rule creation failed: {exc}")

            # Step 2: Get Rule by ID
            try:
                retrieved_rule, _, err = client.zpa.policies.get_rule("client_forwarding", rule_id)
                assert err is None, f"Error retrieving rule: {err}"
                assert retrieved_rule.id == rule_id, "Retrieved rule ID mismatch"
            except Exception as exc:
                errors.append(f"Access Policy Rule retrieval failed: {exc}")

            # Step 3: Update Rule
            try:
                updated_description = "Updated forwarding rule " + generate_random_string()
                _, _, err = client.zpa.policies.update_client_forwarding_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    action="intercept",
                    conditions=[
                        ("client_type", "id", "zpn_client_type_exporter"),
                        ("client_type", "id", "zpn_client_type_zapp"),
                    ],
                )
                if err and str(err) != "Response is None":
                    raise AssertionError(f"Unexpected update error: {err}")
            except Exception as exc:
                errors.append(f"Access Policy Rule update failed: {exc}")

            # Step 4: List Rules and Confirm Presence
            try:
                rules, _, err = client.zpa.policies.list_rules("client_forwarding")
                assert err is None, f"Error listing rules: {err}"
                assert any(r.id == rule_id for r in rules), "Created rule not found in rule list"
            except Exception as exc:
                errors.append(f"Access Policy Rule list verification failed: {exc}")

        finally:
            cleanup_errors = []
            if rule_id:
                try:
                    _, _, err = client.zpa.policies.delete_rule("client_forwarding", rule_id)
                    assert err is None, f"Error deleting rule: {err}"
                except Exception as exc:
                    cleanup_errors.append(f"Failed to delete rule ID {rule_id}: {exc}")

            errors.extend(cleanup_errors)

        assert not errors, f"Errors occurred during Access Policy Rule test:\n{chr(10).join(map(str, errors))}"
