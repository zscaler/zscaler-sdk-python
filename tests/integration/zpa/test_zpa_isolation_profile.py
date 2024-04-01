import pytest
from tests.integration.zpa.conftest import MockZPAClient

@pytest.fixture
def fs():
    yield

class TestIsolationProfile:
    """
    Integration Tests for the Isolation Profile
    """
    
    @pytest.mark.asyncio
    async def test_isolation_profile(self, fs): 
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all isolation profiles
            isolation_profiles = client.isolation_profile.list_profiles()
            assert isinstance(isolation_profiles, list), "Expected a list of isolation profiles"
            if isolation_profiles:  # If there are any isolation profiles
                # Select the first isolation profile for further testing
                first_profile = isolation_profiles[0]
                profile_id = first_profile.get('id')
                
                # Fetch the selected isolation profile by its ID
                fetched_profile = client.isolation_profile.get_profile_by_id(profile_id)
                assert fetched_profile is not None, "Expected a valid isolation profile object"
                assert fetched_profile.get('id') == profile_id, "Mismatch in isolation profile ID"

                # Attempt to retrieve the isolation profile by name
                profile_name = first_profile.get('name')
                profile_by_name = client.isolation_profile.get_profile_by_name(profile_name)
                assert profile_by_name is not None, "Expected a valid isolation profile object when searching by name"
                assert profile_by_name.get('id') == profile_id, "Mismatch in isolation profile ID when searching by name"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during isolation profiles test: {errors}"
