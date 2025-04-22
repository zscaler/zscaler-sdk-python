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
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestApplicationServer:
    """
    Integration Tests for the Application Server
    """

    def test_application_server(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        server_name = "tests-" + generate_random_string()
        server_description = "tests-" + generate_random_string()
        server_address = "192.168.200.1"
        server_id = None

        try:
            # Create a new application server
            created_server, _, err = client.zpa.servers.add_server(
                name=server_name,
                description=server_description,
                enabled=True,
                address=server_address,
            )
            assert err is None, f"Error creating application server: {err}"
            assert created_server is not None
            assert created_server.name == server_name
            assert created_server.description == server_description
            assert created_server.address == server_address
            assert created_server.enabled is True

            server_id = created_server.id
        except Exception as exc:
            errors.append(f"Error during application server creation: {exc}")

        try:
            if server_id:
                # Retrieve the created Application Server by ID
                retrieved_server, _, err = client.zpa.servers.get_server(server_id)
                assert err is None, f"Error fetching server: {err}"
                assert retrieved_server.id == server_id
                assert retrieved_server.name == server_name

                # Update the Application Server
                updated_name = server_name + " Updated"
                _, _, err = client.zpa.servers.update_server(server_id, name=updated_name)
                assert err is None, f"Error updating server: {err}"

                updated_server, _, err = client.zpa.servers.get_server(server_id)
                assert err is None, f"Error fetching updated server: {err}"
                assert updated_server.name == updated_name

                # List segment servers and ensure the updated server is in the list
                servers_list, _, err = client.zpa.servers.list_servers()
                assert err is None, f"Error listing servers: {err}"
                assert any(server.id == server_id for server in servers_list)
        except Exception as exc:
            errors.append(f"Application Server operation failed: {exc}")

        finally:
            # Cleanup: Delete the Application Server if it was created
            if server_id:
                try:
                    delete_response, _, err = client.zpa.servers.delete_server(server_id)
                    assert err is None, f"Error deleting server: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Application Server ID {server_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the Application Server lifecycle test: {errors}"
