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


class TestAccessPolicyIsolationRuleV2:
    """
    Integration Tests for the Isolation Policy Rules V2
    """

    @pytest.mark.vcr()
    def test_access_policy_isolation_rules_v2(self, fs):
        client = MockZPAClient(fs)
        errors = []
        rule_id = None
        scim_group_ids = []
        profile_id = None

        try:

            # Step 2: Get USER IdP
            try:
                idps, _, err = client.zpa.idp.list_idps()
                assert err is None, f"Error listing IdPs: {err}"
                user_idp = next((idp for idp in idps if isinstance(idp.sso_type, list) and "USER" in idp.sso_type), None)
                assert user_idp, "No USER IdP found"
                user_idp_id = user_idp.id
            except Exception as exc:
                errors.append(f"IdP USER selection failed: {exc}")

            # Step 3: Get SCIM Groups
            try:
                scim_groups, _, err = client.zpa.scim_groups.list_scim_groups(idp_id=user_idp_id)
                assert err is None, f"Error listing SCIM groups: {err}"
                assert len(scim_groups) >= 2, "Less than 2 SCIM groups returned"
                scim_group_ids = [g.id for g in scim_groups[:2]]
            except Exception as exc:
                errors.append(f"SCIM Group retrieval failed: {exc}")

            try:
                # Retrieve a list of Isolation profiles model objects
                profiles, _, err = client.zpa.cbi_zpa_profile.list_isolation_profiles()
                if err:
                    raise AssertionError(f"Error listing Isolation profiles: {err}")

                # Make sure we got back a list (not None or a single object)
                if not isinstance(profiles, list):
                    raise AssertionError(f"Expected a list of Isolation profiles objects, got {type(profiles)}")

                if not profiles:
                    raise AssertionError("No Isolation profiles found at all.")

                # profiles[0] is a IsolationProfiles model, so use dot-notation:
                profile_id = profiles[0].id

                print(f"First Isolation profiles: {profile_id}")

            except Exception as exc:
                errors.append(f"Listing Isolation profiles failed: {exc}")
            try:
                rule_name = "tests-apir2-" + generate_random_string()
                rule_description = "Integration test Client Isolation Rule V2"

                created_rule, _, err = client.zpa.policies.add_isolation_rule_v2(
                    name=rule_name,
                    description=rule_description,
                    action="isolate",
                    zpn_isolation_profile_id=profile_id,
                    conditions=[
                        ("scim_group", [(user_idp_id, g_id) for g_id in scim_group_ids]),
                    ],
                )
                assert err is None, f"Error creating isolation rule: {err}"
                assert created_rule is not None
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Rule creation failed: {exc}")

            # Step 2: Retrieve rule and verify
            try:
                retrieved_rule, _, err = client.zpa.policies.get_rule("isolation", rule_id)
                assert err is None, f"Error retrieving isolation rule: {err}"
                assert retrieved_rule.id == rule_id
            except Exception as exc:
                errors.append(f"Rule retrieval failed: {exc}")

            # Step 3: Update rule
            try:
                updated_description = "Updated rule " + generate_random_string()
                _, _, err = client.zpa.policies.update_isolation_rule_v2(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    action="isolate",
                    zpn_isolation_profile_id=profile_id,
                    conditions=[
                        ("scim_group", [(user_idp_id, g_id) for g_id in scim_group_ids]),
                    ],
                )
                if err and str(err) != "Response is None":
                    raise AssertionError(f"Unexpected update error: {err}")
            except Exception as exc:
                errors.append(f"Rule update failed: {exc}")

            # Step 4: List rules and confirm
            try:
                rules, _, err = client.zpa.policies.list_rules("isolation")
                assert err is None, f"Error listing isolation rules: {err}"
                assert any(r.id == rule_id for r in rules), "Rule not found in client isolation policy list"
            except Exception as exc:
                errors.append(f"Rule list verification failed: {exc}")

        finally:
            cleanup_errors = []
            if rule_id:
                try:
                    _, _, err = client.zpa.policies.delete_rule("isolation", rule_id)
                    assert err is None, f"Error deleting rule: {err}"
                except Exception as exc:
                    cleanup_errors.append(f"Rule deletion failed: {exc}")

            errors.extend(cleanup_errors)

        assert not errors, f"Errors occurred during Isolation Policy Rule V2 test:\n{chr(10).join(map(str, errors))}"
