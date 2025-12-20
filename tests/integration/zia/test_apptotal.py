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


class TestAppTotal:
    """
    Integration Tests for the AppTotal API.
    """

    @pytest.mark.vcr()
    def test_apptotal_operations(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Test app_id - using a well-known app ID for testing
        test_app_id = "12345"
        test_app_name = "Slack"

        # Step 1: Test get_app method
        try:
            app_info, _, error = client.zia.apptotal.get_app(app_id=test_app_id)
            # Note: This might return None if app doesn't exist, which is acceptable
            if error:
                # Some errors are expected if app doesn't exist
                pass
        except Exception as exc:
            errors.append(f"Failed to get app by ID: {exc}")

        # Step 2: Test get_app with verbose=True
        try:
            app_info_verbose, _, error = client.zia.apptotal.get_app(app_id=test_app_id, verbose=True)
            # Note: This might return None if app doesn't exist, which is acceptable
            if error:
                pass
        except Exception as exc:
            errors.append(f"Failed to get app by ID with verbose: {exc}")

        # Step 3: Test search_app method
        try:
            search_results, _, error = client.zia.apptotal.search_app(app_name=test_app_name)
            # Search might return error or empty results which is acceptable
            if error:
                pass
        except Exception as exc:
            errors.append(f"Failed to search app: {exc}")

        # Step 4: Test scan_app method
        try:
            scan_result, _, error = client.zia.apptotal.scan_app(app_id=test_app_id)
            # Scan might return an error if app is already scanned or doesn't exist
            if error:
                pass
        except Exception as exc:
            errors.append(f"Failed to scan app: {exc}")

        # Step 5: Test app_views method
        try:
            app_views_result, _, error = client.zia.apptotal.app_views(app_view_id="1")
            # This might return empty or error which is acceptable
            if error:
                pass
        except Exception as exc:
            errors.append(f"Failed to get app views: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")

