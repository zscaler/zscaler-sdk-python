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


class TestAccessPolicyRuleV2:
    """
    Integration Tests for the Access Policy Rules V2
    """

    @pytest.mark.vcr()
    def test_access_policy_rules_v2(self, fs):
        client = MockZPAClient(fs)
        errors = []
        rule_id = None
        user_idp_id = None
        scim_group_ids = []

        try:
            # Step 1: Get USER IdP
            try:
                idps = client.zpa.idp.list_idps()
                user_idp = next((idp for idp in idps if isinstance(idp.sso_type, list) and "USER" in idp.sso_type), None)
                assert user_idp, "No USER IdP found"
                user_idp_id = user_idp.id
            except Exception as exc:
                errors.append(f"USER IdP selection failed: {exc}")

            # Step 2: Get SCIM groups for that IdP
            try:
                scim_groups = client.zpa.scim_groups.list_scim_groups(idp_id=user_idp_id)
                assert len(scim_groups) >= 2, "Less than 2 SCIM groups returned"
                scim_group_ids = [g.id for g in scim_groups[:2]]
            except Exception as exc:
                errors.append(f"SCIM Group retrieval failed: {exc}")

            # Step 3: Create access rule with SCIM conditions
            try:
                rule_name = "tests-apr2-" + generate_random_string()
                rule_description = "Integration test Access Rule V2"

                created_rule = client.zpa.policies.add_access_rule_v2(
                    name=rule_name,
                    description=rule_description,
                    action="allow",
                    conditions=[
                        ("client_type", ["zpn_client_type_exporter", "zpn_client_type_zapp"]),
                        ("scim_group", [(user_idp_id, g_id) for g_id in scim_group_ids]),
                    ],
                )
                assert created_rule is not None
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Access rule creation failed: {exc}")

            # Step 4: Retrieve rule and verify
            try:
                retrieved_rule = client.zpa.policies.get_rule("access", rule_id)
                assert retrieved_rule.id == rule_id
            except Exception as exc:
                errors.append(f"Access rule retrieval failed: {exc}")

            # Step 5: Update rule
            try:
                updated_description = "Updated V2 rule " + generate_random_string()
                _ = client.zpa.policies.update_access_rule_v2(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    action="allow",
                    conditions=[
                        ("client_type", ["zpn_client_type_exporter", "zpn_client_type_zapp"]),
                        ("scim_group", [(user_idp_id, g_id) for g_id in scim_group_ids]),
                    ],
                )
            except Exception as exc:
                errors.append(f"Access rule update failed: {exc}")

            # Step 6: List rules and confirm
            try:
                rules = client.zpa.policies.list_rules("access")
                assert any(r.id == rule_id for r in rules), "Rule not found in access policy list"
            except Exception as exc:
                errors.append(f"Access rule list verification failed: {exc}")

        finally:
            cleanup_errors = []

            if rule_id:
                try:
                    _ = client.zpa.policies.delete_rule("access", rule_id)
                except Exception as exc:
                    cleanup_errors.append(f"Rule deletion failed: {exc}")

            errors.extend(cleanup_errors)

        assert not errors, f"Errors occurred during Access Policy Rule V2 test:\n{chr(10).join(map(str, errors))}"
