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


class TestTrafficDatacenters:
    """
    Integration Tests for the Traffic Datacenters API.
    """

    @pytest.mark.vcr()
    def test_traffic_datacenters_crud(self, fs):
        """Test Traffic Datacenters operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_datacenters
            datacenters, response, err = client.zia.traffic_datacenters.list_datacenters()
            assert err is None, f"List datacenters failed: {err}"
            assert datacenters is not None, "Datacenters list should not be None"
            assert isinstance(datacenters, list), "Datacenters should be a list"

            # Test list_dc_exclusions
            exclusions, response, err = client.zia.traffic_datacenters.list_dc_exclusions()
            assert err is None, f"List DC exclusions failed: {err}"

        except Exception as e:
            errors.append(f"Exception during traffic datacenters test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
