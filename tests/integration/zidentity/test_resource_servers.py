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

from tests.integration.zidentity.conftest import MockZIdentityClient


@pytest.fixture
def fs():
    yield


class TestResourceServers:
    """
    Integration Tests for the Resource Servers.
    """

    def test_resource_servers(self, fs):
        client = MockZIdentityClient(fs)
        errors = []  # Initialize an empty list to collect errors
        resource_id = None

        # List all resource servers
        try:
            resource_response, _, err = client.zidentity.resource_servers.list_resource_servers()  # Correctly unpack the tuple
            assert err is None, f"Error listing resource servers: {err}"
            assert isinstance(resource_response, list), "Expected a list of resource servers"
            if resource_response:  # If there are any resource servers, proceed with further operations
                first_resource = resource_response[0]
                resource_id = first_resource.id  # Access the 'id' attribute using dot notation
                assert resource_id is not None, "Resource Server ID should not be None"
        except Exception as exc:
            errors.append(f"Listing resource servers failed: {str(exc)}")

        if resource_id:
            # Fetch the selected Resource Server by its ID
            try:
                fetched_resource, _, err = client.zidentity.resource_servers.get_resource_server(resource_id)
                assert err is None, f"Error fetching Resource Server by ID: {err}"
                assert fetched_resource is not None, "Expected a valid Resource Server object"
                assert fetched_resource.id == resource_id, "Mismatch in Resource Server ID"  # Use dot notation for object access
            except Exception as exc:
                errors.append(f"Fetching Resource Server by ID failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during Resource Server operations test: {errors}"
