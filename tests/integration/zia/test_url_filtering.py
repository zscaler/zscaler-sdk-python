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


@pytest.fixture
def fs():
    yield


class TestURLFiltering:
    """
    Integration Tests for the URL Filtering API.
    """

    @pytest.mark.vcr()
    def test_url_filtering_crud(self, fs):
        """Test URL Filtering Rules operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_rules
            rules, response, err = client.zia.url_filtering.list_rules()
            assert err is None, f"List rules failed: {err}"
            assert rules is not None, "Rules list should not be None"
            assert isinstance(rules, list), "Rules should be a list"

            # Test list_rules with search
            search_rules, response, err = client.zia.url_filtering.list_rules(
                query_params={"search": "Default"}
            )
            assert err is None, f"List rules with search failed: {err}"

            # Test get_rule - get existing rule if available
            if rules and len(rules) > 0:
                rule_id = rules[0].id
                fetched_rule, response, err = client.zia.url_filtering.get_rule(rule_id)
                assert err is None, f"Get rule failed: {err}"
                assert fetched_rule is not None, "Fetched rule should not be None"

            # Test get_url_and_app_settings
            settings, response, err = client.zia.url_filtering.get_url_and_app_settings()
            assert err is None, f"Get URL and app settings failed: {err}"
            assert settings is not None, "Settings should not be None"

        except Exception as e:
            errors.append(f"Exception during URL filtering test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
