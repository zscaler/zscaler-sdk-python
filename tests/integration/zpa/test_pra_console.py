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
        errors = []

        app_connector_group_id = None
        app_segment_id = None
        segment_group_id = None
        server_group_id = None
        console_id = None
        portal_id = None
        credential_id = None

        SDK_PREFIX = "zscaler_python_sdk"

        try:
            # Create an App Connector Group
            try:
                app_connector_group_name = "tests-" + generate_random_string()
                app_connector_group_description = "tests-" + generate_random_string()
                created_app_connector_group, _, err = client.zpa.app_connector_groups.add_connector_group(
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
                if err:
                    errors.append(f"App Connector Group creation failed: {err}")
                else:
                    app_connector_group_id = created_app_connector_group.id
                    assert app_connector_group_id is not None, "App Connector Group creation failed"
            except Exception as exc:
                errors.append(f"App Connector Group creation failed: {exc}")

            # Create a Segment Group
            try:
                segment_group_name = "tests-" + generate_random_string()
                created_segment_group, _, err  = client.zpa.segment_groups.add_group(name=segment_group_name, enabled=True)
                assert err is None, f"Error during segment group creation: {err}"
                segment_group_id = created_segment_group.id
            except Exception as exc:
                errors.append(f"Error during segment group creation: {exc}")

            # Create a Server Group
            try:
                server_group_name = "tests-" + generate_random_string()
                server_group_description = "tests-" + generate_random_string()
                created_server_group, _, err = client.zpa.server_groups.add_group(
                    name=server_group_name,
                    description=server_group_description,
                    dynamic_discovery=True,
                    app_connector_group_ids=[app_connector_group_id],
                )
                assert err is None, f"Creating Server Group failed: {err}"
                server_group_id = created_server_group.id
            except Exception as exc:
                errors.append(f"Creating Server Group failed: {exc}")

            # Create an Application Segment
            try:
                app_segment_name = "rdp_pra01.acme.com"
                app_segment_description = "rdp_pra01.acme.com"

                app_segment, _, err = client.zpa.app_segments_pra.add_segment_pra(
                    name=app_segment_name,
                    description=app_segment_description,
                    enabled=True,
                    domain_names=["rdp_pra01.acme.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["3389", "3389"],
                    common_apps_dto={
                        "apps_config": [
                            {
                                "enabled": True,
                                "app_types": ["SECURE_REMOTE_ACCESS"],
                                "application_port": "3389",
                                "application_protocol": "RDP",
                                "connection_security": "ANY",
                                "domain": "rdp_pra01.acme.com",
                            }
                        ]
                    },
                )
                assert err is None, f"Error creating application segment PRA: {err}"
                assert app_segment is not None, "No application segment PRA data returned"
                assert app_segment.name == app_segment_name
                
                app_segment_id = app_segment.id
            except Exception as exc:
                errors.append(f"Creating PRA Application Segment failed: {exc}")

            # # Use the application segment's *name* to search for it
            try:
                search_name = "rdp_pra01.acme.com"
                app_segments, _, err = client.zpa.app_segment_by_type.get_segments_by_type(
                    application_type="SECURE_REMOTE_ACCESS",
                    query_params={"search": search_name}
                )
                assert err is None, f"Failed to get Application Segment by type: {err}"
                assert isinstance(app_segments, list), "Expected app_segments to be a list"

                if not app_segments:
                    raise AssertionError(f"No segments found with the specified name: {search_name}")

                # Extract `id` and `appId` from the first segment
                pra_app_id = app_segments[0]["id"]
                # app_id = app_segments[0]["appId"]

            except Exception as exc:
                errors.append(f"Failed to retrieve Application Segment by type: {exc}")

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
                # Create a new pra portal using the retrieved certificate_id
                created_portal, _, err = client.zpa.pra_portal.add_portal(
                    name="tests-" + generate_random_string(),
                    description="tests-" + generate_random_string(),
                    enabled=True,
                    domain="tests-" + generate_random_string() + "acme.com",
                    certificate_id=certificate_id,  # use the retrieved certificate_id
                    user_notification_enabled=True,
                    user_notification=f"{SDK_PREFIX} Test PRA Portal",
                )
                assert err is None, f"Error during portal creation: {err}"
                assert created_portal is not None, "Failed to create portal"
                portal_id = created_portal.id  # Assuming id is accessible like this

            except Exception as exc:
                errors.append(f"Error during portal creation: {exc}")

            try:
                # Create a new pra console using the pra_application_id and portal_id
                created_console, _, err = client.zpa.pra_console.add_console(
                    name="tests-" + generate_random_string(),
                    description="tests-" + generate_random_string(),
                    enabled=True,
                    pra_application_id=pra_app_id,
                    pra_portal_ids=[portal_id],
                )
                assert err is None, f"Error during console creation: {err}"
                assert created_console is not None, "Failed to create console"
                console_id = created_console.id  # Assuming id is accessible like this

            except Exception as exc:
                errors.append(f"Error during console creation: {exc}")

            try:
                # Test listing Consoles
                all_consoles, _, err = client.zpa.pra_console.list_consoles()
                assert err is None, f"Error listing PRA Consoles: {err}"
                assert any(console.id == console_id for console in all_consoles), "Created console not found in list"
            except Exception as exc:
                errors.append(f"Listing PRA Consoles failed: {exc}")
                
            try:
                # Test retrieving the specific PRA Console
                retrieved_console, _, err = client.zpa.pra_console.get_console(console_id)
                assert err is None, f"Error fetching Consoles: {err}"
                assert retrieved_console.id == console_id, "Retrieved console ID does not match"
            except Exception as exc:
                errors.append(f"Failed to retrieve PRA Console: {exc}")

            try:
                if console_id:
                    retrieved_console, _, err = client.zpa.pra_console.get_console(console_id)
                    assert err is None, f"Error fetching console: {err}"
                    assert retrieved_console.id == console_id

                # Update the console
                updated_rule_description = "Updated " + generate_random_string()
                _, _, err = client.zpa.pra_console.update_console(
                    console_id=console_id,
                    description=updated_rule_description,
                    enabled=True,
                    pra_application_id=pra_app_id,
                    pra_portal_ids=[portal_id],
                )
                # If we got an error but it’s "Response is None", treat it as success:
                if err is not None:
                    if isinstance(err, ValueError) and str(err) == "Response is None":
                        print(f"[INFO] Interpreting 'Response is None' as 204 success.")
                    else:
                        raise AssertionError(f"Error updating PRA Console: {err}")
                print(f"PRA Console with ID {console_id} updated successfully (204 No Content).")
            except Exception as exc:
                errors.append(f"Updating PRA Console failed: {exc}")

        finally:
            
            if console_id:
                try:
                    delete_response, _, err = client.zpa.pra_console.delete_console(console_id=console_id)
                    assert err is None, f"Console deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting PRA Console failed: {exc}")

            if portal_id:
                try:
                    delete_response, _, err = client.zpa.pra_portal.delete_portal(portal_id=portal_id)
                    assert err is None, f"Portal deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting PRA Portal failed: {exc}")

            if credential_id:
                try:
                    delete_response, _, err = client.zpa.pra_credential.delete_credential(credential_id=credential_id)
                    assert err is None, f"Credential deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting PRA Credential failed: {exc}")

            if app_segment_id:
                try:
                    delete_response, _, err = client.zpa.app_segments_pra.delete_segment_pra(segment_id=app_segment_id, force_delete=True)
                    assert err is None, f"App Segment deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting PRA Application Segment failed: {exc}")

            if server_group_id:
                try:
                    delete_response, _, err = client.zpa.server_groups.delete_group(group_id=server_group_id)
                    assert err is None, f"Server Group deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting Server Group failed: {exc}")

            if segment_group_id:
                try:
                    delete_response, _, err = client.zpa.segment_groups.delete_group(group_id=segment_group_id)
                    assert err is None, f"Segment Group deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting Segment Group failed: {exc}")

            if app_connector_group_id:
                try:
                    delete_response, _, err = client.zpa.app_connector_groups.delete_connector_group(group_id=app_connector_group_id)
                    assert err is None, f"Connector Group deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Cleanup failed for Connector Group: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the PRA Console operations test: {errors}"
