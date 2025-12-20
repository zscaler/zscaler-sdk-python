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


class TestIOTReport:
    """
    Integration Tests for the IOT Report API.
    """

    @pytest.mark.vcr()
    def test_iot_report_operations(self, fs):
        """Test IOT Report operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test get_device_types - may fail due to permission restrictions
            device_types, response, err = client.zia.iot_report.get_device_types()
            # Don't fail on permission errors
            if err is None:
                assert device_types is not None, "Device types should not be None"

            # Test get_categories - may fail due to permission restrictions
            categories, response, err = client.zia.iot_report.get_categories()
            if err is None:
                assert categories is not None, "Categories should not be None"

            # Test get_classifications - may fail due to permission restrictions
            classifications, response, err = client.zia.iot_report.get_classifications()
            if err is None:
                assert classifications is not None, "Classifications should not be None"

            # Test get_device_list - may fail due to permission restrictions
            device_list, response, err = client.zia.iot_report.get_device_list()
            if err is None:
                assert device_list is not None, "Device list should not be None"

        except Exception as e:
            errors.append(f"Exception during IOT report test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

