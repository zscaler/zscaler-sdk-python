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

    @pytest.mark.asyncio
    async def test_provisioning_key_operations(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        group_id = None
        svc_edge_group_key_id = None

        try:
            # Prerequisite: Create an Service Edge Group for the SERVICE_EDGE_GRP Provisioning Key
            svc_edge_group_name = "tests-" + generate_random_string()
            svc_edge_group_description = "tests-" + generate_random_string()
            created_svc_edge_group = client.service_edges.add_service_edge_group(
                name=svc_edge_group_name,
                description=svc_edge_group_description,
                enabled=True,
                latitude="37.3382082",
                longitude="-121.8863286",
                location="San Jose, CA, USA",
                upgrade_day="SUNDAY",
                upgrade_time_in_secs="66600",
                override_version_profile=True,
                version_profile_name="Default",
                version_profile_id="0",
                is_public="TRUE",
            )
            group_id = created_svc_edge_group.get("id", None)

            svc_edge_group_cert = client.certificates.get_enrolment_cert_by_name(
                "Service Edge"
            )
            svc_edge_group_key_name = "tests-" + generate_random_string()
            svc_edge_group_key = client.provisioning.add_provisioning_key(
                key_type="service_edge",
                name=svc_edge_group_key_name,
                max_usage=2,
                enrollment_cert_id=svc_edge_group_cert.get("id"),
                component_id=group_id,
            )
            svc_edge_group_key_id = svc_edge_group_key.get("id", None)

            # Test listing provisioning keys
            all_svc_edge_group_keys = client.provisioning.list_provisioning_keys(
                "service_edge"
            )
            assert any(
                key["id"] == svc_edge_group_key_id for key in all_svc_edge_group_keys
            ), "Service Edge Group key not found in list"

            # Test retrieving the specific SERVICE_EDGE_GRP Provisioning Key
            retrieved_svc_edge_group_key = client.provisioning.get_provisioning_key(
                svc_edge_group_key_id, "service_edge"
            )
            assert (
                retrieved_svc_edge_group_key["id"] == svc_edge_group_key_id
            ), "Failed to retrieve the correct SERVICE_EDGE_GRP Provisioning Key"

            # Update the SERVICE_EDGE_GRP Provisioning Key (Example: changing `max_usage`)
            updated_svc_edge_key = client.provisioning.update_provisioning_key(
                svc_edge_group_key_id, "service_edge", max_usage="3"
            )
            assert (
                updated_svc_edge_key["max_usage"] == "3"
            ), "Failed to update maxUsage for SERVICE_EDGE_GRP Provisioning Key"

            # Cleanup: Delete the SERVICE_EDGE_GRP Provisioning Key
            delete_status_svc_edge = client.provisioning.delete_provisioning_key(
                svc_edge_group_key_id, "service_edge"
            )
            assert (
                delete_status_svc_edge == 204
            ), "Failed to delete SERVICE_EDGE_GRP Provisioning Key"
            svc_edge_group_key_id = (
                None  # Reset ID after deletion to prevent cleanup attempt
            )

        except Exception as exc:
            errors.append(
                f"Operations on SERVICE_EDGE_GRP Provisioning Key failed: {exc}"
            )

        # Cleanup
        try:
            if svc_edge_group_key_id:
                client.provisioning.delete_provisioning_key(
                    svc_edge_group_key_id, "service_edge"
                )
            if group_id:
                client.service_edges.delete_service_edge_group(group_id)
        except Exception as exc:
            errors.append(f"Cleanup failed: {exc}")

        assert (
            len(errors) == 0
        ), f"Errors occurred during the provisioning key operations test: {errors}"
