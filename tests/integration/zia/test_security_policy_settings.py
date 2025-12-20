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


class TestSecurityPolicySettings:
    """
    Integration Tests for the Security Policy Settings API.
    """

    @pytest.mark.vcr()
    def test_security_policy_settings_operations(self, fs):
        """Test Security Policy Settings operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test get_whitelist
            whitelist, response, err = client.zia.security_policy_settings.get_whitelist()
            assert err is None, f"Get whitelist failed: {err}"
            assert whitelist is not None, "Whitelist should not be None"

            # Test get_blacklist
            blacklist, response, err = client.zia.security_policy_settings.get_blacklist()
            assert err is None, f"Get blacklist failed: {err}"
            assert blacklist is not None, "Blacklist should not be None"

        except Exception as e:
            errors.append(f"Exception during security policy settings test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

