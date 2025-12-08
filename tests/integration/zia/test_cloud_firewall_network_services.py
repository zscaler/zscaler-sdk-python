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


class TestCloudFirewallNetworkServices:
    """
    Integration Tests for the Cloud Firewall network services.
    """

    @pytest.mark.vcr()
    def test_cloud_firewall_network_services(self, fs):
        client = MockZIAClient(fs)
        errors = []

        service_name = "tests-" + generate_random_string()
        service_description = "tests-" + generate_random_string()
        service_ports = [
            ("dest", "tcp", "389"),
            ("dest", "udp", "389"),
            ("dest", "tcp", "636"),
            ("dest", "tcp", "3268", "3269"),
        ]
        service_id = None

        try:
            # Step 1: Add network service
            try:
                created_service = client.zia.cloud_firewall.add_network_service(
                    name=service_name,
                    description=service_description,
                    ports=service_ports,
                )
                print("Created Service:", created_service.as_dict() if created_service else None)
                assert created_service is not None, "Service creation returned None"
                assert created_service.name == service_name
                assert created_service.description == service_description
                service_id = created_service.id
            except Exception as exc:
                errors.append(f"Failed to add network service: {exc}")

            # Step 2: Retrieve service by ID
            try:
                if service_id:
                    service = client.zia.cloud_firewall.get_network_service(service_id)
                    print("Retrieved Service:", service.as_dict() if service else None)
                    assert service is not None
                    assert service.id == service_id
            except Exception as exc:
                errors.append(f"Failed to retrieve network service: {exc}")

            # Step 3: Update service
            try:
                if service_id:
                    updated_name = "updated-" + generate_random_string()
                    updated_description = "updated-" + generate_random_string()

                    updated_service = client.zia.cloud_firewall.update_network_service(
                        service_id=service_id,
                        name=updated_name,
                        description=updated_description,
                        ports=service_ports,
                    )
                    print("Updated Service:", updated_service.as_dict() if updated_service else None)
                    assert updated_service is not None
                    assert updated_service.name == updated_name
                    assert updated_service.description == updated_description
            except Exception as exc:
                errors.append(f"Failed to update network service: {exc}")

            # Step 4: List services and verify presence
            try:
                services_list = client.zia.cloud_firewall.list_network_services()
                print("Listed Services:", [s.as_dict() for s in services_list] if services_list else None)
                assert services_list is not None
                assert any(s.id == service_id for s in services_list), "Updated service not found in list"
            except Exception as exc:
                errors.append(f"Failed to list network services: {exc}")

        finally:
            # Step 5: Cleanup
            try:
                if service_id:
                    _ = client.zia.cloud_firewall.delete_network_service(service_id)
                    print(f"Service with ID {service_id} deleted successfully.")
            except Exception as exc:
                errors.append(f"Cleanup failed: {exc}")

        # Final Assertion
        if errors:
            pytest.fail(f"Test failed with errors: {errors}")
