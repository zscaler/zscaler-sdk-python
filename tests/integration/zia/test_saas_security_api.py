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


class TestSaaSSecurityAPI:
    """
    Integration Tests for the SaaS Security API.
    """

    @pytest.mark.vcr()
    def test_saas_security_api_operations(self, fs):
        """Test SaaS Security API operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_domain_profiles_lite
            profiles, response, err = client.zia.saas_security_api.list_domain_profiles_lite()
            assert err is None, f"List domain profiles lite failed: {err}"
            assert profiles is not None, "Profiles should not be None"
            assert isinstance(profiles, list), "Profiles should be a list"

            # Test list_quarantine_tombstone_lite
            tombstones, response, err = client.zia.saas_security_api.list_quarantine_tombstone_lite()
            assert err is None, f"List quarantine tombstone lite failed: {err}"
            assert tombstones is not None, "Tombstones should not be None"
            assert isinstance(tombstones, list), "Tombstones should be a list"

            # Test list_casb_email_label_lite
            labels, response, err = client.zia.saas_security_api.list_casb_email_label_lite()
            assert err is None, f"List CASB email label lite failed: {err}"
            assert labels is not None, "Labels should not be None"
            assert isinstance(labels, list), "Labels should be a list"

            # Test list_casb_tenant_lite
            tenants, response, err = client.zia.saas_security_api.list_casb_tenant_lite()
            assert err is None, f"List CASB tenant lite failed: {err}"
            assert tenants is not None, "Tenants should not be None"
            assert isinstance(tenants, list), "Tenants should be a list"

            # Test list_saas_scan_info
            scan_info, response, err = client.zia.saas_security_api.list_saas_scan_info()
            assert err is None, f"List SaaS scan info failed: {err}"
            assert scan_info is not None, "Scan info should not be None"

        except Exception as e:
            errors.append(f"Exception during SaaS security API test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

