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
from tests.integration.zcc.conftest import MockZCCClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestTrustedNetworks:
    """
    Integration Tests for the ZCC Trusted Networks API
    """

    @pytest.mark.vcr()
    def test_list_trusted_networks(self, fs):
        """Test listing trusted networks by company"""
        client = MockZCCClient(fs)
        errors = []

        try:
            networks, response, err = client.zcc.trusted_networks.list_by_company()
            assert err is None, f"Error listing trusted networks: {err}"
            assert isinstance(networks, list), "Expected a list of trusted networks"
            
            # Verify response structure if we have networks
            if networks:
                network = networks[0]
                assert hasattr(network, 'as_dict'), "Trusted network should have as_dict method"
        except Exception as exc:
            errors.append(f"Listing trusted networks failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the trusted networks test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_trusted_networks_with_pagination(self, fs):
        """Test listing trusted networks with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            networks, response, err = client.zcc.trusted_networks.list_by_company(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error listing trusted networks with pagination: {err}"
            assert isinstance(networks, list), "Expected a list of trusted networks"
        except Exception as exc:
            errors.append(f"Listing trusted networks with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated trusted networks test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_trusted_networks_with_search(self, fs):
        """Test listing trusted networks with search filter"""
        client = MockZCCClient(fs)
        errors = []

        try:
            networks, response, err = client.zcc.trusted_networks.list_by_company(
                query_params={"search": "test"}
            )
            assert err is None, f"Error listing trusted networks with search: {err}"
            assert isinstance(networks, list), "Expected a list of trusted networks"
        except Exception as exc:
            errors.append(f"Listing trusted networks with search failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the search trusted networks test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_trusted_network_crud_operations(self, fs):
        """Test CRUD operations for trusted networks"""
        client = MockZCCClient(fs)
        errors = []
        created_network_id = None

        try:
            # Create a trusted network
            network_name = f"tests-trusted-network-{generate_random_string(5)}"
            created_network, response, err = client.zcc.trusted_networks.add_trusted_network(
                active=True,
                network_name=network_name,
                dns_servers="10.10.10.10, 10.10.10.11",
                dns_search_domains="test.example.com",
            )
            
            if err is None and created_network:
                assert hasattr(created_network, 'as_dict'), "Created network should have as_dict method"
                created_network_id = created_network.id if hasattr(created_network, 'id') else None
                
                # Update the trusted network
                if created_network_id:
                    updated_network, response, err = client.zcc.trusted_networks.update_trusted_network(
                        id=created_network_id,
                        active=True,
                        network_name=f"{network_name}-updated",
                        dns_servers="10.10.10.10",
                        dns_search_domains="updated.example.com",
                    )
                    
                    if err is None and updated_network:
                        assert hasattr(updated_network, 'as_dict'), "Updated network should have as_dict method"
        except Exception as exc:
            errors.append(f"Trusted network CRUD operations failed: {exc}")
        finally:
            # Cleanup: Delete the created network
            if created_network_id:
                try:
                    _, _, del_err = client.zcc.trusted_networks.delete_trusted_network(created_network_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred during the trusted networks CRUD test:\n{chr(10).join(errors)}"

