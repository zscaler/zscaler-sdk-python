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
from box import Box, BoxList

from tests.conftest import stub_sleep


@pytest.fixture(name="idps")
def fixture_idps():
    return {
        "totalPages": 1,
        "list": [
            {
                "id": "1",
                "modifiedTime": "1623042158",
                "creationTime": "1623041306",
                "modifiedBy": "1",
                "name": "Test",
                "loginUrl": "https://idp.example.com",
                "idpEntityId": "https://idp.example.com/",
                "autoProvision": "0",
                "signSamlRequest": "1",
                "ssoType": ["USER"],
                "domainList": ["example.com"],
                "useCustomSpMetadata": True,
                "scimEnabled": True,
                "enableScimBasedPolicy": False,
                "disableSamlBasedPolicy": False,
                "reauthOnUserUpdate": False,
                "scimSharedSecretExists": False,
                "enabled": True,
                "redirectBinding": False,
            },
            {
                "id": "2",
                "modifiedTime": "1623042158",
                "creationTime": "1623041306",
                "modifiedBy": "1",
                "name": "Test",
                "loginUrl": "https://idp.example.com",
                "idpEntityId": "https://idp.example.com/",
                "autoProvision": "0",
                "signSamlRequest": "1",
                "ssoType": ["USER"],
                "domainList": ["example.com"],
                "useCustomSpMetadata": True,
                "scimEnabled": True,
                "enableScimBasedPolicy": False,
                "disableSamlBasedPolicy": False,
                "reauthOnUserUpdate": False,
                "scimSharedSecretExists": False,
                "enabled": True,
                "redirectBinding": False,
            },
        ],
    }


@responses.activate
@stub_sleep
def test_list_idps(zpa, idps):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/idp?page=1",
        json=idps,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/idp?page=2",
        json=[],
        status=200,
    )
    resp = zpa.idp.list_idps()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_idp(zpa, idps):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/idp/1",
        json=idps["list"][0],
        status=200,
    )
    resp = zpa.idp.get_idp("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"
