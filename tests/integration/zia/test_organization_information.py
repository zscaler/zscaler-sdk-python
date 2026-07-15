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


class TestOrganizationInformation:
    """
    Integration Tests for the Organization Information API.
    """

    @pytest.mark.vcr()
    def test_organization_information_operations(self, fs):
        """Test Organization Information operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test get_organization_information
            org_info, response, err = client.zia.organization_information.get_organization_information()
            assert err is None, f"Get organization information failed: {err}"
            assert org_info is not None, "Organization information should not be None"

            # Test get_org_info_lite
            org_info_lite, response, err = client.zia.organization_information.get_org_info_lite()
            assert err is None, f"Get organization info lite failed: {err}"
            assert org_info_lite is not None, "Organization info lite should not be None"

            # Test get_subscriptions
            subscriptions, response, err = client.zia.organization_information.get_subscriptions()
            assert err is None, f"Get subscriptions failed: {err}"
            assert subscriptions is not None, "Subscriptions should not be None"

        except Exception as e:
            errors.append(f"Exception during organization information test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
