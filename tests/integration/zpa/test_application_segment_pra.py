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


class TestApplicationSegmentPRA:
    """
    Integration Tests for the Applications Segment PRA
    """

    def test_application_segment_pra(self, fs):
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

            #
            try:
                app_segment_name = "ssh_pra.bd-redhat.com"
                app_segment_description = "ssh_pra.bd-redhat.com"

                app_segment, resp, err = client.zpa.app_segments_pra.add_segment_pra(
                    name=app_segment_name,
                    description=app_segment_description,
                    enabled=True,
                    domain_names=["ssh_pra.bd-redhat.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["22", "22"],
                    common_apps_dto={
                        "apps_config": [
                            {
                                "enabled": True,
                                "app_types": ["SECURE_REMOTE_ACCESS"],
                                "application_port": "22",
                                "application_protocol": "SSH",
                                "domain": "ssh_pra.bd-redhat.com",
                            }
                        ]
                    },
                )
                assert err is None, f"Error creating server group: {err}"
                assert app_segment is not None, "No application segment PRA data returned"
                assert app_segment.name == app_segment_name
                
                app_segment_id = app_segment.id
            except Exception as exc:
                errors.append(f"Creating PRA Application Segment failed: {exc}")

            try:
                search_name = "ssh_pra.bd-redhat.com"
                app_segments, resp, err = client.zpa.app_segment_by_type.get_segments_by_type(
                    application_type="SECURE_REMOTE_ACCESS",
                    query_params={"search": search_name}
                )
                assert err is None, f"Failed to get Application Segment by type: {err}"
                assert isinstance(app_segments, list), "Expected app_segments to be a list"

                if not app_segments:
                    raise AssertionError(f"No segments found with the specified name: {search_name}")

                # Extract `id` and `appId` from the first segment
                pra_app_id = app_segments[0]["id"]
                app_id = app_segments[0]["appId"]

            except Exception as exc:
                errors.append(f"Failed to retrieve Application Segment by type: {exc}")

            # Test updating the Application Segment
            try:
                if app_segment_id:
                    updated_description = "Updated " + generate_random_string()
                    _, resp, err = client.zpa.app_segments_pra.update_segment_pra(
                        app_segment_id,
                        name=app_segment_name,
                        description=updated_description,
                        enabled=True,
                        domain_names=["ssh_pra.bd-redhat.com"],
                        segment_group_id=segment_group_id,
                        server_group_ids=[server_group_id],
                        tcp_port_ranges=["22", "22"],
                        common_apps_dto={
                            "apps_config": [
                                {
                                    "app_id": app_id,
                                    "pra_app_id": pra_app_id,
                                    "enabled": True,
                                    "app_types": ["SECURE_REMOTE_ACCESS"],
                                    "application_port": "22",
                                    "application_protocol": "SSH",
                                    "domain": "ssh_pra.bd-redhat.com",
                                }
                            ]
                        },
                    )
                    assert err is None, f"Error updating Application Segment: {err}"
            except Exception as exc:
                errors.append(f"Updating Application Segment failed: {exc}")

        finally:
            # Cleanup resources
            if app_segment_id:
                try:
                    client.zpa.app_segments_pra.delete_segment_pra(segment_id=app_segment_id, force_delete=True)
                except Exception as exc:
                    errors.append(f"Deleting Application Segment failed: {exc}")
            if server_group_id:
                try:
                    client.zpa.server_groups.delete_group(group_id=server_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Server Group failed: {exc}")
            if segment_group_id:
                try:
                    client.zpa.segment_groups.delete_group(group_id=segment_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Segment Group failed: {exc}")

        # Final assertion: no errors
        assert not errors, f"Errors occurred during the Application Segment lifecycle test: {errors}"
