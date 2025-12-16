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
from zscaler.zinsights.models.enums import SortOrder
from zscaler.zinsights.models.inputs import (
    OrderByInput, StringFilter,
    WebEntriesFilterBy, WebOrderBy,
    CasbEntriesFilterBy, CasbEntryOrderBy,
    CyberSecurityEntriesFilterBy, CyberSecurityEntryOrderBy,
    FirewallEntriesFilterBy, FirewallEntryOrderBy,
    ShadowITAppsFilterBy, ShadowITAppsOrderBy,
    ShadowITEntriesFilterBy, ShadowITEntryOrderBy,
    IoTDeviceFilterBy, IoTDeviceOrderBy,
    CasbIncidentFilterBy, TimeRangeInput
)


class TestOrderByInput:
    """
    Tests for OrderByInput base class
    """

    def test_order_by_input(self):
        order_by = OrderByInput(field_name="test_field", order=SortOrder.ASC)
        assert order_by.field_name == "test_field"
        assert order_by.order == SortOrder.ASC
        
        # Test as_dict
        result = order_by.as_dict()
        assert result == {"field_name": "test_field", "order": "ASC"}
        
        # Test to_graphql
        gql = order_by.to_graphql()
        assert "test_field" in gql
        assert "ASC" in gql


class TestFiltersComprehensive:
    """
    Comprehensive tests for all filter types
    """

    def test_web_entries_filter_by_none(self):
        filter_by = WebEntriesFilterBy()
        result = filter_by.as_dict()
        assert result is None

    def test_casb_entries_filter_by(self):
        filter_by = CasbEntriesFilterBy(name=StringFilter(eq="AppName"))
        result = filter_by.as_dict()
        assert result == {"name": {"eq": "AppName"}}

    def test_casb_entry_order_by(self):
        order_by = CasbEntryOrderBy(name=SortOrder.ASC)
        result = order_by.as_dict()
        assert result == {"name": "ASC"}

    def test_casb_entry_order_by_both(self):
        order_by = CasbEntryOrderBy(name=SortOrder.ASC, total=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"name": "ASC", "total": "DESC"}

    def test_cyber_security_entries_filter_by(self):
        filter_by = CyberSecurityEntriesFilterBy(name=StringFilter(ne="Exclude"))
        result = filter_by.as_dict()
        assert result == {"name": {"ne": "Exclude"}}

    def test_cyber_security_entry_order_by(self):
        order_by = CyberSecurityEntryOrderBy(total=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"total": "DESC"}

    def test_firewall_entries_filter_by_none(self):
        filter_by = FirewallEntriesFilterBy()
        result = filter_by.as_dict()
        assert result is None

    def test_shadow_it_entries_filter_by(self):
        filter_by = ShadowITEntriesFilterBy(name=StringFilter(eq="Category1"))
        result = filter_by.as_dict()
        assert result == {"name": {"eq": "Category1"}}

    def test_shadow_it_entry_order_by(self):
        order_by = ShadowITEntryOrderBy(name=SortOrder.ASC, total=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"name": "ASC", "total": "DESC"}

    def test_shadow_it_apps_filter_by_full(self):
        filter_by = ShadowITAppsFilterBy(
            application=StringFilter(eq="App1"),
            application_category=StringFilter(ne="Games"),
            sanctioned_state=StringFilter(in_list=["SANCTIONED"])
        )
        result = filter_by.as_dict()
        assert "application" in result
        assert "application_category" in result
        assert "sanctioned_state" in result

    def test_shadow_it_apps_filter_by_empty(self):
        filter_by = ShadowITAppsFilterBy()
        result = filter_by.as_dict()
        assert result is None

    def test_shadow_it_apps_order_by_single(self):
        order_by = ShadowITAppsOrderBy(risk_index=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"risk_index": "DESC"}

    def test_shadow_it_apps_order_by_multiple(self):
        order_by = ShadowITAppsOrderBy(
            application=SortOrder.ASC,
            computed_risk_index=SortOrder.DESC
        )
        result = order_by.as_dict()
        assert "application" in result
        assert "computed_risk_index" in result

    def test_iot_device_filter_by_single(self):
        filter_by = IoTDeviceFilterBy(category=StringFilter(eq="Camera"))
        result = filter_by.as_dict()
        assert result == {"category": {"eq": "Camera"}}

    def test_iot_device_filter_by_multiple(self):
        filter_by = IoTDeviceFilterBy(
            classifications=StringFilter(in_list=["Class1", "Class2"]),
            category=StringFilter(ne="Unknown")
        )
        result = filter_by.as_dict()
        assert "classifications" in result
        assert "category" in result

    def test_iot_device_filter_by_empty(self):
        filter_by = IoTDeviceFilterBy()
        result = filter_by.as_dict()
        assert result is None

    def test_iot_device_order_by_single(self):
        order_by = IoTDeviceOrderBy(total=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"total": "DESC"}

    def test_casb_incident_filter_by(self):
        filter_by = CasbIncidentFilterBy(policy="Test Policy", app_name="Test App")
        result = filter_by.as_dict()
        assert result == {"policy": "Test Policy", "app_name": "Test App"}
        
        # Test to_graphql
        gql = filter_by.to_graphql()
        assert "policy" in gql
        assert "app_name" in gql

