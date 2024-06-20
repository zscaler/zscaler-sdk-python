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


class TestCloudFirewallNetworkServicesGroup:
    """
    Integration Tests for the Cloud Firewall network services group.
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
                service = next(
                    svc for svc in client.firewall.list_network_services(search=service_name) if svc.name == service_name
                )
                service_ids.append(service.id)
        except Exception as exc:
            errors.append(f"Failed to retrieve network service IDs: {exc}")

        try:
            created_group = client.firewall.add_network_svc_group(
                name=group_name,
                description=group_description,
                service_ids=service_ids,
            )
            assert created_group.name == group_name, "Group name mismatch in creation"
            assert created_group.description == group_description, "Group description mismatch in creation"
            group_id = created_group.id
        except Exception as exc:
            errors.append(f"Failed to add network services group: {exc}")

            # Attempt to retrieve the created network services group by ID
            if group_id:
                try:
                    group = client.firewall.get_network_svc_group(group_id)
                    assert group.id == group_id, "Failed to retrieve the correct network services group"
                except Exception as exc:
                    errors.append(f"Failed to retrieve network services group: {exc}")

            # Attempt to update the network services group
            if group_id:
                try:
                    updated_name = "updated-" + generate_random_string()
                    client.firewall.update_network_svc_group(group_id=group_id, name=updated_name)
                    updated_group = client.firewall.get_network_svc_group(group_id)
                    assert updated_group.name == updated_name, "Group name mismatch after update"
                except Exception as exc:
                    errors.append(f"Failed to update network services group: {exc}")

            # Attempt to list network services group and check if the updated group is in the list
            try:
                groups = client.firewall.list_network_svc_groups()
                assert any(group.id == group_id for group in groups), "Updated network services group not found in list"
            except Exception as exc:
                errors.append(f"Failed to list network services group: {exc}")

        finally:
            # Cleanup: Attempt to delete the network services group
            if group_id:
                try:
                    status_code = client.firewall.delete_network_svc_group(group_id)
                    assert status_code == 204, "Failed to delete network services group"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the network services group lifecycle test: {errors}"
