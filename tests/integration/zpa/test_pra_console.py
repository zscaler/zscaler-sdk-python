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
from tests.test_utils import generate_random_password, generate_random_string


@pytest.fixture
def fs():
    yield


class TestAccessPrivilegedConsoleV2:
    """
    Integration Tests for the Privileged Console v2
    """

    def test_access_privileged_console_v2(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        app_connector_group_id = None
        app_segment_id = None
        segment_group_id = None
        server_group_id = None
        console_id = None
        portal_id = None
        credential_id = None
        pra_application_id = None

        SDK_PREFIX = "zscaler_python_sdk"

        # Generate a random password
        password = generate_random_password()
        try:
            # Create an App Connector Group
            try:
                app_connector_group_name = "tests-" + generate_random_string()
                app_connector_group_description = "tests-" + generate_random_string()
                created_app_connector_group = client.connectors.add_connector_group(
                    name=app_connector_group_name,
                    description=app_connector_group_description,
                    enabled=True,
                    latitude="37.33874",
                    longitude="-121.8852525",
                    location="San Jose, CA, USA",
                    upgrade_day="SUNDAY",
                    upgrade_time_in_secs="66600",
                    override_version_profile=True,
                    version_profile_name="Default",
                    version_profile_id="0",
                    dns_query_type="IPV4_IPV6",
                    pra_enabled=True,
                    tcp_quick_ack_app=True,
                    tcp_quick_ack_assistant=True,
                    tcp_quick_ack_read_assistant=True,
                )
                app_connector_group_id = created_app_connector_group["id"]
            except Exception as exc:
                errors.append(f"Creating App Connector Group failed: {exc}")

            # Create a Segment Group
            try:
                segment_group_name = "tests-" + generate_random_string()
                created_segment_group = client.segment_groups.add_group(name=segment_group_name, enabled=True)
                segment_group_id = created_segment_group["id"]
            except Exception as exc:
                errors.append(f"Creating Segment Group failed: {exc}")

            # Create a Server Group
            try:
                server_group_name = "tests-" + generate_random_string()
                server_group_description = "tests-" + generate_random_string()
                created_server_group = client.server_groups.add_group(
                    name=server_group_name,
                    description=server_group_description,
                    enabled=True,
                    dynamic_discovery=True,
                    app_connector_group_ids=[app_connector_group_id],
                )
                server_group_id = created_server_group["id"]
            except Exception as exc:
                errors.append(f"Creating Server Group failed: {exc}")

            # Create an Application Segment
            try:
                app_segment_name = "tests-" + generate_random_string()
                app_segment_description = "tests-" + generate_random_string()
                app_segment_config_name = "rdp" + app_segment_name
                app_segment = client.app_segments_pra.add_segment_pra(
                    name=app_segment_name,
                    description=app_segment_description,
                    enabled=True,
                    domain_names=["test" + generate_random_string() + ".example.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["22", "3389"],
                    common_apps_dto={
                        "apps_config": [
                            {
                                "name": app_segment_config_name,
                                "description": "rdp" + app_segment_description,
                                "enabled": True,
                                "app_types": ["SECURE_REMOTE_ACCESS"],
                                "application_port": "3389",
                                "application_protocol": "RDP",
                                "connection_security": "ANY",
                                "domain": "rdp_pra_test.acme.com",
                            },
                        ]
                    },
                )
                app_segment_id = app_segment["id"]
            except Exception as exc:
                errors.append(f"Creating PRA Application Segment failed: {exc}")

            # Get the Application Segment ID for the newly created segment
            try:
                search_name = app_segment_config_name
                app_segments = client.app_segments.get_segments_by_type(
                    application_type="SECURE_REMOTE_ACCESS", search=search_name
                )
                assert app_segments and len(app_segments) > 0, "No segments found with the specified name."
                pra_application_id = app_segments[0]["id"]
            except Exception as exc:
                errors.append(f"Failed to get Application Segment by type: {exc}")

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
                # Test listing SCIM groups
                idps = client.idp.list_idps()
                user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
                assert user_idp is not None, "No IdP with sso_type 'USER' found."

                user_idp_id = user_idp["id"]
                resp = client.scim_groups.list_groups(user_idp_id)
                assert isinstance(resp, list), "Response is not in the expected list format."
                assert len(resp) >= 2, "Less than 2 SCIM groups were found for the specified IdP."

                # Extract the first two SCIM group IDs
                scim_group_ids = [(user_idp_id, group["id"]) for group in resp[:2]]
            except Exception as exc:
                errors.append(f"Listing SCIM groups failed: {exc}")

            try:
                # Create a new pra console
                created_console = client.privileged_remote_access.add_console(
                    name="tests-" + generate_random_string(),
                    description="tests-" + generate_random_string(),
                    enabled=True,
                    pra_application_id=pra_application_id,
                    pra_portal_ids=[portal_id],
                )
                assert created_console is not None, "Failed to create console"
                console_id = created_console.id  # Assuming id is accessible like this

            except Exception as exc:
                errors.append(f"Error during console creation: {exc}")

            try:
                # Test listing Consoles
                all_consoles = client.privileged_remote_access.list_consoles()
                assert any(rule["id"] == console_id for rule in all_consoles), "Consoles not found in list"
            except Exception as exc:
                errors.append(f"Failed to list Consoles Rules: {exc}")

            try:
                # Test retrieving the specific PRA Console
                retrieved_console = client.privileged_remote_access.get_console(console_id)
                assert retrieved_console["id"] == console_id, "Failed to retrieve the correct PRA Console"
            except Exception as exc:
                errors.append(f"Failed to retrieve PRA Console: {exc}")

            try:
                # Update the Access Policy Rule
                updated_rule_description = "Updated " + generate_random_string()
                updated_rule = client.privileged_remote_access.update_console(
                    console_id=console_id,
                    description=updated_rule_description,
                    enabled=True,
                    pra_application_id=pra_application_id,
                    pra_portal_ids=[portal_id],
                )
                assert updated_rule["description"] == updated_rule_description, "Failed to update description for PRA Console"
            except Exception as exc:
                errors.append(f"Failed to update PRA Console: {exc}")

        finally:
            # Ensure cleanup is performed even if there are errors
            if console_id:
                try:
                    client.privileged_remote_access.delete_console(console_id=console_id)
                except Exception as exc:
                    errors.append(f"Deleting PRA Console failed: {exc}")

            if portal_id:
                try:
                    client.privileged_remote_access.delete_portal(portal_id=portal_id)
                except Exception as exc:
                    errors.append(f"Deleting PRA Portal failed: {exc}")

            if credential_id:
                try:
                    client.privileged_remote_access.delete_credential(credential_id=credential_id)
                except Exception as exc:
                    errors.append(f"Deleting PRA Credential failed: {exc}")

            if app_segment_id:
                try:
                    client.app_segments_pra.delete_segment_pra(segment_id=app_segment_id, force_delete=True)
                except Exception as exc:
                    errors.append(f"Deleting PRA Application Segment failed: {exc}")

            if server_group_id:
                try:
                    client.server_groups.delete_group(group_id=server_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Server Group failed: {exc}")

            if segment_group_id:
                try:
                    client.segment_groups.delete_group(group_id=segment_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Segment Group failed: {exc}")

            if app_connector_group_id:
                try:
                    client.connectors.delete_connector_group(group_id=app_connector_group_id)
                except Exception as exc:
                    errors.append(f"Cleanup failed for Connector Group: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the Credential Policy Rule operations test: {errors}"
