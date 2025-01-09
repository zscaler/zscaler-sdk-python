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


class TestApplicationSegment:
    """
    Integration Tests for the Applications Segment
    """

    def test_application_segment(self, fs):
        client = MockZPAClient(fs)
        errors = []

        # Initialize IDs for cleanup
        app_connector_group_id = None
        segment_group_id = None
        server_group_id = None
        app_segment_id = None

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
                
            try:
                app_segment_name = "tests-" + generate_random_string()
                app_segment_description = "tests-" + generate_random_string()
                app_segment, _, err = client.zpa.app_segments.add_segment(
                    name=app_segment_name,
                    description=app_segment_description,
                    enabled=True,
                    domain_names=["test.example.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["8080", "8080"],  # Adjusted to tuple format
                )
                assert err is None, f"Creating Application Segment failed: {err}"
                assert app_segment is not None, "No application segment data returned"

                # Access the attribute directly instead of using subscript notation
                app_segment_id = app_segment.id
            except Exception as exc:
                errors.append(f"Creating Application Segment failed: {exc}")


            # Test listing Application Segments - Filter by the unique name
            try:
                # Test listing Portal
                segment_list, _, err = client.zpa.app_segments.list_segments()
                assert err is None, f"Error listing Application Segment: {err}"
                assert any(segment.id == app_segment_id for segment in segment_list)
            except Exception as exc:
                errors.append(f"Listing Application Segment failed: {exc}")

            # Test updating the Application Segment
            try:
                if app_segment_id:
                    # Retrieve the existing segment by ID
                    retrieved_segment, _, err = client.zpa.app_segments.get_segment(app_segment_id)
                    assert err is None, f"Error fetching Application Segment: {err}"
                    assert retrieved_segment.id == app_segment_id
                    assert retrieved_segment.name == app_segment_name

                    updated_name = "Updated " + generate_random_string()
                    # Provide all fields as keyword arguments, mirroring the creation style
                    updated_app, _, err = client.zpa.app_segments.update_segment(
                        app_segment_id,
                        name=updated_name,
                        description="UpdatedDescription " + generate_random_string(),
                        enabled=True,
                        domain_names=["test.example.com"],  
                        segment_group_id=segment_group_id,
                        server_group_ids=[server_group_id],
                        tcp_port_ranges=["8081", "8081"],
                    )
                    assert err is None, f"Error updating Application Segment: {err}"
                    assert updated_app is not None, "No updated ApplicationSegment returned"

                    # Fetch the updated segment to validate the update
                    verified_app, _, err = client.zpa.app_segments.get_segment(app_segment_id)
                    assert err is None, f"Error fetching updated Application Segment: {err}"
                    assert verified_app.name == updated_name
            except Exception as exc:
                errors.append(f"Updating Application Segment failed: {exc}")


        finally:
            # Cleanup resources
            if app_segment_id:
                try:
                    client.zpa.app_segments.delete_segment(segment_id=app_segment_id, force_delete=True)
                except Exception as exc:
                    errors.append(f"Deleting Application Segment failed: {exc}")
                    
            if server_group_id:
                try:
                    client.zpa.server_groups.delete_group(group_id=server_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Server Group failed: {exc}")

            if app_connector_group_id:
                try:
                    client.zpa.app_connector_groups.delete_connector_group(group_id=app_connector_group_id)
                except Exception as exc:
                    errors.append(f"Deleting App Connector Group failed: {exc}")

            if segment_group_id:
                try:
                    client.zpa.segment_groups.delete_group(group_id=segment_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Segment Group failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the Application Segment lifecycle test: {errors}"
