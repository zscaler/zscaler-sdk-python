# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
                created_rule = client.web_dlp.add_rule(
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
                rule_id = created_rule.get("id", None)
                assert rule_id is not None, "DLP Web Rule creation failed"
            except Exception as exc:
                errors.append(f"DLP Web Rule creation failed: {exc}")

            try:
                # Retrieve the specific DLP web rule
                retrieved_rule = client.web_dlp.get_rule(rule_id)
                assert retrieved_rule["id"] == rule_id, "Failed to retrieve the correct DLP web rule"
            except Exception as exc:
                errors.append(f"Retrieving DLP Web Rule failed: {exc}")

            try:
                # Update the DLP web rule
                updated_description = "Updated " + generate_random_string()
                client.web_dlp.update_rule(rule_id, description=updated_description)
                updated_rule = client.web_dlp.get_rule(rule_id)
                assert updated_rule["description"] == updated_description, "Failed to update DLP Web Rule"
            except Exception as exc:
                errors.append(f"Updating DLP Web Rule failed: {exc}")

            try:
                # Verify update by listing DLP web rules
                ip_list = client.web_dlp.list_rules()
                assert any(ip["id"] == rule_id for ip in ip_list), "Updated DLP web rule not found in list"
            except Exception as exc:
                errors.append(f"Listing DLP Web Rules failed: {exc}")

        finally:
            try:
                # Cleanup: Attempt to delete the DLP web rule
                if rule_id:
                    delete_response_code = client.web_dlp.delete_rule(rule_id)
                    assert delete_response_code == 204, "Failed to delete DLP web rule"
            except Exception as cleanup_exc:
                errors.append(f"Deleting DLP Web Rule failed: {cleanup_exc}")

        # Assert that no errors occurred during the test execution
        assert len(errors) == 0, f"Errors occurred during the DLP web rule lifecycle test: {errors}"
