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


class TestServerGroup:
    """
    Integration Tests for the Server Group
    """

    def test_server_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        connector_group_id = None
        server_group_id = None

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        
        try:
            # Create the App Connector Group
            created_connector_group, _, err = client.zpa.app_connector_groups.add_connector_group(
                name=group_name,
                description=group_description,
                enabled=True,
                latitude="37.33874",
                longitude="-121.8852525",
                location="San Jose, CA, USA",
                upgrade_day="SUNDAY",
                upgrade_time_in_secs="66600",
                override_version_profile=True,
                version_profile_name="Default",
                version_profile_id="0",
                dns_query_type="IPV4_IPV6",
                pra_enabled=True,
                tcp_quick_ack_app=True,
                tcp_quick_ack_assistant=True,
                tcp_quick_ack_read_assistant=True,
            )
            assert err is None, f"Error creating app connector group: {err}"
            assert created_connector_group is not None
            assert created_connector_group.name == group_name
            assert created_connector_group.description == group_description

            # Debugging: Check if the `enabled` field exists
            assert "enabled" in created_connector_group.__dict__, f"'enabled' field missing in response: {created_connector_group.__dict__}"
            assert created_connector_group.enabled is True, f"Expected 'enabled' to be True, got: {created_connector_group.enabled}"

            connector_group_id = created_connector_group.id  # Capture the group_id for later use
        except Exception as exc:
            errors.append(exc)

        try:
            # Create a Server Group
            created_server_group, _, err = client.zpa.server_groups.add_group(
                name=group_name,
                description=group_description,
                dynamic_discovery=True,
                app_connector_group_ids=[connector_group_id]  # Pass the connector group ID
            )
            assert err is None, f"Error creating server group: {err}"
            assert created_server_group is not None
            assert created_server_group.name == group_name
            assert created_server_group.description == group_description

            # Debugging: Check if the `enabled` field exists in the server group
            assert "enabled" in created_server_group.__dict__, f"'enabled' field missing in response: {created_server_group.__dict__}"
            assert created_server_group.enabled is True, f"Expected 'enabled' to be True, got: {created_server_group.enabled}"

            server_group_id = created_server_group.id
        except Exception as exc:
            errors.append(f"Error during server group creation: {exc}")

        try:
            if server_group_id:
                # Retrieve the specific Server Group
                retrieved_group, _, err = client.zpa.server_groups.get_group(server_group_id)
                assert err is None, f"Error fetching server group: {err}"
                assert retrieved_group.id == server_group_id
                assert retrieved_group.name == group_name

                # Update the server group
                updated_name = group_name + " Updated"
                _, _, err = client.zpa.server_groups.update_group(server_group_id, name=updated_name)
                assert err is None, f"Error updating server group: {err}"

                updated_group, _, err = client.zpa.server_groups.get_group(server_group_id)
                assert err is None, f"Error fetching updated server group: {err}"
                assert updated_group.name == updated_name

                # List server groups and ensure the updated group is in the list
                groups_list, _, err = client.zpa.server_groups.list_server_groups()
                assert err is None, f"Error listing server groups: {err}"
                assert any(group.id == server_group_id for group in groups_list)
        except Exception as exc:
            errors.append(f"Server group operation failed: {exc}")
                            
        finally:
            # Cleanup - delete the server group first, then the app connector group
            cleanup_errors = []

            if server_group_id:
                try:
                    delete_response, _, err = client.zpa.server_groups.delete_group(server_group_id)
                    assert err is None, f"Error deleting server group: {err}"
                    # Since a 204 No Content response returns None, assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    cleanup_errors.append(f"Cleanup failed for server group ID {server_group_id}: {cleanup_exc}")

            if connector_group_id:
                try:
                    client.zpa.app_connector_groups.delete_connector_group(connector_group_id)
                except Exception as exc:
                    cleanup_errors.append(f"Cleanup failed for App Connector Group: {exc}")

            errors.extend(cleanup_errors)

        assert len(errors) == 0, f"Errors occurred during the server group operations test: {errors}"
