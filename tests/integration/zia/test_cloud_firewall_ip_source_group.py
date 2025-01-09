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
    Integration Tests for the Cloud Firewall IP Source Group with enhanced debugging.
    """

    def test_add_ip_source_group(self, fs):
        client = MockZIAClient(fs)
        errors = []
        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_id = None

        try:
            # Create the IP source group
            try:
                created_group, _, error = client.zia.cloud_firewall_rules.add_ip_source_group(
                    name=group_name,
                    description=group_description,
                    ip_addresses=["192.168.1.1", "192.168.1.2", "192.168.1.3"]
                )
                print(f"Created Group: {created_group.as_dict() if created_group else 'Not Found'}, Error: {error}")
                assert error is None, f"Error creating group: {error}"
                assert created_group is not None, "Group creation returned None"
                assert created_group.name == group_name, "Group name mismatch"
                assert created_group.description == group_description, "Group description mismatch"
                group_id = created_group.id
            except Exception as exc:
                errors.append(f"Failed to add group: {exc}")

            # Update the IP source group
            if group_id:
                try:
                    updated_name = group_name + " Updated"

                    # Fetch Before Update
                    time.sleep(5)
                    fetched_group, _, fetch_error = client.zia.cloud_firewall_rules.get_ip_source_group(group_id)
                    print(f"Group Before Update: {fetched_group.as_dict() if fetched_group else 'Not Found'}, Error: {fetch_error}")

                    # Update the group
                    time.sleep(5)
                    updated_group, zscaler_resp, error = client.zia.cloud_firewall_rules.update_ip_source_group(
                        group_id, name=updated_name
                    )
                    print(f"Updated Group: {updated_group.as_dict() if updated_group else 'Not Found'}, Response: {zscaler_resp}, Error: {error}")

                    assert error is None, f"Error updating group: {error}"
                    assert updated_group is not None, "Updated group response is None"
                    assert updated_group.name == updated_name, f"Failed to update group name: {updated_group.as_dict()}"

                    # Verify using a GET request
                    time.sleep(5)
                    fetched_group, _, fetch_error = client.zia.cloud_firewall_rules.get_ip_source_group(group_id)
                    print(f"Fetched Group After Update: {fetched_group.as_dict() if fetched_group else 'Not Found'}, Error: {fetch_error}")

                    assert fetch_error is None, f"Error retrieving updated group: {fetch_error}"
                    assert fetched_group.name == updated_name, f"Failed to update group name: {fetched_group.as_dict()}"

                except Exception as exc:
                    errors.append(f"Failed to update group: {exc}")

        finally:
            # Cleanup: Attempt to delete the IP source group
            if group_id:
                try:
                    time.sleep(5)
                    delete_response_code = client.zia.cloud_firewall_rules.delete_ip_source_group(group_id)
                    print(f"Delete Response Code: {delete_response_code}")
                    assert delete_response_code == 204, f"Failed to delete IP source group: {delete_response_code}"
                    print(f"Group deleted successfully with ID: {group_id}")
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the IP source group lifecycle test: {errors}"
