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


class TestAccessPolicyTimeoutRuleV2:
    """
    Integration Tests for the Access Policy Timeout Rules V2
    """

    def test_access_policy_timeout_policy_rules_v2(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        rule_id = None
        scim_group_ids = []

        try:
            # Test listing SCIM groups with pagination
            idps, _, err = client.zpa.idp.list_idps()
            if err or not isinstance(idps, list):
                raise AssertionError(f"Failed to retrieve IdPs: {err or f'Expected idps to be a list, got {type(idps)}'}")

            # Convert IDPs to dictionaries
            idps = [idp.as_dict() for idp in idps]

            # Find the IdP with ssoType = USER
            user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
            if not user_idp:
                raise AssertionError("No IdP with ssoType 'USER' found.")

            # Export the ID of the matching IdP
            user_idp_id = user_idp.get("id")
            if not user_idp_id:
                raise AssertionError("The matching IdP does not have an 'id' field.")

            # List SCIM groups using the exported IdP ID
            scim_groups, _, err = client.zpa.scim_groups.list_scim_groups(idp_id=user_idp_id)
            if err or not scim_groups:
                raise AssertionError(f"Failed to list SCIM groups: {err}")

            # Convert SCIMGroup objects to dictionaries
            scim_groups = [group.as_dict() for group in scim_groups]

            # Retrieve the IDs for the first two SCIM groups
            scim_group_ids = [(user_idp_id, group["id"]) for group in scim_groups[:2]]
            if len(scim_group_ids) < 2:
                raise AssertionError("Less than 2 SCIM groups were retrieved.")

            print(f"Exported IdP ID: {user_idp_id}")
            print(f"Retrieved SCIM Group IDs: {scim_group_ids}")

        except Exception as exc:
            errors.append(f"Listing SCIM groups failed: {exc}")

        try:
            # Create a Timeout Policy Rule
            rule_name = "tests-" + generate_random_string()
            rule_description = "updated-" + generate_random_string()
            created_rule, _, err = client.zpa.policies.add_timeout_rule_v2(
                name=rule_name,
                description=rule_description,
                re_auth_idle_timeout="172800",
                re_auth_timeout="600",
                conditions=[
                    ("client_type", ["zpn_client_type_exporter", "zpn_client_type_zapp"]),
                    ("scim_group", scim_group_ids),
                ],
            )
            assert err is None, f"Error creating Timeout Policy Rules: {err}"
            assert created_rule is not None
            assert created_rule.name == rule_name
            assert created_rule.description == rule_description

            rule_id = created_rule.id
        except Exception as exc:
            errors.append(exc)

        try:
            # Test listing Timeout Policy Rules
            all_rules, _, err = client.zpa.policies.list_rules("timeout")
            assert err is None, f"Error listing Timeout Policy Rules: {err}"
            if not any(rule["id"] == rule_id for rule in all_rules):
                raise AssertionError("Timeout Policy Rules not found in list")
        except Exception as exc:
            errors.append(f"Listing Timeout Policy Rules failed: {exc}")

        try:
            # Test retrieving the specific Timeout Policy Rules
            retrieved_rule, _, err =  client.zpa.policies.get_rule("timeout", rule_id)
            if retrieved_rule["id"] != rule_id:
                raise AssertionError("Failed to retrieve the correct Timeout Policy Rules")
        except Exception as exc:
            errors.append(f"Retrieving Timeout Policy Rules failed: {exc}")

        try:
            # Update the Timeout Policy Rule
            updated_rule_description = "Updated " + generate_random_string()
            _, _, err = client.zpa.policies.update_timeout_rule_v2(
                rule_id=rule_id,
                description=updated_rule_description,
                re_auth_idle_timeout="172800",
                re_auth_timeout="600",
                conditions=[
                    ("client_type", ["zpn_client_type_exporter", "zpn_client_type_zapp"]),
                    ("scim_group", scim_group_ids),
                ],
            )
            # If we got an error but it’s "Response is None", treat it as success:
            if err is not None:
                if isinstance(err, ValueError) and str(err) == "Response is None":
                    print(f"[INFO] Interpreting 'Response is None' as 204 success.")
                else:
                    raise AssertionError(f"Error updating Timeout Policy Rules: {err}")
            print(f"Timeout Policys with ID {rule_id} updated successfully (204 No Content).")
        except Exception as exc:
            errors.append(f"Updating Timeout PolicyRules failed: {exc}")

        finally:
            # Ensure cleanup is performed even if there are errors
            if rule_id:
                try:
                    # Cleanup: Delete the Timeout PolicyRules
                    delete_status_rule, _, err = client.zpa.policies.delete_rule("timeout", rule_id)
                    assert err is None, f"Error deleting Timeout Policy Rules: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_status_rule is None, f"Expected None for 204 No Content, got {delete_status_rule}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Timeout Policy Rules ID {rule_id}: {cleanup_exc}")
                except Exception as exc:
                    errors.append(f"Deleting Timeout Policy Rules failed: {exc}")


        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the Timeout Policy Rule operations test: {errors}"
