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


class TestURLFilteringRule:
    """
    Integration Tests for the ZIA URL Filtering Rule
    """

    def test_url_filtering_rule(self, fs):
        client = MockZIAClient(fs)
        errors = []
        rule_id = None

        try:
            # Create a url filtering Rule
            rule_name = "tests-" + generate_random_string()
            rule_description = "tests-" + generate_random_string()
            created_rule = client.url_filtering.add_rule(
                name=rule_name,
                description=rule_description,
                state="ENABLED",
                action="BLOCK",
                order=1,
                rank=7,
                url_categories=["ANY"],
                protocols=["ANY_RULE"],
                device_trust_levels=[
                    "UNKNOWN_DEVICETRUSTLEVEL",
                    "LOW_TRUST",
                    "MEDIUM_TRUST",
                    "HIGH_TRUST",
                ],
                user_agent_types=[
                    "OPERA",
                    "FIREFOX",
                    "MSIE",
                    "MSEDGE",
                    "CHROME",
                    "SAFARI",
                    "MSCHREDGE",
                    "OTHER",
                ],
                user_risk_score_levels=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                request_methods=[
                    "CONNECT",
                    "DELETE",
                    "GET",
                    "HEAD",
                    "OPTIONS",
                    "OTHER",
                    "POST",
                    "PUT",
                    "TRACE",
                ],
            )
            rule_id = created_rule.get("id", None)

            # Retrieve the specific url filtering rule
            retrieved_rule = client.url_filtering.get_rule(rule_id)
            assert retrieved_rule["id"] == rule_id, "Failed to retrieve the correct url filtering rule"

            # Update the url filtering rule
            updated_description = "Updated " + generate_random_string()
            updated_rule = client.url_filtering.update_rule(
                rule_id,
                description=updated_description,
            )
            assert updated_rule["description"] == updated_description, "Failed to update description for url filtering rule"

            # List static ips and ensure the updated static ip is in the list
            ip_list = client.url_filtering.list_rules()
            assert any(ip["id"] == rule_id for ip in ip_list), "Updated url filtering rule not found in list"

        except Exception as exc:
            errors.append(exc)

        finally:
            # Cleanup
            cleanup_errors = []
            if rule_id:
                try:
                    delete_response_code = client.url_filtering.delete_rule(rule_id)
                    assert delete_response_code == 204, "Failed to delete url filtering rule"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting url filtering rule failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the url filtering rule lifecycle test: {errors}"
