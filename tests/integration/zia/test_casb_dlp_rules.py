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


@pytest.fixture
def fs():
    yield


class TestCasbDlpRules:
    """
    Integration Tests for the CASB DLP Rules API.
    
    Note: CRUD operations for CASB DLP rules require specific tenant configuration.
    This test focuses on read operations.
    """

    @pytest.mark.vcr()
    def test_casb_dlp_rules(self, fs):
        client = MockZIAClient(fs)
        errors = []

        rule_type = "OFLCASB_DLP_ITSM"

        try:
            # Step 1: List all CASB DLP rules
            try:
                all_rules, _, error = client.zia.casb_dlp_rules.list_all_rules()
                assert error is None, f"Error listing all CASB DLP rules: {error}"
                # all_rules can be an empty list, which is valid
            except Exception as exc:
                errors.append(f"Failed to list all CASB DLP rules: {exc}")

            # Step 2: List CASB DLP rules by type - ITSM
            try:
                typed_rules, _, error = client.zia.casb_dlp_rules.list_rules(
                    query_params={'rule_type': rule_type}
                )
                assert error is None, f"Error listing CASB DLP rules by type: {error}"
            except Exception as exc:
                errors.append(f"Failed to list CASB DLP rules by type: {exc}")

            # Step 3: List CASB DLP rules by type - FILE
            try:
                file_rules, _, error = client.zia.casb_dlp_rules.list_rules(
                    query_params={'rule_type': 'OFLCASB_DLP_FILE'}
                )
                assert error is None, f"Error listing CASB DLP FILE rules: {error}"
            except Exception as exc:
                errors.append(f"Failed to list CASB DLP FILE rules: {exc}")

            # Step 4: List CASB DLP rules by type - EMAIL
            try:
                email_rules, _, error = client.zia.casb_dlp_rules.list_rules(
                    query_params={'rule_type': 'OFLCASB_DLP_EMAIL'}
                )
                assert error is None, f"Error listing CASB DLP EMAIL rules: {error}"
            except Exception as exc:
                errors.append(f"Failed to list CASB DLP EMAIL rules: {exc}")

            # Step 5: Get a specific rule by ID (if any rules exist)
            try:
                if all_rules and len(all_rules) > 0:
                    first_rule = all_rules[0]
                    first_rule_id = first_rule.id
                    first_rule_type = first_rule.type if hasattr(first_rule, 'type') else rule_type
                    fetched_rule, _, error = client.zia.casb_dlp_rules.get_rule(
                        rule_id=first_rule_id,
                        rule_type=first_rule_type
                    )
                    assert error is None, f"Error retrieving CASB DLP rule: {error}"
                    assert fetched_rule is not None, "Retrieved CASB DLP rule is None"
            except Exception as exc:
                errors.append(f"Failed to retrieve CASB DLP rule: {exc}")

        except Exception as exc:
            errors.append(f"Unexpected error: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
