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


class TestBandwidthRules:
    """
    Integration Tests for the ZIA Bandwidth Rules
    """

    @pytest.mark.vcr()
    def test_bandwidth_control_rules(self, fs):
        client = MockZIAClient(fs)
        errors = []
        class_id = None
        rule_id = None

        try:

            # Step 1: Create a Bandwidth Class (use unique prefix to avoid collision with test_bandwidth_classes.py)
            try:
                bdw_class_name = "tests-bdwrule-" + generate_random_string()
                created_bdw_class, _, error = client.zia.bandwidth_classes.add_class(
                    name=bdw_class_name,
                    web_applications=["ACADEMICGPT", "AD_CREATIVES"],
                    urls=["test1.acme.com", "test2.acme.com"],
                    url_categories=["AI_ML_APPS", "GENERAL_AI_ML", "PROFESSIONAL_SERVICES"],
                )
                assert error is None, f"Error adding Bandwidth Class: {error}"
                assert created_bdw_class is not None, "Failed to create Bandwidth Class"
                class_id = created_bdw_class.id
                assert created_bdw_class.name.startswith("tests-"), "Class name mismatch in creation"
                # (Optionally) Assert the description if needed
            except Exception as exc:
                errors.append(f"Bandwidth Class creation failed: {exc}")

            # Step 3: Create a Bandwidth Rule (use unique prefix)
            try:
                rule_name = "tests-bdwrule-" + generate_random_string()
                created_rule, _, error = client.zia.bandwidth_control_rules.add_rule(
                    name=rule_name,
                    description="Integration test Bandwidth Rule",
                    enabled=True,
                    order=1,
                    rank=7,
                    max_bandwidth='100',
                    min_bandwidth='20',
                    bandwidth_class_ids=[class_id],
                    protocols=[
                        "WEBSOCKETSSL_RULE",
                        "WEBSOCKET_RULE",
                        "DOHTTPS_RULE",
                        "TUNNELSSL_RULE",
                        "HTTP_PROXY",
                        "FOHTTP_RULE",
                        "FTP_RULE",
                        "HTTPS_RULE",
                        "HTTP_RULE",
                        "SSL_RULE",
                        "TUNNEL_RULE"
                    ],
                )
                assert error is None, f"Bandwidth Rule creation failed: {error}"
                assert created_rule is not None, "Bandwidth Rule creation returned None"
                rule_id = created_rule.id
            except Exception as exc:
                errors.append(f"Bandwidth Rule creation failed: {exc}")

            # Step 4: Retrieve the Bandwidth Rule by ID
            try:
                retrieved_rule, _, error = client.zia.bandwidth_control_rules.get_rule(rule_id)
                assert error is None, f"Error retrieving Bandwidth Rule: {error}"
                assert retrieved_rule is not None, "Retrieved Bandwidth Rule is None"
                assert retrieved_rule.id == rule_id, "Incorrect rule retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Bandwidth Rule failed: {exc}")

            # Step 5: Update the Bandwidth Rule
            try:
                updated_description = "Updated integration test Bandwidth Rule"
                updated_rule, _, error = client.zia.bandwidth_control_rules.update_rule(
                    rule_id=rule_id,
                    name=rule_name,
                    description=updated_description,
                    enabled=True,
                    order=1,
                    rank=7,
                    max_bandwidth='100',
                    min_bandwidth='20',
                    bandwidth_class_ids=[class_id],
                    protocols=[
                        "WEBSOCKETSSL_RULE",
                        "WEBSOCKET_RULE",
                        "DOHTTPS_RULE",
                        "TUNNELSSL_RULE",
                        "HTTP_PROXY",
                        "FOHTTP_RULE",
                        "FTP_RULE",
                        "HTTPS_RULE",
                        "HTTP_RULE",
                        "SSL_RULE",
                        "TUNNEL_RULE"
                    ],
                )
                assert error is None, f"Error updating Bandwidth Rule: {error}"
                assert updated_rule is not None, "Updated Bandwidth Rule is None"
                assert (
                    updated_rule.description == updated_description
                ), f"Bandwidth Rule update failed: {updated_rule.as_dict()}"
            except Exception as exc:
                errors.append(f"Updating Bandwidth Rule failed: {exc}")

            # Step 6: List Bandwidth Rules and verify the rule is present
            try:
                rules, _, error = client.zia.bandwidth_control_rules.list_rules()
                assert error is None, f"Error listing Bandwidth Rules: {error}"
                assert rules is not None, "Bandwidth Rules list is None"
                assert any(rule.id == rule_id for rule in rules), "Newly created rule not found in the list of rules."
            except Exception as exc:
                errors.append(f"Listing Bandwidth Rules failed: {exc}")

            # Step 7: List Bandwidth Rules Lite
            try:
                rules_lite, _, error = client.zia.bandwidth_control_rules.list_rules_lite()
                assert error is None, f"Error listing Bandwidth Rules Lite: {error}"
                assert rules_lite is not None, "Bandwidth Rules Lite list is None"
            except Exception as exc:
                errors.append(f"Listing Bandwidth Rules Lite failed: {exc}")

        finally:
            cleanup_errors = []
            # Delete the Bandwidth Rule first (it depends on the class)
            if rule_id:
                try:
                    _, _, error = client.zia.bandwidth_control_rules.delete_rule(rule_id)
                    assert error is None, f"Error deleting Bandwidth Rule: {error}"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Bandwidth Rule failed: {exc}")

            # Delete the Bandwidth Class after the rule is deleted
            if class_id:
                try:
                    _, _, error = client.zia.bandwidth_classes.delete_class(class_id)
                    assert error is None, f"Error deleting Bandwidth Class: {error}"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Bandwidth Class failed: {exc}")

            errors.extend(cleanup_errors)

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
