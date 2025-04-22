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


class TestAccessPolicyRule:
    """
    Integration Tests for the Access Policy Rules with SCIM group conditions
    """

    def test_access_policy_rules(self, fs):
        client = MockZPAClient(fs)
        errors = []
        connector_group_id = None
        rule_id = None
        user_idp_id = None
        scim_group_ids = []

        try:
            # Step 1: Create App Connector Group
            try:
                created_connector_group, _, err = client.zpa.app_connector_groups.add_connector_group(
                    name="tests-" + generate_random_string(),
                    description="Test Connector Group",
                    enabled=True,
                    latitude="37.33874",
                    longitude="-121.8852525",
                    location="San Jose, CA, USA",
                    upgrade_day="SUNDAY",
                    upgrade_time_in_secs="66600",
                    override_version_profile=True,
                    version_profile_name="Default",
                    version_profile_id="0",
                    dns_query_type="IPV4_IPV6",
                    pra_enabled=True,
                    tcp_quick_ack_app=True,
                    tcp_quick_ack_assistant=True,
                    tcp_quick_ack_read_assistant=True,
                )
                assert err is None, f"Error creating app connector group: {err}"
                connector_group_id = created_connector_group.id
            except Exception as exc:
                errors.append(f"App Connector Group creation failed: {exc}")

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

            # Step 4: Create Access Policy Rule
            try:
                rule_name = "tests-" + generate_random_string()
                rule_description = "Access rule with SCIM group conditions"
                created_rule, _, err = client.zpa.policies.add_access_rule(
                    name=rule_name,
                    description=rule_description,
                    action="allow",
                    app_connector_group_ids=[connector_group_id],
                    conditions=[
                        ("scim_group", user_idp_id, scim_group_ids[0]),
                        ("scim_group", user_idp_id, scim_group_ids[1]),
                    ],
                )
                assert err is None, f"Error creating access rule: {err}"
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Access Policy Rule creation failed: {exc}")

            # Step 5: Get Rule by ID
            try:
                retrieved_rule, _, err = client.zpa.policies.get_rule("access", rule_id)
                assert err is None, f"Error retrieving rule: {err}"
                assert retrieved_rule.id == rule_id, "Retrieved rule ID mismatch"
            except Exception as exc:
                errors.append(f"Access Policy Rule retrieval failed: {exc}")

            # Step 6: Update Rule
            try:
                updated_description = "Updated access rule " + generate_random_string()
                _, _, err = client.zpa.policies.update_access_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    action="allow",
                    app_connector_group_ids=[connector_group_id],
                    conditions=[
                        ("scim_group", user_idp_id, scim_group_ids[0]),
                        ("scim_group", user_idp_id, scim_group_ids[1]),
                    ],
                )
                if err and str(err) != "Response is None":
                    raise AssertionError(f"Unexpected update error: {err}")
            except Exception as exc:
                errors.append(f"Access Policy Rule update failed: {exc}")

            # Step 7: List Rules and Confirm Presence
            try:
                rules, _, err = client.zpa.policies.list_rules("access")
                assert err is None, f"Error listing rules: {err}"
                assert any(r.id == rule_id for r in rules), "Created rule not found in rule list"
            except Exception as exc:
                errors.append(f"Access Policy Rule list verification failed: {exc}")

        finally:
            cleanup_errors = []

            # Delete Rule
            if rule_id:
                try:
                    _, _, err = client.zpa.policies.delete_rule("access", rule_id)
                    assert err is None, f"Error deleting rule: {err}"
                except Exception as exc:
                    cleanup_errors.append(f"Failed to delete rule ID {rule_id}: {exc}")

            # Delete App Connector Group
            if connector_group_id:
                try:
                    _, _, err = client.zpa.app_connector_groups.delete_connector_group(connector_group_id)
                    assert err is None, f"Error deleting connector group: {err}"
                except Exception as exc:
                    cleanup_errors.append(f"Failed to delete connector group ID {connector_group_id}: {exc}")

            errors.extend(cleanup_errors)

        assert not errors, f"Errors occurred during Access Policy Rule test:\n{chr(10).join(map(str, errors))}"
