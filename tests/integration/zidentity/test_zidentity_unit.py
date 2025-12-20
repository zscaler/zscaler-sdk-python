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
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def fs():
    yield


class TestGroupsUnit:
    """
    Unit Tests for the ZIdentity Groups API to increase coverage
    """

    def test_list_groups_request_error(self, fs):
        """Test list_groups handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.list_groups()
        
        assert result is None
        assert err is not None

    def test_list_groups_execute_error(self, fs):
        """Test list_groups handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.list_groups()
        
        assert result is None
        assert err is not None

    def test_get_group_request_error(self, fs):
        """Test get_group handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.get_group(group_id=123)
        
        assert result is None
        assert err is not None

    def test_get_group_execute_error(self, fs):
        """Test get_group handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.get_group(group_id=123)
        
        assert result is None
        assert err is not None

    def test_add_group_request_error(self, fs):
        """Test add_group handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_group(name="Test Group")
        
        assert result is None
        assert err is not None

    def test_add_group_execute_error(self, fs):
        """Test add_group handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_group(name="Test Group")
        
        assert result is None
        assert err is not None

    def test_update_group_request_error(self, fs):
        """Test update_group handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.update_group(group_id="123", name="Updated Group")
        
        assert result is None
        assert err is not None

    def test_update_group_execute_error(self, fs):
        """Test update_group handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.update_group(group_id="123", name="Updated Group")
        
        assert result is None
        assert err is not None

    def test_delete_group_request_error(self, fs):
        """Test delete_group handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.delete_group(group_id="123")
        
        assert result is None
        assert err is not None

    def test_delete_group_execute_error(self, fs):
        """Test delete_group handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.delete_group(group_id="123")
        
        assert result is None
        assert err is not None

    def test_list_group_users_details_request_error(self, fs):
        """Test list_group_users_details handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.list_group_users_details(group_id="123")
        
        assert result is None
        assert err is not None

    def test_list_group_users_details_execute_error(self, fs):
        """Test list_group_users_details handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.list_group_users_details(group_id="123")
        
        assert result is None
        assert err is not None

    def test_add_user_to_group_request_error(self, fs):
        """Test add_user_to_group handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_user_to_group(group_id="123", user_id="456")
        
        assert result is None
        assert err is not None

    def test_add_user_to_group_execute_error(self, fs):
        """Test add_user_to_group handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_user_to_group(group_id="123", user_id="456")
        
        assert result is None
        assert err is not None

    def test_add_users_to_group_request_error(self, fs):
        """Test add_users_to_group handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_users_to_group(group_id="123", id=["456", "789"])
        
        assert result is None
        assert err is not None

    def test_add_users_to_group_execute_error(self, fs):
        """Test add_users_to_group handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_users_to_group(group_id="123", id=["456", "789"])
        
        assert result is None
        assert err is not None

    def test_replace_users_groups_request_error(self, fs):
        """Test replace_users_groups handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.replace_users_groups(group_id="123", id=["456", "789"])
        
        assert result is None
        assert err is not None

    def test_replace_users_groups_execute_error(self, fs):
        """Test replace_users_groups handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.replace_users_groups(group_id="123", id=["456", "789"])
        
        assert result is None
        assert err is not None

    def test_remove_user_from_group_request_error(self, fs):
        """Test remove_user_from_group handles request creation errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.remove_user_from_group(group_id="123", user_id="456")
        
        assert result is None
        assert err is not None

    def test_remove_user_from_group_execute_error(self, fs):
        """Test remove_user_from_group handles execution errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.remove_user_from_group(group_id="123", user_id="456")
        
        assert result is None
        assert err is not None


