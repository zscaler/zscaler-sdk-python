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
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="segment_groups")
def fixture_segment_groups():
    return {
        "totalPages": 1,
        "list": [
            {
                "id": "1",
                "creationTime": "1623895870",
                "modifiedBy": "1",
                "name": "Test A",
                "description": "Test",
                "enabled": True,
                "applications": [
                    {
                        "id": "1",
                        "creationTime": "1623895870",
                        "modifiedBy": "1",
                        "name": "Test",
                        "domainName": "test.example.com",
                        "domainNames": ["test.example.com"],
                        "description": "Test",
                        "enabled": True,
                        "passiveHealthEnabled": True,
                        "tcpPortRanges": ["80", "80", "443", "443"],
                        "doubleEncrypt": False,
                        "healthCheckType": "DEFAULT",
                        "icmpAccessType": "NONE",
                        "bypassType": "NEVER",
                        "configSpace": "DEFAULT",
                        "ipAnchored": False,
                        "tcpPortRange": [{"from": "80", "to": "80"}, {"from": "443", "to": "443"}],
                    }
                ],
                "policyMigrated": True,
                "configSpace": "DEFAULT",
                "tcpKeepAliveEnabled": "0",
            },
            {
                "id": "2",
                "creationTime": "1623895870",
                "modifiedBy": "1",
                "name": "Test B",
                "description": "Test",
                "enabled": True,
                "applications": [
                    {
                        "id": "1",
                        "creationTime": "1623895870",
                        "modifiedBy": "1",
                        "name": "Test",
                        "domainName": "test.example.com",
                        "domainNames": ["test.example.com"],
                        "description": "Test",
                        "enabled": True,
                        "passiveHealthEnabled": True,
                        "tcpPortRanges": ["80", "80", "443", "443"],
                        "doubleEncrypt": False,
                        "healthCheckType": "DEFAULT",
                        "icmpAccessType": "NONE",
                        "bypassType": "NEVER",
                        "configSpace": "DEFAULT",
                        "ipAnchored": False,
                        "tcpPortRange": [{"from": "80", "to": "80"}, {"from": "443", "to": "443"}],
                    }
                ],
                "policyMigrated": True,
                "configSpace": "DEFAULT",
                "tcpKeepAliveEnabled": "0",
            },
        ],
    }

def test_full_group_lifecycle(zpa):
    # Assuming 'zpa' is already configured and 'responses' are activated where necessary
    
    # Step 1: Add a new group
    add_response_simulated = {
        "name": "Example",
        "description": "Example",
        "enabled": True,
    }
    add_url = f"{zpa.baseurl}/mgmtconfig/v1/admin/customers/{zpa.customer_id}/segmentGroup"
    responses.add(
        responses.POST,
        url=add_url,
        json=add_response_simulated,
        status=200,
    )
    add_resp = zpa.segment_groups.add_group(
        name="Example",
        enabled=True,
        description="Example",
    )
    assert isinstance(add_resp, Box)
    group_id = add_resp.id

    # Step 2: Update the group
    update_response_simulated = {
        "id": group_id,
        "name": "Test Updated",
        "description": "Test Updated",
        "enabled": True,
    }
    update_url = f"{zpa.baseurl}/mgmtconfig/v1/admin/customers/{zpa.customer_id}/segmentGroup/{group_id}"
    responses.add(
        responses.PUT,
        url=update_url,
        json=update_response_simulated,
        status=200,
    )
    update_resp = zpa.segment_groups.update_group(
        group_id,
        name="Test Updated",
        description="Test Updated",
    )
    assert isinstance(update_resp, Box)

    # Step 3: Get the updated group
    get_url = f"{zpa.baseurl}/mgmtconfig/v1/admin/customers/{zpa.customer_id}/segmentGroup/{group_id}"
    responses.add(
        responses.GET,
        url=get_url,
        json=update_response_simulated,
        status=200,
    )
    get_resp = zpa.segment_groups.get_group(group_id)
    assert isinstance(get_resp, Box)

    # Step 4: List all groups
    list_groups_simulated = [add_response_simulated]  # Simulating a simple list response
    list_url = f"{zpa.baseurl}/mgmtconfig/v1/admin/customers/{zpa.customer_id}/segmentGroup?page=1"
    responses.add(
        responses.GET,
        url=list_url,
        json={"list": list_groups_simulated, "totalPages": 1},
        status=200,
    )
    list_resp = zpa.segment_groups.list_groups()
    assert isinstance(list_resp, BoxList)
    assert len(list_resp) >= 1  # Asserting that at least one group is returned

    # Step 5: Delete the group
    delete_url = f"{zpa.baseurl}/mgmtconfig/v1/admin/customers/{zpa.customer_id}/segmentGroup/{group_id}"
    responses.add(
        responses.DELETE,
        url=delete_url,
        status=204,
    )
    delete_resp = zpa.segment_groups.delete_group(group_id)
    assert delete_resp == 204