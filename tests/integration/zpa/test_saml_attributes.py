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


class TestSamlAttributes:
    """
    Integration Tests for the SAML attributes
    """

    def test_saml_attributes_operations(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        user_idp_id = None
        first_attribute_id = None

        try:
            # Test listing all SAML attributes
            saml_attributes, _, err = client.zpa.saml_attributes.list_saml_attributes()
            assert err is None, f"Error listing SAML attributes: {err}"
            assert isinstance(saml_attributes, list), "Response is not in the expected list format."
            assert len(saml_attributes) > 0, "No SAML attributes were found."
        except Exception as exc:
            errors.append(f"Listing all SAML attributes failed: {str(exc)}")

        try:
            # Step 1: List all IDPs and find the one with sso_type = USER
            idps, _, err = client.zpa.idp.list_idps()
            assert err is None, f"Error listing IDPs: {err}"
            user_idp = next((idp for idp in idps if "USER" in idp.sso_type), None)
            assert user_idp is not None, "No IdP with sso_type 'USER' found."

            user_idp_id = user_idp.id
        except Exception as exc:
            errors.append(f"Finding USER IdP failed: {str(exc)}")

        if user_idp_id:
            try:
                # Step 2: List SAML attributes by IDP
                saml_attributes_by_idp, _, err = client.zpa.saml_attributes.list_saml_attributes_by_idp(user_idp_id)
                assert err is None, f"Error listing SAML attributes by IDP: {err}"
                assert isinstance(saml_attributes_by_idp, list), "Response is not in the expected list format for IDP."
                assert len(saml_attributes_by_idp) > 0, "No SAML attributes were found for the specified IdP by ID."

                # Get the ID of the first attribute
                first_attribute_id = saml_attributes_by_idp[0].id  # Assuming it's a list of objects
            except Exception as exc:
                errors.append(f"Listing SAML attributes by IDP failed: {str(exc)}")

        if first_attribute_id:
            try:
                # Step 3: Get a specific SAML attribute using the retrieved ID
                saml_attribute, _, err = client.zpa.saml_attributes.get_saml_attribute(first_attribute_id)
                assert err is None, f"Error getting SAML attribute: {err}"

                # Debugging: Print the type and content of the response to understand the format
                print(f"Response type: {type(saml_attribute)}")
                print(f"Response content: {saml_attribute}")

                # Check if the response is a dict, or handle it appropriately based on its actual format
                assert isinstance(saml_attribute, dict), f"Response is not in the expected dict format, got {type(saml_attribute)}."
                assert saml_attribute["id"] == first_attribute_id, "Retrieved SAML attribute ID does not match the requested ID."
            except Exception as exc:
                errors.append(f"Getting a specific SAML attribute failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during SAML attributes operations test: {errors}"
