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


class TestTrafficVPNCredential:
    """
    Integration Tests for the ZIA Traffic VPN Credential.
    """

    def test_traffic_vpn_credential(self, fs):
        client = MockZIAClient(fs)
        errors = []
        created_vpn_ids = []
        static_ip_id = None
        randomIP = generate_random_ip("104.239.237.0/24")

        # Create Static IP for VPN Credential of type IP
        try:
            created_static_ip = client.traffic.add_static_ip(ip_address=randomIP, comment="tests-" + generate_random_string())
            assert created_static_ip is not None, "Static IP creation returned None"
            static_ip_id = created_static_ip["id"]
        except Exception as exc:
            errors.append(f"Failed to add static IP: {exc}")

        # Create VPN Credential of type IP
        try:
            vpn_ip_credential = client.traffic.add_vpn_credential(
                authentication_type="IP",
                pre_shared_key="testkey-" + generate_random_string(),
                ip_address=randomIP,
            )
            assert vpn_ip_credential, "Failed to create IP VPN Credential"
            created_vpn_ids.append(vpn_ip_credential.id)
        except Exception as exc:
            errors.append(f"Create IP VPN Credential failed: {exc}")

        # Create VPN Credential of type UFQDN
        try:
            email = "tests-" + generate_random_string() + "@bd-hashicorp.com"
            vpn_ufqdn_credential = client.traffic.add_vpn_credential(
                authentication_type="UFQDN",
                pre_shared_key="testkey-" + generate_random_string(),
                fqdn=email,
            )
            assert vpn_ufqdn_credential, "Failed to create UFQDN VPN Credential"
            created_vpn_ids.append(vpn_ufqdn_credential.id)
        except Exception as exc:
            errors.append(f"Create UFQDN VPN Credential failed: {exc}")

        # Update VPN Credential of type IP
        if created_vpn_ids:
            try:
                updated_comment = "Updated IP VPN Credential"
                updated_vpn_ip = client.traffic.update_vpn_credential(created_vpn_ids[0], comments=updated_comment)
                assert updated_vpn_ip.comments == updated_comment, "Failed to update IP VPN Credential"
            except Exception as exc:
                errors.append(f"Update IP VPN Credential failed: {exc}")

        # Update VPN Credential of type UFQDN
        if len(created_vpn_ids) > 1:
            try:
                updated_comment = "Updated UFQDN VPN Credential"
                updated_vpn_ufqdn = client.traffic.update_vpn_credential(created_vpn_ids[1], comments=updated_comment)
                assert updated_vpn_ufqdn.comments == updated_comment, "Failed to update UFQDN VPN Credential"
            except Exception as exc:
                errors.append(f"Update UFQDN VPN Credential failed: {exc}")

            finally:
                # Cleanup: Delete any remaining VPN Credentials
                for vpn_id in created_vpn_ids:
                    try:
                        client.traffic.delete_vpn_credential(vpn_id)
                    except Exception as cleanup_exc:
                        errors.append(f"Cleanup failed for VPN Credential ID {vpn_id}: {cleanup_exc}")

                # Cleanup: Delete the static IP
                if static_ip_id:
                    try:
                        client.traffic.delete_static_ip(static_ip_id)
                    except Exception as cleanup_exc:
                        errors.append(f"Cleanup failed for Static IP ID {static_ip_id}: {cleanup_exc}")

            # Assert no errors occurred during the test
            assert len(errors) == 0, f"Errors occurred during VPN credential operations test: {errors}"
