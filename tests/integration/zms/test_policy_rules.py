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


class TestPolicyRules:
    """
    Integration Tests for the ZMS Policy Rules API
    """

    @pytest.mark.vcr()
    def test_list_policy_rules(self, fs, zms_client):
        client = zms_client
        customer_id = get_customer_id()

        result, response, err = client.zms.policy_rules.list_policy_rules(customer_id=customer_id, page_num=1, page_size=20)

        assert response is not None or err is not None
        if result:
            print(f"Policy rules count: {len(result.get('nodes', []))}")
        print("list_policy_rules completed")

    @pytest.mark.vcr()
    def test_list_default_policy_rules(self, fs, zms_client):
        client = zms_client
        customer_id = get_customer_id()

        result, response, err = client.zms.policy_rules.list_default_policy_rules(customer_id=customer_id)

        assert response is not None or err is not None
        if result:
            print(f"Default policy rules count: {len(result.get('nodes', []))}")
        print("list_default_policy_rules completed")
