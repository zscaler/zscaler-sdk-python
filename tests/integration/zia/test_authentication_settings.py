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


import pytest
from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestExemptedUrls:
    """
    Integration Tests for Authentication Settings Exempted URLs.
    """

    def test_add_urls_to_exempt_list(self, fs):
        client = MockZIAClient(fs)
        urls_to_add = ["example.com", "testsite.com"]
        try:
            updated_exempt_list = client.authentication_settings.add_urls_to_exempt_list(urls_to_add)
            assert updated_exempt_list is not None, "The update exempt list operation returned None."
        except Exception as exc:
            pytest.fail(f"Failed to add URLs to exempt list: {exc}")

    def test_get_exempted_urls(self, fs):
        client = MockZIAClient(fs)
        try:
            exempt_list = client.authentication_settings.get_exempted_urls()
            assert isinstance(exempt_list, list), "Failed to retrieve exempt list."
        except Exception as exc:
            pytest.fail(f"Exempt list retrieval failed: {exc}")

    def test_delete_urls_from_exempt_list(self, fs):
        client = MockZIAClient(fs)
        try:
            urls_to_clean = ["example.com", "testsite.com"]
            client.authentication_settings.delete_urls_from_exempt_list(urls_to_clean)
            print("Cleanup successful for exempt URLs list.")
        except Exception as exc:
            print(f"Cleanup failed for exempt URLs list: {exc}")
