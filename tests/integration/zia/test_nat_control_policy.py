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


class TestNatControlPolicy:
    """
    Integration Tests for the NAT Control Policy API.
    """

    @pytest.mark.vcr()
    def test_nat_control_policy_crud(self, fs):
        """Test NAT Control Policy operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_rules
            rules, response, err = client.zia.nat_control_policy.list_rules()
            assert err is None, f"List NAT rules failed: {err}"
            assert rules is not None, "Rules list should not be None"
            assert isinstance(rules, list), "Rules should be a list"

            # Test get_rule with first rule if available
            if rules and len(rules) > 0:
                rule_id = rules[0].id
                fetched_rule, response, err = client.zia.nat_control_policy.get_rule(rule_id)
                assert err is None, f"Get NAT rule failed: {err}"
                assert fetched_rule is not None, "Fetched rule should not be None"

        except Exception as e:
            errors.append(f"Exception during NAT control policy test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
