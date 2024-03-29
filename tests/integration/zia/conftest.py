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
import responses

from zscaler.zia import ZIAClientHelper


@pytest.fixture(name="session")
def fixture_session():
    return {
        "authType": "ADMIN_LOGIN",
        "obfuscateApiKey": False,
        "passwordExpiryTime": 0,
        "passwordExpiryDays": 0,
    }


@pytest.fixture(name="zia")
@responses.activate
def zia(session):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        content_type="application/json",
        json=session,
        status=200,
    )
    # THIS IS A FAKE (EXAMPLE) USERNAME AND PASSWORD AND NOT USED IN PRODUCTION
    return ZIAClientHelper(
        username="test@example.com",
        password="hunter2",
        cloud="zscaler",
        api_key="123456789abcdef",
        sandbox_token="SANDBOXTOKEN",
    )


@pytest.fixture(name="paginated_items")
def fixture_pagination_items():
    def _method(num):
        items = []
        for x in range(0, num):
            items.append({"id": x})
        return items

    return _method
