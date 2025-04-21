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


class TestSecurityWhitelistBlacklist:
    """
    Integration Tests for the Security Whitelist and Blacklist Workflow.
    """

    def test_security_policy_whitelist_blacklist_workflow(self, fs):
        client = MockZIAClient(fs)
        errors = []

        whitelist_urls = ["example.com", "testsite.com"]
        blacklist_urls = ["badexample.com", "malicious.com"]
        new_whitelist_urls = ["newsite.com"]
        new_blacklist_urls = ["newbadexample.com"]

        try:
            # Step 1: Add URLs to whitelist
            try:
                result, _, error = client.zia.security_policy_settings.add_urls_to_whitelist(whitelist_urls)
                assert error is None, f"Error adding to whitelist: {error}"
                assert all(url in result.whitelist_urls for url in whitelist_urls), "Not all URLs added to whitelist"
            except Exception as exc:
                errors.append(f"Failed to add URLs to whitelist: {exc}")

            # Step 2: Get whitelist
            try:
                result, _, error = client.zia.security_policy_settings.get_whitelist()
                assert error is None, f"Error retrieving whitelist: {error}"
                assert isinstance(result.whitelist_urls, list), "Whitelist is not a list"
            except Exception as exc:
                errors.append(f"Failed to get whitelist: {exc}")

            # Step 3: Replace whitelist
            try:
                result, _, error = client.zia.security_policy_settings.replace_whitelist(new_whitelist_urls)
                assert error is None, f"Error replacing whitelist: {error}"
                assert result.whitelist_urls == new_whitelist_urls, "Whitelist replace failed"
            except Exception as exc:
                errors.append(f"Failed to replace whitelist: {exc}")

            # Step 4: Delete from whitelist
            try:
                result, _, error = client.zia.security_policy_settings.delete_urls_from_whitelist(new_whitelist_urls)
                assert error is None, f"Error deleting from whitelist: {error}"
                assert new_whitelist_urls[0] not in result.whitelist_urls, "URL not removed from whitelist"
            except Exception as exc:
                errors.append(f"Failed to delete URLs from whitelist: {exc}")

            # Step 5: Add URLs to blacklist
            try:
                result, _, error = client.zia.security_policy_settings.add_urls_to_blacklist(blacklist_urls)
                assert error is None, f"Error adding to blacklist: {error}"
                assert all(url in result.blacklist_urls for url in blacklist_urls), "Not all URLs added to blacklist"
            except Exception as exc:
                errors.append(f"Failed to add URLs to blacklist: {exc}")

            # Step 6: Get blacklist
            try:
                result, _, error = client.zia.security_policy_settings.get_blacklist()
                assert error is None, f"Error retrieving blacklist: {error}"
                assert isinstance(result.blacklist_urls, list), "Blacklist is not a list"
            except Exception as exc:
                errors.append(f"Failed to get blacklist: {exc}")

            # Step 7: Replace blacklist
            try:
                result, _, error = client.zia.security_policy_settings.replace_blacklist(new_blacklist_urls)
                assert error is None, f"Error replacing blacklist: {error}"
                assert result.blacklist_urls == new_blacklist_urls, "Blacklist replace failed"
            except Exception as exc:
                errors.append(f"Failed to replace blacklist: {exc}")

        finally:
            # Step 8: Cleanup — Erase whitelist and blacklist
            try:
                _, _, error = client.zia.security_policy_settings.erase_whitelist()
                assert error is None, f"Error erasing whitelist: {error}"
            except Exception as exc:
                errors.append(f"Whitelist cleanup failed: {exc}")

            try:
                _, _, error = client.zia.security_policy_settings.erase_blacklist()
                assert error is None, f"Error erasing blacklist: {error}"
            except Exception as exc:
                errors.append(f"Blacklist cleanup failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during security policy test:\n{chr(10).join(errors)}"
