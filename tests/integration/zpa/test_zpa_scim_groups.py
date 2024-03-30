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


def test_list_scim_groups(zpa):
    idps = zpa.idp.list_idps()

    user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
    assert user_idp is not None, "No IdP with sso_type 'USER' found."

    user_idp_id = user_idp["id"]

    resp = zpa.scim_groups.list_groups(user_idp_id)

    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No SCIM groups were found for the specified IdP."


def test_get_scim_group(zpa):
    idps = zpa.idp.list_idps()
    user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
    assert user_idp is not None, "No IdP with sso_type 'USER' found."

    user_idp_id = user_idp["id"]

    scim_groups = zpa.scim_groups.list_groups(user_idp_id)
    assert len(scim_groups) > 0, "No SCIM groups found for the specified IdP."

    first_group_id = scim_groups[0].id

    resp = zpa.scim_groups.get_group(first_group_id)

    assert isinstance(resp, Box), "Response is not in the expected Box format."
    assert (
        resp.id == first_group_id
    ), "Retrieved SCIM group ID does not match the requested ID."
