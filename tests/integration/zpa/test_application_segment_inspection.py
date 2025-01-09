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


import time
import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestApplicationSegmentInspection:
    """
    Integration Tests for the Applications Segment Inspection
    """

    def test_application_segment_inspection(self, fs):
        client = MockZPAClient(fs)
        errors = []

        # IDs for cleanup
        app_connector_group_id = None
        segment_group_id = None
        server_group_id = None
        app_segment_id = None

        try:

            try:
                app_connector_group_name = "tests-" + generate_random_string()
                app_connector_group_description = "tests-" + generate_random_string()

                created_app_connector_group, resp, err = client.zpa.app_connector_groups.add_connector_group(
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
                assert err is None, f"App Connector Group creation failed: {err}"
                assert created_app_connector_group is not None, "No App Connector Group data returned"

                app_connector_group_id = created_app_connector_group.id
                assert app_connector_group_id, "App Connector Group creation returned empty ID"
            except Exception as exc:
                errors.append(f"App Connector Group creation failed: {exc}")

            #
            # 3) Create a Segment Group
            #
            try:
                segment_group_name = "tests-" + generate_random_string()
                created_segment_group, resp, err = client.zpa.segment_groups.add_group(
                    name=segment_group_name,
                    enabled=True
                )
                assert err is None, f"Error during segment group creation: {err}"
                assert created_segment_group is not None, "No segment group data returned"

                segment_group_id = created_segment_group.id
            except Exception as exc:
                errors.append(f"Error during segment group creation: {exc}")

            #
            # 4) Create a Server Group
            #
            try:
                server_group_name = "tests-" + generate_random_string()
                server_group_description = "tests-" + generate_random_string()

                created_server_group, resp, err = client.zpa.server_groups.add_group(
                    name=server_group_name,
                    description=server_group_description,
                    enabled=True,
                    dynamic_discovery=True,
                    app_connector_group_ids=[app_connector_group_id],
                )
                assert err is None, f"Creating Server Group failed: {err}"
                assert created_server_group is not None, "No server group data returned"

                server_group_id = created_server_group.id
            except Exception as exc:
                errors.append(f"Creating Server Group failed: {exc}")

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

            #
            try:
                app_segment_name = "server1.bd-redhat.com"
                app_segment_description = "server1.bd-redhat.com"

                app_segment, resp, err = client.zpa.app_segments_inspection.add_segment_inspection(
                    name=app_segment_name,
                    description=app_segment_description,
                    enabled=True,
                    domain_names=["server1.bd-redhat.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["443", "443"],
                    common_apps_dto={
                        "apps_config": [
                            {
                                "enabled": True,
                                "app_types": ["INSPECT"],
                                "application_port": "443",
                                "application_protocol": "HTTPS",
                                "certificate_id": certificate_id,
                                "domain": "server1.bd-redhat.com",
                            }
                        ]
                    },
                )
                assert err is None, f"Error creating application segment inspection: {err}"
                assert app_segment is not None, "No application segment inspection data returned"
                assert app_segment.name == app_segment_name

                app_segment_id = app_segment.id
            except Exception as exc:
                errors.append(f"Creating Inspection Application Segment failed: {exc}")

            try:
                time.sleep(5)
                search_name = "server1.bd-redhat.com"
                app_segments, resp, err = client.zpa.app_segment_by_type.get_segments_by_type(
                    application_type="INSPECT",
                    query_params={"search": search_name}
                )
                assert err is None, f"Failed to get Application Segment by type: {err}"
                assert isinstance(app_segments, list), "Expected app_segments to be a list"

                if not app_segments:
                    raise AssertionError(f"No segments found with the specified name: {search_name}")

                # Extract `id` and `appId` from the first segment
                inspect_app_id = app_segments[0]["id"]
                app_id = app_segments[0]["appId"]

            except Exception as exc:
                errors.append(f"Failed to retrieve Application Segment by type: {exc}")

            # Test updating the Application Segment
            try:
                if app_segment_id:
                    updated_description = "Updated " + generate_random_string()
                    _, resp, err = client.zpa.app_segments_inspection.update_segment_inspection(
                        app_segment_id,
                        name=app_segment_name,
                        description=updated_description,
                        enabled=True,
                        domain_names=["server1.bd-redhat.com"],
                        segment_group_id=segment_group_id,
                        server_group_ids=[server_group_id],
                        tcp_port_ranges=["443", "443"],
                        common_apps_dto={
                            "apps_config": [
                                {
                                    "app_id":app_id,  # Use app_id retrieved earlier
                                    "inspect_app_id":inspect_app_id,  # Use inspect_app_id retrieved earlier
                                    "enabled": True,
                                    "app_types": ["INSPECT"],
                                    "application_port": "443",
                                    "application_protocol": "HTTPS",
                                    "certificate_id": certificate_id,
                                    "domain": "server1.bd-redhat.com",
                                }
                            ]
                        },
                    )
                    assert err is None, f"Error updating Application Segment: {err}"
            except Exception as exc:
                errors.append(f"Updating Application Segment failed: {exc}")

        finally:
            cleanup_errors = []
            
            time.sleep(5)
            if app_segment_id:
                try:
                    _, resp, del_err = client.zpa.app_segments_inspection.delete_segment_inspection(
                        segment_id=app_segment_id, force_delete=True
                    )
                    if del_err:
                        cleanup_errors.append(f"Deleting Application Segment failed: {del_err}")
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Application Segment failed: {exc}")

            if server_group_id:
                try:
                    _, resp, del_err = client.zpa.server_groups.delete_group(group_id=server_group_id)
                    if del_err:
                        cleanup_errors.append(f"Deleting Server Group failed: {del_err}")
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Server Group failed: {exc}")

            if segment_group_id:
                try:
                    _, resp, del_err = client.zpa.segment_groups.delete_group(group_id=segment_group_id)
                    if del_err:
                        cleanup_errors.append(f"Deleting Segment Group failed: {del_err}")
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Segment Group failed: {exc}")

            if cleanup_errors:
                errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during the Application Segment lifecycle test: {errors}"
