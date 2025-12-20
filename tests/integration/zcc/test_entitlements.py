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


class TestEntitlements:
    """
    Integration Tests for the ZCC Entitlements API
    """

    @pytest.mark.vcr()
    def test_get_zdx_group_entitlements(self, fs):
        """Test getting ZDX group entitlements"""
        client = MockZCCClient(fs)
        errors = []

        try:
            entitlements, response, err = client.zcc.entitlements.get_zdx_group_entitlements()
            assert err is None, f"Error getting ZDX group entitlements: {err}"
            assert isinstance(entitlements, list), "Expected a list of entitlements"
            
            # Verify response structure if we have entitlements
            if entitlements:
                entitlement = entitlements[0]
                assert hasattr(entitlement, 'as_dict'), "Entitlement should have as_dict method"
        except Exception as exc:
            errors.append(f"Getting ZDX group entitlements failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the ZDX entitlements test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_zdx_group_entitlements_with_pagination(self, fs):
        """Test getting ZDX group entitlements with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            entitlements, response, err = client.zcc.entitlements.get_zdx_group_entitlements(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error getting ZDX group entitlements: {err}"
            assert isinstance(entitlements, list), "Expected a list of entitlements"
        except Exception as exc:
            errors.append(f"Getting ZDX group entitlements with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated ZDX entitlements test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_zpa_group_entitlements(self, fs):
        """Test getting ZPA group entitlements"""
        client = MockZCCClient(fs)
        errors = []

        try:
            entitlements, response, err = client.zcc.entitlements.get_zpa_group_entitlements()
            assert err is None, f"Error getting ZPA group entitlements: {err}"
            assert isinstance(entitlements, list), "Expected a list of entitlements"
            
            # Verify response structure if we have entitlements
            if entitlements:
                entitlement = entitlements[0]
                assert hasattr(entitlement, 'as_dict'), "Entitlement should have as_dict method"
        except Exception as exc:
            errors.append(f"Getting ZPA group entitlements failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the ZPA entitlements test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_zpa_group_entitlements_with_pagination(self, fs):
        """Test getting ZPA group entitlements with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            entitlements, response, err = client.zcc.entitlements.get_zpa_group_entitlements(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error getting ZPA group entitlements: {err}"
            assert isinstance(entitlements, list), "Expected a list of entitlements"
        except Exception as exc:
            errors.append(f"Getting ZPA group entitlements with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated ZPA entitlements test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_get_zpa_group_entitlements_with_search(self, fs):
        """Test getting ZPA group entitlements with search filter"""
        client = MockZCCClient(fs)
        errors = []

        try:
            entitlements, response, err = client.zcc.entitlements.get_zpa_group_entitlements(
                query_params={"search": "test"}
            )
            assert err is None, f"Error getting ZPA group entitlements with search: {err}"
            assert isinstance(entitlements, list), "Expected a list of entitlements"
        except Exception as exc:
            errors.append(f"Getting ZPA group entitlements with search failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the search ZPA entitlements test:\n{chr(10).join(errors)}"