class TestUsersUnit:
    """
    Unit Tests for the ZIdentity Users API to increase coverage
    """

    def test_list_users_request_error(self, fs):
        """Test list_users handles request creation errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_users()
        
        assert result is None
        assert err is not None

    def test_list_users_execute_error(self, fs):
        """Test list_users handles execution errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_users()
        
        assert result is None
        assert err is not None

    def test_get_user_request_error(self, fs):
        """Test get_user handles request creation errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.get_user(user_id="123")
        
        assert result is None
        assert err is not None

    def test_get_user_execute_error(self, fs):
        """Test get_user handles execution errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.get_user(user_id="123")
        
        assert result is None
        assert err is not None

    def test_add_user_request_error(self, fs):
        """Test add_user handles request creation errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.add_user(login_name="test@example.com")
        
        assert result is None
        assert err is not None

    def test_add_user_execute_error(self, fs):
        """Test add_user handles execution errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.add_user(login_name="test@example.com")
        
        assert result is None
        assert err is not None

    def test_update_user_request_error(self, fs):
        """Test update_user handles request creation errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.update_user(user_id="123", login_name="updated@example.com")
        
        assert result is None
        assert err is not None

    def test_update_user_execute_error(self, fs):
        """Test update_user handles execution errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.update_user(user_id="123", login_name="updated@example.com")
        
        assert result is None
        assert err is not None

    def test_delete_user_request_error(self, fs):
        """Test delete_user handles request creation errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.delete_user(user_id="123")
        
        assert result is None
        assert err is not None

    def test_delete_user_execute_error(self, fs):
        """Test delete_user handles execution errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.delete_user(user_id="123")
        
        assert result is None
        assert err is not None

    def test_list_user_group_details_request_error(self, fs):
        """Test list_user_group_details handles request creation errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_user_group_details(user_id="123")
        
        assert result is None
        assert err is not None

    def test_list_user_group_details_execute_error(self, fs):
        """Test list_user_group_details handles execution errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_user_group_details(user_id="123")
        
        assert result is None
        assert err is not None


class TestUserEntitlementUnit:
    """
    Unit Tests for the ZIdentity User Entitlement API to increase coverage
    """

    def test_get_admin_entitlement_request_error(self, fs):
        """Test get_admin_entitlement handles request creation errors correctly"""
        from zscaler.zidentity.user_entitlement import EntitlementAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_admin_entitlement(user_id="123")
        
        assert result is None
        assert err is not None

    def test_get_admin_entitlement_execute_error(self, fs):
        """Test get_admin_entitlement handles execution errors correctly"""
        from zscaler.zidentity.user_entitlement import EntitlementAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_admin_entitlement(user_id="123")
        
        assert result is None
        assert err is not None

    def test_get_service_entitlement_request_error(self, fs):
        """Test get_service_entitlement handles request creation errors correctly"""
        from zscaler.zidentity.user_entitlement import EntitlementAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_service_entitlement(user_id="123")
        
        assert result is None
        assert err is not None

    def test_get_service_entitlement_execute_error(self, fs):
        """Test get_service_entitlement handles execution errors correctly"""
        from zscaler.zidentity.user_entitlement import EntitlementAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_service_entitlement(user_id="123")
        
        assert result is None
        assert err is not None


class TestResourceServersUnit:
    """
    Unit Tests for the ZIdentity Resource Servers API to increase coverage
    """

    def test_list_resource_servers_request_error(self, fs):
        """Test list_resource_servers handles request creation errors correctly"""
        from zscaler.zidentity.resource_servers import ResourceServersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        rs_api = ResourceServersAPI(mock_executor)
        result, response, err = rs_api.list_resource_servers()
        
        assert result is None
        assert err is not None

    def test_list_resource_servers_execute_error(self, fs):
        """Test list_resource_servers handles execution errors correctly"""
        from zscaler.zidentity.resource_servers import ResourceServersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        rs_api = ResourceServersAPI(mock_executor)
        result, response, err = rs_api.list_resource_servers()
        
        assert result is None
        assert err is not None

    def test_list_resource_servers_parsing_error(self, fs):
        """Test list_resource_servers handles parsing errors correctly"""
        from zscaler.zidentity.resource_servers import ResourceServersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        rs_api = ResourceServersAPI(mock_executor)
        result, response, err = rs_api.list_resource_servers()
        
        assert result is None
        assert err is not None

    def test_get_resource_server_request_error(self, fs):
        """Test get_resource_server handles request creation errors correctly"""
        from zscaler.zidentity.resource_servers import ResourceServersAPI
        
        mock_executor = Mock()
        mock_executor.create_request = Mock(return_value=(None, Exception("Request error")))
        
        rs_api = ResourceServersAPI(mock_executor)
        result, response, err = rs_api.get_resource_server(resource_id="123")
        
        assert result is None
        assert err is not None

    def test_get_resource_server_execute_error(self, fs):
        """Test get_resource_server handles execution errors correctly"""
        from zscaler.zidentity.resource_servers import ResourceServersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        mock_executor.execute = Mock(return_value=(None, Exception("Execution error")))
        
        rs_api = ResourceServersAPI(mock_executor)
        result, response, err = rs_api.get_resource_server(resource_id="123")
        
        assert result is None
        assert err is not None

    def test_get_resource_server_parsing_error(self, fs):
        """Test get_resource_server handles parsing errors correctly"""
        from zscaler.zidentity.resource_servers import ResourceServersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        rs_api = ResourceServersAPI(mock_executor)
        result, response, err = rs_api.get_resource_server(resource_id="123")
        
        assert result is None
        assert err is not None


