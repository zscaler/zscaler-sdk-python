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


class TestServerGroup:
    """
    Integration Tests for the Server Group
    """

    def test_server_group(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        connector_group_id = None
        server_group_id = None

        try:
            # Prerequisite: Create an App Connector Group
            connector_group_name = "tests-" + generate_random_string()
            connector_group_description = "Integration test for connector group"
            created_connector_group = client.connectors.add_connector_group(
                name=connector_group_name,
                description=connector_group_description,
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
            connector_group_id = created_connector_group.get("id", None)
        except Exception as exc:
            errors.append(f"Creating App Connector Group failed: {exc}")

        try:
            # Create a Server Group
            server_group_name = "tests-" + generate_random_string()
            server_group_description = "Integration test for server group"
            created_server_group = client.server_groups.add_group(
                name=server_group_name,
                description=server_group_description,
                dynamic_discovery=True,
                app_connector_group_ids=[connector_group_id],  # Correctly formatted as a list
            )
            server_group_id = created_server_group.get("id", None)
        except Exception as exc:
            errors.append(f"Creating Server Group failed: {exc}")

        try:
            # Test listing server groups
            all_server_groups = client.server_groups.list_groups()
            if not any(group["id"] == server_group_id for group in all_server_groups):
                raise AssertionError("Server group not found in list")
        except Exception as exc:
            errors.append(f"Listing Server Groups failed: {exc}")

        try:
            # Test retrieving the specific Server Group
            retrieved_server_group = client.server_groups.get_group(server_group_id)
            if retrieved_server_group["id"] != server_group_id:
                raise AssertionError("Failed to retrieve the correct Server Group")
        except Exception as exc:
            errors.append(f"Retrieving Server Group failed: {exc}")

        try:
            # Update the Server Group
            updated_description = "Updated " + generate_random_string()
            updated_server_group = client.server_groups.update_group(server_group_id, description=updated_description)
            if updated_server_group["description"] != updated_description:
                raise AssertionError("Failed to update description for Server Group")
        except Exception as exc:
            errors.append(f"Updating Server Group failed: {exc}")

        # Cleanup
        if server_group_id:
            try:
                # Cleanup: Delete the Server Group
                delete_status_server_group = client.server_groups.delete_group(server_group_id)
                if delete_status_server_group != 204:
                    raise AssertionError("Failed to delete Server Group")
            except Exception as exc:
                errors.append(f"Deleting Server Group failed: {exc}")

        if connector_group_id:
            try:
                client.connectors.delete_connector_group(connector_group_id)
            except Exception as exc:
                errors.append(f"Cleanup failed for Connector Group: {exc}")

        assert len(errors) == 0, f"Errors occurred during the server group operations test: {errors}"
