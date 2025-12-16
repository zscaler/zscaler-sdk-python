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
from zscaler.zinsights.models.enums import (
    SortOrder, WebTrafficUnits, TrendInterval,
    IncidentsGroupBy, ActionStatus
)
from zscaler.zinsights.models.inputs import (
    StringFilter, WebEntriesFilterBy, WebOrderBy,
    FirewallEntriesFilterBy, FirewallEntryOrderBy,
    CasbEntriesFilterBy, CasbEntryOrderBy,
    CyberSecurityEntriesFilterBy, CyberSecurityEntryOrderBy,
    ShadowITAppsFilterBy, ShadowITAppsOrderBy,
    IoTDeviceFilterBy, IoTDeviceOrderBy,
    TimeRangeInput
)


class TestEnums:
    """
    Tests for Z-Insights enum types
    """

    def test_sort_order(self):
        assert SortOrder.ASC.value == "ASC"
        assert SortOrder.DESC.value == "DESC"

    def test_web_traffic_units(self):
        assert WebTrafficUnits.TRANSACTIONS.value == "TRANSACTIONS"
        assert WebTrafficUnits.BYTES.value == "BYTES"

    def test_trend_interval(self):
        assert TrendInterval.DAY.value == "DAY"
        assert TrendInterval.HOUR.value == "HOUR"

    def test_incidents_group_by(self):
        assert IncidentsGroupBy.THREAT_CATEGORY_ID.value == "THREAT_CATEGORY_ID"
        assert IncidentsGroupBy.APP_ID.value == "APP_ID"

    def test_action_status(self):
        assert ActionStatus.ALLOW.value == "ALLOW"
        assert ActionStatus.BLOCK.value == "BLOCK"


class TestStringFilter:
    """
    Tests for StringFilter input type
    """

    def test_string_filter_eq(self):
        sf = StringFilter(eq="test_value")
        result = sf.as_dict()
        assert result == {"eq": "test_value"}

    def test_string_filter_ne(self):
        sf = StringFilter(ne="exclude_value")
        result = sf.as_dict()
        assert result == {"ne": "exclude_value"}

    def test_string_filter_in_list(self):
        sf = StringFilter(in_list=["val1", "val2", "val3"])
        result = sf.as_dict()
        assert result == {"in": ["val1", "val2", "val3"]}

    def test_string_filter_nin(self):
        sf = StringFilter(nin=["bad1", "bad2"])
        result = sf.as_dict()
        assert result == {"nin": ["bad1", "bad2"]}

    def test_string_filter_combined(self):
        sf = StringFilter(eq="test", ne="exclude")
        result = sf.as_dict()
        assert "eq" in result
        assert "ne" in result

    def test_string_filter_empty(self):
        sf = StringFilter()
        result = sf.as_dict()
        assert result is None


class TestWebFiltersAndOrders:
    """
    Tests for Web Traffic filters and orders
    """

    def test_web_entries_filter_by(self):
        filter_by = WebEntriesFilterBy(name=StringFilter(eq="Location1"))
        result = filter_by.as_dict()
        assert result == {"name": {"eq": "Location1"}}

    def test_web_order_by(self):
        order_by = WebOrderBy(name=SortOrder.ASC, total=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"name": "ASC", "total": "DESC"}

    def test_web_order_by_partial(self):
        order_by = WebOrderBy(total=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"total": "DESC"}


class TestFirewallFiltersAndOrders:
    """
    Tests for Firewall filters and orders
    """

    def test_firewall_entries_filter_by(self):
        filter_by = FirewallEntriesFilterBy(name=StringFilter(in_list=["Loc1", "Loc2"]))
        result = filter_by.as_dict()
        assert result == {"name": {"in": ["Loc1", "Loc2"]}}

    def test_firewall_entry_order_by(self):
        order_by = FirewallEntryOrderBy(field_name="total", order=SortOrder.DESC)
        result = order_by.as_dict()
        assert result == {"field_name": "total", "order": "DESC"}


class TestShadowITFiltersAndOrders:
    """
    Tests for Shadow IT filters and orders
    """

    def test_shadow_it_apps_filter_by(self):
        filter_by = ShadowITAppsFilterBy(
            application=StringFilter(eq="Dropbox"),
            sanctioned_state=StringFilter(ne="UNSANCTIONED")
        )
        result = filter_by.as_dict()
        assert "application" in result
        assert result["application"] == {"eq": "Dropbox"}
        assert "sanctioned_state" in result

    def test_shadow_it_apps_order_by(self):
        order_by = ShadowITAppsOrderBy(
            risk_index=SortOrder.DESC,
            data_consumed=SortOrder.DESC
        )
        result = order_by.as_dict()
        assert result == {"risk_index": "DESC", "data_consumed": "DESC"}


class TestIoTFiltersAndOrders:
    """
    Tests for IoT filters and orders
    """

    def test_iot_device_filter_by(self):
        filter_by = IoTDeviceFilterBy(
            category=StringFilter(eq="Camera"),
            classifications=StringFilter(nin=["Unknown"])
        )
        result = filter_by.as_dict()
        assert "category" in result
        assert "classifications" in result

    def test_iot_device_order_by(self):
        order_by = IoTDeviceOrderBy(
            total=SortOrder.DESC,
            category=SortOrder.ASC
        )
        result = order_by.as_dict()
        assert result == {"total": "DESC", "category": "ASC"}


class TestTimeRangeInput:
    """
    Tests for TimeRangeInput
    """

    def test_time_range_input(self):
        tr = TimeRangeInput(start_time=1000000, end_time=2000000)
        result = tr.as_dict()
        assert result == {"start_time": 1000000, "end_time": 2000000}

