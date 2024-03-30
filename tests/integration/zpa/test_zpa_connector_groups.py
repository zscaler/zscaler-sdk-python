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
def test_app_connector_groups(zpa):
    add_group_name = "tests-" + generate_random_string()
    update_group_name = "tests-" + generate_random_string()

    add_resp = zpa.connectors.add_connector_group(
        name=add_group_name,
        description="A description for " + add_group_name,
        enabled=True,
        city_country="San Jose, US",
        latitude="37.3382082",
        longitude="-121.8863286",
        location="San Jose, CA, USA",
        upgrade_day="SUNDAY",
        upgrade_time_in_secs="66600",
        override_version_profile=True,
        version_profile_name="Default",
        version_profile_id="0",
        dns_query_type="IPV4_IPV6",
        pra_enabled=False,
        tcp_quick_ack_app=True,
        tcp_quick_ack_assistant=True,
        tcp_quick_ack_read_assistant=True,
    )

    assert isinstance(add_resp, Box)
    assert "id" in add_resp, "Add response does not contain an 'id' field"
    group_id = add_resp["id"]

    verify_add_resp = zpa.connectors.get_connector_group(group_id)
    assert (
        verify_add_resp["name"] == add_group_name
    ), "Group name does not match after creation"

    zpa.connectors.update_connector_group(
        group_id,
        name=update_group_name,
        description="Updated description for " + update_group_name,
    )

    get_resp = zpa.connectors.get_connector_group(group_id)
    assert isinstance(get_resp, Box)
    assert get_resp["name"] == update_group_name, "Group name did not update correctly"

    list_resp = zpa.connectors.list_connector_groups()
    assert isinstance(list_resp, BoxList), "Expected a list of groups"
    assert any(
        group["id"] == group_id for group in list_resp
    ), "Updated group not found in list"

    zpa.connectors.delete_connector_group(group_id)
