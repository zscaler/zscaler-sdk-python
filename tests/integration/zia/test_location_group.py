"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import pytest

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestLocationGroup:
    """
    Integration Tests for the Location Group.
    """

    def test_location_group(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        group_id = None

        try:
            # List all groups
            groups = client.zia.locations.list_location_groups()
            assert isinstance(groups, list), "Expected a list of groups"

            # Use lite version to list location groups with minimal details
            try:
                lite_groups = client.zia.locations.list_location_groups_lite()
                assert isinstance(lite_groups, list), "Expected a lite list of groups"
            except Exception as exc:
                errors.append(f"Listing lite groups failed: {exc}")

            # Use lite version to list location groups with minimal details
            try:
                lite_count = client.zia.locations.list_location_groups_count()
                assert isinstance(lite_count, int), "Expected the count of all groups to be an integer"
            except Exception as exc:
                errors.append(f"Listing the count of all groups failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing groups failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during groups test: {errors}"
