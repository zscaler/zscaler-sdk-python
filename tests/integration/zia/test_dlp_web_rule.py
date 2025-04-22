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
            rule_name = "tests-" + generate_random_string()
            rule_description = "tests-" + generate_random_string()
            created_rule, _, error = client.zia.dlp_web_rules.add_rule(
                name=rule_name,
                description=rule_description,
                enabled=True,
                action="BLOCK",
                order=1,
                rank=7,
                severity="RULE_SEVERITY_HIGH",
                protocols=["FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
                cloud_applications=["WINDOWS_LIVE_HOTMAIL"],
                user_risk_score_levels=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            )
            assert error is None, f"DLP Web Rule creation failed: {error}"
            assert created_rule is not None, "DLP Web Rule creation returned None"
            rule_id = created_rule.id
        except Exception as exc:
            errors.append(f"DLP Web Rule creation failed: {exc}")

        # Step 4: Retrieve the DLP Web Rule by ID
        try:
            retrieved_rule, _, error = client.zia.dlp_web_rules.get_rule(rule_id)
            assert error is None, f"Error retrieving DLP Web Rule: {error}"
            assert retrieved_rule is not None, "Retrieved DLP Web Rule is None"
            assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
        except Exception as exc:
            errors.append(f"Retrieving DLP Web Rule failed: {exc}")

            # Step 5: Update the DLP Web Rule
            try:
                updated_description = "Updated integration test DLP Web Rule"
                updated_rule, _, error = client.zia.dlp_web_rules.update_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    enabled=True,
                    action="BLOCK",
                    order=1,
                    rank=7,
                    severity="RULE_SEVERITY_HIGH",
                    protocols=["FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
                    cloud_applications=["WINDOWS_LIVE_HOTMAIL"],
                    user_risk_score_levels=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                )
                assert error is None, f"Error updating DLP Web Rule: {error}"
                assert updated_rule is not None, "Updated DLP Web Rule is None"
                assert updated_rule.description == updated_description, f"DLP Web Rule update failed: {updated_rule.as_dict()}"
            except Exception as exc:
                errors.append(f"Updating DLP Web Rule failed: {exc}")

            # Step 6: List DLP Web Rule and verify the rule is present
            try:
                rules, _, error = client.zia.dlp_web_rules.list_rules()
                assert error is None, f"Error listing DLP Web Rules: {error}"
                assert rules is not None, "DLP Web Rule list is None"
                assert any(rule.id == rule_id for rule in rules), "Newly created rule not found in the list of rules."
            except Exception as exc:
                errors.append(f"Listing DLP Web Rules failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                if rule_id:
                    # Delete the DLP Web Rule
                    _, _, error = client.zia.dlp_web_rules.delete_rule(rule_id)
                    assert error is None, f"Error deleting DLP Web Rule: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting DLP Web Rule failed: {exc}")

            errors.extend(cleanup_errors)

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
