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


def test_list_idps(zpa):
    resp = zpa.idp.list_idps()
    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No idps were found."


def test_get_idp(zpa):
    list_idps = zpa.idp.list_idps()
    assert len(list_idps) > 0, "No IdPs to retrieve."

    # Assuming the list returns BoxList of idps and we can access 'id'
    first_idp_id = list_idps[0].id

    # Now, use that 'id' to get a specific idp
    resp = zpa.idp.get_idp(first_idp_id)

    # Perform your assertions on the retrieved idp
    assert isinstance(resp, Box), "Response is not in the expected Box format."
    assert (
        resp.id == first_idp_id
    ), f"Retrieved IdP ID does not match requested ID: {first_idp_id}."
