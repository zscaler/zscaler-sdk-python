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


class TestDedicatedIPGateways:
    """
    Integration Tests for the Dedicated IP Gateways API.
    """

    @pytest.mark.vcr()
    def test_dedicated_ip_gateways_operations(self, fs):
        """Test Dedicated IP Gateways operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_dedicated_ip_gw_lite
            gateways, response, err = client.zia.dedicated_ip_gateways.list_dedicated_ip_gw_lite()
            assert err is None, f"List dedicated IP gateways lite failed: {err}"
            assert gateways is not None, "Gateways should not be None"
            assert isinstance(gateways, list), "Gateways should be a list"

        except Exception as e:
            errors.append(f"Exception during dedicated IP gateways test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

