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


class TestSecurityWhitelistBlacklist:
    """
    Integration Tests for the Security Whitelist and Blacklist.
    """

    def test_add_url_to_whitelist(self, fs):
        client = MockZIAClient(fs)
        url_to_add = "example.com"
        try:
            updated_whitelist = client.security.add_urls_to_whitelist([url_to_add])
            assert url_to_add in updated_whitelist, f"{url_to_add} not added to whitelist."
        except Exception as exc:
            pytest.fail(f"Failed to add URL to whitelist: {exc}")

    def test_get_whitelist(self, fs):
        client = MockZIAClient(fs)
        try:
            whitelist = client.security.get_whitelist()
            assert isinstance(whitelist, list), "Failed to retrieve whitelist."
        except Exception as exc:
            pytest.fail(f"Whitelist retrieval failed: {exc}")

    def test_replace_url_from_whitelist(self, fs):
        client = MockZIAClient(fs)
        url_to_replace = ["newsite.com"]
        try:
            updated_whitelist = client.security.replace_whitelist(url_to_replace)
            assert url_to_replace[0] in updated_whitelist, "Whitelist replace operation failed."
        except Exception as exc:
            pytest.fail(f"Failed to replace whitelist: {exc}")

    def test_delete_urls_from_whitelist(self, fs):
        client = MockZIAClient(fs)
        url_to_delete = "example.com"
        try:
            updated_whitelist = client.security.delete_urls_from_whitelist([url_to_delete])
            assert url_to_delete not in updated_whitelist, f"{url_to_delete} was not deleted from whitelist."
        except Exception as exc:
            pytest.fail(f"Failed to delete URL from whitelist: {exc}")

    def test_add_urls_to_blacklist(self, fs):
        client = MockZIAClient(fs)
        url_to_add = "badexample.com"
        try:
            updated_blacklist = client.security.add_urls_to_blacklist([url_to_add])
            assert url_to_add in updated_blacklist, f"{url_to_add} not added to blacklist."
        except Exception as exc:
            pytest.fail(f"Failed to add URL to blacklist: {exc}")

    def test_get_blacklist(self, fs):
        client = MockZIAClient(fs)
        try:
            blacklist = client.security.get_blacklist()
            assert isinstance(blacklist, list), "Failed to retrieve blacklist."
        except Exception as exc:
            pytest.fail(f"Blacklist retrieval failed: {exc}")

    def test_replace_blacklist(self, fs):
        client = MockZIAClient(fs)
        new_blacklist_urls = ["newbadexample.com"]
        try:
            updated_blacklist = client.security.replace_blacklist(new_blacklist_urls)
            assert new_blacklist_urls[0] in updated_blacklist, "Blacklist replace operation failed."
        except Exception as exc:
            pytest.fail(f"Failed to replace blacklist: {exc}")

    def test_erase_blacklist(self, fs):
        client = MockZIAClient(fs)
        try:
            result = client.security.erase_blacklist()
            assert result == 204 or "successfully erased" in result.lower(), "Failed to erase blacklist."
        except Exception as exc:
            pytest.fail(f"Failed to erase blacklist: {exc}")
