"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

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
        network_id = None

        # List all trusted networks
        try:
            network_response, _, err = client.zpa.trusted_networks.list_trusted_networks()
            assert err is None, f"Error listing trusted networks: {err}"
            assert isinstance(network_response, list), "Expected a list of trusted networks"
            if network_response:
                first_network = network_response[0]
                network_id = first_network.id
                assert network_id is not None, "Trusted network ID should not be None"
        except Exception as exc:
            errors.append(f"Listing trusted networks failed: {str(exc)}")

        if network_id:
            # Fetch the selected trusted network by its ID
            try:
                fetched_group, _, err = client.zpa.trusted_networks.get_network(network_id)
                assert err is None, f"Error fetching trusted network by ID: {err}"
                assert fetched_group is not None, "Expected a valid trusted network object"
                assert fetched_group.id == network_id, "Mismatch in trusted network ID"
            except Exception as exc:
                errors.append(f"Fetching trusted network by ID failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during trusted network operations test: {errors}"
