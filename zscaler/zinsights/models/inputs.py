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

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Any, Dict
from zscaler.zinsights.models.enums import SortOrder, ActionStatus


# ============================================================================
# Base Classes
# ============================================================================

@dataclass
class OrderByInput:
    """
    Base class for ordering query results.

    Attributes:
        field_name: The field to order by.
        order: The sort order (ASC or DESC).
    """
    field_name: str
    order: SortOrder = SortOrder.DESC

    def to_graphql(self) -> str:
        """Convert to GraphQL input format."""
        return f"{{ field_name: {self.field_name}, order: {self.order.value} }}"

    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"field_name": self.field_name, "order": self.order.value}


@dataclass
class NewsFeedEntriesOrderBy(OrderByInput):
    """
    Ordering options for news feed queries.
    """
    pass


# ============================================================================
# StringFilter - Base filter for all domains (must be defined first)
# ============================================================================

@dataclass
class StringFilter:
    """
    String filter for GraphQL queries.

    Supports equality, inequality, and list matching.

    Attributes:
        eq: Equals - exact string match.
        ne: Not equals - exclude exact string match.
        in_list: In - match any string in the list.
        nin: Not in - exclude any string in the list.
    """
    eq: Optional[str] = None
    ne: Optional[str] = None
    in_list: Optional[List[str]] = None  # 'in' is a Python keyword
    nin: Optional[List[str]] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.eq is not None:
            result["eq"] = self.eq
        if self.ne is not None:
            result["ne"] = self.ne
        if self.in_list is not None:
            result["in"] = self.in_list
        if self.nin is not None:
            result["nin"] = self.nin
        return result if result else None


# ============================================================================
# Base Filter and Order Classes (DRY)
# ============================================================================

@dataclass
class BaseNameFilterBy:
    """
    Base filter class for entries that only filter by name.
    """
    name: Optional[StringFilter] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.name is None:
            return None
        name_filter = self.name.as_dict()
        if name_filter is None:
            return None
        return {"name": name_filter}


@dataclass
class BaseNameTotalOrderBy:
    """
    Base order class for entries with name and total fields.
    """
    name: Optional[SortOrder] = None
    total: Optional[SortOrder] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.name is not None:
            result["name"] = self.name.value
        if self.total is not None:
            result["total"] = self.total.value
        return result if result else None


# ============================================================================
# Web Traffic Filters and Orders
# ============================================================================

@dataclass
class WebEntriesFilterBy(BaseNameFilterBy):
    """Filter options for web traffic entries using StringFilter."""
    pass


@dataclass
class WebOrderBy(BaseNameTotalOrderBy):
    """Ordering options for web traffic entries (name, total)."""
    pass


# ============================================================================
# CASB / SaaS Security Filters and Orders
# ============================================================================

@dataclass
class CasbEntriesFilterBy(BaseNameFilterBy):
    """Filter options for CASB (SaaS Security) entries using StringFilter."""
    pass


@dataclass
class CasbEntryOrderBy(BaseNameTotalOrderBy):
    """Ordering options for CASB entries (name, total)."""
    pass


# ============================================================================
# Cyber Security Filters and Orders
# ============================================================================

@dataclass
class CyberSecurityEntriesFilterBy(BaseNameFilterBy):
    """Filter options for Cyber Security entries using StringFilter."""
    pass


@dataclass
class CyberSecurityEntryOrderBy(BaseNameTotalOrderBy):
    """Ordering options for Cyber Security entries (name, total)."""
    pass


# ============================================================================
# Firewall Filters and Orders
# ============================================================================

@dataclass
class FirewallEntriesFilterBy(BaseNameFilterBy):
    """Filter options for Zero Trust Firewall entries using StringFilter."""
    pass


