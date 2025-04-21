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


class TestAccessPolicyForwardingRuleV2:
    """
    Integration Tests for the Client Forwarding Policy Rules V2
    """

    def test_client_forwarding_policy_rules_v2(self, fs):
        client = MockZPAClient(fs)
        errors = []
        rule_id = None

        try:
            # Step 1: Create rule
            try:
                rule_name = "tests-" + generate_random_string()
                rule_description = "Integration test Client Forwarding Rule V2"

                created_rule, _, err = client.zpa.policies.add_client_forwarding_rule_v2(
                    name=rule_name,
                    description=rule_description,
                    action="intercept",
                    conditions=[
                        ("client_type", ["zpn_client_type_exporter", "zpn_client_type_zapp"])
                    ],
                )
                assert err is None, f"Error creating forwarding rule: {err}"
                assert created_rule is not None
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Rule creation failed: {exc}")

            # Step 2: Retrieve rule and verify
            try:
                retrieved_rule, _, err = client.zpa.policies.get_rule("client_forwarding", rule_id)
                assert err is None, f"Error retrieving forwarding rule: {err}"
                assert retrieved_rule.id == rule_id
            except Exception as exc:
                errors.append(f"Rule retrieval failed: {exc}")

            # Step 3: Update rule
            try:
                updated_description = "Updated rule " + generate_random_string()
                _, _, err = client.zpa.policies.update_client_forwarding_rule_v2(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    action="intercept",
                    conditions=[
                        ("client_type", ["zpn_client_type_exporter", "zpn_client_type_zapp"])
                    ],
                )
                if err and str(err) != "Response is None":
                    raise AssertionError(f"Unexpected update error: {err}")
            except Exception as exc:
                errors.append(f"Rule update failed: {exc}")

            # Step 4: List rules and confirm
            try:
                rules, _, err = client.zpa.policies.list_rules("client_forwarding")
                assert err is None, f"Error listing forwarding rules: {err}"
                assert any(r.id == rule_id for r in rules), "Rule not found in client forwarding policy list"
            except Exception as exc:
                errors.append(f"Rule list verification failed: {exc}")

        finally:
            cleanup_errors = []
            if rule_id:
                try:
                    _, _, err = client.zpa.policies.delete_rule("client_forwarding", rule_id)
                    assert err is None, f"Error deleting rule: {err}"
                except Exception as exc:
                    cleanup_errors.append(f"Rule deletion failed: {exc}")

            errors.extend(cleanup_errors)

        assert not errors, f"Errors occurred during Client Forwarding Policy Rule V2 test:\n{chr(10).join(map(str, errors))}"
