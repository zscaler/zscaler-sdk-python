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

from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_ip, generate_random_string


@pytest.fixture
def fs():
    yield


class TestTrafficStaticIP:
    """
    Integration Tests for the traffic static ip
    """

    def test_traffic_static_ip(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        randomIP = generate_random_ip("104.239.237.0/24")
        comment = "tests-" + generate_random_string()
        static_ip_id = None

        try:
            # Attempt to create a new static IP
            try:
                created_static_ip = client.traffic.add_static_ip(
                    comment=comment,
                    ip_address=randomIP,
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                assert created_static_ip.comment == comment, "Comment mismatch"
                assert created_static_ip.ip_address == randomIP, "IP address mismatch"
                static_ip_id = created_static_ip.id
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")

            # Attempt to retrieve the created static IP by ID
            if static_ip_id:
                try:
                    retrieved_ip = client.traffic.get_static_ip(static_ip_id)
                    assert retrieved_ip.id == static_ip_id, "Retrieved IP ID mismatch"
                    assert retrieved_ip.comment == comment, "Retrieved comment mismatch"
                except Exception as exc:
                    errors.append(f"Failed to retrieve static IP: {exc}")

            # Attempt to update the static IP
            if static_ip_id:
                try:
                    updated_comment = comment + " Updated"
                    client.traffic.update_static_ip(static_ip_id, comment=updated_comment)
                    updated_static_ip = client.traffic.get_static_ip(static_ip_id)
                    assert updated_static_ip.comment == updated_comment, "Failed to update comment"
                except Exception as exc:
                    errors.append(f"Failed to update static IP: {exc}")

            # Attempt to list static IPs and check if the updated IP is in the list
            try:
                ip_list = client.traffic.list_static_ips()
                assert any(ip.id == static_ip_id for ip in ip_list), "Updated IP not found in list"
            except Exception as exc:
                errors.append(f"Failed to list static IPs: {exc}")

        finally:
            # Cleanup: Attempt to delete the static IP
            if static_ip_id:
                try:
                    delete_response_code = client.traffic.delete_static_ip(static_ip_id)
                    assert str(delete_response_code) == "204", "Failed to delete static IP"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the static ip lifecycle test: {errors}"