@dataclass
class FirewallEntryOrderBy:
    """
    Ordering options for Zero Trust Firewall entries.

    Attributes:
        field_name: The field to order by (e.g., 'name', 'total').
        order: Sort order (ASC or DESC).
    """
    field_name: str
    order: SortOrder = SortOrder.DESC

    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for GraphQL variables."""
        return {"field_name": self.field_name, "order": self.order.value}


# ============================================================================
# Shadow IT Filters and Orders
# ============================================================================

@dataclass
class ShadowITAppsFilterBy:
    """
    Filter options for Shadow IT apps entries.

    Attributes:
        application: Filter by application name using StringFilter.
        application_category: Filter by application category using StringFilter.
        sanctioned_state: Filter by sanctioned state using StringFilter.
    """
    application: Optional[StringFilter] = None
    application_category: Optional[StringFilter] = None
    sanctioned_state: Optional[StringFilter] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.application is not None:
            af = self.application.as_dict()
            if af:
                result["application"] = af
        if self.application_category is not None:
            acf = self.application_category.as_dict()
            if acf:
                result["application_category"] = acf
        if self.sanctioned_state is not None:
            ssf = self.sanctioned_state.as_dict()
            if ssf:
                result["sanctioned_state"] = ssf
        return result if result else None


@dataclass
class ShadowITAppsOrderBy:
    """
    Ordering options for Shadow IT apps entries.

    Attributes:
        application: Sort order for application field.
        application_category: Sort order for application_category field.
        risk_index: Sort order for risk_index field.
        computed_risk_index: Sort order for computed_risk_index field.
        sanctioned_state: Sort order for sanctioned_state field.
        data_consumed: Sort order for data_consumed field.
    """
    application: Optional[SortOrder] = None
    application_category: Optional[SortOrder] = None
    risk_index: Optional[SortOrder] = None
    computed_risk_index: Optional[SortOrder] = None
    sanctioned_state: Optional[SortOrder] = None
    data_consumed: Optional[SortOrder] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.application is not None:
            result["application"] = self.application.value
        if self.application_category is not None:
            result["application_category"] = self.application_category.value
        if self.risk_index is not None:
            result["risk_index"] = self.risk_index.value
        if self.computed_risk_index is not None:
            result["computed_risk_index"] = self.computed_risk_index.value
        if self.sanctioned_state is not None:
            result["sanctioned_state"] = self.sanctioned_state.value
        if self.data_consumed is not None:
            result["data_consumed"] = self.data_consumed.value
        return result if result else None


@dataclass
class ShadowITEntriesFilterBy(BaseNameFilterBy):
    """Filter options for Shadow IT summary entries (used in group_by queries)."""
    pass


@dataclass
class ShadowITEntryOrderBy(BaseNameTotalOrderBy):
    """Ordering options for Shadow IT summary entries (name, total)."""
    pass


# ============================================================================
# IoT Filters and Orders
# ============================================================================

@dataclass
class IoTDeviceFilterBy:
    """
    Filter options for IoT device entries.

    Attributes:
        classifications: Filter by device classification using StringFilter.
        classification_uuid: Filter by classification UUID using StringFilter.
        category: Filter by device category using StringFilter.
    """
    classifications: Optional[StringFilter] = None
    classification_uuid: Optional[StringFilter] = None
    category: Optional[StringFilter] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.classifications is not None:
            cf = self.classifications.as_dict()
            if cf:
                result["classifications"] = cf
        if self.classification_uuid is not None:
            cuf = self.classification_uuid.as_dict()
            if cuf:
                result["classification_uuid"] = cuf
        if self.category is not None:
            cat = self.category.as_dict()
            if cat:
                result["category"] = cat
        return result if result else None


@dataclass
class IoTDeviceOrderBy:
    """
    Ordering options for IoT device entries.

    Attributes:
        classifications: Sort order for the classifications field.
        classification_uuid: Sort order for the classification_uuid field.
        category: Sort order for the category field.
        total: Sort order for the total field.
    """
    classifications: Optional[SortOrder] = None
    classification_uuid: Optional[SortOrder] = None
    category: Optional[SortOrder] = None
    total: Optional[SortOrder] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.classifications is not None:
            result["classifications"] = self.classifications.value
        if self.classification_uuid is not None:
            result["classification_uuid"] = self.classification_uuid.value
        if self.category is not None:
            result["category"] = self.category.value
        if self.total is not None:
            result["total"] = self.total.value
        return result if result else None


# ============================================================================
# Legacy / Other Filters (kept for backwards compatibility)
# ============================================================================

@dataclass
class CasbIncidentFilterBy:
    """
    Filter options for CASB incident entries.

    Attributes:
        policy: Filter by policy name.
        app_name: Filter by application name.
        user_name: Filter by user name.
    """
    policy: Optional[str] = None
    app_name: Optional[str] = None
    user_name: Optional[str] = None

    def to_graphql(self) -> str:
        """Convert to GraphQL input format."""
        parts = []
        if self.policy is not None:
            parts.append(f'policy: "{self.policy}"')
        if self.app_name is not None:
            parts.append(f'app_name: "{self.app_name}"')
        if self.user_name is not None:
            parts.append(f'user_name: "{self.user_name}"')
        return "{ " + ", ".join(parts) + " }" if parts else ""

    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        if self.policy is not None:
            result["policy"] = self.policy
        if self.app_name is not None:
            result["app_name"] = self.app_name
        if self.user_name is not None:
            result["user_name"] = self.user_name
        return result


@dataclass
class TimeRangeInput:
    """
    Time range input for queries.

    Attributes:
        start_time: Start time in epoch milliseconds.
        end_time: End time in epoch milliseconds.
    """
    start_time: int
    end_time: int

    def as_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {"start_time": self.start_time, "end_time": self.end_time}


# Export all input types
__all__ = [
    # Base classes
    "OrderByInput",
    "StringFilter",
    "BaseNameFilterBy",
    "BaseNameTotalOrderBy",

    # Web Traffic
    "WebEntriesFilterBy",
    "WebOrderBy",

    # CASB / SaaS Security
    "CasbEntriesFilterBy",
    "CasbEntryOrderBy",
    "CasbIncidentFilterBy",

    # Cyber Security
    "CyberSecurityEntriesFilterBy",
    "CyberSecurityEntryOrderBy",

    # Firewall
    "FirewallEntriesFilterBy",
    "FirewallEntryOrderBy",

    # Shadow IT
    "ShadowITAppsFilterBy",
    "ShadowITAppsOrderBy",
    "ShadowITEntriesFilterBy",
    "ShadowITEntryOrderBy",

    # IoT
    "IoTDeviceFilterBy",
    "IoTDeviceOrderBy",

    # Other
    "NewsFeedEntriesOrderBy",
    "TimeRangeInput",
]
