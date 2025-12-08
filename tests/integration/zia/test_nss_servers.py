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

from tests.integration.zia.conftest import MockZIAClient, NameGenerator


@pytest.fixture
def fs():
    yield


class TestNSSServers:
    """
    Integration Tests for the NSS Servers
    """

    @pytest.mark.vcr()
    def test_nss_servers(self, fs):
        client = MockZIAClient(fs)
        errors = []
        nss_id = None
        update_server = None
        
        # Use deterministic names for VCR
        names = NameGenerator("nss-server")

        try:
            try:
                create_server = client.zia.nss_servers.add_nss_server(
                    name=names.name,
                    status="ENABLED",
                    type="NSS_FOR_FIREWALL",
                )
                assert create_server is not None, "NSS Server creation failed."
                nss_id = create_server.id
            except Exception as e:
                errors.append(f"Exception during add_nss_server: {str(e)}")

            try:
                if nss_id:
                    update_server = client.zia.nss_servers.update_nss_server(
                        nss_id=nss_id,
                        name=names.updated_name,
                        status="DISABLED",
                        type="NSS_FOR_FIREWALL",
                    )
                    assert update_server is not None, "NSS Server update returned None."
            except Exception as e:
                errors.append(f"Exception during update_server: {str(e)}")

            try:
                if update_server:
                    nss = client.zia.nss_servers.get_nss_server(update_server.id)
                    assert nss.id == nss_id, "Retrieved NSS Server ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_nss_server: {str(e)}")

            try:
                if update_server:
                    servers = client.zia.nss_servers.list_nss_servers(query_params={"search": update_server.name})
                    assert servers is not None and isinstance(servers, list), "No NSS Servers found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_nss_servers: {str(e)}")

        finally:
            try:
                if update_server:
                    _ = client.zia.nss_servers.delete_nss_server(update_server.id)
            except Exception as e:
                errors.append(f"Exception during delete_nss_server: {str(e)}")

        # Final Assertion
        if errors:
            pytest.fail(f"Test failed with errors: {errors}")
