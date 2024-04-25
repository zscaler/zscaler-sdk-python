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
            idps = client.idp.list_idps()
            assert isinstance(idps, list), "Expected a list of identity providers"
            if idps:  # If there are any identity providers, proceed with further operations
                first_idp = idps[0]
                idp_id = first_idp.get("id")
        except Exception as exc:
            errors.append(f"Listing identity providers failed: {str(exc)}")

        if idp_id:
            # Fetch the selected identity provider by its ID
            try:
                fetched_idp = client.idp.get_idp(idp_id)
                assert fetched_idp is not None, "Expected a valid identity provider object"
                assert fetched_idp.get("id") == idp_id, "Mismatch in identity provider ID"
            except Exception as exc:
                errors.append(f"Fetching identity provider by ID failed: {str(exc)}")

            # Attempt to retrieve the identity provider by name
            try:
                idp_name = first_idp.get("name")
                idp_by_name = client.idp.get_idp_by_name(idp_name)
                assert idp_by_name is not None, "Expected a valid identity provider object when searching by name"
                assert idp_by_name.get("id") == idp_id, "Mismatch in identity provider ID when searching by name"
            except Exception as exc:
                errors.append(f"Fetching identity provider by name failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during identity provider operations test: {errors}"
