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

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestPRAPortal:
    """
    Integration Tests for the PRA Portal.
    """

    def test_pra_portal(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        portal_id = None
        certificate_id = None

        SDK_PREFIX = "zscaler_python_sdk"

        portal_name = "tests-" + generate_random_string()
        portal_description = "tests-" + generate_random_string()

        # List all certificates
        try:
            certs_list, _, err = client.zpa.certificates.list_issued_certificates()
            assert err is None, f"Error listing certificates: {err}"
            assert isinstance(certs_list, list), "Expected a list of certificates"
            if certs_list:  # If there are any certificates, proceed with further operations
                first_certificate = certs_list[0]  # Fetch the first certificate in the list
                certificate_id = first_certificate.id  # Access the 'id' attribute directly
                assert certificate_id is not None, "Certificate ID should not be None"
        except Exception as exc:
            errors.append(f"Listing certificates failed: {str(exc)}")

        try:
            # Create a new PRA portal
            created_portal, _, err = client.zpa.pra_portal.add_portal(
                name=portal_name,
                description=portal_description,
                enabled=True,
                domain="tests-" + generate_random_string() + "acme.com",
                certificate_id=certificate_id,
                user_notification_enabled=True,
                user_notification=f"{SDK_PREFIX} Test PRA Portal",
            )
            assert err is None, f"Failed to create portal: {err}"
            assert created_portal is not None
            assert created_portal.name == portal_name
            assert created_portal.description == portal_description
            assert created_portal.enabled is True
            
            portal_id = created_portal.id  # Assuming id is accessible like this
        except Exception as exc:
            errors.append(f"Error during portal creation: {exc}")

        try:
            # Test listing Portal
            portals_list, _, err = client.zpa.pra_portal.list_portals()
            assert err is None, f"Error listing PRA portals: {err}"
            assert any(portal.id == portal_id for portal in portals_list)
        except Exception as exc:
            errors.append(f"Listing PRA portal failed: {exc}")

        try:
            # Test retrieving the specific portal
            retrieved_portal, _, err = client.zpa.pra_portal.get_portal(portal_id)
            assert err is None, f"Error fetching PRA portal: {err}"
            assert retrieved_portal.id == portal_id
            assert retrieved_portal.name == portal_name
        except Exception as exc:
            errors.append(f"Retrieving PRA portal failed: {exc}")

        try:
            if portal_id:
                # Retrieve the created app pra portal by ID
                retrieved_portal, _, err = client.zpa.pra_portal.get_portal(portal_id)
                assert err is None, f"Error fetching group: {err}"
                assert retrieved_portal.id == portal_id
                assert retrieved_portal.name == portal_name

                # Update the app pra portal
                updated_description = portal_name + " Updated"
                _, _, err = client.zpa.pra_portal.update_portal(
                    portal_id,
                    name=portal_name,
                    description=updated_description,
                    enabled=True,
                    certificate_id=certificate_id,
                    domain="tests-" + generate_random_string() + "acme.com",
                    user_notification_enabled=True,
                user_notification=f"{SDK_PREFIX} Test PRA Portal",
                )
                assert err is None, f"Error updating pra portal: {err}"

                updated_group, _, err = client.zpa.pra_portal.get_portal(portal_id)
                assert err is None, f"Error fetching updated pra portal: {err}"
                assert updated_group.description == updated_description

                # List app pra portal and ensure the updated group is in the list
                portal_list, _, err = client.zpa.pra_portal.list_portals()
                assert err is None, f"Error listing pra portals: {err}"
                assert any(group.id == portal_id for group in portal_list)
        except Exception as exc:
            errors.append(exc)

        finally:
            cleanup_errors = []

            try:
                # Attempt to delete resources created during the test
                if portal_id:
                    delete_response, _, err = client.zpa.pra_portal.delete_portal(portal_id)
                    assert err is None, f"Portal deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting portal failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the portal lifecycle test: {errors}"
