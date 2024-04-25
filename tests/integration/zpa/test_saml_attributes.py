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


class TestSamlAttributes:
    """
    Integration Tests for the SAML attributes
    """

    def test_saml_attributes_operations(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # Test listing all SAML attributes
            resp = client.saml_attributes.list_attributes()
            assert isinstance(resp, list), "Response is not in the expected list format."
            assert len(resp) > 0, "No SAML attributes were found."
        except Exception as exc:
            errors.append(f"Listing all SAML attributes failed: {exc}")

        try:
            # Test listing SAML attributes by IDP
            idps = client.idp.list_idps()
            user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
            assert user_idp is not None, "No IdP with sso_type 'USER' found."

            user_idp_id = user_idp["id"]
            resp = client.saml_attributes.list_attributes_by_idp(user_idp_id)
            assert isinstance(resp, list), "Response is not in the expected list format for IDP."
            assert len(resp) > 0, "No SAML attributes were found for the specified IdP by ID."
        except Exception as exc:
            errors.append(f"Listing SAML attributes by IDP failed: {exc}")

        try:
            # Test getting a specific SAML attribute
            attributes = client.saml_attributes.list_attributes_by_idp(user_idp["id"])
            assert len(attributes) > 0, "No SAML attributes found for the specified IdP."

            first_attribute_id = attributes[0]["id"]  # Assuming attributes is a list of dicts
            resp = client.saml_attributes.get_attribute(first_attribute_id)
            assert isinstance(resp, dict), "Response is not in the expected dict format."
            assert resp["id"] == first_attribute_id, "Retrieved SAML attribute ID does not match the requested ID."
        except Exception as exc:
            errors.append(f"Getting a specific SAML attribute failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during SAML attributes operations test: {errors}"
