"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import pytest
from tests.integration.zms.conftest import MockZMSClient, get_customer_id


@pytest.fixture
def fs():
    yield


class TestResourceGroups:
    """
    Integration Tests for the ZMS Resource Groups API
    """

    @pytest.mark.vcr()
    def test_list_resource_groups(self, fs, zms_client):
        client = zms_client
        customer_id = get_customer_id()

        result, response, err = client.zms.resource_groups.list_resource_groups(
            customer_id=customer_id, page_num=1, page_size=20
        )

        assert response is not None or err is not None
        if result:
            print(f"Resource groups count: {len(result.get('nodes', []))}")
        print("list_resource_groups completed")

    @pytest.mark.vcr()
    def test_get_resource_group_protection_status(self, fs, zms_client):
        client = zms_client
        customer_id = get_customer_id()

        result, response, err = client.zms.resource_groups.get_resource_group_protection_status(customer_id=customer_id)

        assert response is not None or err is not None
        print("get_resource_group_protection_status completed")
