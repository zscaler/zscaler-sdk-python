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


class TestTrafficGRETunnel:
    """
    Integration Tests for the ZIA Traffic GRE Tunnel.
    """

    @pytest.mark.vcr()
    def test_gre_tunnel_workflow(self, fs):
        client = MockZIAClient(fs)
        errors = []
        gre_tunnel_ids = []
        static_ip_id = None
        static_ip_address = None
        randomIP = generate_random_ip("104.239.237.0/24")

        try:
            # Step 1: Create Static IP for GRE Tunnel
            try:
                created_static_ip = client.zia.traffic_static_ip.add_static_ip(
                    ip_address=randomIP, comment="tests-" + generate_random_string()
                )
                static_ip_id = created_static_ip.id
                static_ip_address = created_static_ip.ip_address
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")

            # Step 2: Create GRE Tunnel using the static IP
            try:
                gre_tunnel = client.zia.gre_tunnel.add_gre_tunnel(
                    source_ip=static_ip_address,
                    ip_unnumbered=True,
                    comment="tests-" + generate_random_string(),
                )
                assert gre_tunnel is not None, "GRE Tunnel creation returned None"
                gre_tunnel_ids.append(gre_tunnel.id)
            except Exception as exc:
                errors.append(f"Create GRE Tunnel failed: {exc}")

            # Step 3: Update GRE Tunnel
            if gre_tunnel_ids:
                try:
                    updated_comment = "Updated GRE Tunnel " + generate_random_string()
                    updated_tunnel = client.zia.gre_tunnel.update_gre_tunnel(
                        tunnel_id=gre_tunnel_ids[0],
                        source_ip=static_ip_address,
                        ip_unnumbered=True,
                        comment=updated_comment,
                    )
                    assert updated_tunnel.comment == updated_comment, "GRE Tunnel update failed"
                except Exception as exc:
                    errors.append(f"Update GRE Tunnel failed: {exc}")

            # Step 4: Retrieve GRE Tunnel
            try:
                fetched_tunnel = client.zia.gre_tunnel.get_gre_tunnel(gre_tunnel_ids[0])
                assert fetched_tunnel.id == gre_tunnel_ids[0], "Fetched tunnel ID mismatch"
            except Exception as exc:
                errors.append(f"Fetch GRE Tunnel failed: {exc}")

            # Step 5: List GRE Tunnels and verify presence
            try:
                tunnels_list = client.zia.gre_tunnel.list_gre_tunnels()
                assert any(tunnel.id == gre_tunnel_ids[0] for tunnel in tunnels_list), "Created GRE Tunnel not listed"
            except Exception as exc:
                errors.append(f"List GRE Tunnels failed: {exc}")

        finally:
            # Step 6: Cleanup
            cleanup_errors = []

            for tunnel_id in gre_tunnel_ids:
                try:
                    _ = client.zia.gre_tunnel.delete_gre_tunnel(tunnel_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting GRE Tunnel failed: {exc}")

            if static_ip_id:
                try:
                    _ = client.zia.traffic_static_ip.delete_static_ip(static_ip_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting static IP failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during GRE Tunnel workflow test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_traffic_list_vips_recommended(self, fs):
        client = MockZIAClient(fs)
        errors = []
        static_ip_id = None
        static_ip_address = generate_random_ip("104.239.237.0/24")

        try:
            # Step 1: Create Static IP
            try:
                created_static_ip = client.zia.traffic_static_ip.add_static_ip(
                    ip_address=static_ip_address, comment="tests-" + generate_random_string()
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                static_ip_id = created_static_ip.id
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")

            # Step 2: Fetch Recommended VIPs using that IP
            try:
                recommended_vips = client.zia.gre_tunnel.list_vips_recommended(
                    query_params={"source_ip": static_ip_address}
                )
                assert isinstance(recommended_vips, list), "Expected list of recommended VIPs"
                assert recommended_vips, "Received empty recommended VIP list"
            except Exception as exc:
                errors.append(f"Listing recommended VIPs failed: {exc}")

        finally:
            # Step 3: Cleanup
            cleanup_errors = []
            if static_ip_id:
                try:
                    _ = client.zia.traffic_static_ip.delete_static_ip(static_ip_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Static IP failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during recommended VIP listing test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_traffic_list_vip_group_by_dc(self, fs):
        client = MockZIAClient(fs)
        errors = []
        static_ip_id = None
        static_ip_address = generate_random_ip("104.239.237.0/24")

        try:
            # Step 1: Create Static IP
            try:
                created_static_ip = client.zia.traffic_static_ip.add_static_ip(
                    ip_address=static_ip_address, comment="tests-" + generate_random_string()
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                static_ip_id = created_static_ip.id
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")

            # Step 2: Fetch VIP Groups by Datacenter using the created static IP
            try:
                vip_groups = client.zia.gre_tunnel.list_vip_group_by_dc(
                    query_params={"source_ip": static_ip_address}
                )
                assert isinstance(vip_groups, list), "Expected list of VIP groups"
                assert vip_groups, "Received empty VIP group list"
            except Exception as exc:
                errors.append(f"Listing VIP group by DC failed: {exc}")

        finally:
            # Step 3: Cleanup
            cleanup_errors = []
            if static_ip_id:
                try:
                    _ = client.zia.traffic_static_ip.delete_static_ip(static_ip_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Static IP failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during VIP group by DC test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_traffic_get_closest_diverse_vip_ids(self, fs):
        client = MockZIAClient(fs)
        errors = []
        static_ip_id = None
        static_ip_address = generate_random_ip("104.239.237.0/24")

        try:
            # Step 1: Create Static IP
            try:
                created_static_ip = client.zia.traffic_static_ip.add_static_ip(
                    ip_address=static_ip_address, comment="tests-" + generate_random_string()
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                static_ip_id = created_static_ip.id
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")

            # Step 2: Get closest diverse VIP IDs
            try:
                closest_vips = client.zia.gre_tunnel.get_closest_diverse_vip_ids(static_ip_address)
                assert isinstance(closest_vips, tuple), "Returned value should be a tuple"
                assert len(closest_vips) == 2, "Expected exactly two VIP IDs"
                assert all(isinstance(vip_id, int) for vip_id in closest_vips), "VIP IDs should be integers"
            except Exception as exc:
                errors.append(f"Getting closest diverse VIP IDs failed: {exc}")

        finally:
            # Step 3: Cleanup
            cleanup_errors = []
            if static_ip_id:
                try:
                    _ = client.zia.traffic_static_ip.delete_static_ip(static_ip_id)
                except Exception as exc:
                    cleanup_errors.append(f"Deleting Static IP failed: {exc}")

            errors.extend(cleanup_errors)

        # Final assertion
        assert len(errors) == 0, f"Errors occurred during diverse VIP ID test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_traffic_list_vips(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            # Step 1: List VIPs with a page size of 10.
            try:
                vips = client.zia.gre_tunnel.list_vips(query_params={"page_size": "10"})
                assert isinstance(vips, list), "Expected VIPs to be returned as a list."
                assert len(vips) <= 10, f"Expected at most 10 VIPs, but got {len(vips)}."
            except Exception as exc:
                errors.append(f"Listing VIPs with page_size 10 failed: {exc}")

            # Step 2: List VIPs with the same query parameters for additional validation.
            try:
                vips_large = client.zia.gre_tunnel.list_vips(query_params={"page_size": "10"})
                assert isinstance(vips_large, list), "Expected VIPs to be returned as a list."
                # Optionally, further validations on vips_large can be added if needed.
            except Exception as exc:
                errors.append(f"Listing VIPs with repeated query parameters failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing VIPs with specific parameters failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during listing VIPs test: {'; '.join(errors)}"
