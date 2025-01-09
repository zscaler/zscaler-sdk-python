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


class TestIdP:
    """
    Integration Tests for the identity provider.
    """

    def test_idp(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        idp_id = None

        # List all identity providers
        try:
            idps_response, _, err = client.zpa.idp.list_idps()  # Correctly unpack the tuple
            assert err is None, f"Error listing identity providers: {err}"
            assert isinstance(idps_response, list), "Expected a list of identity providers"
            if idps_response:  # If there are any identity providers, proceed with further operations
                first_idp = idps_response[0]
                idp_id = first_idp.id  # Access the 'id' attribute using dot notation
                assert idp_id is not None, "IDP ID should not be None"
        except Exception as exc:
            errors.append(f"Listing identity providers failed: {str(exc)}")
            
        if idp_id:
            # Fetch the selected identity provider by its ID
            try:
                fetched_idp, _, err = client.zpa.idp.get_idp(idp_id)
                assert err is None, f"Error fetching identity provider by ID: {err}"
                assert fetched_idp is not None, "Expected a valid identity provider object"
                assert fetched_idp.id == idp_id, "Mismatch in identity provider ID"  # Use dot notation for object access
            except Exception as exc:
                errors.append(f"Fetching identity provider by ID failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during identity provider operations test: {errors}"
