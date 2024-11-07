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


class TestCloudFirewallNetworkServices:
    """
    Integration Tests for the Cloud Firewall network services.
    """

    def test_cloud_firewall_network_services(self, fs):
        client = MockZIAClient(fs)
        errors = []

        service_name = "tests-" + generate_random_string()
        service_description = "tests-" + generate_random_string()
        service_id = None

        try:
            # Adding network service
            created_service = client.firewall.add_network_service(
                name=service_name,
                description=service_description,
                ports=[
                    ("dest", "tcp", "389"),
                    ("dest", "udp", "389"),
                    ("dest", "tcp", "636"),
                    ("dest", "tcp", "3268", "3269"),
                ],
            )
            print("Created Service:", created_service)
            assert created_service.name == service_name, "Service name mismatch in creation"
            assert created_service.description == service_description, "Service description mismatch in creation"
            service_id = created_service.id

            # # Attempt to retrieve the created network services by ID
            service = client.firewall.get_network_service(service_id)
            print("Retrieved Service:", service)
            assert service.id == service_id, "Failed to retrieve the correct network services"

            # # Attempt to update the network services
            updated_name = "updated-" + generate_random_string()
            client.firewall.update_network_service(service_id=service_id, name=updated_name)
            updated_service = client.firewall.get_network_service(service_id)
            print("Updated Service:", updated_service)
            assert updated_service.name == updated_name, "Service name mismatch after update"

            # Attempt to list network services and check if the updated service is in the list
            services = client.firewall.list_network_services()
            print("Listed Services:", services)
            assert any(svc.id == service_id for svc in services), "Updated network services not found in list"

        except Exception as exc:
            errors.append(f"Failed to interact with network services: {exc}")

        finally:
            # Cleanup: Attempt to delete the network services
            if service_id:
                try:
                    status_code = client.firewall.delete_network_service(service_id)
                    print("Delete Status Code:", status_code)
                    assert status_code == 204, "Failed to delete network services"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        print("Errors:", errors)
        assert len(errors) == 0, f"Errors occurred during the network services lifecycle test: {errors}"
