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


def test_list_trusted_networks(zpa):
    resp = zpa.trusted_networks.list_networks()
    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No networks were found."


def test_get_trusted_network(zpa):
    list_networks = zpa.trusted_networks.list_networks()
    assert len(list_networks) > 0, "No networks to retrieve."

    # Assuming the list returns BoxList of networks and we can access 'id'
    network_id = list_networks[0].id

    # Now, use that 'id' to get a specific network
    resp = zpa.trusted_networks.get_network(network_id)

    # Perform your assertions on the retrieved network
    assert isinstance(resp, Box), "Response is not in the expected Box format."
    assert (
        resp.id == network_id
    ), f"Retrieved network ID does not match requested ID: {network_id}."
