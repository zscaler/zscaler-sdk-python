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


class TestIPv6Config:
    """
    Integration Tests for the IPv6 Configuration API.
    """

    @pytest.mark.vcr()
    def test_ipv6_config_operations(self, fs):
        """Test IPv6 Configuration operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test get_ipv6_config
            ipv6_config, response, err = client.zia.ipv6_config.get_ipv6_config()
            assert err is None, f"Get IPv6 config failed: {err}"
            assert ipv6_config is not None, "IPv6 config should not be None"

            # Test list_dns64_prefix
            dns64_prefixes, response, err = client.zia.ipv6_config.list_dns64_prefix()
            assert err is None, f"List DNS64 prefix failed: {err}"
            assert dns64_prefixes is not None, "DNS64 prefixes should not be None"
            assert isinstance(dns64_prefixes, list), "DNS64 prefixes should be a list"

            # Test list_nat64_prefix
            nat64_prefixes, response, err = client.zia.ipv6_config.list_nat64_prefix()
            assert err is None, f"List NAT64 prefix failed: {err}"
            assert nat64_prefixes is not None, "NAT64 prefixes should not be None"
            assert isinstance(nat64_prefixes, list), "NAT64 prefixes should be a list"

        except Exception as e:
            errors.append(f"Exception during IPv6 config test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

