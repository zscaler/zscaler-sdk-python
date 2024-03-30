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


def test_list_machine_groups(zpa):
    resp = zpa.machine_groups.list_groups()
    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No Groups were found."


def test_get_machine_group(zpa):
    list_groups = zpa.machine_groups.list_groups()
    assert len(list_groups) > 0, "No Groups to retrieve."

    # Assuming the list returns BoxList of groups and we can access 'id'
    first_group_id = list_groups[0].id

    # Now, use that 'id' to get a specific group
    resp = zpa.machine_groups.get_group(first_group_id)

    # Perform your assertions on the retrieved group
    assert isinstance(resp, Box), "Response is not in the expected Box format."
    assert (
        resp.id == first_group_id
    ), f"Retrieved Group ID does not match requested ID: {first_group_id}."
