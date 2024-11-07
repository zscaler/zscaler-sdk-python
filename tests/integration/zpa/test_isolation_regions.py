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

from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestCBIRegions:
    """
    Integration Tests for the CBI Region.
    """

    def test_cbi_region(self, fs):
        client = MockZPAClient(fs)  # Client instantiation with fixture as specified
        errors = []  # Initialize an empty list to collect errors

        # List all CBI regions
        try:
            regions = client.isolation.list_regions()
            assert isinstance(regions, list) and len(regions) >= 2, "Expected at least two CBI regions"
            tested_regions = regions[:2]  # Test the first two regions
        except AssertionError as exc:
            errors.append(f"Assertion error: {str(exc)}")
        except Exception as exc:
            errors.append(f"Listing CBI regions failed: {str(exc)}")

        # Fetch and test each of the selected CBI regions by their IDs
        for region in tested_regions:
            region_id = region["id"]
            try:
                fetched_region = client.isolation.get_region(region_id)
                assert fetched_region is not None, "Expected a valid CBI region object"
                assert fetched_region["id"] == region_id, "Mismatch in CBI region ID"
            except AssertionError as exc:
                errors.append(f"Assertion error in region {region_id}: {str(exc)}")
            except Exception as exc:
                errors.append(f"Fetching CBI region by ID {region_id} failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during CBI region operations test: {errors}"
