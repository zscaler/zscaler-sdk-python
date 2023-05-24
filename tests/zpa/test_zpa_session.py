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


import responses
from responses import matchers


@responses.activate
def test_create_token(zpa, session):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/signin",
        json=session,
        status=200,
        match=[
            matchers.urlencoded_params_matcher(
                {
                    "client_id": "1",
                    "client_secret": "yyy",
                }
            ),
            matchers.header_matcher({"Content-Type": "application/x-www-form-urlencoded"}),
        ],
    )

    resp = zpa.session.create_token(client_id="1", client_secret="yyy")

    assert isinstance(resp, str)
    assert resp == "xyz"
