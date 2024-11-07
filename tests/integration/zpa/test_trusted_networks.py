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

from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestTrustedNetworks:
    """
    Integration Tests for the Trusted Networks
    """

    def test_trusted_networks(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all trusted networks
            try:
                trusted_networks = client.trusted_networks.list_networks()
                assert isinstance(trusted_networks, list), "Expected a list of trusted networks"
            except Exception as exc:
                errors.append(f"Failed to list trusted networks: {exc}")

            if trusted_networks:  # Proceed only if there are any trusted networks
                try:
                    # Select the first trusted network for further testing
                    first_network = trusted_networks[0]
                    network_id = first_network.get("id")

                    # Fetch the selected trusted network by its ID
                    fetched_network = client.trusted_networks.get_network(network_id)
                    assert fetched_network is not None, "Expected a valid trusted network object"
                    assert fetched_network.get("id") == network_id, "Mismatch in trusted network ID"
                except Exception as exc:
                    errors.append(f"Failed to fetch network by ID: {exc}")

                try:
                    # Attempt to retrieve the trusted network by name
                    network_name = first_network.get("name")
                    network_by_name = client.trusted_networks.get_network_by_name(network_name)
                    assert network_by_name is not None, "Expected a valid trusted network object when searching by name"
                    assert network_by_name.get("id") == network_id, "Mismatch in trusted network ID when searching by name"
                except Exception as exc:
                    errors.append(f"Failed to fetch network by name: {exc}")

                try:
                    # Test get_network_udid using the network_id of the first network
                    network_udid = first_network.get("network_id")
                    network_by_udid = client.trusted_networks.get_network_udid(network_udid)
                    assert network_by_udid is not None, "Expected a valid trusted network object when searching by network_id"
                    assert (
                        network_by_udid.get("network_id") == network_udid
                    ), "Mismatch in trusted network network_id when searching by network_id"
                except Exception as exc:
                    errors.append(f"Failed to fetch network by network_id: {exc}")

        # Catch any unexpected errors that might not have been caught by inner try-except blocks
        except Exception as exc:
            errors.append(f"Unexpected error during trusted networks test: {exc}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during trusted network operations test: {'; '.join(errors)}"
