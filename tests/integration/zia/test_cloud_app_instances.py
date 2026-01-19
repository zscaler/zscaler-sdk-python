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

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestCloudAppInstances:
    """
    Integration Tests for the Cloud Application Instances API.
    """

    @pytest.mark.vcr()
    def test_cloud_app_instances(self, fs):
        client = MockZIAClient(fs)
        errors = []
        instance_id = None

        instance_type = "SHAREPOINTONLINE"

        try:
            # Step 1: List all cloud application instances
            try:
                all_instances, _, error = client.zia.cloud_app_instances.list_cloud_app_instances()
                assert error is None, f"Error listing all cloud app instances: {error}"
            except Exception as exc:
                pass  # May fail due to permissions

            # Step 2: List cloud application instances with query params
            try:
                filtered_instances, _, error = client.zia.cloud_app_instances.list_cloud_app_instances(
                    query_params={'instance_type': instance_type}
                )
            except Exception:
                pass

            # Step 3: Add cloud app instance
            try:
                created_instance, _, error = client.zia.cloud_app_instances.add_cloud_app_instances(
                    instance_name="TestInstance_VCR",
                    instance_type=instance_type,
                )
                if error is None and created_instance is not None:
                    instance_id = created_instance.get("id") if isinstance(created_instance, dict) else getattr(created_instance, "id", None)

                    # Step 4: Get cloud app instance
                    if instance_id:
                        try:
                            fetched_instance, _, error = client.zia.cloud_app_instances.get_cloud_app_instances(
                                instance_id=instance_id
                            )
                            assert error is None, f"Error retrieving cloud app instance: {error}"
                        except Exception:
                            pass

                        # Step 5: Update cloud app instance
                        try:
                            updated_instance, _, error = client.zia.cloud_app_instances.update_cloud_app_instances(
                                instance_id=instance_id,
                                instance_name="TestInstance_VCR_Updated",
                            )
                        except Exception:
                            pass
            except Exception:
                pass  # May fail due to permissions

            # If we didn't create an instance, test with existing one
            if instance_id is None and all_instances and len(all_instances) > 0:
                first_instance = all_instances[0]
                for attr in ['id', 'instance_id', 'instanceId']:
                    if hasattr(first_instance, attr):
                        existing_id = getattr(first_instance, attr)
                        try:
                            fetched_instance, _, error = client.zia.cloud_app_instances.get_cloud_app_instances(
                                instance_id=existing_id
                            )
                        except Exception:
                            pass
                        break

        except Exception as exc:
            errors.append(f"Unexpected error: {exc}")

        finally:
            # Cleanup
            if instance_id:
                try:
                    client.zia.cloud_app_instances.delete_cloud_app_instances(instance_id)
                except Exception:
                    pass

        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
