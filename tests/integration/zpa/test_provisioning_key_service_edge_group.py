import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestServiceEdgeGroupProvisioningKey:
    """
    Integration Tests for the Provisioning Key API
    """

    def test_provisioning_key_operations(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        svc_edge_group_id = None
        svc_edge_group_key_id = None

        try:
            try:
                # Prerequisite: Create an Service Edge Group for the SERVICE_EDGE_GRP Provisioning Key
                svc_edge_group_name = "tests-" + generate_random_string()
                svc_edge_group_description = "tests-" + generate_random_string()
                created_svc_edge_group = client.service_edges.add_service_edge_group(
                    name=svc_edge_group_name,
                    description=svc_edge_group_description,
                    enabled=True,
                    latitude="37.33874",
                    longitude="-121.8852525",
                    location="San Jose, CA, USA",
                    upgrade_day="SUNDAY",
                    upgrade_time_in_secs="66600",
                    override_version_profile=True,
                    version_profile_name="Default",
                    version_profile_id="0",
                    is_public="TRUE",
                )
                svc_edge_group_id = created_svc_edge_group.get("id", None)
                assert svc_edge_group_id is not None, "Service Edge Group creation failed"
            except Exception as exc:
                errors.append(f"Service Edge Group creation failed: {exc}")

            try:
                # Obtain the "Connector" enrolment certificate ID
                svc_edge_cert = client.certificates.get_enrolment_cert_by_name("Service Edge")
                assert svc_edge_cert, "Failed to retrieve 'Service Edge' enrolment certificate"
            except Exception as exc:
                errors.append(f"Retrieving 'service edge' enrolment certificate failed: {exc}")

            try:
                # Create a SERVICE_EDGE_GRP Provisioning Key
                connector_key_name = "tests-" + generate_random_string()
                created_svc_edge_group_key = client.provisioning.add_provisioning_key(
                    key_type="service_edge",
                    name=connector_key_name,
                    max_usage=2,
                    enrollment_cert_id=svc_edge_cert.get("id"),
                    component_id=svc_edge_group_id,
                )
                svc_edge_group_key_id = created_svc_edge_group_key.get("id", None)
                assert svc_edge_group_key_id is not None, "SERVICE_EDGE_GRP Provisioning Key creation failed"
            except Exception as exc:
                errors.append(f"SERVICE_EDGE_GRP Provisioning Key creation failed: {exc}")

            try:
                # List provisioning keys to verify creation
                all_svc_edge_group_keys = client.provisioning.list_provisioning_keys("service_edge")
                assert any(
                    key["id"] == svc_edge_group_key_id for key in all_svc_edge_group_keys
                ), "Newly created service edge group key not found in list"
            except Exception as exc:
                errors.append(f"Listing service edge group keys failed: {exc}")

            try:
                # Retrieve the specific SERVICE_EDGE_GRP Provisioning Key
                retrieved_connector_key = client.provisioning.get_provisioning_key(svc_edge_group_key_id, "service_edge")
                assert (
                    retrieved_connector_key["id"] == svc_edge_group_key_id
                ), "Failed to retrieve the correct SERVICE_EDGE_GRP Provisioning Key"
            except Exception as exc:
                errors.append(f"Retrieving SERVICE_EDGE_GRP Provisioning Key failed: {exc}")

            try:
                # Update the SERVICE_EDGE_GRP Provisioning Key
                updated_connector_key = client.provisioning.update_provisioning_key(
                    svc_edge_group_key_id, "service_edge", max_usage="3"
                )
                assert updated_connector_key["max_usage"] == "3", "Failed to update SERVICE_EDGE_GRP Provisioning Key"
            except Exception as exc:
                errors.append(f"Updating SERVICE_EDGE_GRP Provisioning Key failed: {exc}")

        finally:
            try:
                # Cleanup: Attempt to delete the SERVICE_EDGE_GRP Provisioning Key
                if svc_edge_group_key_id:
                    delete_status_connector = client.provisioning.delete_provisioning_key(
                        svc_edge_group_key_id, "service_edge"
                    )
                    assert delete_status_connector == 204, "Failed to delete SERVICE_EDGE_GRP Provisioning Key"
            except Exception as cleanup_exc:
                errors.append(f"Deleting SERVICE_EDGE_GRP Provisioning Key failed: {cleanup_exc}")

            try:
                # Cleanup: Attempt to delete the Service Edge Group
                if svc_edge_group_id:
                    client.service_edges.delete_service_edge_group(svc_edge_group_id)
            except Exception as cleanup_exc:
                errors.append(f"Deleting Service Edge Group failed: {cleanup_exc}")

        # Assert no errors occurred during the test execution
        assert len(errors) == 0, f"Errors occurred during the provisioning key operations test: {errors}"
