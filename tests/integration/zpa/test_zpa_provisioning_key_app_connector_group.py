import pytest
from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield

class TestAppConnectorGroupProvisioningKey:
    """
    Integration Tests for the Provisioning Key API
    """

    @pytest.mark.asyncio
    async def test_provisioning_key_operations(self, fs): 
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        connector_group_id = None
        connector_key_id = None
        
        try:
            # Prerequisite: Create an App Connector Group for the CONNECTOR_GRP Provisioning Key
            connector_group_name = "tests-" + generate_random_string()
            connector_group_description = "tests-" + generate_random_string()
            created_connector_group = client.connectors.add_connector_group(
                name=connector_group_name,
                description=connector_group_description,
                enabled=True,
                latitude="37.3382082",
                longitude="-121.8863286",
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
                tcp_quick_ack_read_assistant=True
            )
            connector_group_id = created_connector_group.get('id', None)

            connector_cert = client.certificates.get_enrolment_cert_by_name("Connector")
            connector_key_name = "tests-" + generate_random_string()
            created_connector_key = client.provisioning.add_provisioning_key(
                key_type="connector",
                name=connector_key_name,
                max_usage=2,
                enrollment_cert_id=connector_cert.get('id'),
                component_id=connector_group_id,
            )
            connector_key_id = created_connector_key.get('id', None)
            
            # Test listing provisioning keys
            all_connector_keys = client.provisioning.list_provisioning_keys("connector")
            assert any(key['id'] == connector_key_id for key in all_connector_keys), "Connector key not found in list"

            # Test retrieving the specific CONNECTOR_GRP Provisioning Key
            retrieved_connector_key = client.provisioning.get_provisioning_key(connector_key_id, "connector")
            assert retrieved_connector_key['id'] == connector_key_id, "Failed to retrieve the correct CONNECTOR_GRP Provisioning Key"

            # Update the CONNECTOR_GRP Provisioning Key (Example: changing `max_usage`)
            updated_connector_key = client.provisioning.update_provisioning_key(
                connector_key_id, "connector", max_usage='3')
            assert updated_connector_key['max_usage'] == '3', "Failed to update maxUsage for CONNECTOR_GRP Provisioning Key"
            
            # Cleanup: Delete the CONNECTOR_GRP Provisioning Key
            delete_status_connector = client.provisioning.delete_provisioning_key(connector_key_id, "connector")
            assert delete_status_connector == 204, "Failed to delete CONNECTOR_GRP Provisioning Key"
            connector_key_id = None  # Reset ID after deletion to prevent cleanup attempt

        except Exception as exc:
            errors.append(f"Operations on CONNECTOR_GRP Provisioning Key failed: {exc}")

        # Cleanup
        try:
            if connector_key_id:
                client.provisioning.delete_provisioning_key(connector_key_id, "connector")
            if connector_group_id:
                client.connectors.delete_connector_group(connector_group_id)
        except Exception as exc:
            errors.append(f"Cleanup failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the provisioning key operations test: {errors}"
