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
import time


@pytest.fixture
def fs():
    yield


class TestCloudFirewallIPSourceGroup:
    """
    Integration Tests for the Cloud Firewall IP Source Group.
    """

    def test_add_ip_source_group(self, fs):
        client = MockZIAClient(fs)
        errors = []
        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_addresses = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
        group_id = None

        try:
            # Step 1: Create the IP source group
            try:
                created_group, _, error = client.zia.cloud_firewall.add_ip_source_group(
                    name=group_name,
                    description=group_description,
                    ip_addresses=group_addresses,
                )
                print(f"Created Group: {created_group.as_dict() if created_group else 'Not Found'}, Error: {error}")
                assert error is None, f"Error creating group: {error}"
                assert created_group is not None, "Group creation returned None"
                assert created_group.name == group_name, "Group name mismatch"
                assert created_group.description == group_description, "Group description mismatch"
                group_id = created_group.id
            except Exception as exc:
                errors.append(f"Failed to add group: {exc}")

            # Step 2: Update the IP source group
            try:
                if group_id:
                    updated_name = group_name + " Updated"
                    updated_description = group_description + " Updated"

                    # Optional: Fetch before update
                    time.sleep(3)
                    fetched_before, _, fetch_error = client.zia.cloud_firewall.get_ip_source_group(group_id)
                    print(
                        f"Group Before Update: {fetched_before.as_dict() if fetched_before else 'Not Found'}, Error: {fetch_error}"
                    )

                    # Update
                    time.sleep(3)
                    updated_group, _, error = client.zia.cloud_firewall.update_ip_source_group(
                        group_id=group_id,
                        name=updated_name,
                        description=updated_description,
                        ip_addresses=group_addresses,
                    )
                    print(f"Updated Group: {updated_group.as_dict() if updated_group else 'Not Found'}, Error: {error}")
                    assert error is None, f"Error updating group: {error}"
                    assert updated_group is not None, "Updated group response is None"
                    assert updated_group.name == updated_name, "Group name mismatch after update"
                    assert updated_group.description == updated_description, "Group description mismatch after update"

                    # Fetch after update to confirm
                    time.sleep(3)
                    fetched_after, _, fetch_error = client.zia.cloud_firewall.get_ip_source_group(group_id)
                    print(
                        f"Fetched Group After Update: {fetched_after.as_dict() if fetched_after else 'Not Found'}, Error: {fetch_error}"
                    )
                    assert fetch_error is None, f"Error retrieving updated group: {fetch_error}"
                    assert fetched_after.name == updated_name, "Group name not updated correctly"
                    assert fetched_after.description == updated_description, "Group description not updated correctly"
            except Exception as exc:
                errors.append(f"Failed to update group: {exc}")

        finally:
            # Step 3: Cleanup
            try:
                if group_id:
                    time.sleep(3)
                    _, _, error = client.zia.cloud_firewall.delete_ip_source_group(group_id)
                    assert error is None, f"Failed to delete IP source group: {error}"
                    print(f"Group deleted successfully with ID: {group_id}")
            except Exception as exc:
                errors.append(f"Cleanup failed: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
