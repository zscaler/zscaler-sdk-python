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


class TestTrafficVPNCredentials:
    """
    Integration Tests for the Traffic VPN Credentials API.
    """

    @pytest.mark.vcr()
    def test_traffic_vpn_credentials_crud(self, fs):
        """Test Traffic VPN Credentials operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_vpn_credentials
            credentials, response, err = client.zia.traffic_vpn_credentials.list_vpn_credentials()
            assert err is None, f"List VPN credentials failed: {err}"
            assert credentials is not None, "Credentials list should not be None"
            assert isinstance(credentials, list), "Credentials should be a list"

            # Test list_vpn_credentials with type filter
            ufqdn_credentials, response, err = client.zia.traffic_vpn_credentials.list_vpn_credentials(
                query_params={"type": "UFQDN"}
            )
            assert err is None, f"List UFQDN credentials failed: {err}"

            # Test list_vpn_credentials with pagination
            paginated_credentials, response, err = client.zia.traffic_vpn_credentials.list_vpn_credentials(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"List credentials with pagination failed: {err}"

            # Test get_vpn_credential with existing credential if available
            if credentials and len(credentials) > 0:
                credential_id = credentials[0].id
                fetched_credential, response, err = client.zia.traffic_vpn_credentials.get_vpn_credential(
                    credential_id=credential_id
                )
                assert err is None, f"Get VPN credential failed: {err}"
                assert fetched_credential is not None, "Fetched credential should not be None"

        except Exception as e:
            errors.append(f"Exception during traffic VPN credentials test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
