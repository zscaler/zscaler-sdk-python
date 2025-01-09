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
        errors = []  # Collect errors throughout the test lifecycle

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_id = None

        try:
            # Create an IP destination group
            try:
                created_group, _, error = client.zia.cloud_firewall_rules.add_ip_destination_group(
                    name=group_name,
                    type="DSTN_IP",
                    addresses=["1.1.1.1", "8.8.8.8"],
                    description=group_description,
                )
                assert error is None, f"Error adding IP destination group: {error}"
                assert created_group is not None, "Failed to create IP destination group"
                group_id = created_group.id
                assert created_group.name == group_name, "Group name mismatch in creation"
                assert created_group.description == group_description, "Group description mismatch in creation"
            except Exception as exc:
                errors.append(f"Failed to add IP destination group: {exc}")

            # Retrieve the created group by ID
            if group_id:
                try:
                    group, _, error = client.zia.cloud_firewall_rules.get_ip_destination_group(group_id)
                    assert error is None, f"Error retrieving IP destination group: {error}"
                    assert group is not None, "Retrieved IP destination group is None"
                    assert group.id == group_id, "Incorrect IP destination group retrieved"
                except Exception as exc:
                    errors.append(f"Failed to retrieve IP destination group: {exc}")

            # Attempt to retrieve the created IP destination group by ID
            if group_id:
                try:
                    group, _, error = client.zia.cloud_firewall_rules.get_ip_destination_group(group_id)
                    assert error is None, f"Error retrieving  IP destination group: {error}"
                    assert group is not None, "Retrieved IP destination group is None"
                    assert group.id == group_id, "Failed to retrieve the correct IP destination group"
                except Exception as exc:
                    errors.append(f"Failed to retrieve IP destination group: {exc}")

            # Update the IP destination group
            if group_id:
                try:
                    updated_name = "updated-" + generate_random_string()
                    updated_group, _, error = client.zia.cloud_firewall_rules.update_ip_destination_group(
                        group_id=group_id, name=updated_name
                    )
                    assert error is None, f"Error updating IP destination group: {error}"
                    assert updated_group.name == updated_name, "Group name mismatch after update"
                except Exception as exc:
                    errors.append(f"Failed to update IP destination group: {exc}")

            # List IP destination groups and check if the updated group is present
            # try:
            #     groups, _, error = client.zia.cloud_firewall_rules.list_ip_destination_groups()
            #     assert error is None, f"Error listing IP destination groups: {error}"
            #     assert groups is not None, "IP destination group list is None"
            #     assert any(g.id == group_id for g in groups), "Updated IP destination group not found in list"
            # except Exception as exc:
            #     errors.append(f"Failed to list IP destination groups: {exc}")

        # Updated Test Cleanup
        finally:
            cleanup_errors = []
            try:
                if group_id:
                    _, error = client.zia.cloud_firewall_rules.delete_ip_destination_group(group_id)
                    assert error is None, f"Error deleting IP destination group: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting IP destination group failed: {exc}")

            errors.extend(cleanup_errors)

        # Final Error Check
        assert len(errors) == 0, f"Errors occurred during the IP destination group lifecycle test: {errors}"

