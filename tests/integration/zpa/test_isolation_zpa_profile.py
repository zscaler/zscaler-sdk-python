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


@pytest.fixture
def fs():
    yield


class TestZPACBIProfile:
    """
    Integration Tests for the CBI ZPA isolation profile.
    """

    def test_isolation_zpa_profile(self, fs):
        client = MockZPAClient(fs)  # Assuming the client instantiation is taken care of elsewhere
        errors = []  # Initialize an empty list to collect errors
        cbi_profile_id = None

        # List all CBI ZPA profiles
        try:
            profiles_response, _, err = client.zpa.cbi_zpa_profile.list_cbi_zpa_profiles()
            assert err is None, f"Error listing ZPA CBI Profiles: {err}"
            assert isinstance(profiles_response, list), "Expected a list of ZPA CBI Profiles"

            if profiles_response:  # If there are any ZPA CBI Profiles, proceed with further operations
                first_profile = profiles_response[0]
                cbi_profile_id = first_profile.id  # Access the 'id' attribute using dot notation
                assert cbi_profile_id is not None, "Isolation Profile ID should not be None"
        except Exception as exc:
            errors.append(f"Listing ZPA CBI Profile failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during CBI ZPA profile operations test: {errors}"
