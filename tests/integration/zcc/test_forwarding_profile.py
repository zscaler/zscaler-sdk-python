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


class TestForwardingProfile:
    """
    Integration Tests for the ZCC Forwarding Profile API
    """

    @pytest.mark.vcr()
    def test_list_forwarding_profiles(self, fs):
        """Test listing forwarding profiles by company"""
        client = MockZCCClient(fs)
        errors = []

        try:
            profiles, response, err = client.zcc.forwarding_profile.list_by_company()
            assert err is None, f"Error listing forwarding profiles: {err}"
            assert isinstance(profiles, list), "Expected a list of forwarding profiles"
            
            # Verify response structure if we have profiles
            if profiles:
                profile = profiles[0]
                assert hasattr(profile, 'as_dict'), "Forwarding profile should have as_dict method"
        except Exception as exc:
            errors.append(f"Listing forwarding profiles failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the forwarding profile test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_forwarding_profiles_with_pagination(self, fs):
        """Test listing forwarding profiles with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            profiles, response, err = client.zcc.forwarding_profile.list_by_company(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error listing forwarding profiles with pagination: {err}"
            assert isinstance(profiles, list), "Expected a list of forwarding profiles"
        except Exception as exc:
            errors.append(f"Listing forwarding profiles with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated forwarding profile test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_forwarding_profiles_with_search(self, fs):
        """Test listing forwarding profiles with search filter"""
        client = MockZCCClient(fs)
        errors = []

        try:
            profiles, response, err = client.zcc.forwarding_profile.list_by_company(
                query_params={"search": "test"}
            )
            assert err is None, f"Error listing forwarding profiles with search: {err}"
            assert isinstance(profiles, list), "Expected a list of forwarding profiles"
        except Exception as exc:
            errors.append(f"Listing forwarding profiles with search failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the search forwarding profile test:\n{chr(10).join(errors)}"

