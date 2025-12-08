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


class TestCloudFirewallNetworkAppGroup:
    """
    Integration Tests for the Cloud Firewall Network Application Group.
    """

    @pytest.mark.vcr()
    def test_cloud_firewall_network_app_group(self, fs):
        client = MockZIAClient(fs)
        errors = []

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_id = None

        try:
            created_group = client.zia.cloud_firewall.add_network_app_group(
                name=group_name,
                description=group_description,
                network_applications=["APNS", "APPSTORE", "DICT"],
            )
            assert created_group is not None, "Failed to create network application group group"
            group_id = created_group.id
            assert created_group.name == group_name, "Group name mismatch in creation"
            assert created_group.description == group_description, "Group description mismatch in creation"
        except Exception as exc:
            errors.append(f"Failed to add network application group group: {exc}")

            # Attempt to retrieve the created network application group by ID
            if group_id:
                try:
                    group = client.zia.cloud_firewall.get_network_app_group(group_id)
                    assert group is not None, "Retrieved network application group group is None"
                    assert group.id == group_id, "Incorrect network application group group retrieved"
                except Exception as exc:
                    errors.append(f"Failed to retrieve network application group group: {exc}")

            # Attempt to update the network application group
            if group_id:
                try:
                    updated_name = "updated-" + generate_random_string()
                    updated_group = client.zia.cloud_firewall.update_network_app_group(
                        group_id=group_id, name=updated_name
                    )
                    assert updated_group.name == updated_name, "Group name mismatch after update"
                except Exception as exc:
                    errors.append(f"Failed to update network application group group: {exc}")

            # Attempt to list network application groups and check if the updated group is in the list
            try:
                groups = client.zia.cloud_firewall.list_network_app_groups()
                assert groups is not None, "network application group group list is None"
                assert any(g.id == group_id for g in groups), "Updated network application group group not found in list"
            except Exception as exc:
                errors.append(f"Failed to list network application group groups: {exc}")

        finally:
            try:
                if group_id:
                    _ = client.zia.cloud_firewall.delete_network_app_group(group_id)
            except Exception as exc:
                errors.append(f"Deleting network application group failed: {exc}")

        # Final assertion
        if errors:
            pytest.fail(f"Test failed with errors: {errors}")
