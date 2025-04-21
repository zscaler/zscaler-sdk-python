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

        try:
            # Step 1: Create Static IP for IP-based VPN Credential
            try:
                created_static_ip, _, error = client.zia.traffic_static_ip.add_static_ip(
                    ip_address=randomIP,
                    comment="tests-" + generate_random_string()
                )
                assert error is None, f"Error creating static IP: {error}"
                static_ip_id = created_static_ip.id
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")

            # Step 2: Create VPN Credential of type IP
            try:
                vpn_ip_credential, _, error = client.zia.traffic_vpn_credentials.add_vpn_credential(
                    type="IP",
                    pre_shared_key="testkey-" + generate_random_string(),
                    ip_address=randomIP,
                )
                assert error is None, f"Error creating IP VPN Credential: {error}"
                created_vpn_ids.append(vpn_ip_credential.id)
            except Exception as exc:
                errors.append(f"Create IP VPN Credential failed: {exc}")

            # Step 3: Create VPN Credential of type UFQDN
            try:
                email = "tests-" + generate_random_string() + "@securitygeek.io"
                vpn_ufqdn_credential, _, error = client.zia.traffic_vpn_credentials.add_vpn_credential(
                    type="UFQDN",
                    pre_shared_key="testkey-" + generate_random_string(),
                    fqdn=email,
                )
                assert error is None, f"Error creating UFQDN VPN Credential: {error}"
                created_vpn_ids.append(vpn_ufqdn_credential.id)
            except Exception as exc:
                errors.append(f"Create UFQDN VPN Credential failed: {exc}")

            # Step 4: Update VPN Credential of type IP
            # if len(created_vpn_ids) >= 1:
            #     try:
            #         updated_comment = "Updated IP VPN Credential"
            #         updated_vpn_ip, _, error = client.zia.traffic_vpn_credentials.update_vpn_credential(
            #             created_vpn_ids[0],
            #             comments=updated_comment,
            #             # type="IP",
            #             pre_shared_key="testkey-" + generate_random_string(),
            #             # ip_address=randomIP,
            #         )
            #         assert error is None, f"Error updating IP VPN Credential: {error}"
            #         assert updated_vpn_ip.comments == updated_comment, "IP VPN Credential update failed"
            #     except Exception as exc:
            #         errors.append(f"Update IP VPN Credential failed: {exc}")

            # # Step 5: Update VPN Credential of type UFQDN
            # if len(created_vpn_ids) >= 2:
            #     try:
            #         updated_comment = "Updated UFQDN VPN Credential"
            #         updated_vpn_ufqdn, _, error = client.zia.traffic_vpn_credentials.update_vpn_credential(
            #             created_vpn_ids[1],
            #             comments=updated_comment,
            #             # type="UFQDN",
            #             pre_shared_key="testkey-" + generate_random_string(),
            #             # fqdn=email,
            #         )
            #         assert error is None, f"Error updating UFQDN VPN Credential: {error}"
            #         assert updated_vpn_ufqdn.comments == updated_comment, "UFQDN VPN Credential update failed"
            #     except Exception as exc:
            #         errors.append(f"Update UFQDN VPN Credential failed: {exc}")

        finally:
            cleanup_errors = []

            # Step 6: Bulk Delete VPN Credentials
            if created_vpn_ids:
                try:
                    _, _, error = client.zia.traffic_vpn_credentials.bulk_delete_vpn_credentials(created_vpn_ids)
                    assert error is None, f"Error in bulk deleting VPN Credentials: {error}"
                except Exception as exc:
                    cleanup_errors.append(f"Bulk deletion of VPN Credentials failed: {exc}")

            # Step 7: Delete the Static IP
            if static_ip_id:
                try:
                    _, _, error = client.zia.traffic_static_ip.delete_static_ip(static_ip_id)
                    assert error is None, f"Error deleting Static IP: {error}"
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Static IP failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during VPN credential operations test:\n{chr(10).join(errors)}"
