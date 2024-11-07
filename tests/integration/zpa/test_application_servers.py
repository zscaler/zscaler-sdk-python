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
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestSegmentGroup:
    """
    Integration Tests for the Application Server
    """

    def test_application_server(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        server_name = "tests-" + generate_random_string()
        server_description = "tests-" + generate_random_string()
        server_address = "192.168.200.1"

        try:
            # Create a new application server
            created_server = client.servers.add_server(
                name=server_name,
                description=server_description,
                enabled=True,
                address=server_address,
            )
            assert created_server is not None
            assert created_server.name == server_name
            assert created_server.description == server_description
            assert created_server.address == server_address
            assert created_server.enabled is True

            server_id = created_server.id
        except Exception as exc:
            errors.append(exc)

        try:
            # Retrieve the created segment group by ID
            retrieved_server = client.servers.get_server(server_id)
            assert retrieved_server.id == server_id
            assert retrieved_server.name == server_name
        except Exception as exc:
            errors.append(exc)

        try:
            # Update the segment group
            updated_name = server_name + " Updated"
            client.servers.update_server(server_id, name=updated_name)

            updated_group = client.servers.get_server(server_id)
            assert updated_group.name == updated_name
        except Exception as exc:
            errors.append(exc)

        try:
            # List segment groups and ensure the updated group is in the list
            groups_list = client.servers.list_servers()
            assert any(group.id == server_id for group in groups_list)
        except Exception as exc:
            errors.append(exc)

        try:
            # Search for the segment group by name
            search_result = client.servers.get_server_by_name(updated_name)
            assert search_result is not None
            assert search_result.id == server_id
        except Exception as exc:
            errors.append(exc)

        try:
            # Delete the segment group
            delete_response_code = client.servers.delete_server(server_id)
            assert str(delete_response_code) == "204"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the application server lifecycle test: {errors}"
