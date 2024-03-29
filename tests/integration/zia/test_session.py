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


@responses.activate
def test_create(zia, session):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        json=session,
        status=200,
    )

    resp = zia.session.create(api_key="test1234567890", username="test@example.com", password="hunter2")

    assert isinstance(resp, dict)
    assert resp.auth_type == "ADMIN_LOGIN"
    assert resp.obfuscate_api_key is False
    assert resp.password_expiry_time == 0
    assert resp.password_expiry_days == 0


@responses.activate
def test_status(zia, session):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        json=session,
        status=200,
    )

    resp = zia.session.status()

    assert isinstance(resp, dict)
    assert resp.auth_type == "ADMIN_LOGIN"
    assert resp.obfuscate_api_key is False
    assert resp.password_expiry_time == 0
    assert resp.password_expiry_days == 0


@responses.activate
def test_delete(zia):
    delete_status = {"status": "ACTIVE"}
    responses.add(
        responses.DELETE,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        json=delete_status,
        status=200,
    )

    resp = zia.session.delete()

    assert isinstance(resp, int)
    assert resp == 200
