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


def test_list_posture_profile(zpa):
    resp = zpa.posture_profiles.list_profiles()
    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No profiles were found."


def test_get_posture_profile(zpa):
    list_profiles = zpa.posture_profiles.list_profiles()
    assert len(list_profiles) > 0, "No profiles to retrieve."

    # Assuming the list returns BoxList of profiles and we can access 'id'
    first_profile_id = list_profiles[0].id

    # Now, use that 'id' to get a specific profile
    resp = zpa.posture_profiles.get_profile(first_profile_id)

    # Perform your assertions on the retrieved profile
    assert isinstance(resp, Box), "Response is not in the expected Box format."
    assert (
        resp.id == first_profile_id
    ), f"Retrieved profile ID does not match requested ID: {first_profile_id}."
