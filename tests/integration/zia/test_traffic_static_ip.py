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

from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_ip, generate_random_string
import time

@pytest.fixture
def fs():
    yield


class TestTrafficStaticIP:
    """
    Integration Tests for the traffic static IP (ZIA)
    """

    def test_traffic_static_ip(self, fs):
        client = MockZIAClient(fs)
        errors = []

        randomIP = generate_random_ip("104.239.237.0/24")
        checkIP = generate_random_ip("104.239.237.0/24")  # ✅ Different IP for validation
        comment = "tests-" + generate_random_string()
        static_ip_id = None

        try:
            # Step 1: Create Static IP
            try:
                created_static_ip, _, error = client.zia.traffic_static_ip.add_static_ip(
                    comment=comment,
                    ip_address=randomIP,
                )
                assert error is None, f"Error creating static IP: {error}"
                assert created_static_ip is not None, "Static IP creation returned None"
                assert created_static_ip.comment == comment
                assert created_static_ip.ip_address == randomIP
                static_ip_id = created_static_ip.id
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")

            # Step 2: Retrieve the created static IP
            try:
                if static_ip_id:
                    time.sleep(2)
                    retrieved_ip, _, error = client.zia.traffic_static_ip.get_static_ip(static_ip_id)
                    assert error is None, f"Error retrieving static IP: {error}"
                    assert retrieved_ip.id == static_ip_id
                    assert retrieved_ip.comment == comment
            except Exception as exc:
                errors.append(f"Failed to retrieve static IP: {exc}")

            # Step 3: Check if a brand new IP is valid
            try:
                time.sleep(2)
                is_valid, _, error = client.zia.traffic_static_ip.check_static_ip(checkIP)
                if error:
                    raise AssertionError(f"Error checking static IP validity: {error}")
                assert is_valid is True, f"Static IP {checkIP} is not valid or already in use"
            except Exception as exc:
                errors.append(f"Static IP validation check failed: {exc}")

            # Step 4: List static IPs and check if created IP exists
            try:
                time.sleep(2)
                ip_list, _, error = client.zia.traffic_static_ip.list_static_ips()
                assert error is None, f"Error listing static IPs: {error}"
                assert any(ip.id == static_ip_id for ip in ip_list), "Created static IP not found in list"
            except Exception as exc:
                errors.append(f"Failed to list static IPs: {exc}")

        finally:
            # Step 5: Cleanup
            cleanup_errors = []
            if static_ip_id:
                try:
                    time.sleep(2)
                    _, _, error = client.zia.traffic_static_ip.delete_static_ip(static_ip_id)
                    assert error is None, f"Error deleting static IP: {error}"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting static IP failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during the static IP lifecycle test:\n{chr(10).join(errors)}"
