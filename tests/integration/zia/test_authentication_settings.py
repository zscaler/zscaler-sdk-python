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
from tests.integration.zia.conftest import MockZIAClient, TestNameGenerator


@pytest.fixture
def fs():
    yield


class TestExemptedUrls:
    """
    Integration Test for Authentication Settings Exempted URLs Workflow.
    """

    @pytest.mark.vcr()
    def test_exempted_urls_workflow(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Use deterministic URLs for VCR testing
        test_urls = TestNameGenerator.generate_urls(count=5, domain="vcr-test.com")

        try:
            # Step 1: Add URLs to the exempt list
            try:
                updated_urls, _, error = client.zia.authentication_settings.add_urls_to_exempt_list(test_urls)
                assert error is None, f"Error adding URLs to exempt list: {error}"
                assert isinstance(updated_urls, list), "Expected a list in response"
                assert all(url in updated_urls for url in test_urls), "Some test URLs were not added"
            except Exception as exc:
                errors.append(f"Failed to add URLs to exempt list: {exc}")

            # Step 2: Retrieve and verify the exempt list
            try:
                current_urls, _, error = client.zia.authentication_settings.get_exempted_urls()
                assert error is None, f"Error retrieving exempt list: {error}"
                assert isinstance(current_urls, list), "Expected list response from get_exempted_urls"
                assert all(url in current_urls for url in test_urls), "Some test URLs not found in exempt list"
            except Exception as exc:
                errors.append(f"Failed to retrieve or verify exempt list: {exc}")

        finally:
            # Step 3: Cleanup - delete all URLs
            try:
                _, _, error = client.zia.authentication_settings.delete_urls_from_exempt_list([])
                assert error is None, f"Error clearing exempt list: {error}"
            except Exception as exc:
                errors.append(f"Cleanup failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the exempt URL workflow test:\n{chr(10).join(errors)}"
