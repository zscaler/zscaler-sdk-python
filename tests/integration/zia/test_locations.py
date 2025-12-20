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


class TestLocations:
    """
    Integration Tests for the Locations API.
    """

    @pytest.mark.vcr()
    def test_locations_operations(self, fs):
        """Test Locations operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_locations
            locations, response, err = client.zia.locations.list_locations()
            assert err is None, f"List locations failed: {err}"
            assert locations is not None, "Locations should not be None"
            assert isinstance(locations, list), "Locations should be a list"

            # Test list_locations_lite
            locations_lite, response, err = client.zia.locations.list_locations_lite()
            assert err is None, f"List locations lite failed: {err}"

            # Test get_location if available
            if locations and len(locations) > 0:
                location_id = locations[0].id
                fetched_location, response, err = client.zia.locations.get_location(location_id)
                assert err is None, f"Get location failed: {err}"
                assert fetched_location is not None, "Fetched location should not be None"

                # Test list_sub_locations
                sub_locations, response, err = client.zia.locations.list_sub_locations(location_id)
                # May be empty or error if no sub-locations exist
                if err is None:
                    assert sub_locations is not None, "Sub-locations should not be None"

            # Test list_location_groups
            groups, response, err = client.zia.locations.list_location_groups()
            assert err is None, f"List location groups failed: {err}"
            assert groups is not None, "Location groups should not be None"

            # Test list_location_groups_lite
            groups_lite, response, err = client.zia.locations.list_location_groups_lite()
            assert err is None, f"List location groups lite failed: {err}"

            # Test get_location_group if available
            if groups and len(groups) > 0:
                group_id = groups[0].id
                fetched_group, response, err = client.zia.locations.get_location_group(group_id)
                assert err is None, f"Get location group failed: {err}"

            # Test list_location_groups_count
            count, response, err = client.zia.locations.list_location_groups_count()
            assert err is None, f"List location groups count failed: {err}"

            # Test get_supported_countries - may not be available on all tenants
            countries, response, err = client.zia.locations.get_supported_countries()
            if err is None:
                assert countries is not None, "Countries should not be None"

            # Test list_cities_by_name - may not be available on all tenants
            cities, response, err = client.zia.locations.list_cities_by_name(
                query_params={"country": "United States", "search": "San"}
            )
            # May return empty list or error

        except Exception as e:
            errors.append(f"Exception during locations test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

