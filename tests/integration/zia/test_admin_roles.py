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


class TestAdminRole:
    """
    Integration Tests for the admin roles
    """

    def test_admin_role_management(self, fs):
        client = MockZIAClient(fs)
        errors = []  # List to collect errors

        try:
            roles, response, error = client.zia.admin_roles.list_roles()
            assert error is None, f"Error fetching roles: {error}"
            assert isinstance(roles, list), "Roles response is not a list"
            assert len(roles) > 0, "No roles returned from the API"
        except Exception as exc:
            errors.append(f"Listing all roles failed: {exc}")

        # Extract the name of the first role for search test
        first_role_name = roles[0].name if roles else None

        # Test searching for a specific role by name
        if first_role_name:
            try:
                search_query = {"search": first_role_name}
                filtered_roles, response, error = client.zia.admin_roles.list_roles(query_params=search_query)

                assert error is None, f"Error searching for role '{first_role_name}': {error}"
                assert isinstance(filtered_roles, list), "Filtered roles response is not a list"
                assert any(role.name == first_role_name for role in filtered_roles), (
                    f"Search for role '{first_role_name}' did not return expected results"
                )
            except Exception as exc:
                errors.append(f"Search test failed for role '{first_role_name}': {exc}")

        # Test include_auditor_role parameter
        try:
            roles_with_auditor, response, error = client.zia.admin_roles.list_roles(
                query_params={"include_auditor_role": True}
            )
            assert error is None, f"Error fetching roles with auditor role: {error}"
            assert isinstance(roles_with_auditor, list), "Roles with auditor role response is not a list"
        except Exception as exc:
            errors.append(f"Fetching roles with auditor role failed: {exc}")

        # Test include_partner_role parameter
        try:
            roles_with_partner, response, error = client.zia.admin_roles.list_roles(
                query_params={"include_partner_role": True}
            )
            assert error is None, f"Error fetching roles with partner role: {error}"
            assert isinstance(roles_with_partner, list), "Roles with partner role response is not a list"
        except Exception as exc:
            errors.append(f"Fetching roles with partner role failed: {exc}")

        # Test include_api_role parameter
        try:
            roles_with_api, response, error = client.zia.admin_roles.list_roles(
                query_params={"include_api_role": True}
            )
            assert error is None, f"Error fetching roles with API role: {error}"
            assert isinstance(roles_with_api, list), "Roles with API role response is not a list"
        except Exception as exc:
            errors.append(f"Fetching roles with API role failed: {exc}")

        # Final assertion: If any test failed, report errors
        assert not errors, f"Errors occurred during admin roles test: {errors}"
