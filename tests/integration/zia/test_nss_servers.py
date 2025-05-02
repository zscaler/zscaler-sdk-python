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
import random


@pytest.fixture
def fs():
    yield


class TestNSSServers:
    """
    Integration Tests for the NSS Servers
    """

    def test_nss_servers(self, fs):
        client = MockZIAClient(fs)
        errors = []
        nss_id = None
        update_server = None

        try:
            try:
                create_server, _, error = client.zia.nss_servers.add_nss_server(
                    name=f"TestNSSServer_{random.randint(1000, 10000)}",
                    status='ENABLED',
                    type='NSS_FOR_FIREWALL',
                )
                assert error is None, f"Add NSS Server Error: {error}"
                assert create_server is not None, "NSS Server creation failed."
                nss_id = create_server.id
            except Exception as e:
                errors.append(f"Exception during add_nss_server: {str(e)}")

            try:
                if nss_id:
                    update_server, _, error = client.zia.nss_servers.update_nss_server(
                        nss_id=nss_id,
                        name=f"TestNSSServer_{random.randint(1000, 10000)}",
                        status='DISABLED',
                        type='NSS_FOR_FIREWALL',
                    )
                    assert error is None, f"Update NSS Server Error: {error}"
                    assert update_server is not None, "NSS Server update returned None."
            except Exception as e:
                errors.append(f"Exception during update_server: {str(e)}")

            try:
                if update_server:
                    nss, _, error = client.zia.nss_servers.get_nss_server(update_server.id)
                    assert error is None, f"Get NSS Server Error: {error}"
                    assert nss.id == nss_id, "Retrieved NSS Server ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_nss_server: {str(e)}")

            try:
                if update_server:
                    servers, _, error = client.zia.nss_servers.list_nss_servers(query_params={"search": update_server.name})
                    assert error is None, f"List NSS Servers Error: {error}"
                    assert servers is not None and isinstance(servers, list), "No NSS Servers found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_nss_servers: {str(e)}")

        finally:
            try:
                if update_server:
                    _, _, error = client.zia.nss_servers.delete_nss_server(update_server.id)
                    assert error is None, f"Delete NSS Servers Error: {error}"
            except Exception as e:
                errors.append(f"Exception during delete_nss_server: {str(e)}")

        # Final Assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
