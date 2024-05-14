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

        # Initialize IDs for cleanup
        app_connector_group_id = None
        segment_group_id = None
        server_group_id = None
        app_segment_id = None
        first_cert_id = None

        try:
            # Retrieve the first certificate
            try:
                certs = client.certificates.list_all_certificates()
                assert certs, "Failed to retrieve certificates"
                first_cert_id = certs[0]["id"]
            except Exception as exc:
                errors.append(f"Retrieving certificates failed: {exc}")

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
                app_segment = client.app_segments_inspection.add_segment_inspection(
                    name=app_segment_name,
                    description=app_segment_description,
                    enabled=True,
                    domain_names=["test" + generate_random_string() + ".example.com"],
                    segment_group_id=segment_group_id,
                    server_group_ids=[server_group_id],
                    tcp_port_ranges=["443", "443"],
                    common_apps_dto={
                        "apps_config": [
                            {
                                "name": app_segment_name,
                                "description": app_segment_description,
                                "enabled": True,
                                "app_types": ["INSPECT"],
                                "application_port": "443",
                                "application_protocol": "HTTPS",
                                "certificate_id": first_cert_id,
                                "domain": "server1.bd-redhat.com",
                            }
                        ]
                    },
                )
                app_segment_id = app_segment["id"]
            except Exception as exc:
                errors.append(f"Creating Application Segment failed: {exc}")

            # Test retrieving the specific Application Segment
            try:
                remote_app = client.app_segments_inspection.get_segment_inspection(segment_id=app_segment_id)
                assert remote_app["id"] == app_segment_id
            except Exception as exc:
                errors.append(f"Retrieving Application Segment failed: {exc}")

            # Test listing Application Segments - Filter by the unique name
            try:
                apps = client.app_segments_inspection.list_segment_inspection(search=app_segment_name)
                assert any(app["id"] == app_segment_id for app in apps), "Newly created app segment should be in the list"
            except Exception as exc:
                errors.append(f"Listing Application Segments failed: {exc}")

            # Test updating the Application Segment
            try:
                updated_description = "Updated " + generate_random_string()
                client.app_segments_inspection.update_segment_inspection(
                    segment_id=app_segment_id, description=updated_description
                )
                updated_app = client.app_segments_inspection.get_segment_inspection(segment_id=app_segment_id)
                assert updated_app["description"] == updated_description
            except Exception as exc:
                errors.append(f"Updating Application Segment failed: {exc}")

        finally:
            # Cleanup resources
            cleanup_errors = []
            if app_segment_id:
                try:
                    client.app_segments_inspection.delete_segment_inspection(segment_id=app_segment_id, force_delete=True)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Application Segment failed: {exc}")
            if server_group_id:
                try:
                    client.server_groups.delete_group(group_id=server_group_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Server Group failed: {exc}")
            if segment_group_id:
                try:
                    client.segment_groups.delete_group(group_id=segment_group_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Segment Group failed: {exc}")
            if cleanup_errors:
                errors.extend(cleanup_errors)

            assert len(errors) == 0, f"Errors occurred during the Application Segment lifecycle test: {errors}"
