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


class TestAccessPolicyTimeoutV1:
    """
    Integration Tests for the Access Policy Rules with SCIM group conditions
    """

    @pytest.mark.vcr()
    def test_access_policy_timeout_rules_v1(self, fs):
        client = MockZPAClient(fs)
        errors = []
        rule_id = None
        scim_group_ids = []
        profile_id = None

        try:

            # Step 2: Get USER IdP
            try:
                idps = client.zpa.idp.list_idps()
                user_idp = next((idp for idp in idps if isinstance(idp.sso_type, list) and "USER" in idp.sso_type), None)
                assert user_idp, "No USER IdP found"
                user_idp_id = user_idp.id
            except Exception as exc:
                errors.append(f"IdP USER selection failed: {exc}")

            # Step 3: Get SCIM Groups
            try:
                scim_groups = client.zpa.scim_groups.list_scim_groups(idp_id=user_idp_id)
                assert len(scim_groups) >= 2, "Less than 2 SCIM groups returned"
                scim_group_ids = [g.id for g in scim_groups[:2]]
            except Exception as exc:
                errors.append(f"SCIM Group retrieval failed: {exc}")

            # Step 4: Create Access Policy Rule
            try:
                rule_name = "tests-aptr1-" + generate_random_string()
                rule_description = "Access rule with SCIM group conditions"
                created_rule = client.zpa.policies.add_timeout_rule(
                    name=rule_name,
                    description=rule_description,
                    action="RE_AUTH",
                    reauth_idle_timeout="2592000",
                    reauth_timeout="3456000",
                    conditions=[
                        ("scim_group", user_idp_id, scim_group_ids[0]),
                        ("scim_group", user_idp_id, scim_group_ids[1]),
                    ],
                )
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Access Policy Rule creation failed: {exc}")

            # Step 5: Get Rule by ID
            try:
                retrieved_rule = client.zpa.policies.get_rule("timeout", rule_id)
                assert retrieved_rule.id == rule_id, "Retrieved rule ID mismatch"
            except Exception as exc:
                errors.append(f"Access Policy Rule retrieval failed: {exc}")

            # Step 6: Update Rule
            try:
                updated_description = "Updated access rule " + generate_random_string()
                _ = client.zpa.policies.update_timeout_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    action="RE_AUTH",
                    reauth_idle_timeout="2592000",
                    reauth_timeout="3456000",
                    conditions=[
                        ("scim_group", user_idp_id, scim_group_ids[0]),
                        ("scim_group", user_idp_id, scim_group_ids[1]),
                    ],
                )
            except Exception as exc:
                errors.append(f"Access Policy Rule update failed: {exc}")

            # Step 7: List Rules and Confirm Presence
            try:
                rules = client.zpa.policies.list_rules("timeout")
                assert any(r.id == rule_id for r in rules), "Created rule not found in rule list"
            except Exception as exc:
                errors.append(f"Access Policy Rule list verification failed: {exc}")

        finally:
            cleanup_errors = []

            # Delete Rule
            if rule_id:
                try:
                    _ = client.zpa.policies.delete_rule("timeout", rule_id)
                except Exception as exc:
                    cleanup_errors.append(f"Failed to delete rule ID {rule_id}: {exc}")

            errors.extend(cleanup_errors)

        assert not errors, f"Errors occurred during Access Policy Rule test:\n{chr(10).join(map(str, errors))}"
