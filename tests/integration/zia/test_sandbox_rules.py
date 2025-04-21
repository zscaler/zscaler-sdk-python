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

from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestSandboxRules:
    """
    Integration Tests for the ZIA Sandbox Rules
    """

    def test_sandbox_rule(self, fs):
        client = MockZIAClient(fs)
        errors = []
        department_id = None
        group_id = None
        rule_id = None

        try:
            # Step 1: Retrieve department
            try:
                departments, _, error = client.zia.user_management.list_departments(query_params={'search': 'A000'})
                assert error is None, f"Department listing error: {error}"
                department = next((d for d in departments if hasattr(d, "id")), None)
                assert department, "No valid departments available for assignment"
                department_id = department.id
            except Exception as exc:
                errors.append(f"Department retrieval failed: {exc}")

            # Step 2: Retrieve group
            try:
                groups, _, error = client.zia.user_management.list_groups(query_params={'search': 'A000'})
                assert error is None, f"Group listing error: {error}"
                group = next((g for g in groups if hasattr(g, "id")), None)
                assert group, "No valid groups available for assignment"
                group_id = group.id
            except Exception as exc:
                errors.append(f"Group retrieval failed: {exc}")

            # Step 3: Create a Sandbox Rule
            try:
                rule_name = "tests-" + generate_random_string()
                created_rule, _, error = client.zia.sandbox_rules.add_rule(
                    name=rule_name,
                    description="Integration test Sandbox Rule",
                    ba_rule_action="BLOCK",
                    state="ENABLED",
                    order=1,
                    rank=7,
                    first_time_enable=True,
                    ml_action_enabled=True,
                    first_time_operation="ALLOW_SCAN",
                    url_categories=["OTHER_ADULT_MATERIAL"],
                    protocols=["FOHTTP_RULE", "FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
                    ba_policy_categories=["ADWARE_BLOCK", "BOTMAL_BLOCK", "ANONYP2P_BLOCK", "RANSOMWARE_BLOCK"],
                    file_types=["FTCATEGORY_BZIP2", "FTCATEGORY_P7Z"],
                    by_threat_score=40,
                    groups=[group_id],
                    departments=[department_id],
                )
                assert error is None, f"Sandbox Rule creation failed: {error}"
                assert created_rule is not None, "Sandbox Rule creation returned None"
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Sandbox Rule creation failed: {exc}")

            # Step 4: Retrieve the Sandbox Rule by ID
            try:
                retrieved_rule, _, error = client.zia.sandbox_rules.get_rule(rule_id)
                assert error is None, f"Error retrieving Sandbox Rule: {error}"
                assert retrieved_rule is not None, "Retrieved Sandbox Rule is None"
                assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Sandbox Rule failed: {exc}")

            # Step 5: Update the Sandbox Rule
            try:
                updated_description = "Updated integration test Sandbox Rule"
                updated_rule, _, error = client.zia.sandbox_rules.update_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    ba_rule_action="ALLOW",
                    state="ENABLED",
                    order=1,
                    rank=7,
                    first_time_enable=True,
                    ml_action_enabled=True,
                    first_time_operation="ALLOW_SCAN",
                    url_categories=["OTHER_ADULT_MATERIAL"],
                    protocols=["FOHTTP_RULE", "FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
                    ba_policy_categories=["ADWARE_BLOCK", "BOTMAL_BLOCK", "ANONYP2P_BLOCK", "RANSOMWARE_BLOCK"],
                    file_types=["FTCATEGORY_BZIP2", "FTCATEGORY_P7Z"],
                    by_threat_score=45,
                    groups=[group_id],
                    departments=[department_id],
                )
                assert error is None, f"Error updating Sandbox Rule: {error}"
                assert updated_rule is not None, "Updated Sandbox Rule is None"
                assert updated_rule.description == updated_description, f"Sandbox Rule update failed: {updated_rule.as_dict()}"
            except Exception as exc:
                errors.append(f"Updating Sandbox Rule failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                if rule_id:
                    _, _, error = client.zia.sandbox_rules.delete_rule(rule_id)
                    assert error is None, f"Error deleting Sandbox Rule: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Sandbox Rule failed: {exc}")

            errors.extend(cleanup_errors)

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
