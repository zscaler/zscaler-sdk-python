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
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAppSegmentMicrotenants:
    """
    Integration Tests to test Application Segment Move and Share to Microtenants
    """

    def test_app_segment_microtenant_move(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        microtenant_id = None
        app_connector_group_id = None
        segment_group_id = None
        server_group_id = None

        default_app_connector_group_id = None
        default_segment_group_id = None
        default_server_group_id = None
        default_app_segment_id = None

        microtenant_name = "tests-microtenant" + generate_random_string()
        microtenant_description = "tests-microtenant" + generate_random_string()

        # Step 1: Create Microtenant Resource along with a segment_group, app_connector_group, and server_group
        try:
            auth_domains = client.authdomains.get_auth_domains()
            available_domains = auth_domains.auth_domains
            if not available_domains:
                errors.append("No available authentication domains found.")
                assert False, "No available authentication domains found."
        except Exception as exc:
            errors.append(f"Error retrieving authentication domains: {exc}")
            assert False, f"Error retrieving authentication domains: {exc}"

        for domain in available_domains:
            try:
                # Create a new microtenant with the current domain
                created_microtenant = client.microtenants.add_microtenant(
                    name=microtenant_name,
                    description=microtenant_description,
                    enabled=True,
                    privileged_approvals_enabled=True,
                    criteria_attribute="AuthDomain",
                    criteria_attribute_values=[domain],
                )
                assert created_microtenant is not None
                assert created_microtenant.name == microtenant_name
                assert created_microtenant.description == microtenant_description
                assert created_microtenant.enabled is True

                # Extract the microtenant ID
                microtenant_id = created_microtenant.id
                assert microtenant_id is not None, "Failed to retrieve microtenant ID"
                break
            except Exception as exc:
                if "domains.already.exists.in.other.microtenant" in str(exc) or "domains.does.not.belong.to.customer" in str(
                    exc
                ):
                    continue  # Try the next domain
                else:
                    errors.append(exc)
                    break

        if not microtenant_id:
            errors.append("Failed to create microtenant with available domains.")
            assert False, "Failed to create microtenant with available domains."

        try:
            # Create an App Connector Group for the microtenant
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
                microtenant_id=microtenant_id,
            )
            app_connector_group_id = created_app_connector_group["id"]
        except Exception as exc:
            errors.append(f"Creating App Connector Group failed: {exc}")

        try:
            # Create a Server Group for the microtenant
            server_group_name = "tests-" + generate_random_string()
            server_group_description = "tests-" + generate_random_string()
            created_server_group = client.server_groups.add_group(
                name=server_group_name,
                description=server_group_description,
                enabled=True,
                dynamic_discovery=True,
                app_connector_group_ids=[app_connector_group_id],
                microtenant_id=microtenant_id,
            )
            server_group_id = created_server_group["id"]
        except Exception as exc:
            errors.append(f"Creating Server Group failed: {exc}")

        try:
            # Create a Segment Group for the microtenant
            segment_group_name = "tests-" + generate_random_string()
            created_segment_group = client.segment_groups.add_group(
                name=segment_group_name, enabled=True, microtenant_id=microtenant_id
            )
            segment_group_id = created_segment_group["id"]
        except Exception as exc:
            errors.append(f"Creating Segment Group failed: {exc}")

        # Step 2: Create Resources under the default tenant (without microtenant_id)
        try:
            # Create an App Connector Group for the default tenant
            default_app_connector_group_name = "tests-" + generate_random_string()
            default_app_connector_group_description = "tests-" + generate_random_string()
            created_default_app_connector_group = client.connectors.add_connector_group(
                name=default_app_connector_group_name,
                description=default_app_connector_group_description,
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
            default_app_connector_group_id = created_default_app_connector_group["id"]
        except Exception as exc:
            errors.append(f"Creating Default App Connector Group failed: {exc}")

        try:
            # Create a Segment Group for the default tenant
            default_segment_group_name = "tests-" + generate_random_string()
            created_default_segment_group = client.segment_groups.add_group(name=default_segment_group_name, enabled=True)
            default_segment_group_id = created_default_segment_group["id"]
        except Exception as exc:
            errors.append(f"Creating Default Segment Group failed: {exc}")

        try:
            # Create a Server Group for the default tenant
            default_server_group_name = "tests-" + generate_random_string()
            default_server_group_description = "tests-" + generate_random_string()
            created_default_server_group = client.server_groups.add_group(
                name=default_server_group_name,
                description=default_server_group_description,
                enabled=True,
                dynamic_discovery=True,
                app_connector_group_ids=[default_app_connector_group_id],
            )
            default_server_group_id = created_default_server_group["id"]
        except Exception as exc:
            errors.append(f"Creating Default Server Group failed: {exc}")

        try:
            # Create an Application Segment for the default tenant
            default_app_segment_name = "tests-" + generate_random_string()
            default_app_segment_description = "tests-" + generate_random_string()
            default_app_segment = client.app_segments.add_segment(
                name=default_app_segment_name,
                description=default_app_segment_description,
                enabled=True,
                domain_names=["test.example.com"],
                segment_group_id=default_segment_group_id,
                server_group_ids=[default_server_group_id],
                tcp_port_ranges=["8001", "8001"],
            )
            default_app_segment_id = default_app_segment["id"]
        except Exception as exc:
            errors.append(f"Creating Default Application Segment failed: {exc}")

        # Step 4: Move the default application segment to the microtenant created in step 1
        try:
            assert default_app_segment_id is not None, "default_app_segment_id is None"
            assert segment_group_id is not None, "segment_group_id is None"
            assert server_group_id is not None, "server_group_id is None"
            assert microtenant_id is not None, "microtenant_id is None"

            client.app_segments.app_segment_move(
                application_id=default_app_segment_id,
                target_segment_group_id=segment_group_id,
                target_server_group_id=server_group_id,
                target_microtenant_id=microtenant_id,
            )
        except Exception as exc:
            errors.append(f"Moving Application Segment to Microtenant failed: {exc}")

        finally:
            # Cleanup resources
            if microtenant_id:
                try:
                    client.microtenants.delete_microtenant(microtenant_id=microtenant_id)
                except Exception as exc:
                    errors.append(f"Deleting Microtenant failed: {exc}")

            # Delete resources under the default tenant
            try:
                if default_app_segment_id:
                    client.app_segments.delete_segment(default_app_segment_id)
            except Exception as exc:
                errors.append(f"Deleting Default Application Segment failed: {exc}")

            try:
                if default_server_group_id:
                    client.server_groups.delete_group(default_server_group_id)
            except Exception as exc:
                errors.append(f"Deleting Default Server Group failed: {exc}")

            try:
                if default_segment_group_id:
                    client.segment_groups.delete_group(default_segment_group_id)
            except Exception as exc:
                errors.append(f"Deleting Default Segment Group failed: {exc}")

            try:
                if default_app_connector_group_id:
                    client.connectors.delete_connector_group(default_app_connector_group_id)
            except Exception as exc:
                errors.append(f"Deleting Default App Connector Group failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the Application Segment lifecycle test: {errors}"
