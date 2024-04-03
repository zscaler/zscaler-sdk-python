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
from tests.test_utils import generate_random_string

@pytest.fixture
def fs():
    yield

class TestCloudFirewallIPSourceGroup:
    """
    Integration Tests for the Cloud Firewall IP Source Group.
    """
    
    @pytest.mark.asyncio
    async def test_add_ip_source_group(self, fs):
        client = MockZIAClient(fs)
        group_name = "tests-" + generate_random_string()
        group_description = "tests-" + generate_random_string()
        try:
            created_group = client.firewall.add_ip_source_group(
                name=group_name,
                description=group_description,
                ip_addresses=[ "192.168.100.1", "192.168.100.2", "192.168.100.3"],
            )
            assert created_group.name == group_name, "Group name mismatch in creation"
            assert created_group.description == group_description, "Group description mismatch in creation"
            global created_group_id  # For cleanup
            created_group_id = created_group.id
        except Exception as exc:
            pytest.fail(f"Failed to add IP source group: {exc}")

    @pytest.mark.asyncio
    async def test_get_ip_source_group(self, fs):
        client = MockZIAClient(fs)
        try:
            group = client.firewall.get_ip_source_group(created_group_id)
            assert group.id == created_group_id, "Failed to retrieve the correct IP source group"
        except Exception as exc:
            pytest.fail(f"Failed to retrieve IP source group: {exc}")

    @pytest.mark.asyncio
    async def test_update_ip_source_group(self, fs):
        client = MockZIAClient(fs)
        updated_name = "updated-" + generate_random_string()
        try:
            client.firewall.update_ip_source_group(
                group_id=created_group_id,
                name=updated_name
            )
            updated_group = client.firewall.get_ip_source_group(created_group_id)
            assert updated_group.name == updated_name, "Group name mismatch after update"
        except Exception as exc:
            pytest.fail(f"Failed to update IP source group: {exc}")

    @pytest.mark.asyncio
    async def test_list_ip_source_groups(self, fs):
        client = MockZIAClient(fs)
        try:
            groups = client.firewall.list_ip_source_groups()
            assert isinstance(groups, list), "Failed to list IP source groups"
            assert any(group.id == created_group_id for group in groups), "Created group not found in list"
        except Exception as exc:
            pytest.fail(f"Failed to list IP source groups: {exc}")

    @pytest.mark.asyncio
    async def test_delete_ip_source_group(self, fs):
        client = MockZIAClient(fs)
        try:
            status_code = client.firewall.delete_ip_source_group(created_group_id)
            assert status_code == 204, "Failed to delete IP source group"
        except Exception as exc:
            pytest.fail(f"Failed to delete IP source group: {exc}")

@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    """Cleanup the created resources after tests"""
    def remove_created_group():
        try:
            client = MockZIAClient()
            client.firewall.delete_ip_source_group(created_group_id)
        except Exception:
            pass  # Handle cleanup failure silently
    request.addfinalizer(remove_created_group)
