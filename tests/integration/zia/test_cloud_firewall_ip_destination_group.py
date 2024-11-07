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
        errors = []  # Initialize an empty list to collect errors

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_id = None

        try:
            # Attempt to create an IP destination group
            try:
                created_group = client.firewall.add_ip_destination_group(
                    name=group_name,
                    type="DSTN_IP",
                    addresses=["1.1.1.1", "8.8.8.8"],
                    description=group_description,
                )
                assert created_group.name == group_name, "Group name mismatch in creation"
                assert created_group.description == group_description, "Group description mismatch in creation"
                group_id = created_group.id
            except Exception as exc:
                errors.append(f"Failed to add IP destination group: {exc}")

            # Attempt to retrieve the created IP destination group by ID
            if group_id:
                try:
                    group = client.firewall.get_ip_destination_group(group_id)
                    assert group.id == group_id, "Failed to retrieve the correct IP destination group"
                except Exception as exc:
                    errors.append(f"Failed to retrieve IP destination group: {exc}")

            # Attempt to update the IP destination group
            if group_id:
                try:
                    updated_name = "updated-" + generate_random_string()
                    client.firewall.update_ip_destination_group(group_id=group_id, name=updated_name)
                    updated_group = client.firewall.get_ip_destination_group(group_id)
                    assert updated_group.name == updated_name, "Group name mismatch after update"
                except Exception as exc:
                    errors.append(f"Failed to update IP destination group: {exc}")

            # Attempt to list IP destination groups and check if the updated group is in the list
            try:
                groups = client.firewall.list_ip_destination_groups()
                assert any(group.id == group_id for group in groups), "Updated IP destination group not found in list"
            except Exception as exc:
                errors.append(f"Failed to list IP destination groups: {exc}")

        finally:
            # Cleanup: Attempt to delete the IP destination group
            if group_id:
                try:
                    status_code = client.firewall.delete_ip_destination_group(group_id)
                    assert status_code == 204, "Failed to delete IP destination group"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the IP destination group lifecycle test: {errors}"
