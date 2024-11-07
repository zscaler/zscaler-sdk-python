import pytest

from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestIsolationProfile:
    """
    Integration Tests for the Isolation Profile.
    """

    def test_isolation_profile(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Attempt to list all isolation profiles
        try:
            isolation_profiles = client.isolation.list_profiles()
            assert isinstance(isolation_profiles, list), "Expected a list of isolation profiles"
        except Exception as exc:
            errors.append(f"Listing isolation profiles failed: {str(exc)}")

        # Process each isolation profile if the list is not empty
        if isolation_profiles:
            for first_profile in isolation_profiles:
                profile_id = first_profile.get("id")

                # Fetch the selected isolation profile by its ID
                try:
                    fetched_profile = client.isolation.get_profile_by_id(profile_id)
                    assert fetched_profile is not None, "Expected a valid isolation profile object"
                    assert fetched_profile.get("id") == profile_id, "Mismatch in isolation profile ID"
                except Exception as exc:
                    errors.append(f"Fetching isolation profile by ID failed: {str(exc)}")

                # Attempt to retrieve the isolation profile by name
                try:
                    profile_name = first_profile.get("name")
                    profile_by_name = client.isolation.get_profile_by_name(profile_name)
                    assert profile_by_name is not None, "Expected a valid isolation profile object when searching by name"
                    assert profile_by_name.get("id") == profile_id, "Mismatch in isolation profile ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching isolation profile by name failed: {str(exc)}")

                # Once we've tested one profile, exit the loop to avoid redundant testing
                break

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during isolation profile operations test: {errors}"
