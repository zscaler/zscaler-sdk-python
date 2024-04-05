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
from tests.test_utils import generate_random_string

@pytest.fixture
def fs():
    yield

class TestLocationManagement:
    """
    Integration Tests for the ZIA Location Management
    """
    
    @pytest.mark.asyncio
    async def test_location_management_vpn_ufqdn_type(self, fs):
        client = MockZIAClient(fs)
        errors = []
        vpn_id = None
        location_id = None

        try:
            # Create VPN Credential IP Type
            try:
                email = "tests-" + generate_random_string() + "@bd-hashicorp.com"
                created_vpn_credential = client.traffic.add_vpn_credential(
                    authentication_type="UFQDN",
                    pre_shared_key="testkey-" + generate_random_string(),
                    fqdn=email
                )
                vpn_id = created_vpn_credential.get("id", None)
                assert vpn_id is not None, "VPN Credential creation failed"
            except Exception as exc:
                errors.append(f"VPN Credential creation failed: {exc}")

            # Create Location Management
            try:
                location_name = "Integration test location - " + generate_random_string()
                created_location = client.locations.add_location(
                    name=location_name,
                    tz="UNITED_STATES_AMERICA_LOS_ANGELES",
                    auth_required=True,
                    idle_time_in_minutes=720,
                    display_time_unit="HOUR",
                    surrogate_ip=True,
                    xff_forward_enabled=True,
                    ofw_enabled=True,
                    ips_control=True,
                    vpn_credentials=[{'id': vpn_id, 'type': 'UFQDN'}]
                )
                location_id = created_location.get("id", None)
                assert location_id is not None, "Location creation failed"
            except Exception as exc:
                errors.append(f"Location creation failed: {exc}")

            try:
                # Verify the location management by retrieving it
                retrieved_location = client.locations.get_location(location_id)
                assert retrieved_location["id"] == location_id, "Incorrect location retrieved"
            except Exception as exc:
                errors.append(f"Retrieving Location Management failed: {exc}")

            try:
                # Update the Location Management
                updated_description = "Updated integration test location management"
                client.locations.update_location(
                    location_id,
                    description=updated_description,
                )
                updated_location = client.locations.get_location(location_id)
                assert updated_location["description"] == updated_description, "Location Management update failed"
            except Exception as exc:
                errors.append(f"Updating Location Management failed: {exc}")

        finally:
            # Cleanup operations
            cleanup_errors = []
            if location_id:
                try:
                    delete_status_location = client.locations.delete_location(location_id)
                    assert delete_status_location == 204, "Location deletion failed"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting location failed: {exc}")

            if vpn_id:
                try:
                    delete_status_vpn = client.traffic.delete_vpn_credential(vpn_id)
                    assert delete_status_vpn == 204, "VPN Credential deletion failed"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting VPN Credential failed: {exc}")

            errors.extend(cleanup_errors)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the location management lifecycle test: {errors}"