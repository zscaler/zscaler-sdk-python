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


class TestUserPortalLink:
    """
    Integration Tests for the User Portal Link
    """

    @pytest.mark.vcr()
    def test_portal_link(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        portal_id = None
        portal_link_id = None

        portal_name = "tests-uportlnk-" + generate_random_string()
        portal_description = "tests-uportlnk-" + generate_random_string()
        ext_label = "tests-uplnk-" + generate_random_string()  # Unique ext_label to avoid duplicates

        try:
            # Create the User Portal
            created_portal, _, err = client.zpa.user_portal_controller.add_user_portal(
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
            assert err is None, f"Error creating user portal: {err}"
            assert created_portal is not None
            assert created_portal.name == portal_name
            assert created_portal.description == portal_description

            # Debugging: Check if the `enabled` field exists
            assert (
                "enabled" in created_portal.__dict__
            ), f"'enabled' field missing in response: {created_portal.__dict__}"
            assert (
                created_portal.enabled is True
            ), f"Expected 'enabled' to be True, got: {created_portal.enabled}"

            portal_id = created_portal.id  # Capture the portal_id for later use
        except Exception as exc:
            errors.append(exc)

        try:
            # Create a User Portal Links
            created_portal_link, _, err = client.zpa.user_portal_link.add_portal_link(
                name=portal_name,
                description=portal_description,
                enabled=True,
                link="server1.example.com",
                user_notification_enabled=True,
                icon_text='',
                protocol='https://',
                user_portal_ids=[portal_id],
            )
            assert err is None, f"Error creating user portal link: {err}"
            assert created_portal_link is not None
            assert created_portal_link.name == portal_name
            assert created_portal_link.description == portal_description

            # Debugging: Check if the `enabled` field exists in the user portal link
            assert (
                "enabled" in created_portal_link.__dict__
            ), f"'enabled' field missing in response: {created_portal_link.__dict__}"
            assert created_portal_link.enabled is True, f"Expected 'enabled' to be True, got: {created_portal_link.enabled}"

            portal_link_id = created_portal_link.id
        except Exception as exc:
            errors.append(f"Error during user portal link creation: {exc}")

        try:
            if portal_link_id:
                # Retrieve the specific user portal link
                retrieved_portal, _, err = client.zpa.user_portal_link.get_portal_link(portal_link_id)
                assert err is None, f"Error fetching user portal link: {err}"
                assert retrieved_portal.id == portal_link_id
                assert retrieved_portal.name == portal_name

                # Update the user portal link
                updated_name = portal_name + " Updated"
                _, _, err = client.zpa.user_portal_link.update_portal_link(
                    portal_link_id, 
                    name=updated_name,
                    enabled=True,
                    link="server1.example.com",
                    user_notification_enabled=True,
                    icon_text='',
                    protocol='https://',
                    user_portal_ids=[portal_id],
                )
                assert err is None, f"Error updating user portal link: {err}"

                updated_portal, _, err = client.zpa.user_portal_link.get_portal_link(portal_link_id)
                assert err is None, f"Error fetching updated user portal link: {err}"
                assert updated_portal.name == updated_name

                # List user portal link and ensure the updated portal is in the list
                portal_list, _, err = client.zpa.user_portal_link.list_portal_link()
                assert err is None, f"Error listing user portal link: {err}"
                assert any(portal.id == portal_link_id for portal in portal_list)
        except Exception as exc:
            errors.append(f"user portal link operation failed: {exc}")

        finally:
            # Cleanup - delete the user portal link first, then the User Portal
            cleanup_errors = []

            if portal_link_id:
                try:
                    delete_response, _, err = client.zpa.user_portal_link.delete_portal_link(portal_link_id)
                    assert err is None, f"Error deleting user portal link: {err}"
                    # Since a 204 No Content response returns None, assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    cleanup_errors.append(f"Cleanup failed for user portal link ID {portal_link_id}: {cleanup_exc}")

            if portal_id:
                try:
                    client.zpa.user_portal_controller.delete_user_portal(portal_id)
                except Exception as exc:
                    cleanup_errors.append(f"Cleanup failed for User Portal: {exc}")

            errors.extend(cleanup_errors)

        assert len(errors) == 0, f"Errors occurred during the user portal link operations test: {errors}"
