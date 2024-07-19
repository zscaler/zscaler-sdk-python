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

    def test_location_management_vpn_ufqdn_type(self, fs):
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
                    fqdn=email,
                )
                vpn_id = created_vpn_credential.get("id", None)
                assert vpn_id is not None, "VPN Credential creation failed"
            except Exception as exc:
                errors.append(f"VPN Credential creation failed: {exc}")

            # Create Location Management
            try:
                location_name = "tests-" + generate_random_string()
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
                    vpn_credentials=[{"id": vpn_id, "type": "UFQDN"}],
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

            try:
                # Retrieve the list of all locations
                locations = client.locations.list_locations()
                # Check if the newly created location is in the list of locations
                found_location = any(location["id"] == location_id for location in locations)
                assert found_location, "Newly created location not found in the list of locations."
            except Exception as exc:
                errors.append(f"Listing locations failed: {exc}")

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

    def test_sub_location(self, fs):
        client = MockZIAClient(fs)
        errors = []
        parent_location_id = None
        sub_location_id = None

        try:
            # Create VPN Credential IP Type
            try:
                email = "tests-" + generate_random_string() + "@bd-hashicorp.com"
                created_vpn_credential = client.traffic.add_vpn_credential(
                    authentication_type="UFQDN",
                    pre_shared_key="testkey-" + generate_random_string(),
                    fqdn=email,
                )
                vpn_id = created_vpn_credential.get("id", None)
                assert vpn_id is not None, "VPN Credential creation failed"
            except Exception as exc:
                errors.append(f"VPN Credential creation failed: {exc}")

            # Create Location Management (Parent Location)
            try:
                parent_location_name = "tests - " + generate_random_string()
                created_location = client.locations.add_location(
                    name=parent_location_name,
                    tz="UNITED_STATES_AMERICA_LOS_ANGELES",
                    auth_required=True,
                    idle_time_in_minutes=720,
                    display_time_unit="HOUR",
                    surrogate_ip=True,
                    xff_forward_enabled=True,
                    ofw_enabled=True,
                    ips_control=True,
                    vpn_credentials=[{"id": vpn_id, "type": "UFQDN"}],
                )
                parent_location_id = created_location.get("id", None)
                assert parent_location_id is not None, "Parent Location creation failed"
            except Exception as exc:
                errors.append(f"Parent Location creation failed: {exc}")

            # Create Sublocation Management
            try:
                sublocation_name = "tests - " + generate_random_string()
                created_sublocation = client.locations.add_location(
                    name=sublocation_name,
                    description=sublocation_name,
                    country="UNITED_STATES",
                    tz="UNITED_STATES_AMERICA_LOS_ANGELES",
                    profile="CORPORATE",
                    parent_id=parent_location_id,  # Passing the ID of the parent location
                    auth_required=True,
                    idle_time_in_minutes=720,
                    display_time_unit="HOUR",
                    surrogate_ip=True,
                    xff_forward_enabled=True,
                    ofw_enabled=True,
                    ips_control=True,
                    ip_addresses=["10.5.0.0-10.5.255.255"],
                    up_bandwidth=10000,
                    dn_bandwidth=10000,
                )
                sub_location_id = created_sublocation.get("id", None)
                assert sub_location_id is not None, "Sublocation creation failed"
            except Exception as exc:
                errors.append(f"Sublocation creation failed: {exc}")

            try:
                # Verify the sublocation management by retrieving it
                retrieved_sublocation = client.locations.get_location(sub_location_id)
                assert retrieved_sublocation["id"] == sub_location_id, "Incorrect SubLocation retrieved"
            except Exception as exc:
                errors.append(f"Retrieving SubLocation Management failed: {exc}")

            try:
                # Update the Location Management
                updated_description = "Updated integration test SubLocation management"
                client.locations.update_location(
                    sub_location_id,
                    description=updated_description,
                )
                updated_sublocation = client.locations.get_location(sub_location_id)
                assert updated_sublocation["description"] == updated_description, "SubLocation Management update failed"
            except Exception as exc:
                errors.append(f"Updating SubLocation Management failed: {exc}")

            # Additional try-except block to test list_sub_locations
            try:
                # Retrieve the list of sub-locations for the parent location
                sub_locations = client.locations.list_sub_locations(parent_location_id)
                # Check if the newly created sub-location is in the list of sub-locations
                found_sub_location = any(sub_location["id"] == sub_location_id for sub_location in sub_locations)
                assert found_sub_location, "Newly created sub-location not found in the list of sub-locations."
            except Exception as exc:
                errors.append(f"Listing sub-locations failed: {exc}")

        finally:
            # Cleanup operations
            cleanup_errors = []

            # First, attempt to delete the sublocation if it was created
            if sub_location_id:
                try:
                    delete_status_sublocation = client.locations.delete_location(sub_location_id)
                    assert delete_status_sublocation == 204, "SubLocation deletion failed"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting SubLocation failed: {exc}")

            # Next, attempt to delete the parent location if it was created
            if parent_location_id:
                try:
                    delete_status_parent_location = client.locations.delete_location(parent_location_id)
                    assert delete_status_parent_location == 204, "Parent Location deletion failed"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Parent Location failed: {exc}")

            errors.extend(cleanup_errors)

            # Assert that no errors occurred during the test
            assert len(errors) == 0, f"Errors occurred during the sublocation management lifecycle test: {errors}"

    def test_bulk_delete_location_management(self, fs):
        client = MockZIAClient(fs)
        errors = []
        vpn_ids = []
        location_ids = []

        try:
            # Create 3 VPN Credentials
            for _ in range(3):
                try:
                    email = "tests-" + generate_random_string() + "@bd-hashicorp.com"
                    created_vpn_credential = client.traffic.add_vpn_credential(
                        authentication_type="UFQDN",
                        pre_shared_key="testkey-" + generate_random_string(),
                        fqdn=email,
                    )
                    vpn_id = created_vpn_credential.get("id", None)
                    assert vpn_id is not None, "VPN Credential creation failed"
                    vpn_ids.append(vpn_id)
                except Exception as exc:
                    errors.append(f"VPN Credential creation failed: {exc}")

            # Create 3 Locations and associate each with a VPN Credential
            for vpn_id in vpn_ids:
                try:
                    location_name = "tests - " + generate_random_string()
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
                        vpn_credentials=[{"id": vpn_id, "type": "UFQDN"}],
                    )
                    location_id = created_location.get("id", None)
                    assert location_id is not None, "Location creation failed"
                    location_ids.append(location_id)
                except Exception as exc:
                    errors.append(f"Location creation failed: {exc}")

            # Bulk delete the created locations
            try:
                status_code = client.locations.bulk_delete_locations(location_ids)
                assert status_code == 204, f"Bulk deletion failed with status code {status_code}"
            except Exception as exc:
                errors.append(f"Bulk deletion of locations failed: {exc}")

        except Exception as exc:
            errors.append(f"Test setup failed: {exc}")

        finally:
            # Cleanup operations
            cleanup_errors = []
            if vpn_ids:
                try:
                    delete_status_vpn = client.traffic.bulk_delete_vpn_credentials(vpn_ids)
                    assert delete_status_vpn == 204, "VPN Credential deletion failed"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting VPN Credential failed: {exc}")

            errors.extend(cleanup_errors)

            # Assert that no errors occurred during the test
            assert len(errors) == 0, f"Errors occurred during location management test: {errors}"

    def test_list_cities_by_name(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            cities_list = client.locations.list_cities_by_name(prefix="San Jose")
            assert isinstance(cities_list, list), "Expected cities list not received"
        except Exception as exc:
            errors.append(f"Listing cities by name failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during test_list_cities_by_name: {errors}"

    def test_get_geo_by_ip(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            # Attempt to retrieve geographical data by IP
            geo_data = client.locations.get_geo_by_ip(ip="8.8.8.8")
            assert geo_data is not None, "Expected geographical data not received"

            assert "city_name" in geo_data, "City name information is missing in geographical data"
            assert "state_name" in geo_data, "State name information is missing in geographical data"
            assert "country_name" in geo_data, "Country name information is missing in geographical data"

        except Exception as exc:
            errors.append(f"Retrieving geo data by IP failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during test_get_geo_by_ip: {errors}"

    def test_list_region_geo_coordinates(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            region_data = client.locations.list_region_geo_coordinates(latitude=37.3860517, longitude=-122.0838511)
            assert region_data is not None, "Expected region geographical data not received"

            assert "city_name" in region_data, "City name information is missing in region geographical data"
            assert "state_name" in region_data, "State name information is missing in region geographical data"
            assert "country_name" in region_data, "Country name information is missing in region geographical data"

        except Exception as exc:
            errors.append(f"Listing region geo coordinates failed: {exc}")
        assert len(errors) == 0, f"Errors occurred during test_list_region_geo_coordinates: {errors}"
