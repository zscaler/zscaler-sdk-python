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

from tests.integration.zia.conftest import MockZIAClient, NameGenerator
from tests.test_utils import generate_random_ip, generate_random_string, reset_vcr_counters
import time


@pytest.fixture
def fs():
    yield


class TestTrafficStaticIP:
    """
    Integration Tests for the traffic static IP (ZIA)
    """

    @pytest.mark.vcr()
    def test_traffic_static_ip(self, fs):
        # Reset counters for deterministic values
        reset_vcr_counters()
        
        client = MockZIAClient(fs)
        errors = []

        # Use deterministic test name generator
        names = NameGenerator("static-ip")
        
        randomIP = generate_random_ip("104.239.237.0/24")
        checkIP = generate_random_ip("104.239.237.0/24")  # Different IP for validation
        comment = names.name
        static_ip_id = None

        try:
            # Step 1: Create Static IP
            try:
                created_static_ip = client.zia.traffic_static_ip.add_static_ip(
                    comment=comment,
                    ip_address=randomIP,
                )
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
                    retrieved_ip = client.zia.traffic_static_ip.get_static_ip(static_ip_id)
                    assert retrieved_ip.id == static_ip_id
                    assert retrieved_ip.comment == comment
            except Exception as exc:
                errors.append(f"Failed to retrieve static IP: {exc}")

            # Step 3: Check if a brand new IP is valid
            try:
                time.sleep(2)
                is_valid = client.zia.traffic_static_ip.check_static_ip(checkIP)
                assert is_valid is True, f"Static IP {checkIP} is not valid or already in use"
            except Exception as exc:
                errors.append(f"Static IP validation check failed: {exc}")

            # Step 4: List static IPs and check if created IP exists
            try:
                time.sleep(2)
                ip_list = client.zia.traffic_static_ip.list_static_ips()
                assert any(ip.id == static_ip_id for ip in ip_list), "Created static IP not found in list"
            except Exception as exc:
                errors.append(f"Failed to list static IPs: {exc}")

        finally:
            # Step 5: Cleanup
            cleanup_errors = []
            if static_ip_id:
                try:
                    time.sleep(2)
                    _ = client.zia.traffic_static_ip.delete_static_ip(static_ip_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting static IP failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during the static IP lifecycle test:\n{chr(10).join(errors)}"
