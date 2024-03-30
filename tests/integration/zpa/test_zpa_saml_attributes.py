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


from box import Box, BoxList


def test_list_saml_attributes(zpa):
    resp = zpa.saml_attributes.list_attributes()

    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No Saml attributes were found for the specified IdP."


def test_list_saml_attributes_by_idp(zpa):
    idps = zpa.idp.list_idps()

    user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
    assert user_idp is not None, "No IdP with sso_type 'USER' found."

    user_idp_id = user_idp["id"]

    resp = zpa.saml_attributes.list_attributes_by_idp(user_idp_id)

    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No SAML attributes were found for the specified IdP."


def test_get_saml_attribute(zpa):
    idps = zpa.idp.list_idps()

    user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
    assert user_idp is not None, "No IdP with sso_type 'USER' found."

    attributes = zpa.saml_attributes.list_attributes_by_idp(user_idp["id"])
    assert len(attributes) > 0, "No SAML attributes found for the specified IdP."

    first_attribute_id = attributes[0].id
    resp = zpa.saml_attributes.get_attribute(first_attribute_id)

    assert isinstance(resp, Box), "Response is not in the expected Box format."
    assert (
        resp.id == first_attribute_id
    ), "Retrieved SAML attribute ID does not match the requested ID."
