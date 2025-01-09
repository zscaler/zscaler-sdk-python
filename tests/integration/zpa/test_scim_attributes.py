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


class TestScimAttributes:
    """
    Integration Tests for the SCIM attributes.
    """

    def test_scim_attributes_operations(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        user_idp_id = None
        first_attribute_id = None

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
                # Step 2: List SCIM attributes for the USER IdP
                scim_attributes, _, err = client.zpa.scim_attributes.list_scim_attributes(user_idp_id)
                assert err is None, f"Error listing SCIM attributes: {err}"
                assert isinstance(scim_attributes, list), "Response is not in the expected list format."
                assert len(scim_attributes) > 0, "No SCIM attributes were found for the specified IdP."

                # Get the ID of the first attribute
                first_attribute_id = scim_attributes[0].id  # Assuming scim_attributes is a list of objects
            except Exception as exc:
                errors.append(f"Listing SCIM attributes failed: {exc}")

        if first_attribute_id:
            try:
                # Step 3: Get the SCIM attribute using the retrieved ID
                scim_attribute, _, err = client.zpa.scim_attributes.get_scim_attribute(user_idp_id, first_attribute_id)
                assert err is None, f"Error getting SCIM attribute: {err}"
                assert scim_attribute is not None, "No SCIM attribute found for the specified ID."
                assert scim_attribute.id == first_attribute_id, "Retrieved SCIM attribute ID does not match the requested ID."
            except Exception as exc:
                errors.append(f"Getting a specific SCIM attribute failed: {exc}")

            try:
                # Step 4: Get the values for the SCIM attribute
                attribute_values, _, err = client.zpa.scim_attributes.get_scim_values(user_idp_id, first_attribute_id)
                assert err is None, f"Error getting SCIM attribute values: {err}"
                assert isinstance(attribute_values, list), "Expected a list of values for the SCIM attribute."
                assert len(attribute_values) > 0, "No values returned for the SCIM attribute."
            except Exception as exc:
                errors.append(f"Getting SCIM attribute values failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during SCIM attributes operations test: {errors}"
