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


class TestFileTypeControlRules:
    """
    Integration Tests for the ZIA Cloud File Type Control Rules
    """

    def test_file_type_control_rule(self, fs):
        client = MockZIAClient(fs)
        errors = []
        rule_id = None

        try:

            # Step 3: Create a file type control rule
            try:
                rule_name = "tests-" + generate_random_string()
                created_rule, _, error = client.zia.file_type_control_rule.add_rule(
                    name=rule_name,
                    description="Integration test file type control rule",
                    enabled=True,
                    order=1,
                    rank=7,
                    filtering_action='ALLOW',
                    operation="DOWNLOAD",
                    url_categories = ["OTHER_ADULT_MATERIAL"],
                    protocols=["FOHTTP_RULE", "FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
                    device_trust_levels=["UNKNOWN_DEVICETRUSTLEVEL", "LOW_TRUST", "MEDIUM_TRUST", "HIGH_TRUST"],
                    file_types=["FTCATEGORY_ALZ", "FTCATEGORY_P7Z", "FTCATEGORY_B64"],
                )
                assert error is None, f"Firewall Rule creation failed: {error}"
                assert created_rule is not None, "Firewall Rule creation returned None"
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Firewall Rule creation failed: {exc}")

            # Step 4: Retrieve the Firewall Rule by ID
            try:
                retrieved_rule, _, error = client.zia.file_type_control_rule.get_rule(rule_id)
                assert error is None, f"Error retrieving Firewall Rule: {error}"
                assert retrieved_rule is not None, "Retrieved Firewall Rule is None"
                assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Firewall Rule failed: {exc}")

            # Step 5: Update the Firewall Rule
            try:
                updated_description = "Updated integration test File Type Control Rule"
                updated_rule, _, error = client.zia.file_type_control_rule.update_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    enabled=True,
                    order=1,
                    rank=7,
                    filtering_action='ALLOW',
                    operation="DOWNLOAD",
                    url_categories = ["OTHER_ADULT_MATERIAL"],
                    protocols=["FOHTTP_RULE", "FTP_RULE", "HTTPS_RULE", "HTTP_RULE"],
                    device_trust_levels=["UNKNOWN_DEVICETRUSTLEVEL", "LOW_TRUST", "MEDIUM_TRUST", "HIGH_TRUST"],
                    file_types=["FTCATEGORY_ALZ", "FTCATEGORY_P7Z", "FTCATEGORY_B64"],
                )
                assert error is None, f"Error updating File Type Control Rule: {error}"
                assert updated_rule is not None, "Updated File Type Control Rule is None"
                assert (
                    updated_rule.description == updated_description
                ), f"File Type Control Rule update failed: {updated_rule.as_dict()}"
            except Exception as exc:
                errors.append(f"Updating File Type Control Rule failed: {exc}")

            # Step 6: List File Type Control Rules and verify the rule is present
            try:
                rules, _, error = client.zia.file_type_control_rule.list_rules()
                assert error is None, f"Error listing File Type Control Rules: {error}"
                assert rules is not None, "File Type Control Rules list is None"
                assert any(rule.id == rule_id for rule in rules), "Newly created rule not found in the list of rules."
            except Exception as exc:
                errors.append(f"Listing File Type Control Rules failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                if rule_id:
                    # Delete the file type control rule
                    _, _, error = client.zia.file_type_control_rule.delete_rule(rule_id)
                    assert error is None, f"Error deleting client.zia.file_type_control_rule.: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting File Type Control Rule failed: {exc}")

            errors.extend(cleanup_errors)

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
