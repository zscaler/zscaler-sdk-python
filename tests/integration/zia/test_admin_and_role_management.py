import pytest
from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestAdminRole:
    """
    Integration Tests for the admin roles
    """

    @pytest.mark.asyncio
    async def test_admin_role_management(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all roles
            roles = client.admin_and_role_management.list_roles()
            assert isinstance(roles, list), "Expected a list of roles"
            if roles:  # If there are any roles
                # Select the first role for further testing
                first_role = roles[0]
                role_id = first_role.get("id")
                
                # Fetch the selected role by its ID
                try:
                    fetched_role = client.admin_and_role_management.get_role(role_id)
                    assert fetched_role is not None, "Expected a valid role object"
                    assert fetched_role.get("id") == role_id, "Mismatch in role ID"
                except Exception as exc:
                    errors.append(f"Fetching role by ID failed: {exc}")

                # Attempt to retrieve the role by name
                try:
                    role_name = first_role.get("name")
                    role_by_name = client.admin_and_role_management.get_roles_by_name(role_name)
                    assert role_by_name is not None, "Expected a valid role object when searching by name"
                    assert role_by_name.get("id") == role_id, "Mismatch in role ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching role by name failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing roles failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during roles test: {errors}"
