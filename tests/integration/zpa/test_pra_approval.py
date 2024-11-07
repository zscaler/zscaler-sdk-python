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
            created_segment_group = client.segment_groups.add_group(
                name=segment_group_name,
                description="tests-" + generate_random_string(),
                enabled=True,
            )
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
                app_connector_group_ids=[app_connector_group_id],  # List of App Connector Group IDs
            )
            server_group_id = created_server_group["id"]
        except Exception as exc:
            errors.append(f"Creating Server Group failed: {exc}")

        # Create an Application Segment
        try:
            app_segment_name = "tests-" + generate_random_string()
            app_segment_description = "tests-" + generate_random_string()
            app_segment = client.app_segments.add_segment(
                name=app_segment_name,
                description=app_segment_description,
                enabled=True,
                domain_names=["test.example.com"],
                segment_group_id=segment_group_id,
                server_group_ids=[server_group_id],
                tcp_port_ranges=["8000", "8000"],
            )
            app_segment_id = app_segment["id"]
        except Exception as exc:
            errors.append(f"Creating Application Segment failed: {exc}")

        try:
            # Create a new privileged approval
            created_approval = client.privileged_remote_access.add_approval(
                email_ids=["carol.kirk@bd-hashicorp.com"],
                application_ids=[app_segment_id],  # Assuming a valid application ID
                start_time=start_time,
                end_time=end_time,
                status="ACTIVE",
                working_hours={
                    "start_time_cron": "0 0 16 ? * SUN,MON,TUE,WED,THU,FRI,SAT",
                    "end_time_cron": "0 0 0 ? * MON,TUE,WED,THU,FRI,SAT,SUN",
                    "start_time": "09:00",
                    "end_time": "17:00",
                    "days": ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
                    "time_zone": "America/Vancouver",
                },
            )
            assert created_approval is not None, "Failed to create approval"
            approval_id = created_approval.id  # Assuming id is accessible like this

        except Exception as exc:
            errors.append(f"Error during approval creation: {exc}")

        try:
            # List all approvals using the search parameter and verify the created approval is in the list
            approval_list = client.privileged_remote_access.list_approval(
                max_items=1,
                search="carol.kirk@bd-hashicorp.com",
                search_field="email_ids",
            )
            assert any(
                approval["email_ids"][0] == "carol.kirk@bd-hashicorp.com" for approval in approval_list
            ), "Created approval not found in the list"
        except Exception as exc:
            errors.append(f"Error listing approvals: {exc}")

        try:
            # Assuming get_approval method returns a Box object
            retrieved_approval = client.privileged_remote_access.get_approval(approval_id)
            assert retrieved_approval.id == approval_id, "Mismatch in retrieved approval ID"

            # Example assertions (modify based on actual returned attributes)
            assert retrieved_approval.status == "ACTIVE", "Approval status mismatch"

        except Exception as exc:
            errors.append(f"Error retrieving approval: {exc}")

        finally:
            cleanup_errors = []

            try:
                # Attempt to delete resources created during the test
                if approval_id:
                    delete_status = client.privileged_remote_access.delete_approval(approval_id)
                    assert delete_status == 204, "Approval deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Approval failed: {exc}")

            try:
                # Attempt to delete resources created during the test
                if app_segment_id:
                    delete_status = client.app_segments.delete_segment(app_segment_id)
                    assert delete_status == 204, "Application Segment deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Application Segment failed: {exc}")

            try:
                if segment_group_id:
                    delete_status = client.segment_groups.delete_group(segment_group_id)
                    assert delete_status == 204, "Segment Group deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Segment Group failed: {exc}")

            try:
                if server_group_id:
                    delete_status = client.server_groups.delete_group(server_group_id)
                    assert delete_status == 204, "Server Group deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting Server Group failed: {exc}")

            try:
                if app_connector_group_id:
                    delete_status = client.connectors.delete_connector_group(app_connector_group_id)
                    assert delete_status == 204, "App Connector Group deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting App Connector Group failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the approval lifecycle test: {errors}"
