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

from tests.integration.zia.conftest import MockZIAClient
from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string
import time

@pytest.fixture
def fs():
    yield


class TestForwardingControlZPAGateway:
    """
    Integration Tests for the ZIA Forwarding Control ZPA Gateway
    """

    def test_forwarding_control_zpa_gateway(self, fs):
        ziaClient = MockZIAClient(fs)
        zpaClient = MockZPAClient(fs)

        errors = []
        app_connector_group_id = None
        segment_group_id = None
        server_group_id = None
        app_segment_id = None
        gateway_id = None

        try:
            # Step 1: Create App Connector Group
            try:
                created_app_connector_group, _, error = zpaClient.zpa.app_connector_groups.add_connector_group(
                    name="tests-" + generate_random_string(),
                    description="tests-" + generate_random_string(),
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
                assert error is None, f"App Connector Group creation failed: {error}"
                app_connector_group_id = created_app_connector_group.id
            except Exception as exc:
                errors.append(f"Creating App Connector Group failed: {exc}")

            # Step 2: Create Segment Group
            try:
                created_segment_group, _, error = zpaClient.zpa.segment_groups.add_group(
                    name="tests-" + generate_random_string(),
                    enabled=True
                )
                assert error is None, f"Segment Group creation failed: {error}"
                segment_group_id = created_segment_group.id
            except Exception as exc:
                errors.append(f"Creating Segment Group failed: {exc}")

            # Step 3: Create Server Group
            try:
                created_server_group, _, error = zpaClient.zpa.server_groups.add_group(
                    name="tests-" + generate_random_string(),
                    description="tests-" + generate_random_string(),
                    enabled=True,
                    dynamic_discovery=True,
                    app_connector_group_ids=[app_connector_group_id],
                )
                assert error is None, f"Server Group creation failed: {error}"
                server_group_id = created_server_group.id
                server_group_name = created_server_group.as_dict().get("name")
            except Exception as exc:
                errors.append(f"Creating Server Group failed: {exc}")

            # Step 4: Create Application Segment
            try:
                app_segment, _, error = zpaClient.zpa.application_segment.add_segment(
                    name="tests-" + generate_random_string(),
                    description="tests-" + generate_random_string(),
                    enabled=True,
                    ip_anchored=True,
                    is_cname_enabled=True,
                    tcp_keep_alive="1",
                    icmp_access_type="PING_TRACEROUTING",
                    health_reporting="ON_ACCESS",
                    domain_names=["test.example.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["8001", "8001"],
                )
                assert error is None, f"Application Segment creation failed: {error}"
                app_segment_id = app_segment.id
                app_segment_name = app_segment.as_dict().get("name")
            except Exception as exc:
                errors.append(f"Creating Application Segment failed: {exc}")

            # Step 5: Create ZPA Gateway
            try:
                created_gateway, _, error = ziaClient.zia.zpa_gateway.add_gateway(
                    name="tests-" + generate_random_string(),
                    description="Integration test ZPA Gateway",
                    type="ZPA",
                    zpa_server_group={
                        "external_id": server_group_id,
                        "name": server_group_name,
                    },
                    zpa_app_segments=[{
                        "external_id": app_segment_id,
                        "name": app_segment_name,
                    }],
                )
                assert error is None, f"ZPA Gateway creation failed: {error}"
                gateway_id = created_gateway.id
            except Exception as exc:
                errors.append(f"ZPA Gateway creation failed: {exc}")

            # Step 6: Retrieve ZPA Gateway
            try:
                retrieved_gateway, _, error = ziaClient.zia.zpa_gateway.get_gateway(gateway_id)
                assert error is None, f"Error retrieving gateway: {error}"
                assert retrieved_gateway.id == gateway_id, "Incorrect gateway retrieved"
            except Exception as exc:
                errors.append(f"Retrieving ZPA Gateway failed: {exc}")

            # Step 7: Update ZPA Gateway
            time.sleep(2)
            try:
                updated_description = "Updated integration test ZPA Gateway"
                updated_name = "updated-" + generate_random_string()
                updated_gateway, _, error = ziaClient.zia.zpa_gateway.update_gateway(
                    gateway_id=gateway_id,
                    name=updated_name,
                    description=updated_description,
                    type="ZPA",
                    zpa_server_group={
                        "external_id": server_group_id,
                        "name": server_group_name,
                    },
                    zpa_app_segments=[{
                        "external_id": app_segment_id,
                        "name": app_segment_name,
                    }],
                )
                assert error is None, f"Error updating gateway: {error}"
                assert updated_gateway.description == updated_description, "ZPA Gateway update failed"
            except Exception as exc:
                errors.append(f"Updating ZPA Gateway failed: {exc}")

            # Step 8: List and verify gateway
            time.sleep(2)
            try:
                gateways, _, error = ziaClient.zia.zpa_gateway.list_gateways()
                assert error is None, f"Error listing gateways: {error}"
                found_gateway = any(g.id == gateway_id for g in gateways)
                assert found_gateway, "Newly created gateway not found in the list"
            except Exception as exc:
                errors.append(f"Listing gateway failed: {exc}")
            time.sleep(2)
            
        finally:
            cleanup_errors = []
            try:
                if gateway_id:
                    _, _, error = ziaClient.zia.zpa_gateway.delete_gateway(gateway_id)
                    assert error is None, f"ZPA Gateway deletion failed: {error}"
            except Exception as exc:
                cleanup_errors.append(f"Deleting ZPA Gateway failed: {exc}")

            if app_segment_id:
                try:
                    _, _, error = zpaClient.zpa.application_segment.delete_segment(segment_id=app_segment_id, force_delete=True)
                    assert error is None, f"Application Segment deletion failed: {error}"
                except Exception as exc:
                    errors.append(f"Deleting Application Segment failed: {exc}")

            if server_group_id:
                try:
                    _, _, error = zpaClient.zpa.server_groups.delete_group(group_id=server_group_id)
                    assert error is None, f"Server Group deletion failed: {error}"
                except Exception as exc:
                    errors.append(f"Deleting Server Group failed: {exc}")

            if segment_group_id:
                try:
                    _, _, error = zpaClient.zpa.segment_groups.delete_group(group_id=segment_group_id)
                    assert error is None, f"Segment Group deletion failed: {error}"
                except Exception as exc:
                    errors.append(f"Deleting Segment Group failed: {exc}")

            errors.extend(cleanup_errors)

        assert len(errors) == 0, f"Errors occurred during the ZPA Gateway lifecycle test:\n{chr(10).join(errors)}"
