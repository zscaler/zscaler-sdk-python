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


class TestCloudApplications:
    """
    Integration Tests for the Cloud Applications API.
    """

    @pytest.mark.vcr()
    def test_cloud_applications(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Step 1: List all cloud application policies
        try:
            all_apps, _, error = client.zia.cloud_applications.list_cloud_app_policy()
            assert error is None, f"Error listing all cloud applications: {error}"
            # all_apps can be an empty list, which is valid
            assert all_apps is not None, "Cloud applications list is None"
        except Exception as exc:
            errors.append(f"Failed to list all cloud applications: {exc}")

        # Step 2: List cloud application policies with pagination
        try:
            paginated_apps, _, error = client.zia.cloud_applications.list_cloud_app_policy(
                query_params={'page': 1, 'page_size': 10}
            )
            assert error is None, f"Error listing cloud applications with pagination: {error}"
        except Exception as exc:
            errors.append(f"Failed to list cloud applications with pagination: {exc}")

        # Step 3: List cloud application policies filtered by app_class
        try:
            filtered_apps, _, error = client.zia.cloud_applications.list_cloud_app_policy(
                query_params={'app_class': 'WEB_MAIL'}
            )
            assert error is None, f"Error listing cloud applications by app_class: {error}"
        except Exception as exc:
            errors.append(f"Failed to list cloud applications by app_class: {exc}")

        # Step 4: List cloud application policies with search
        try:
            searched_apps, _, error = client.zia.cloud_applications.list_cloud_app_policy(
                query_params={'search': 'Google'}
            )
            assert error is None, f"Error searching cloud applications: {error}"
        except Exception as exc:
            errors.append(f"Failed to search cloud applications: {exc}")

        # Step 5: List cloud application policies with group_results
        try:
            grouped_apps, _, error = client.zia.cloud_applications.list_cloud_app_policy(
                query_params={'group_results': True}
            )
            assert error is None, f"Error listing cloud applications with group_results: {error}"
        except Exception as exc:
            errors.append(f"Failed to list cloud applications with group_results: {exc}")

        # Step 6: List cloud application SSL policies
        try:
            ssl_apps, _, error = client.zia.cloud_applications.list_cloud_app_ssl_policy()
            assert error is None, f"Error listing cloud applications SSL policy: {error}"
            assert ssl_apps is not None, "Cloud applications SSL policy list is None"
        except Exception as exc:
            errors.append(f"Failed to list cloud applications SSL policy: {exc}")

        # Step 7: List cloud application SSL policies with pagination
        try:
            paginated_ssl_apps, _, error = client.zia.cloud_applications.list_cloud_app_ssl_policy(
                query_params={'page': 1, 'page_size': 10}
            )
            assert error is None, f"Error listing cloud applications SSL policy with pagination: {error}"
        except Exception as exc:
            errors.append(f"Failed to list cloud applications SSL policy with pagination: {exc}")

        # Step 8: List cloud application SSL policies filtered by app_class
        try:
            filtered_ssl_apps, _, error = client.zia.cloud_applications.list_cloud_app_ssl_policy(
                query_params={'app_class': 'WEB_MAIL'}
            )
            assert error is None, f"Error listing cloud applications SSL policy by app_class: {error}"
        except Exception as exc:
            errors.append(f"Failed to list cloud applications SSL policy by app_class: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")

