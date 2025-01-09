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


class TestDLPWebRule:
    """
    Integration Tests for the ZIA DLP Web Rule
    """

    def test_dlp_web_rule(self, fs):
        client = MockZIAClient(fs)
        errors = []
        rule_id = None

        try:
            try:
                # Create a DLP Web Rule
                rule_name = "tests-" + generate_random_string()
                rule_description = "tests-" + generate_random_string()
                created_rule, _, error = client.zia.dlp_web_rules.add_rule(
                    name=rule_name,
                    description=rule_description,
                    state="ENABLED",
                    action="BLOCK",
                    order=1,
                    rank=7,
                    severity="RULE_SEVERITY_HIGH",
                    protocols=["FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
                    cloud_applications=["WINDOWS_LIVE_HOTMAIL"],
                    user_risk_score_levels=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                )
                assert error is None, f"Error creating DLP Web Rule: {error}"
                assert created_rule is not None, "DLP Web Rule creation returned None"
                assert created_rule.name == rule_name, "DLP Web Rule name mismatch"
                assert created_rule.description == rule_description, "DLP Web Rule description mismatch"
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Failed to add DLP Web Rule: {exc}")

            # Attempt to update the rule DLP Web Rule
            if rule_id:
                try:
                    updated_name = rule_name + " Updated"
                    _, _, error = client.zia.dlp_web_rules.update_rule(rule_id, name=updated_name)
                    assert error is None, f"Error updating DLP Web Rule: {error}"
                    
                    updated_rule, _, error = client.zia.dlp_web_rules.get_rule(rule_id)
                    assert error is None, f"Error retrieving updated DLP Web Rule: {error}"
                    assert updated_rule.name == updated_name, "Failed to update DLP Web Rule name"
                except Exception as exc:
                    errors.append(f"Failed to update DLP Web Rule: {exc}")

            try:
                # Verify update by listing DLP web rules
                rules, _, error = client.zia.dlp_web_rules.list_rules()
                assert error is None, f"Error listing rules: {error}"
                assert isinstance(rules, list), "Expected a list of rules"
                assert len(rules) > 0, "No rules found for the specified rule type"
            except Exception as exc:
                errors.append(f"Listing rules failed: {exc}")

        finally:
            # Cleanup: Attempt to delete the rule label
            if rule_id:
                try:
                    delete_response_code = client.zia.dlp_web_rules.delete_rule(rule_id)
                    assert str(delete_response_code) != "204", "Failed to delete label"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the rule label lifecycle test: {errors}"
