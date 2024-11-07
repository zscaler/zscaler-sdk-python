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
from tests.integration.zcon.conftest import MockZCONClient


@pytest.fixture
def fs():
    yield


class TestLocations:
    """
    Integration Tests for the ZIA Locations
    """

    def test_locations(self, fs):
        client = MockZCONClient(fs)
        errors = []  # Initialize an empty list to collect errors
        location_id = None

        try:
            # Test list_locations function
            try:
                locations = client.locations.list_locations()
                assert isinstance(locations, list), "Expected a list of locations"
                assert len(locations) > 0, "Expected at least one location"
                location_id = locations[0].get("id")
                assert location_id is not None, "Expected the first location to have an ID"
            except Exception as exc:
                errors.append(f"Listing locations failed: {exc}")

            # Test get_location function using the location_id from the previous step
            if location_id:
                try:
                    location_details = client.locations.get_location(location_id)
                    assert location_details is not None, "Expected valid location details"
                    assert location_details.get("id") == location_id, "Mismatch in location ID"
                except Exception as exc:
                    errors.append(f"Fetching location by ID failed: {exc}")

            # Test list_locations_lite function
            try:
                locations_lite = client.locations.list_locations_lite()
                assert isinstance(locations_lite, list), "Expected a list of lite locations"
                assert len(locations_lite) > 0, "Expected at least one lite location"
                first_lite_location_id = locations_lite[0].get("id")
                assert first_lite_location_id is not None, "Expected the first lite location to have an ID"
            except Exception as exc:
                errors.append(f"Listing lite locations failed: {exc}")

        except Exception as exc:
            errors.append(f"Test Locations suite failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during locations test: {errors}"
