"""
Unit tests for Zscaler model instantiation across all services.

Tests model creation with different input types:
- Plain dictionaries
- Model objects
- Nested model objects with collections
"""

import pytest
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection

# Import models from all services
from zscaler.zia.models import location_management, rule_labels, admin_users
from zscaler.zpa.models import segment_group, application_segment, app_connector_groups
from zscaler.zdx.models import devices as zdx_devices, users as zdx_users
from zscaler.zcc.models import devices as zcc_devices
from zscaler.ztw.models import location_management as ztw_location_management
from zscaler.zidentity.models import users as zidentity_users, groups as zidentity_groups
from zscaler.zwa.models import common as zwa_common


class TestZscalerObjectBaseClass:
    """Test the base ZscalerObject functionality."""

    def test_zscaler_object_initialization_empty(self):
        """Test ZscalerObject can be instantiated with no config."""
        obj = ZscalerObject()
        assert obj is not None

    def test_zscaler_object_initialization_with_config(self):
        """Test ZscalerObject can be instantiated with config."""
        config = {"id": "123", "name": "test"}
        obj = ZscalerObject(config)
        assert obj is not None

    def test_zscaler_object_repr(self):
        """Test ZscalerObject string representation."""
        obj = ZscalerObject()
        repr_str = repr(obj)
        assert isinstance(repr_str, str)

    def test_zscaler_object_getitem(self):
        """Test ZscalerObject __getitem__ method."""
        obj = ZscalerObject()
        obj.test_attr = "test_value"
        assert obj["test_attr"] == "test_value"

    def test_zscaler_object_getitem_missing_key(self):
        """Test ZscalerObject __getitem__ raises KeyError for missing key."""
        obj = ZscalerObject()
        with pytest.raises(KeyError):
            _ = obj["missing_key"]

    def test_zscaler_object_contains(self):
        """Test ZscalerObject __contains__ method."""
        obj = ZscalerObject()
        obj.test_attr = "test_value"
        assert "test_attr" in obj
        assert "missing_attr" not in obj

    def test_zscaler_object_get_method(self):
        """Test ZscalerObject get method with default."""
        obj = ZscalerObject()
        obj.test_attr = "test_value"
        assert obj.get("test_attr") == "test_value"
        assert obj.get("missing_attr", "default") == "default"
        assert obj.get("missing_attr") is None


class TestZscalerCollectionClass:
    """Test the ZscalerCollection functionality."""

    def test_form_list_empty(self):
        """Test ZscalerCollection.form_list with empty list."""
        result = ZscalerCollection.form_list([], ZscalerObject)
        assert result == []

    def test_form_list_none(self):
        """Test ZscalerCollection.form_list with None."""
        result = ZscalerCollection.form_list(None, ZscalerObject)
        assert result == []

    def test_form_list_with_dicts(self):
        """Test ZscalerCollection.form_list converts dicts to objects."""
        input_list = [{"id": "1"}, {"id": "2"}]
        result = ZscalerCollection.form_list(input_list, ZscalerObject)
        assert len(result) == 2
        assert all(isinstance(item, ZscalerObject) for item in result)

    def test_is_formed(self):
        """Test ZscalerCollection.is_formed method."""
        obj = ZscalerObject()
        assert ZscalerCollection.is_formed(obj, ZscalerObject) is True
        assert ZscalerCollection.is_formed({}, ZscalerObject) is False


class TestZIAModels:
    """Test ZIA model instantiation."""

    @pytest.mark.parametrize(
        "model_class,config",
        [
            (
                location_management.LocationManagement,
                {
                    "id": 123456,
                    "name": "Test Location",
                    "description": "Test Description",
                    "country": "US",
                    "tz": "America/Los_Angeles",
                },
            ),
            (
                rule_labels.RuleLabels,
                {"id": 123, "name": "Test Label", "description": "Test Description"},
            ),
            (
                admin_users.AdminUser,
                {
                    "id": 123,
                    "loginName": "admin@example.com",
                    "userName": "Admin User",
                    "email": "admin@example.com",
                },
            ),
        ],
    )
    def test_zia_model_instantiation_from_dict(self, model_class, config):
        """Test ZIA models can be instantiated from dictionaries."""
        model = model_class(config)
        assert model is not None
        assert isinstance(model, ZscalerObject)
        assert model.id == config["id"]
        # Check name attribute if it exists (not all models have 'name')
        if "name" in config:
            assert model.name == config["name"]

    def test_zia_location_instantiation_with_model(self):
        """Test ZIA Location can be instantiated from model object."""
        config = {
            "id": 123456,
            "name": "Test Location",
            "description": "Test Description",
        }
        # Create model from dict
        location1 = location_management.LocationManagement(config)
        
        # Create another model from the first model's attributes
        location2 = location_management.LocationManagement(
            {"id": location1.id, "name": location1.name, "description": location1.description}
        )
        
        assert location1.id == location2.id
        assert location1.name == location2.name


