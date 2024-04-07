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

class TestTrafficGRETunnel:
    """
    Integration Tests for the ZIA Traffic GRE Tunnel.
    """

    @pytest.mark.asyncio
    async def test_traffic_gre_tunnel(self, fs):
        client = MockZIAClient(fs)
        errors = []
        gre_tunnel_ids = []
        static_ip_id = None
        randomIP = generate_random_ip("104.239.237.0/24")

        # Create Static IP for GRE Tunnel
        try:
            created_static_ip = client.traffic.add_static_ip(
                ip_address=randomIP, comment='tests-' + generate_random_string()
            )
            assert created_static_ip is not None, "Static IP creation returned None"
            static_ip_id = created_static_ip["id"]
            # Use the IP address from the created static IP for the GRE tunnel
            static_ip_address = created_static_ip["ip_address"]  # Assuming the key is 'ip_address'
        except Exception as exc:
            errors.append(f"Failed to add static IP: {exc}")

        # Create GRE Tunnel using the IP address from the static IP creation
        try:
            gre_tunnel = client.traffic.add_gre_tunnel(
                source_ip=static_ip_address,  # Use the IP address from the created static IP
                comment='tests-' + generate_random_string(),
            )
            assert gre_tunnel, "Failed to create GRE Tunnel"
            gre_tunnel_ids.append(gre_tunnel["id"])
        except Exception as exc:
            errors.append(f"Create GRE Tunnel failed: {exc}")

        # Update GRE Tunnel
        if gre_tunnel_ids:
            try:
                updated_comment = 'Updated GRE Tunnel ' + generate_random_string()
                updated_gre_tunnel = client.traffic.update_gre_tunnel(
                    tunnel_id=gre_tunnel_ids[0],
                    source_ip=static_ip_address,
                    comment=updated_comment
                )
                # No need to check for status_code; presence of 'comment' implies success
                assert updated_gre_tunnel["comment"] == updated_comment, "Failed to update GRE Tunnel"
            except Exception as exc:
                errors.append(f"Update GRE Tunnel failed: {exc}")

        # Get and verify GRE Tunnel details
        try:
            fetched_gre_tunnel = client.traffic.get_gre_tunnel(gre_tunnel_ids[0])
            assert fetched_gre_tunnel["id"] == gre_tunnel_ids[0], "Failed to fetch GRE Tunnel"
        except Exception as exc:
            errors.append(f"Fetch GRE Tunnel failed: {exc}")

        # List GRE Tunnels and verify creation
        try:
            tunnels_list = client.traffic.list_gre_tunnels()
            assert any(tunnel["id"] == gre_tunnel_ids[0] for tunnel in tunnels_list), "Newly created GRE Tunnel not listed"
        except Exception as exc:
            errors.append(f"List GRE Tunnels failed: {exc}")

        finally:
            # Cleanup: Delete any created GRE Tunnel
            for tunnel_id in gre_tunnel_ids:
                try:
                    deletion_status = client.traffic.delete_gre_tunnel(tunnel_id)
                    assert deletion_status == 204, f"Failed to delete GRE Tunnel with ID {tunnel_id}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for GRE Tunnel ID {tunnel_id}: {cleanup_exc}")

            # Cleanup: Delete the static IP
            if static_ip_id:
                try:
                    deletion_status = client.traffic.delete_static_ip(static_ip_id)
                    assert deletion_status == 204, "Static IP deletion failed"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Static IP ID {static_ip_id}: {cleanup_exc}")

        # Assert no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during GRE Tunnel operations test: {'; '.join(errors)}"
