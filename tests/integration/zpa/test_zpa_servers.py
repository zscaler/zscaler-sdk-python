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
from utils import generate_random_string
from tests.conftest import stub_sleep


@stub_sleep
def test_application_servers(zpa):
    add_server_name = "tests-" + generate_random_string()
    update_server_name = "tests-" + generate_random_string()

    add_resp = zpa.servers.add_server(
        name=add_server_name,
        description="A description for " + add_server_name,
        enabled=True,
        address="192.168.0.1",
    )

    assert isinstance(add_resp, Box)
    assert "id" in add_resp, "Add response does not contain an 'id' field"
    server_id = add_resp["id"]

    verify_add_resp = zpa.servers.get_server(server_id)
    assert (
        verify_add_resp["name"] == add_server_name
    ), "Server name does not match after creation"

    zpa.servers.update_server(
        server_id,
        name=update_server_name,
        description="Updated description for " + update_server_name,
        address="192.168.0.2",
    )

    get_resp = zpa.servers.get_server(server_id)
    assert isinstance(get_resp, Box)
    assert (
        get_resp["name"] == update_server_name
    ), "Server name did not update correctly"

    list_resp = zpa.servers.list_servers()
    assert isinstance(list_resp, BoxList), "Expected a list of Servers"
    assert any(
        server["id"] == server_id for server in list_resp
    ), "Updated Server not found in list"

    zpa.servers.delete_server(server_id)
