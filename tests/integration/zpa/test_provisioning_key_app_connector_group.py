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

    def test_provisioning_key_operations(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        connector_group_id = None
        connector_key_id = None

        try:
            try:
                # Create an App Connector Group
                connector_group_name = "tests-" + generate_random_string()
                connector_description = "tests-" + generate_random_string()
                created_connector_group = client.connectors.add_connector_group(
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
                connector_group_id = created_connector_group.get("id", None)
                assert connector_group_id is not None, "App Connector Group creation failed"
            except Exception as exc:
                errors.append(f"App Connector Group creation failed: {exc}")

            try:
                # Obtain the "Connector" enrolment certificate ID
                connector_cert = client.certificates.get_enrolment_cert_by_name("Connector")
                assert connector_cert, "Failed to retrieve 'Connector' enrolment certificate"
            except Exception as exc:
                errors.append(f"Retrieving 'Connector' enrolment certificate failed: {exc}")

            try:
                # Create a CONNECTOR_GRP Provisioning Key
                connector_key_name = "tests-" + generate_random_string()
                created_connector_key = client.provisioning.add_provisioning_key(
                    key_type="connector",
                    name=connector_key_name,
                    max_usage=2,
                    enrollment_cert_id=connector_cert.get("id"),
                    component_id=connector_group_id,
                )
                connector_key_id = created_connector_key.get("id", None)
                assert connector_key_id is not None, "CONNECTOR_GRP Provisioning Key creation failed"
            except Exception as exc:
                errors.append(f"CONNECTOR_GRP Provisioning Key creation failed: {exc}")

            try:
                # List provisioning keys to verify creation
                all_connector_keys = client.provisioning.list_provisioning_keys("connector")
                assert any(
                    key["id"] == connector_key_id for key in all_connector_keys
                ), "Newly created connector key not found in list"
            except Exception as exc:
                errors.append(f"Listing connector keys failed: {exc}")

            try:
                # Retrieve the specific CONNECTOR_GRP Provisioning Key
                retrieved_connector_key = client.provisioning.get_provisioning_key(connector_key_id, "connector")
                assert (
                    retrieved_connector_key["id"] == connector_key_id
                ), "Failed to retrieve the correct CONNECTOR_GRP Provisioning Key"
            except Exception as exc:
                errors.append(f"Retrieving CONNECTOR_GRP Provisioning Key failed: {exc}")

            try:
                # Update the CONNECTOR_GRP Provisioning Key
                updated_connector_key = client.provisioning.update_provisioning_key(
                    connector_key_id, "connector", max_usage="3"
                )
                assert updated_connector_key["max_usage"] == "3", "Failed to update CONNECTOR_GRP Provisioning Key"
            except Exception as exc:
                errors.append(f"Updating CONNECTOR_GRP Provisioning Key failed: {exc}")

        finally:
            try:
                # Cleanup: Attempt to delete the CONNECTOR_GRP Provisioning Key
                if connector_key_id:
                    delete_status_connector = client.provisioning.delete_provisioning_key(connector_key_id, "connector")
                    assert delete_status_connector == 204, "Failed to delete CONNECTOR_GRP Provisioning Key"
            except Exception as cleanup_exc:
                errors.append(f"Deleting CONNECTOR_GRP Provisioning Key failed: {cleanup_exc}")

            try:
                # Cleanup: Attempt to delete the App Connector Group
                if connector_group_id:
                    client.connectors.delete_connector_group(connector_group_id)
            except Exception as cleanup_exc:
                errors.append(f"Deleting App Connector Group failed: {cleanup_exc}")

        # Assert no errors occurred during the test execution
        assert len(errors) == 0, f"Errors occurred during the provisioning key operations test: {errors}"
