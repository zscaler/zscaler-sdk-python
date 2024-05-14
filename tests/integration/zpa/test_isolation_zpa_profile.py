# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
            profiles = client.isolation.list_zpa_profiles()
            assert isinstance(profiles, list) and profiles, "Expected a non-empty list of CBI ZPA profiles"
            first_profile = profiles[0]
            cbi_profile_id = first_profile.get("cbi_profile_id")
            assert cbi_profile_id is not None, "No CBI profile ID found in the first profile"
        except AssertionError as exc:
            errors.append(f"Assertion error: {str(exc)}")
        except Exception as exc:
            errors.append(f"Listing CBI ZPA profiles failed: {str(exc)}")

        # Fetch the selected CBI ZPA profile by its ID
        if cbi_profile_id:
            try:
                fetched_profile = client.isolation.get_zpa_profile(cbi_profile_id)
                assert fetched_profile is not None, "Expected a valid CBI ZPA profile object"
                assert fetched_profile.get("cbi_profile_id") == cbi_profile_id, "Mismatch in CBI ZPA profile ID"
            except AssertionError as exc:
                errors.append(f"Assertion error: {str(exc)}")
            except Exception as exc:
                errors.append(f"Fetching CBI ZPA profile by ID failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during CBI ZPA profile operations test: {errors}"
