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


class TestWebPolicy:
    """
    Integration Tests for the ZCC Web Policy API
    """

    @pytest.mark.vcr()
    def test_list_web_policies(self, fs):
        """Test listing web policies by company"""
        client = MockZCCClient(fs)
        errors = []

        try:
            policies, response, err = client.zcc.web_policy.list_by_company()
            assert err is None, f"Error listing web policies: {err}"
            assert isinstance(policies, list), "Expected a list of web policies"
            
            # Verify response structure if we have policies
            if policies:
                policy = policies[0]
                assert hasattr(policy, 'as_dict'), "Web policy should have as_dict method"
        except Exception as exc:
            errors.append(f"Listing web policies failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the web policy test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_web_policies_with_pagination(self, fs):
        """Test listing web policies with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            policies, response, err = client.zcc.web_policy.list_by_company(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error listing web policies with pagination: {err}"
            assert isinstance(policies, list), "Expected a list of web policies"
        except Exception as exc:
            errors.append(f"Listing web policies with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated web policy test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_web_policies_with_device_type(self, fs):
        """Test listing web policies filtered by device type"""
        client = MockZCCClient(fs)
        errors = []

        device_types = ["windows", "macos", "ios", "android", "linux"]

        for device_type in device_types:
            try:
                policies, response, err = client.zcc.web_policy.list_by_company(
                    query_params={"device_type": device_type}
                )
                assert err is None, f"Error listing web policies for {device_type}: {err}"
                assert isinstance(policies, list), f"Expected a list of web policies for {device_type}"
            except Exception as exc:
                errors.append(f"Listing web policies for {device_type} failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the web policy device type test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_web_policies_with_search(self, fs):
        """Test listing web policies with search filter"""
        client = MockZCCClient(fs)
        errors = []

        try:
            policies, response, err = client.zcc.web_policy.list_by_company(
                query_params={"search": "test"}
            )
            assert err is None, f"Error listing web policies with search: {err}"
            assert isinstance(policies, list), "Expected a list of web policies"
        except Exception as exc:
            errors.append(f"Listing web policies with search failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the search web policy test:\n{chr(10).join(errors)}"

