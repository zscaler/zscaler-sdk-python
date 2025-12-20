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


class TestGRETunnel:
    """
    Integration Tests for the GRE Tunnel API.
    """

    @pytest.mark.vcr()
    def test_gre_tunnel_operations(self, fs):
        """Test GRE Tunnel operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_gre_tunnels
            tunnels, response, err = client.zia.gre_tunnel.list_gre_tunnels()
            assert err is None, f"List GRE tunnels failed: {err}"
            assert tunnels is not None, "Tunnels should not be None"
            assert isinstance(tunnels, list), "Tunnels should be a list"

            # Test get_gre_tunnel if available
            if tunnels and len(tunnels) > 0:
                tunnel_id = tunnels[0].id
                fetched_tunnel, response, err = client.zia.gre_tunnel.get_gre_tunnel(tunnel_id)
                assert err is None, f"Get GRE tunnel failed: {err}"
                assert fetched_tunnel is not None, "Fetched tunnel should not be None"

            # Test list_gre_ranges
            gre_ranges, response, err = client.zia.gre_tunnel.list_gre_ranges()
            assert err is None, f"List GRE ranges failed: {err}"

        except Exception as e:
            errors.append(f"Exception during GRE tunnel test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
