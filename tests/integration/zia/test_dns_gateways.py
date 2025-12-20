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


class TestDNSGateways:
    """
    Integration Tests for the DNS Gateways API.
    """

    @pytest.mark.vcr()
    def test_dns_gateways_crud(self, fs):
        """Test DNS Gateways operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_dns_gateways
            gateways, response, err = client.zia.dns_gatways.list_dns_gateways()
            assert err is None, f"List DNS gateways failed: {err}"
            assert gateways is not None, "Gateways list should not be None"
            assert isinstance(gateways, list), "Gateways should be a list"

            # Test get_dns_gateways with first gateway if available
            if gateways and len(gateways) > 0:
                gateway_id = gateways[0].id
                fetched_gateway, response, err = client.zia.dns_gatways.get_dns_gateways(gateway_id)
                assert err is None, f"Get DNS gateway failed: {err}"
                assert fetched_gateway is not None, "Fetched gateway should not be None"

        except Exception as e:
            errors.append(f"Exception during DNS gateways test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
