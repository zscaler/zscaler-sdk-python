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

        instance_type = "SHAREPOINTONLINE"

        try:
            # Step 1: List all cloud application instances
            try:
                all_instances, _, error = client.zia.cloud_app_instances.list_cloud_app_instances()
                assert error is None, f"Error listing all cloud app instances: {error}"
                # all_instances can be an empty list, which is valid
            except Exception as exc:
                errors.append(f"Failed to list all cloud app instances: {exc}")

            # Step 2: List cloud application instances with query params - SHAREPOINTONLINE
            try:
                filtered_instances, _, error = client.zia.cloud_app_instances.list_cloud_app_instances(
                    query_params={'instance_type': instance_type}
                )
                assert error is None, f"Error listing cloud app instances with filter: {error}"
            except Exception as exc:
                errors.append(f"Failed to list cloud app instances with filter: {exc}")

            # Step 3: List cloud application instances with different types
            try:
                onedrive_instances, _, error = client.zia.cloud_app_instances.list_cloud_app_instances(
                    query_params={'instance_type': 'ONEDRIVE'}
                )
                assert error is None, f"Error listing ONEDRIVE instances: {error}"
            except Exception as exc:
                errors.append(f"Failed to list ONEDRIVE instances: {exc}")

            # Step 4: List cloud application instances with pagination
            try:
                paginated_instances, _, error = client.zia.cloud_app_instances.list_cloud_app_instances(
                    query_params={'page': 1, 'page_size': 10}
                )
                assert error is None, f"Error listing cloud app instances with pagination: {error}"
            except Exception as exc:
                errors.append(f"Failed to list cloud app instances with pagination: {exc}")

            # Step 5: Get a specific instance by ID (if any instances exist)
            try:
                if all_instances and len(all_instances) > 0:
                    first_instance = all_instances[0]
                    # Try different attribute names for the ID
                    first_instance_id = None
                    for attr in ['id', 'instance_id', 'instanceId']:
                        if hasattr(first_instance, attr):
                            first_instance_id = getattr(first_instance, attr)
                            break
                    if first_instance_id:
                        fetched_instance, _, error = client.zia.cloud_app_instances.get_cloud_app_instances(
                            instance_id=first_instance_id
                        )
                        assert error is None, f"Error retrieving cloud app instance: {error}"
                        assert fetched_instance is not None, "Retrieved cloud app instance is None"
            except Exception as exc:
                errors.append(f"Failed to retrieve cloud app instance: {exc}")

        except Exception as exc:
            errors.append(f"Unexpected error: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
