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

    @pytest.mark.vcr()
    def test_cloud_firewall_network_services_group(self, fs):
        client = MockZIAClient(fs)
        errors = []

        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        group_id = None
        service_ids = []

        # Step 1: Search for the required network services and extract their IDs
        try:
            for service_name in ["ICMP_ANY", "UDP_ANY", "TCP_ANY", "DNS"]:
                services, _, error = client.zia.cloud_firewall.list_network_services(query_params={"search": service_name})
                assert error is None, f"Error searching for network service '{service_name}': {error}"
                assert services, f"No services found for '{service_name}'"

                service = next((svc for svc in services if svc.name == service_name), None)
                assert service is not None, f"Service '{service_name}' not found in list"
                service_ids.append(service.id)
        except Exception as exc:
            errors.append(f"Failed to retrieve network service IDs: {exc}")

        # Step 2: Add the network service group
        try:
            created_group, _, error = client.zia.cloud_firewall.add_network_svc_group(
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

        # Step 3: Retrieve the group by ID
        try:
            if group_id:
                group, _, error = client.zia.cloud_firewall.get_network_svc_group(group_id)
                assert error is None, f"Error retrieving network service group: {error}"
                assert group is not None, "Retrieved network service group is None"
                assert group.id == group_id, "Incorrect network service group retrieved"
        except Exception as exc:
            errors.append(f"Failed to retrieve network service group: {exc}")

        # Step 4: Update the network services group
        try:
            if group_id:
                updated_name = "updated-" + generate_random_string()
                updated_description = group_description + " updated"

                updated_group, _, error = client.zia.cloud_firewall.update_network_svc_group(
                    group_id=group_id,
                    name=updated_name,
                    description=updated_description,
                    service_ids=service_ids,  # Reuse original IDs to avoid clearing
                )
                assert error is None, f"Error updating network service group: {error}"
                assert updated_group.name == updated_name, "Group name mismatch after update"
                assert updated_group.description == updated_description, "Group description mismatch after update"
        except Exception as exc:
            errors.append(f"Failed to update network service group: {exc}")

        # Step 5: List network service groups and verify update
        try:
            groups, _, error = client.zia.cloud_firewall.list_network_svc_groups()
            assert error is None, f"Error listing network service groups: {error}"
            assert groups is not None, "Network service group list is None"
            assert any(g.id == group_id for g in groups), "Updated network service group not found in list"
        except Exception as exc:
            errors.append(f"Failed to list network service groups: {exc}")

        finally:
            # Ensure label cleanup
            try:
                if group_id:
                    _, _, error = client.zia.cloud_firewall.delete_network_svc_group(group_id)
                    assert error is None, f"Delete network service group Error: {error}"
            except Exception as e:
                errors.append(f"Exception during network service group: {str(e)}")

        # Final Assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
