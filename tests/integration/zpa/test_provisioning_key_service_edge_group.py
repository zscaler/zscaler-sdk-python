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


class TestServiceEdgeGroupProvisioningKey:
    """
    Integration Tests for the Provisioning Key API
    """

    def test_service_edge_provisioning_key(self, fs):
        client = MockZPAClient(fs)
        errors = []

        svc_edge_group_id = None
        svc_edge_group_key_id = None
        svc_edge_cert_id = None
        key_type="service_edge"
        
        try:
            try:
                # Create a Service Edge Group
                created_svc_edge_group, _, err = client.zpa.service_edge_group.add_service_edge_group(
                    name="tests-" + generate_random_string(),
                    description="tests-" + generate_random_string(),
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
                if err:
                    errors.append(f"Service Edge Group creation failed: {err}")
                else:
                    svc_edge_group_id = created_svc_edge_group.id
                    assert svc_edge_group_id is not None, "Service Edge Group creation failed"
            except Exception as exc:
                errors.append(f"Service Edge Group creation failed: {exc}")

            try:
                # Retrieve the 'Service Edge' enrollment certificate
                svc_edge_certs, _, err = client.zpa.enrollment_certificates.list_enrolment(query_params={'search': 'Service Edge'})
                if err:
                    errors.append(f"Retrieving 'service edge' enrolment certificate failed: {err}")
                else:
                    assert svc_edge_certs, "Failed to retrieve 'Service Edge' enrolment certificate"
                    svc_edge_cert = svc_edge_certs[0]
                    svc_edge_cert_id = svc_edge_cert.id
                    assert svc_edge_cert_id, "Enrollment certificate missing 'id'"
            except Exception as exc:
                errors.append(f"Retrieving 'service edge' enrolment certificate failed: {exc}")

            try:
                # Create a SERVICE_EDGE_GRP Provisioning Key
                connector_key_name = "tests-" + generate_random_string()
                (created_svc_edge_group_key, _, err) = client.zpa.provisioning.add_provisioning_key(
                    key_type=key_type,
                    name=connector_key_name,
                    max_usage=2,
                    enrollment_cert_id=svc_edge_cert_id,
                    component_id=svc_edge_group_id
                )
                if err:
                    errors.append(f"SERVICE_EDGE_GRP Provisioning Key creation failed: {err}")
                else:
                    svc_edge_group_key_id = created_svc_edge_group_key.id
                    assert svc_edge_group_key_id is not None, "SERVICE_EDGE_GRP Provisioning Key creation failed"
            except Exception as exc:
                errors.append(f"SERVICE_EDGE_GRP Provisioning Key creation failed: {exc}")

            try:
                # List provisioning keys
                all_svc_edge_group_keys, _, err = client.zpa.provisioning.list_provisioning_keys(key_type)
                if err:
                    errors.append(f"Listing service edge group keys failed: {err}")
                else:
                    # Check that the newly created key is in the list
                    assert any(
                        key.id == svc_edge_group_key_id for key in all_svc_edge_group_keys
                    ), "Newly created service edge group key not found in list"
            except Exception as exc:
                errors.append(f"Listing service edge group keys failed: {exc}")

            try:
                # Retrieve the specific SERVICE_EDGE_GRP Provisioning Key
                retrieved_connector_key, _, err = client.zpa.provisioning.get_provisioning_key(svc_edge_group_key_id, key_type)
                if err:
                    errors.append(f"Retrieving SERVICE_EDGE_GRP Provisioning Key failed: {err}")
                else:
                    assert retrieved_connector_key.id == svc_edge_group_key_id, "Failed to retrieve the correct SERVICE_EDGE_GRP Provisioning Key"
            except Exception as exc:
                errors.append(f"Retrieving SERVICE_EDGE_GRP Provisioning Key failed: {exc}")

            try:
                # Update the server group
                updated_name = connector_key_name + " Updated"
                _, _, err = client.zpa.provisioning.update_provisioning_key(svc_edge_group_key_id, key_type, name=updated_name)
                assert err is None, f"Error updating server group: {err}"
            except Exception as exc:
                errors.append(f"Updating SERVICE_EDGE_GRP Provisioning Key failed: {exc}")


        finally:
            cleanup_errors = []

            # Attempt to delete the SERVICE_EDGE_GRP Provisioning Key
            if svc_edge_group_key_id:
                try:
                    delete_response, _, err = client.zpa.provisioning.delete_provisioning_key(svc_edge_group_key_id, key_type)
                    assert err is None, f"Deleting SERVICE_EDGE_GRP Provisioning Key failed: {err}"
                    # For 204 No Content, delete_response should be None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    cleanup_errors.append(f"Cleanup failed for Deleting SERVICE_EDGE_GRP Provisioning Key ID {svc_edge_group_key_id}: {cleanup_exc}")

            # Attempt to delete the Service Edge Group
            if svc_edge_group_id:
                try:
                    _, _, err = client.zpa.service_edge_group.delete_service_edge_group(svc_edge_group_id)
                    if err:
                        cleanup_errors.append(f"Deleting Service Edge Group failed: {err}")
                except Exception as exc:
                    cleanup_errors.append(f"Cleanup failed for Deleting Service Edge Group: {exc}")

            errors.extend(cleanup_errors)

        assert len(errors) == 0, f"Errors occurred during the provisioning key operations test: {errors}"
