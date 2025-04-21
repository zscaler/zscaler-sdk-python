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


class TestAppConnectorGroupProvisioningKey:
    """
    Integration Tests for the Provisioning Key API.
    """

    def test_connector_group_provisioning_key(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        connector_group_id = None
        connector_key_id = None
        key_type="connector"
        
        try:
            try:
                # Create an App Connector Group
                connector_group_name = "tests-" + generate_random_string()
                connector_description = "tests-" + generate_random_string()
                created_connector_group, _, err = client.zpa.app_connector_groups.add_connector_group(
                    name=connector_group_name,
                    description=connector_description,
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
                    connector_group_id = created_connector_group.id
                    assert connector_group_id is not None, "App Connector Group creation failed"
            except Exception as exc:
                errors.append(f"App Connector Group creation failed: {exc}")

            try:
                # Retrieve the 'Service Edge' enrollment certificate
                connector_certs, _, err = client.zpa.enrollment_certificates.list_enrolment(query_params={'search': 'Connector'})
                if err:
                    errors.append(f"Retrieving 'connector' enrolment certificate failed: {err}")
                else:
                    assert connector_certs, "Failed to retrieve 'Connector Edge' enrolment certificate"
                    connector_cert = connector_certs[0]
                    connector_cert_id = connector_cert.id
                    assert connector_cert_id, "Enrollment certificate missing 'id'"
            except Exception as exc:
                errors.append(f"Retrieving 'connector' enrolment certificate failed: {exc}")

            try:
                # Create a CONNECTOR_GRP Provisioning Key
                connector_key_name = "tests-" + generate_random_string()
                (created_connector_key, _, err) = client.zpa.provisioning.add_provisioning_key(
                    key_type=key_type,
                    name=connector_key_name,
                    max_usage=2,
                    enrollment_cert_id=connector_cert_id,
                    component_id=connector_group_id
                )
                if err:
                    errors.append(f"CONNECTOR_GRP Provisioning Key creation failed: {err}")
                else:
                    connector_key_id = created_connector_key.id
                    assert connector_key_id is not None, "CONNECTOR_GRP Provisioning Key creation failed"
            except Exception as exc:
                errors.append(f"CONNECTOR_GRP Provisioning Key creation failed: {exc}")

            try:
                # List provisioning keys
                all_connector_keys, _, err = client.zpa.provisioning.list_provisioning_keys(key_type)
                if err:
                    errors.append(f"Listing connector group keys failed: {err}")
                else:
                    # Check that the newly created key is in the list
                    assert any(
                        key.id == connector_key_id for key in all_connector_keys
                    ), "Newly created connector group key not found in list"
            except Exception as exc:
                errors.append(f"Listing connector group keys failed: {exc}")

            try:
                # Retrieve the specific SERVICE_EDGE_GRP Provisioning Key
                retrieved_connector_key, _, err = client.zpa.provisioning.get_provisioning_key(connector_key_id, key_type)
                if err:
                    errors.append(f"Retrieving CONNECTOR_GRP Provisioning Key failed: {err}")
                else:
                    assert retrieved_connector_key.id == connector_key_id, "Failed to retrieve the correct CONNECTOR_GRP Provisioning Key"
            except Exception as exc:
                errors.append(f"Retrieving CONNECTOR_GRP Provisioning Key failed: {exc}")

            try:
                # Update the server group
                updated_name = connector_key_name + " Updated"
                _, _, err = client.zpa.provisioning.update_provisioning_key(connector_key_id, key_type, name=updated_name)
                assert err is None, f"Error updating provisioning key: {err}"
            except Exception as exc:
                errors.append(f"Updating CONNECTOR_GRP Provisioning Key failed: {exc}")


        finally:
            cleanup_errors = []

            # Attempt to delete the SERVICE_EDGE_GRP Provisioning Key
            if connector_key_id:
                try:
                    delete_response, _, err = client.zpa.provisioning.delete_provisioning_key(connector_key_id, key_type)
                    assert err is None, f"Deleting CONNECTOR_GRP Provisioning Key failed: {err}"
                    # For 204 No Content, delete_response should be None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    cleanup_errors.append(f"Cleanup failed for Deleting CONNECTOR_GRP Provisioning Key ID {connector_key_id}: {cleanup_exc}")

            # Attempt to delete the Connector Group
            if connector_group_id:
                try:
                    _, _, err = client.zpa.app_connector_groups.delete_connector_group(connector_group_id)
                    if err:
                        cleanup_errors.append(f"Deleting Connector Group failed: {err}")
                except Exception as exc:
                    cleanup_errors.append(f"Cleanup failed for Deleting Connector Group: {exc}")

            errors.extend(cleanup_errors)

        assert len(errors) == 0, f"Errors occurred during the provisioning key operations test: {errors}"
