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

from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestCloudFirewallIPDestinationGroup:
    """
    Integration Tests for the Cloud Firewall IP Destination Group.
    """

    def test_cloud_firewall_ip_destination_group(self, fs):
        client = MockZIAClient(fs)
        errors = []

        group_id = None
        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_addresses = ["1.1.1.1", "8.8.8.8"]
        group_type = "DSTN_IP"

        try:
            # Step 1: Create IP destination group
            try:
                created_group, _, error = client.zia.cloud_firewall.add_ip_destination_group(
                    name=group_name,
                    description=group_description,
                    addresses=group_addresses,
                    type=group_type,
                )
                assert error is None, f"Error adding IP destination group: {error}"
                assert created_group is not None, "Failed to create IP destination group"
                group_id = created_group.id
                assert created_group.name == group_name, "Group name mismatch in creation"
                assert created_group.description == group_description, "Group description mismatch in creation"
            except Exception as exc:
                errors.append(f"Failed to add IP destination group: {exc}")

            # Step 2: Retrieve the created group by ID
            try:
                if group_id:
                    group, _, error = client.zia.cloud_firewall.get_ip_destination_group(group_id)
                    assert error is None, f"Error retrieving IP destination group: {error}"
                    assert group is not None, "Retrieved IP destination group is None"
                    assert group.id == group_id, "Incorrect IP destination group retrieved"
            except Exception as exc:
                errors.append(f"Failed to retrieve IP destination group: {exc}")

            # Step 3: Update the IP destination group
            try:
                if group_id:
                    updated_name = "updated-" + generate_random_string()
                    updated_description = "updated-" + generate_random_string()
                    updated_group, _, error = client.zia.cloud_firewall.update_ip_destination_group(
                        group_id=group_id,
                        name=updated_name,
                        description=updated_description,
                        addresses=group_addresses,
                        type=group_type,
                    )
                    assert error is None, f"Error updating IP destination group: {error}"
                    assert updated_group.name == updated_name, "Group name mismatch after update"
                    assert updated_group.description == updated_description, "Group description mismatch after update"
            except Exception as exc:
                errors.append(f"Failed to update IP destination group: {exc}")

            # Step 4: List IP destination groups and verify
            try:
                groups, _, error = client.zia.cloud_firewall.list_ip_destination_groups()
                assert error is None, f"Error listing IP destination groups: {error}"
                assert groups is not None, "IP destination group list is None"
                assert any(g.id == group_id for g in groups), "Updated IP destination group not found in list"
            except Exception as exc:
                errors.append(f"Failed to list IP destination groups: {exc}")

        finally:
            # Step 5: Cleanup
            try:
                if group_id:
                    _, _, error = client.zia.cloud_firewall.delete_ip_destination_group(group_id)
                    assert error is None, f"Error deleting IP destination group: {error}"
            except Exception as exc:
                errors.append(f"Deleting IP destination group failed: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
