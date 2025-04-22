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
        errors = []
        group_id = None

        try:
            # Step 1: List all groups
            try:
                group_list, _, error = client.zia.locations.list_location_groups()
                assert error is None, f"List Location Groups Error: {error}"
                assert isinstance(group_list, list), "Expected a list of groups"
            except Exception as exc:
                errors.append(f"Listing all groups failed: {exc}")

            # Step 2: List lite version of groups
            try:
                lite_groups, _, error = client.zia.locations.list_location_groups_lite()
                assert error is None, f"List Lite Groups Error: {error}"
                assert isinstance(lite_groups, list), "Expected a lite list of groups"
            except Exception as exc:
                errors.append(f"Listing lite groups failed: {exc}")

            # Step 3: Get count of location groups
            try:
                lite_count, _, error = client.zia.locations.list_location_groups_count()
                assert error is None, f"Location Group Count Error: {error}"
                assert isinstance(lite_count, int), f"Expected integer count, got {type(lite_count).__name__}"
            except Exception as exc:
                errors.append(f"Listing the count of all groups failed: {exc}")

        except Exception as exc:
            errors.append(f"Unexpected failure during location group operations: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
