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


class TestUserPortal:
    """
    Integration Tests for the User Portal
    """

    @pytest.mark.vcr()
    def test_user_portal(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        portal_name = "tests-uport-" + generate_random_string()
        portal_description = "tests-uport-" + generate_random_string()
        ext_label = "tests-uport-" + generate_random_string()  # Unique ext_label to avoid duplicates
        portal_id = None  # Initialize portal_id

        try:
            # Create a new portal
            created_portal = client.zpa.user_portal_controller.add_user_portal(
                name=portal_name,
                description=portal_description,
                enabled=True,
                user_notification=portal_description,
                user_notification_enabled=True,
                managed_by_zs=True,
                domain='securitygeek.io',
                ext_label=ext_label,
                ext_domain_name='-securitygeek-io.b.zscalerportal.net',
                ext_domain="securitygeek.io"
            )
            assert created_portal is not None
            assert created_portal.name == portal_name
            assert created_portal.description == portal_description
            assert created_portal.enabled is True
            # Note: managed_by_zs is not returned in the API response, so we don't assert it
            assert created_portal.user_notification_enabled is True
            assert created_portal.user_notification == portal_description

            portal_id = created_portal.id  # Capture the portal_id for later use
        except Exception as exc:
            errors.append(f"Error during portal creation: {exc}")

        try:
            if portal_id:
                # Retrieve the created portal by ID
                retrieved_portal = client.zpa.user_portal_controller.get_user_portal(portal_id)
                assert retrieved_portal.id == portal_id
                assert retrieved_portal.name == portal_name

                # Update the portal
                updated_name = portal_name + " Updated"
                _ = client.zpa.user_portal_controller.update_user_portal(
                    portal_id, 
                    name=updated_name,
                    description=portal_description,
                    enabled=True,
                    user_notification=portal_description,
                    user_notification_enabled=True,
                    managed_by_zs=True,
                    domain='securitygeek.io',
                    ext_label=ext_label,
                    ext_domain_name='-securitygeek-io.b.zscalerportal.net',
                    ext_domain="securitygeek.io"                    
                    )

                updated_portal = client.zpa.user_portal_controller.get_user_portal(portal_id)
                assert updated_portal.name == updated_name

                # List portals and ensure the updated portal is in the list
                portal_list = client.zpa.user_portal_controller.list_user_portals()
                assert any(portal.id == portal_id for portal in portal_list)
        except Exception as exc:
            errors.append(f"Portal operation failed: {exc}")

        finally:
            # Cleanup: Delete the portal if it was created
            if portal_id:
                try:
                    delete_response = client.zpa.user_portal_controller.delete_user_portal(portal_id)
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for portal ID {portal_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the portal lifecycle test: {errors}"
