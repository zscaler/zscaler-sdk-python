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
import time

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string, generate_time_bounds


@pytest.fixture
def fs():
    yield


class TestPRAApproval:
    """
    Integration Tests for the PRA Approval.
    """

    def test_pra_approval(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        approval_id = None
        app_segment_id = None
        segment_group_id = None
        app_connector_group_id = None
        server_group_id = None

        start_time, end_time = generate_time_bounds("America/Vancouver", "RFC1123Z")
        # email_id = 'test-' + generate_random_string() + "@bd-hashicorp.com"

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
                time.sleep(2)
                segment_group_name = "tests-" + generate_random_string()
                created_segment_group, _, err  = client.zpa.segment_groups.add_group(name=segment_group_name, enabled=True)
                assert err is None, f"Error during segment group creation: {err}"
                segment_group_id = created_segment_group.id
            except Exception as exc:
                errors.append(f"Error during segment group creation: {exc}")

            # Create a Server Group
            try:
                time.sleep(2)
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
                time.sleep(2)
                app_segment_name = "example.acme.com"
                app_segment_description = "example.acme.com"

                app_segment, _, err = client.zpa.app_segments.add_segment(
                    name=app_segment_name,
                    description=app_segment_description,
                    enabled=True,
                    domain_names=["example.acme.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["8080", "8080"],
                )
                assert err is None, f"Error creating application segment: {err}"
                assert app_segment is not None, "No application segment data returned"
                assert app_segment.name == app_segment_name
                
                app_segment_id = app_segment.id
            except Exception as exc:
                errors.append(f"Creating Application Segment failed: {exc}")

            try:
                time.sleep(2)
                # Create a new privileged approval
                new_approval_data = {
                    "email_ids": ["carol.kirk@bd-hashicorp.com"],
                    "application_ids": [app_segment_id],
                    "start_time": start_time,
                    "end_time": end_time,
                    "status": "ACTIVE",
                    "working_hours": {
                        "start_time_cron": "0 0 16 ? * SUN,MON,TUE,WED,THU,FRI,SAT",
                        "end_time_cron": "0 0 0 ? * MON,TUE,WED,THU,FRI,SAT,SUN",
                        "start_time": "09:00",
                        "end_time": "17:00",
                        "days": ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
                        "time_zone": "America/Vancouver",
                    },
                }

                created_approval, _, err = client.zpa.pra_approval.add_approval(**new_approval_data)
                assert err is None, f"Error creating PRA approval: {err}"
                assert created_approval is not None, "No PRA approval data returned"

                approval_id = created_approval.id
                print(f"PRA Approval created successfully: {created_approval.as_dict()}")

            except Exception as exc:
                errors.append(f"Creating PRA approval failed: {exc}")

            try:
                # Test listing approvals
                approval_list, _, err = client.zpa.pra_approval.list_approval()
                assert err is None, f"Error listing PRA approval: {err}"
                assert any(approval.id == approval_id for approval in approval_list), "Created approval not found in list"
            except Exception as exc:
                errors.append(f"Listing PRA approvals failed: {exc}")

            try:
                # Test retrieving the specific PRA Console
                retrieved_approval, _, err = client.zpa.pra_approval.get_approval(approval_id)
                assert err is None, f"Error fetching approvals: {err}"
                assert retrieved_approval.id == approval_id, "Retrieved console ID does not match"
                assert retrieved_approval.status == "ACTIVE", "Approval status mismatch"
            except Exception as exc:
                errors.append(f"Failed to retrieve PRA approval: {exc}")

        finally:
            
            if approval_id:
                try:
                    time.sleep(2)
                    delete_response, _, err = client.zpa.pra_approval.delete_approval(approval_id=approval_id)
                    assert err is None, f"approval deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting approval failed: {exc}")

            if app_segment_id:
                try:
                    time.sleep(2)
                    delete_response, _, err = client.zpa.app_segments.delete_segment(segment_id=app_segment_id, force_delete=True)
                    assert err is None, f"App Segment deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting Application Segment failed: {exc}")

            if server_group_id:
                try:
                    time.sleep(2)
                    delete_response, _, err = client.zpa.server_groups.delete_group(group_id=server_group_id)
                    assert err is None, f"Server Group deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting Server Group failed: {exc}")

            if segment_group_id:
                try:
                    time.sleep(2)
                    delete_response, _, err = client.zpa.segment_groups.delete_group(group_id=segment_group_id)
                    assert err is None, f"Segment Group deletion failed: {err}"
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as exc:
                    errors.append(f"Deleting Segment Group failed: {exc}")

            if app_connector_group_id:
                try:
                    time.sleep(2)
                    delete_response, _, err = client.zpa.app_connector_groups.delete_connector_group(app_connector_group_id)
                    assert err is None, f"Error deleting group: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for app connector group ID {app_connector_group_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the PRA Approval operations test: {errors}"
