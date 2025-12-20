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


class TestCloudAppControl:
    """
    Integration Tests for the Cloud App Control API.
    """

    @pytest.mark.vcr()
    def test_cloudappcontrol_operations(self, fs):
        """Test Cloud App Control operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test get_rule_type_mapping
            mapping, response, err = client.zia.cloudappcontrol.get_rule_type_mapping()
            assert err is None, f"Get rule type mapping failed: {err}"
            assert mapping is not None, "Mapping should not be None"

            # Test list_rules for STREAMING_MEDIA rule type
            rules, response, err = client.zia.cloudappcontrol.list_rules(rule_type="STREAMING_MEDIA")
            assert err is None, f"List rules failed: {err}"
            assert rules is not None, "Rules should not be None"
            assert isinstance(rules, list), "Rules should be a list"

            # Test get_rule if available
            if rules and len(rules) > 0:
                rule_id = rules[0].id
                fetched_rule, response, err = client.zia.cloudappcontrol.get_rule(
                    rule_type="STREAMING_MEDIA", rule_id=str(rule_id)
                )
                assert err is None, f"Get rule failed: {err}"

        except Exception as e:
            errors.append(f"Exception during cloud app control test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

