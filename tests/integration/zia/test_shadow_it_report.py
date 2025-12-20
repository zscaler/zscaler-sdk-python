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


class TestShadowITReport:
    """
    Integration Tests for the Shadow IT Report API.
    """

    @pytest.mark.vcr()
    def test_shadow_it_report_operations(self, fs):
        """Test Shadow IT Report operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_apps
            apps, response, err = client.zia.shadow_it_report.list_apps()
            assert err is None, f"List apps failed: {err}"
            assert apps is not None, "Apps list should not be None"
            assert isinstance(apps, list), "Apps should be a list"

            # Test list_apps with pagination
            apps_paginated, response, err = client.zia.shadow_it_report.list_apps(
                query_params={"page_number": 0, "limit": 10}
            )
            assert err is None, f"List apps with pagination failed: {err}"

            # Test list_custom_tags
            tags, response, err = client.zia.shadow_it_report.list_custom_tags()
            assert err is None, f"List custom tags failed: {err}"
            assert isinstance(tags, list), "Tags should be a list"

        except Exception as e:
            errors.append(f"Exception during shadow IT report test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
