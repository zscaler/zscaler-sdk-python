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


class TestProxies:
    """
    Integration Tests for the Proxies API.
    """

    @pytest.mark.vcr()
    def test_proxies_crud(self, fs):
        """Test Proxies operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_proxy_gateways
            gateways, response, err = client.zia.proxies.list_proxy_gateways()
            assert err is None, f"List proxy gateways failed: {err}"
            assert gateways is not None, "Gateways list should not be None"
            assert isinstance(gateways, list), "Gateways should be a list"

            # Test list_proxy_gateway_lite
            gateways_lite, response, err = client.zia.proxies.list_proxy_gateway_lite()
            assert err is None, f"List proxy gateways lite failed: {err}"

            # Test list_proxies
            proxies, response, err = client.zia.proxies.list_proxies()
            assert err is None, f"List proxies failed: {err}"
            assert proxies is not None, "Proxies list should not be None"

            # Test list_proxies_lite
            proxies_lite, response, err = client.zia.proxies.list_proxies_lite()
            assert err is None, f"List proxies lite failed: {err}"

            # Test get_proxy with first proxy if available
            if proxies and len(proxies) > 0:
                proxy_id = proxies[0].id
                fetched_proxy, response, err = client.zia.proxies.get_proxy(proxy_id)
                assert err is None, f"Get proxy failed: {err}"
                assert fetched_proxy is not None, "Fetched proxy should not be None"

        except Exception as e:
            errors.append(f"Exception during proxies test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
