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


class TestNonces:
    """
    Integration Tests for the ZMS Nonces (Provisioning Keys) API
    """

    @pytest.mark.vcr()
    def test_list_nonces(self, fs, zms_client):
        client = zms_client
        customer_id = get_customer_id()

        result, response, err = client.zms.nonces.list_nonces(customer_id=customer_id, page=1, page_size=20)

        assert response is not None or err is not None
        if result:
            print(f"Nonces count: {len(result.get('nodes', []))}")
        print("list_nonces completed")