class TestZIdentityServiceUnit:
    """
    Unit Tests for the ZIdentity Service to increase coverage
    """

    def test_zidentity_service_properties(self, fs):
        """Test ZIdentityService property accessors"""
        from zscaler.zidentity.zidentity_service import ZIdentityService
        from zscaler.zidentity.groups import GroupsAPI
        from zscaler.zidentity.users import UsersAPI
        from zscaler.zidentity.resource_servers import ResourceServersAPI
        from zscaler.zidentity.user_entitlement import EntitlementAPI
        
        mock_executor = Mock()
        
        service = ZIdentityService(mock_executor)
        
        # Test all API properties return correct types
        assert isinstance(service.groups, GroupsAPI)
        assert isinstance(service.users, UsersAPI)
        assert isinstance(service.resource_servers, ResourceServersAPI)
        assert isinstance(service.user_entitlement, EntitlementAPI)


class TestGroupsParsingErrors:
    """
    Tests for Groups API response parsing errors
    """

    def test_list_groups_parsing_error(self, fs):
        """Test list_groups handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.list_groups()
        
        assert result is None
        assert err is not None

    def test_get_group_parsing_error(self, fs):
        """Test get_group handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.get_group(group_id=123)
        
        assert result is None
        assert err is not None

    def test_add_group_parsing_error(self, fs):
        """Test add_group handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_group(name="Test Group")
        
        assert result is None
        assert err is not None

    def test_update_group_parsing_error(self, fs):
        """Test update_group handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.update_group(group_id="123", name="Updated Group")
        
        assert result is None
        assert err is not None

    def test_list_group_users_details_parsing_error(self, fs):
        """Test list_group_users_details handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.list_group_users_details(group_id="123")
        
        assert result is None
        assert err is not None

    def test_add_user_to_group_parsing_error(self, fs):
        """Test add_user_to_group handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_user_to_group(group_id="123", user_id="456")
        
        assert result is None
        assert err is not None

    def test_add_users_to_group_parsing_error(self, fs):
        """Test add_users_to_group handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.add_users_to_group(group_id="123", id=["456", "789"])
        
        assert result is None
        assert err is not None

    def test_replace_users_groups_parsing_error(self, fs):
        """Test replace_users_groups handles parsing errors correctly"""
        from zscaler.zidentity.groups import GroupsAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        groups_api = GroupsAPI(mock_executor)
        result, response, err = groups_api.replace_users_groups(group_id="123", id=["456", "789"])
        
        assert result is None
        assert err is not None


class TestUserEntitlementParsingErrors:
    """
    Tests for User Entitlement API response parsing errors
    """

    def test_get_admin_entitlement_parsing_error(self, fs):
        """Test get_admin_entitlement handles parsing errors correctly"""
        from zscaler.zidentity.user_entitlement import EntitlementAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_admin_entitlement(user_id="123")
        
        assert result is None
        assert err is not None

    def test_get_service_entitlement_parsing_error(self, fs):
        """Test get_service_entitlement handles parsing errors correctly"""
        from zscaler.zidentity.user_entitlement import EntitlementAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        ent_api = EntitlementAPI(mock_executor)
        result, response, err = ent_api.get_service_entitlement(user_id="123")
        
        assert result is None
        assert err is not None


class TestUsersParsingErrors:
    """
    Tests for Users API response parsing errors
    """

    def test_list_users_parsing_error(self, fs):
        """Test list_users handles parsing errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_users()
        
        assert result is None
        assert err is not None

    def test_get_user_parsing_error(self, fs):
        """Test get_user handles parsing errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.get_user(user_id="123")
        
        assert result is None
        assert err is not None

    def test_add_user_parsing_error(self, fs):
        """Test add_user handles parsing errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.add_user(login_name="test@example.com")
        
        assert result is None
        assert err is not None

    def test_update_user_parsing_error(self, fs):
        """Test update_user handles parsing errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error
        mock_response = Mock()
        mock_response.get_body = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.update_user(user_id="123", login_name="updated@example.com")
        
        assert result is None
        assert err is not None

    def test_list_user_group_details_parsing_error(self, fs):
        """Test list_user_group_details handles parsing errors correctly"""
        from zscaler.zidentity.users import UsersAPI
        
        mock_executor = Mock()
        mock_request = Mock()
        mock_executor.create_request = Mock(return_value=(mock_request, None))
        
        # Mock response that causes parsing error - get_results raises exception
        mock_response = Mock()
        mock_response.get_results = Mock(side_effect=Exception("Parsing error"))
        mock_executor.execute = Mock(return_value=(mock_response, None))
        
        users_api = UsersAPI(mock_executor)
        result, response, err = users_api.list_user_group_details(user_id="123")
        
        assert result is None
        assert err is not None

