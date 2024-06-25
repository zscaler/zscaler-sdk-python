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

from tests.integration.zia.conftest import MockZIAClient
from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


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
        # Initialize IDs for cleanup
        app_connector_group_id = None
        segment_group_id = None
        server_group_id = None
        app_segment_id = None
        gateway_id = None

        try:
            # Create an App Connector Group
            try:
                app_connector_group_name = "tests-" + generate_random_string()
                app_connector_group_description = "tests-" + generate_random_string()
                created_app_connector_group = zpaClient.connectors.add_connector_group(
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
                created_segment_group = zpaClient.segment_groups.add_group(name=segment_group_name, enabled=True)
                segment_group_id = created_segment_group["id"]
            except Exception as exc:
                errors.append(f"Creating Segment Group failed: {exc}")

            # Create a Server Group
            try:
                server_group_name = "tests-" + generate_random_string()
                server_group_description = "tests-" + generate_random_string()
                created_server_group = zpaClient.server_groups.add_group(
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
                app_segment = zpaClient.app_segments.add_segment(
                    name=app_segment_name,
                    description=app_segment_description,
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
                app_segment_id = app_segment["id"]
            except Exception as exc:
                errors.append(f"Creating Application Segment failed: {exc}")

            try:
                # Create a ZPA Gateway
                gateway_name = "tests-" + generate_random_string()
                created_gateway = ziaClient.zpa_gateway.add_gateway(
                    name=gateway_name,
                    description="Integration test ZPA Gateway",
                    type="ZPA",
                    zpa_server_group={
                        "external_id": server_group_id,
                        "name": server_group_name,
                    },
                )
                gateway_id = created_gateway.get("id", None)
                assert gateway_id is not None, "ZPA Gateway creation failed"
            except Exception as exc:
                errors.append(f"ZPA Gateway creation failed: {exc}")

            try:
                # Verify the gateway by retrieving it
                retrieved_gateway = ziaClient.zpa_gateway.get_gateway(gateway_id)
                assert retrieved_gateway["id"] == gateway_id, "Incorrect gateway retrieved"
            except Exception as exc:
                errors.append(f"Retrieving ZPA Gateway failed: {exc}")

            try:
                # Update the ZPA Gateway
                updated_description = "Updated integration test ZPA Gateway"
                ziaClient.zpa_gateway.update_gateway(
                    gateway_id,
                    description=updated_description,
                )
                updated_gateway = ziaClient.zpa_gateway.get_gateway(gateway_id)
                assert updated_gateway["description"] == updated_description, "ZPA Gateway update failed"
            except Exception as exc:
                errors.append(f"Updating ZPA Gateway failed: {exc}")

            try:
                # Retrieve the list of all gateways
                gateways = ziaClient.zpa_gateway.list_gateways()
                # Check if the newly created gateway is in the list of gateways
                found_gateway = any(gateway["id"] == gateway_id for gateway in gateways)
                assert found_gateway, "Newly created gateway not found in the list of gateways."
            except Exception as exc:
                errors.append(f"Listing gateway failed: {exc}")

        finally:
            cleanup_errors = []
            try:
                # Attempt to delete resources created during the test
                if gateway_id:
                    delete_status = ziaClient.zpa_gateway.delete_gateway(gateway_id)
                    assert delete_status == 204, "ZPA Gateway deletion failed"
            except Exception as exc:
                cleanup_errors.append(f"Deleting ZPA Gateway failed: {exc}")

            # Cleanup resources
            if app_segment_id:
                try:
                    zpaClient.app_segments.delete_segment(segment_id=app_segment_id, force_delete=True)
                except Exception as exc:
                    errors.append(f"Deleting Application Segment failed: {exc}")

            if server_group_id:
                try:
                    zpaClient.server_groups.delete_group(group_id=server_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Server Group failed: {exc}")

            if segment_group_id:
                try:
                    zpaClient.segment_groups.delete_group(group_id=segment_group_id)
                except Exception as exc:
                    errors.append(f"Deleting Segment Group failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert no errors occurred during the entire test process
        assert len(errors) == 0, f"Errors occurred during the zpa gateway lifecycle test: {errors}"