class TestZPAModels:
    """Test ZPA model instantiation."""

    @pytest.mark.parametrize(
        "model_class,config",
        [
            (
                segment_group.SegmentGroup,
                {
                    "id": "123456",
                    "name": "Test Segment Group",
                    "description": "Test Description",
                    "enabled": True,
                },
            ),
            (
                app_connector_groups.AppConnectorGroup,
                {
                    "id": "123456",
                    "name": "Test Connector Group",
                    "description": "Test Description",
                    "enabled": True,
                    "cityCountry": "San Jose, US",
                    "countryCode": "US",
                },
            ),
        ],
    )
    def test_zpa_model_instantiation_from_dict(self, model_class, config):
        """Test ZPA models can be instantiated from dictionaries."""
        model = model_class(config)
        assert model is not None
        assert isinstance(model, ZscalerObject)
        assert model.id == config["id"]
        assert model.name == config["name"]

    def test_zpa_segment_group_with_nested_collections(self):
        """Test ZPA SegmentGroup with nested application segments."""
        config = {
            "id": "123456",
            "name": "Test Segment Group",
            "description": "Test Description",
            "enabled": True,
            "applications": [
                {"id": "app1", "name": "App 1"},
                {"id": "app2", "name": "App 2"},
            ],
        }
        
        segment_group_obj = segment_group.SegmentGroup(config)
        assert segment_group_obj is not None
        assert segment_group_obj.id == "123456"
        assert segment_group_obj.name == "Test Segment Group"


class TestZDXModels:
    """Test ZDX model instantiation."""

    def test_zdx_device_detail_instantiation(self):
        """Test ZDX DeviceDetail model instantiation."""
        config = {
            "id": "device123",
            "name": "Test Device",
            "os_type": "Windows",
            "os_version": "10",
        }
        
        device = zdx_devices.DeviceDetail(config)
        assert device is not None
        assert isinstance(device, ZscalerObject)

    def test_zdx_devices_collection(self):
        """Test ZDX Devices model with collection."""
        config = {
            "next_offset": "100",
            "devices": [
                {"id": "device1", "name": "Device 1"},
                {"id": "device2", "name": "Device 2"},
            ],
        }
        
        devices_obj = zdx_devices.Devices(config)
        assert devices_obj is not None
        assert devices_obj.next_offset == "100"
        assert len(devices_obj.devices) == 2


class TestZCCModels:
    """Test ZCC model instantiation."""

    def test_zcc_device_instantiation(self):
        """Test ZCC Device model instantiation."""
        config = {
            "deviceId": "12345",
            "osVersion": "Windows 10",
            "platform": "windows",
        }
        
        device = zcc_devices.Device(config)
        assert device is not None
        assert isinstance(device, ZscalerObject)


class TestZTWModels:
    """Test ZTW model instantiation."""

    def test_ztw_location_instantiation(self):
        """Test ZTW LocationManagement model instantiation."""
        config = {
            "id": "12345",
            "name": "Test ZTW Location",
            "description": "Test Description",
        }
        
        location = ztw_location_management.LocationManagement(config)
        assert location is not None
        assert isinstance(location, ZscalerObject)
        assert location.id == "12345"
        assert location.name == "Test ZTW Location"


class TestZIdentityModels:
    """Test ZIdentity model instantiation."""

    def test_zidentity_user_instantiation(self):
        """Test ZIdentity User model instantiation."""
        config = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
        }
        
        user = zidentity_users.UserRecord(config)
        assert user is not None
        assert isinstance(user, ZscalerObject)

    def test_zidentity_group_instantiation(self):
        """Test ZIdentity Group model instantiation."""
        config = {
            "id": "group123",
            "name": "Test Group",
            "description": "Test Description",
        }
        
        group = zidentity_groups.GroupRecord(config)
        assert group is not None
        assert isinstance(group, ZscalerObject)


class TestZWAModels:
    """Test ZWA model instantiation."""

    def test_zwa_common_pagination_instantiation(self):
        """Test ZWA Pagination model instantiation."""
        config = {
            "cursor": "next_page_cursor",
        }
        
        pagination = zwa_common.Pagination(config)
        assert pagination is not None
        assert isinstance(pagination, ZscalerObject)


class TestModelEdgeCases:
    """Test edge cases for model instantiation."""

    def test_model_instantiation_with_none_config(self):
        """Test models can handle None config."""
        location = location_management.LocationManagement(None)
        assert location is not None

    def test_model_instantiation_with_empty_dict(self):
        """Test models can handle empty dictionary."""
        location = location_management.LocationManagement({})
        assert location is not None

    def test_model_instantiation_with_missing_optional_fields(self):
        """Test models handle missing optional fields gracefully."""
        config = {"id": 123, "name": "Test"}  # Missing description and other fields
        location = location_management.LocationManagement(config)
        assert location is not None
        assert location.id == 123
        assert location.name == "Test"

    def test_model_with_camelcase_and_snake_case(self):
        """Test models handle both camelCase (API format) and snake_case."""
        config = {
            "id": "123",
            "name": "Test",
            "nonEditable": True,  # camelCase from API
            "parentId": "456",  # camelCase from API
        }
        location = location_management.LocationManagement(config)
        assert location is not None
        assert location.non_editable is True
        assert location.parent_id == "456"

