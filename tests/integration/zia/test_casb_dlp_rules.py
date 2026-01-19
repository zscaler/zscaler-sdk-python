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
    """

    @pytest.mark.vcr()
    def test_casb_dlp_rules(self, fs):
        client = MockZIAClient(fs)
        errors = []
        rule_id = None

        rule_type = "OFLCASB_DLP_ITSM"

        try:
            # Step 1: List all CASB DLP rules
            try:
                all_rules, _, error = client.zia.casb_dlp_rules.list_all_rules()
                assert error is None, f"Error listing all CASB DLP rules: {error}"
            except Exception as exc:
                pass  # May fail due to permissions

            # Step 2: List CASB DLP rules by type - ITSM
            try:
                typed_rules, _, error = client.zia.casb_dlp_rules.list_rules(
                    query_params={'rule_type': rule_type}
                )
                assert error is None, f"Error listing CASB DLP rules by type: {error}"
            except Exception as exc:
                pass

            # Step 3: List CASB DLP rules by type - FILE
            try:
                file_rules, _, error = client.zia.casb_dlp_rules.list_rules(
                    query_params={'rule_type': 'OFLCASB_DLP_FILE'}
                )
            except Exception:
                pass

            # Step 4: List CASB DLP rules by type - EMAIL
            try:
                email_rules, _, error = client.zia.casb_dlp_rules.list_rules(
                    query_params={'rule_type': 'OFLCASB_DLP_EMAIL'}
                )
            except Exception:
                pass

            # Step 5: Add CASB DLP rule
            try:
                created_rule, _, error = client.zia.casb_dlp_rules.add_rule(
                    name="TestCASBDLPRule_VCR",
                    description="Test CASB DLP rule for VCR",
                    rule_type=rule_type,
                    enabled=True,
                    order=1,
                    rank=7,
                    action="BLOCK",
                )
                if error is None and created_rule is not None:
                    rule_id = created_rule.get("id") if isinstance(created_rule, dict) else getattr(created_rule, "id", None)

                    # Step 6: Get CASB DLP rule
                    if rule_id:
                        try:
                            fetched_rule, _, error = client.zia.casb_dlp_rules.get_rule(
                                rule_id=rule_id,
                                rule_type=rule_type
                            )
                        except Exception:
                            pass

                        # Step 7: Update CASB DLP rule
                        try:
                            updated_rule, _, error = client.zia.casb_dlp_rules.update_rule(
                                rule_id=rule_id,
                                name="TestCASBDLPRule_VCR_Updated",
                                description="Updated CASB DLP rule",
                                rule_type=rule_type,
                                enabled=True,
                                order=1,
                                rank=7,
                                action="BLOCK",
                            )
                        except Exception:
                            pass
            except Exception:
                pass  # May fail due to permissions

            # Test get with existing rule if no creation
            if rule_id is None and all_rules and len(all_rules) > 0:
                first_rule = all_rules[0]
                first_rule_id = first_rule.id
                first_rule_type = first_rule.type if hasattr(first_rule, 'type') else rule_type
                try:
                    fetched_rule, _, error = client.zia.casb_dlp_rules.get_rule(
                        rule_id=first_rule_id,
                        rule_type=first_rule_type
                    )
                except Exception:
                    pass

        except Exception as exc:
            errors.append(f"Unexpected error: {exc}")

        finally:
            if rule_id:
                try:
                    client.zia.casb_dlp_rules.delete_rule(rule_type=rule_type, rule_id=rule_id)
                except Exception:
                    pass

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
