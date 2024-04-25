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

    def test_traffic_gre_tunnel(self, fs):
        client = MockZIAClient(fs)
        errors = []
        gre_tunnel_ids = []
        static_ip_id = None
        randomIP = generate_random_ip("104.239.237.0/24")

        # Create Static IP for GRE Tunnel
        try:
            created_static_ip = client.traffic.add_static_ip(ip_address=randomIP, comment="tests-" + generate_random_string())
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
                ip_unnumbered=True,
                comment="tests-" + generate_random_string(),
            )
            assert gre_tunnel, "Failed to create GRE Tunnel"
            gre_tunnel_ids.append(gre_tunnel["id"])
        except Exception as exc:
            errors.append(f"Create GRE Tunnel failed: {exc}")

        # Update GRE Tunnel
        if gre_tunnel_ids:
            try:
                updated_comment = "Updated GRE Tunnel " + generate_random_string()
                updated_gre_tunnel = client.traffic.update_gre_tunnel(
                    tunnel_id=gre_tunnel_ids[0],
                    source_ip=static_ip_address,
                    ip_unnumbered=True,
                    comment=updated_comment,
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
            # Change the access method to attribute-style because the response is in Box format
            assert any(tunnel.id == gre_tunnel_ids[0] for tunnel in tunnels_list), "Newly created GRE Tunnel not listed"
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

    def test_traffic_list_gre_ranges(self, fs):
        client = MockZIAClient(fs)
        errors = []
        randomIP = generate_random_ip("104.239.237.0/24")
        static_ip_id = None

        # Test Case 1: With static IP
        try:
            # Create Static IP for GRE Tunnel
            try:
                created_static_ip = client.traffic.add_static_ip(
                    ip_address=randomIP, comment="tests-" + generate_random_string()
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                static_ip_id = created_static_ip["id"]
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")
                raise AssertionError(f"Precondition failed: {exc}")  # To ensure we don't proceed if static IP creation fails

            # List GRE Ranges using the created static IP
            try:
                gre_ranges_with_static_ip = client.traffic.list_gre_ranges(static_ip=static_ip_id)
                assert isinstance(gre_ranges_with_static_ip, list), "GRE ranges listing with static IP did not return a list."
                # Additional assertions based on expected values in gre_ranges_with_static_ip
            except Exception as exc:
                errors.append(f"Listing GRE ranges with static IP failed: {exc}")

        finally:
            # Cleanup: Delete the static IP if it was created
            if static_ip_id:
                try:
                    deletion_status = client.traffic.delete_static_ip(static_ip_id)
                    assert deletion_status == 204, f"Static IP deletion failed for ID {static_ip_id}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Static IP ID {static_ip_id}: {cleanup_exc}")

        # Test Case 2: Without passing static IP
        try:
            # List GRE Ranges without using static IP
            gre_ranges_without_static_ip = client.traffic.list_gre_ranges()
            assert isinstance(
                gre_ranges_without_static_ip, list
            ), "GRE ranges listing without static IP did not return a list."
            # Additional assertions based on expected values in gre_ranges_without_static_ip
        except Exception as exc:
            errors.append(f"Listing GRE ranges without static IP failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during listing GRE ranges test: {'; '.join(errors)}"

    def test_traffic_list_vips_recommended(self, fs):
        client = MockZIAClient(fs)
        errors = []
        randomIP = generate_random_ip("104.239.237.0/24")
        static_ip_id = None

        try:
            # Create Static IP for the test
            try:
                created_static_ip = client.traffic.add_static_ip(
                    ip_address=randomIP, comment="tests-" + generate_random_string()
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                static_ip_id = created_static_ip["id"]
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")
                raise AssertionError(f"Precondition failed: {exc}")  # To ensure we don't proceed if static IP creation fails

            # Fetching recommended VIPs using the created static IP
            try:
                recommended_vips = client.traffic.list_vips_recommended(source_ip=randomIP)
                assert isinstance(recommended_vips, list), "Recommended VIPs listing did not return a list."
                assert recommended_vips, "Expected non-empty list of recommended VIPs."
                # Optionally, further assertions to validate the content of recommended VIPs, if specific data is known/expected
            except Exception as exc:
                errors.append(f"Listing recommended VIPs with static IP failed: {exc}")
        finally:
            # Cleanup: Delete the static IP if it was created
            if static_ip_id:
                try:
                    deletion_status = client.traffic.delete_static_ip(static_ip_id)
                    assert deletion_status == 204, f"Static IP deletion failed for ID {static_ip_id}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Static IP ID {static_ip_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during listing recommended VIPs test: {'; '.join(errors)}"

    def test_traffic_list_vip_group_by_dc(self, fs):
        client = MockZIAClient(fs)
        errors = []
        randomIP = generate_random_ip("104.239.237.0/24")
        static_ip_id = None

        try:
            # Create Static IP for the test
            try:
                created_static_ip = client.traffic.add_static_ip(
                    ip_address=randomIP, comment="tests-" + generate_random_string()
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                static_ip_id = created_static_ip["id"]
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")
                raise AssertionError(f"Precondition failed: {exc}")  # To ensure we don't proceed if static IP creation fails

            # Fetching VIP groups by data center using the created static IP
            try:
                vip_groups = client.traffic.list_vip_group_by_dc(source_ip=randomIP)
                assert isinstance(vip_groups, list), "VIP groups listing did not return a list."
                assert vip_groups, "Expected non-empty list of VIP groups."
                # Optionally, further assertions to validate the content of VIP groups, if specific data is known/expected
            except Exception as exc:
                errors.append(f"Listing VIP group by DC failed: {exc}")
        finally:
            # Cleanup: Delete the static IP if it was created
            if static_ip_id:
                try:
                    deletion_status = client.traffic.delete_static_ip(static_ip_id)
                    assert deletion_status == 204, f"Static IP deletion failed for ID {static_ip_id}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Static IP ID {static_ip_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during listing VIP group by DC test: {'; '.join(errors)}"

    def test_traffic_get_closest_diverse_vip_ids(self, fs):
        client = MockZIAClient(fs)
        errors = []
        randomIP = generate_random_ip("104.239.237.0/24")
        static_ip_id = None

        try:
            # Create Static IP for the test
            try:
                created_static_ip = client.traffic.add_static_ip(
                    ip_address=randomIP, comment="tests-" + generate_random_string()
                )
                assert created_static_ip is not None, "Static IP creation returned None"
                static_ip_id = created_static_ip["id"]
            except Exception as exc:
                errors.append(f"Failed to add static IP: {exc}")
                raise AssertionError(f"Precondition failed: {exc}")  # To ensure we don't proceed if static IP creation fails

            # Fetching closest diverse VIP IDs using the created static IP
            try:
                closest_vips = client.traffic.get_closest_diverse_vip_ids(ip_address=randomIP)
                assert isinstance(closest_vips, tuple), "Fetching closest diverse VIP IDs did not return a tuple."
                assert len(closest_vips) == 2, "Expected two VIP IDs."
                # Optionally, further assertions to validate the VIP IDs, if specific IDs are known/expected
            except Exception as exc:
                errors.append(f"Getting closest diverse VIP IDs failed: {exc}")
        finally:
            # Cleanup: Delete the static IP if it was created
            if static_ip_id:
                try:
                    deletion_status = client.traffic.delete_static_ip(static_ip_id)
                    assert deletion_status == 204, f"Static IP deletion failed for ID {static_ip_id}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Static IP ID {static_ip_id}: {cleanup_exc}")

        assert len(errors) == 0, f"Errors occurred during getting closest diverse VIP IDs test: {'; '.join(errors)}"

    def test_traffic_list_vips(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            # Example test with max_items=10
            vips = client.traffic.list_vips(max_items=10)
            assert (
                isinstance(vips, list) and len(vips) <= 10
            ), "Listing VIPs with max_items=10 did not return a list of max 10 items."

            # Example test with page_size=200, max_pages=2
            vips_large = client.traffic.list_vips(page_size=200, max_pages=2)
            assert isinstance(vips_large, list), "Listing VIPs with page_size=200, max_pages=2 did not return a list."
            # Additional assertions based on expected values in vips_large
        except Exception as exc:
            errors.append(f"Listing VIPs with specific parameters failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during listing VIPs test: {'; '.join(errors)}"
