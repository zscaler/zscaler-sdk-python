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


class TestCloudFirewallNetworkServicesGroup:
    """
    Integration Tests for the Cloud Firewall Network Services Group.
    """

    def test_cloud_firewall_network_services_group(self, fs):
        client = MockZIAClient(fs)
        errors = []

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_id = None
        service_ids = []

        # Search for the required network services and extract their IDs
        try:
            for service_name in ["ICMP_ANY", "UDP_ANY", "TCP_ANY", "DNS"]:
                services, _, error = client.zia.cloud_firewall_rules.list_network_services(
                    query_params={"search": service_name}
                )
                assert error is None, f"Error searching for network service '{service_name}': {error}"
                assert services, f"No services found for '{service_name}'"

                # Extract the correct service by matching the name
                service = next((svc for svc in services if svc.name == service_name), None)
                assert service is not None, f"Service '{service_name}' not found in list"
                service_ids.append(service.id)
        except Exception as exc:
            errors.append(f"Failed to retrieve network service IDs: {exc}")

        try:
            # Add the network service group
            created_group, _, error = client.zia.cloud_firewall_rules.add_network_svc_group(
                name=group_name,
                description=group_description,
                service_ids=service_ids,
            )
            assert error is None, f"Error adding network service group: {error}"
            assert created_group is not None, "Failed to create network service group"
            group_id = created_group.id
            assert created_group.name == group_name, "Group name mismatch in creation"
            assert created_group.description == group_description, "Group description mismatch in creation"
        except Exception as exc:
            errors.append(f"Failed to add network service group: {exc}")

        # Retrieve the created network services group by ID
        if group_id:
            try:
                group, _, error = client.zia.cloud_firewall_rules.get_network_svc_group(group_id)
                assert error is None, f"Error retrieving network service group: {error}"
                assert group is not None, "Retrieved network service group is None"
                assert group.id == group_id, "Incorrect network service group retrieved"
            except Exception as exc:
                errors.append(f"Failed to retrieve network service group: {exc}")

        # Update the network services group
        if group_id:
            try:
                updated_name = "updated-" + generate_random_string()
                updated_group, _, error = client.zia.cloud_firewall_rules.update_network_svc_group(
                    group_id=group_id, name=updated_name
                )
                assert error is None, f"Error updating network service group: {error}"
                assert updated_group.name == updated_name, "Group name mismatch after update"
            except Exception as exc:
                errors.append(f"Failed to update network service group: {exc}")

        # List network services group and check if the updated group is in the list
        try:
            groups, _, error = client.zia.cloud_firewall_rules.list_network_svc_groups()
            assert error is None, f"Error listing network service groups: {error}"
            assert groups is not None, "Network service group list is None"
            assert any(g.id == group_id for g in groups), "Updated network service group not found in list"
        except Exception as exc:
            errors.append(f"Failed to list network service groups: {exc}")

        finally:
            cleanup_errors = []
            try:
                if group_id:
                    delete_status, _, error = client.zia.cloud_firewall_rules.delete_network_svc_group(group_id)
                    assert error is None, f"Error deleting network service group: {error}"
                    assert delete_status == 204, "Network service group deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting network service group failed: {exc}")

        # Assert that no errors occurred during the test
        errors.extend(cleanup_errors)
        assert len(errors) == 0, f"Errors occurred during the network services group lifecycle test: {errors}"
