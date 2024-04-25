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

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string, generate_time_bounds


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

        # List all certificates
        try:
            certs = client.certificates.list_issued_certificates()
            assert isinstance(certs, list), "Expected a list of certificates"
            if certs:  # If there are any certificates, proceed with further operations
                first_certificate = certs[0]
                certificate_id = first_certificate.get("id")
        except Exception as exc:
            errors.append(f"Listing certificates failed: {str(exc)}")

        try:
            # Create a new pra portal
            created_portal = client.privileged_remote_access.add_portal(
                name="tests-" + generate_random_string(),
                description="tests-" + generate_random_string(),
                enabled=True,
                domain="tests-" + generate_random_string() + "acme.com",
                certificate_id=certificate_id,
                user_notification_enabled=True,
                user_notification=f"{SDK_PREFIX} Test PRA Portal",
            )
            assert created_portal is not None, "Failed to create portal"
            portal_id = created_portal.id  # Assuming id is accessible like this

        except Exception as exc:
            errors.append(f"Error during portal creation: {exc}")

        try:
            # Test listing Portal
            all_portals = client.privileged_remote_access.list_portals()
            if not any(portal["id"] == portal_id for portal in all_portals):
                raise AssertionError("Portal not found in list")
        except Exception as exc:
            errors.append(f"Listing Portal failed: {exc}")

        try:
            # Test retrieving the specific portal
            retrieved_portal = client.privileged_remote_access.get_portal(portal_id)
            if retrieved_portal["id"] != portal_id:
                raise AssertionError("Failed to retrieve the correct portal")
        except Exception as exc:
            errors.append(f"Retrieving portal failed: {exc}")

        try:
            # Update the portal
            updated_description = "Updated " + generate_random_string()
            updated_portal = client.privileged_remote_access.update_portal(
                portal_id,
                description=updated_description,
                enabled=True,
                user_notification_enabled=True,
                user_notification=f"{SDK_PREFIX} Test PRA Portal",
            )
            if updated_portal["description"] != updated_description:
                raise AssertionError("Failed to update description for portal")
        except Exception as exc:
            errors.append(f"Updating portal failed: {exc}")

        finally:
            cleanup_errors = []

            try:
                # Attempt to delete resources created during the test
                if portal_id:
                    delete_status = client.privileged_remote_access.delete_portal(portal_id)
                    assert delete_status == 204, "Portal deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Portal failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the portal lifecycle test: {errors}"
