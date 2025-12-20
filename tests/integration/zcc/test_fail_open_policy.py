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
from tests.integration.zcc.conftest import MockZCCClient


@pytest.fixture
def fs():
    yield


class TestFailOpenPolicy:
    """
    Integration Tests for the ZCC Fail Open Policy API
    """

    @pytest.mark.vcr()
    def test_list_fail_open_policies(self, fs):
        """Test listing fail open policies by company"""
        client = MockZCCClient(fs)
        errors = []

        try:
            policies, response, err = client.zcc.fail_open_policy.list_by_company()
            assert err is None, f"Error listing fail open policies: {err}"
            assert isinstance(policies, list), "Expected a list of fail open policies"
            
            # Verify response structure if we have policies
            if policies:
                policy = policies[0]
                assert hasattr(policy, 'as_dict'), "Fail open policy should have as_dict method"
        except Exception as exc:
            errors.append(f"Listing fail open policies failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the fail open policy test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_fail_open_policies_with_pagination(self, fs):
        """Test listing fail open policies with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            policies, response, err = client.zcc.fail_open_policy.list_by_company(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error listing fail open policies with pagination: {err}"
            assert isinstance(policies, list), "Expected a list of fail open policies"
        except Exception as exc:
            errors.append(f"Listing fail open policies with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated fail open policy test:\n{chr(10).join(errors)}"

