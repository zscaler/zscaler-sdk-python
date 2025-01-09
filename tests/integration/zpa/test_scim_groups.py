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


class TestScimGroups:
    """
    Integration Tests for the SCIM Groups
    """

    def test_scim_groups(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        user_idp_id = None
        first_group_id = None

        try:
            # Step 1: List all IDPs and find the one with sso_type = USER
            idps, _, err = client.zpa.idp.list_idps()
            assert err is None, f"Error listing IDPs: {err}"
            user_idp = next((idp for idp in idps if "USER" in idp.sso_type), None)
            assert user_idp is not None, "No IdP with sso_type 'USER' found."

            user_idp_id = user_idp.id
        except Exception as exc:
            errors.append(f"Finding USER IdP failed: {exc}")

        if user_idp_id:
            try:
                # Step 2: List SCIM groups for the USER IdP
                scim_groups, _, err = client.zpa.scim_groups.list_scim_groups(user_idp_id)
                assert err is None, f"Error listing SCIM groups: {err}"
                assert isinstance(scim_groups, list), "Response is not in the expected list format."
                assert len(scim_groups) > 0, "No SCIM groups were found for the specified IdP."

                # Get the ID of the first group
                first_group_id = scim_groups[0].id  # Assuming scim_groups is a list of objects
            except Exception as exc:
                errors.append(f"Listing SCIM groups failed: {exc}")

        if first_group_id:
            try:
                # Step 3: Get the SCIM group using the retrieved ID
                scim_group, _, err = client.zpa.scim_groups.get_scim_group(first_group_id)
                assert err is None, f"Error getting SCIM group: {err}"
                assert scim_group is not None, "No SCIM group found for the specified ID."
                assert scim_group.id == first_group_id, "Retrieved SCIM group ID does not match the requested ID."
            except Exception as exc:
                errors.append(f"Getting a specific SCIM group failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during SCIM groups operations test: {errors}"
