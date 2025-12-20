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


@pytest.fixture
def fs():
    yield


class TestCloudFirewall:
    """
    Integration Tests for the Cloud Firewall API.
    """

    @pytest.mark.vcr()
    def test_cloud_firewall_operations(self, fs):
        """Test Cloud Firewall operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_ip_destination_groups
            dest_groups, response, err = client.zia.cloud_firewall.list_ip_destination_groups()
            assert err is None, f"List IP destination groups failed: {err}"
            assert dest_groups is not None, "Destination groups should not be None"
            assert isinstance(dest_groups, list), "Destination groups should be a list"

            # Test list_ip_destination_groups_lite
            dest_groups_lite, response, err = client.zia.cloud_firewall.list_ip_destination_groups_lite()
            assert err is None, f"List IP destination groups lite failed: {err}"

            # Test list_ipv6_destination_groups
            ipv6_dest_groups, response, err = client.zia.cloud_firewall.list_ipv6_destination_groups()
            assert err is None, f"List IPv6 destination groups failed: {err}"

            # Test list_ipv6_destination_groups_lite
            ipv6_dest_lite, response, err = client.zia.cloud_firewall.list_ipv6_destination_groups_lite()
            assert err is None, f"List IPv6 destination groups lite failed: {err}"

            # Test get_ip_destination_group if available
            if dest_groups and len(dest_groups) > 0:
                group_id = dest_groups[0].id
                fetched_group, response, err = client.zia.cloud_firewall.get_ip_destination_group(group_id)
                assert err is None, f"Get IP destination group failed: {err}"

            # Test list_ip_source_groups
            src_groups, response, err = client.zia.cloud_firewall.list_ip_source_groups()
            assert err is None, f"List IP source groups failed: {err}"
            assert src_groups is not None, "Source groups should not be None"

            # Test list_ip_source_groups_lite
            src_groups_lite, response, err = client.zia.cloud_firewall.list_ip_source_groups_lite()
            assert err is None, f"List IP source groups lite failed: {err}"

            # Test list_ipv6_source_groups
            ipv6_src_groups, response, err = client.zia.cloud_firewall.list_ipv6_source_groups()
            assert err is None, f"List IPv6 source groups failed: {err}"

            # Test list_ipv6_source_groups_lite
            ipv6_src_lite, response, err = client.zia.cloud_firewall.list_ipv6_source_groups_lite()
            assert err is None, f"List IPv6 source groups lite failed: {err}"

            # Test get_ip_source_group if available
            if src_groups and len(src_groups) > 0:
                src_id = src_groups[0].id
                fetched_src, response, err = client.zia.cloud_firewall.get_ip_source_group(src_id)
                assert err is None, f"Get IP source group failed: {err}"

            # Test list_network_app_groups
            app_groups, response, err = client.zia.cloud_firewall.list_network_app_groups()
            assert err is None, f"List network app groups failed: {err}"
            assert app_groups is not None, "App groups should not be None"

            # Test get_network_app_group if available
            if app_groups and len(app_groups) > 0:
                app_group_id = app_groups[0].id
                fetched_app_group, response, err = client.zia.cloud_firewall.get_network_app_group(app_group_id)
                assert err is None, f"Get network app group failed: {err}"

            # Test list_network_apps
            apps, response, err = client.zia.cloud_firewall.list_network_apps()
            assert err is None, f"List network apps failed: {err}"
            assert apps is not None, "Network apps should not be None"

            # Test get_network_app if available
            if apps and len(apps) > 0:
                app_id = apps[0].id
                fetched_app, response, err = client.zia.cloud_firewall.get_network_app(app_id)
                assert err is None, f"Get network app failed: {err}"

            # Test list_network_svc_groups
            svc_groups, response, err = client.zia.cloud_firewall.list_network_svc_groups()
            assert err is None, f"List network service groups failed: {err}"
            assert svc_groups is not None, "Service groups should not be None"

            # Test list_network_svc_groups_lite
            svc_groups_lite, response, err = client.zia.cloud_firewall.list_network_svc_groups_lite()
            assert err is None, f"List network service groups lite failed: {err}"

            # Test get_network_svc_group if available
            if svc_groups and len(svc_groups) > 0:
                svc_id = svc_groups[0].id
                fetched_svc, response, err = client.zia.cloud_firewall.get_network_svc_group(svc_id)
                assert err is None, f"Get network service group failed: {err}"

        except Exception as e:
            errors.append(f"Exception during cloud firewall test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

