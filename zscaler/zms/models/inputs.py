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

from dataclasses import dataclass
from typing import Optional, List, Any, Dict
from zscaler.zms.models.enums import SortDirection

# ============================================================================
# Base Expression Filters
# ============================================================================


@dataclass
class StringExpression:
    """
    String expression for flexible string filtering.

    Attributes:
        contains: Contains substring match.
        ends: Ends-with match.
        equals: Exact string match.
        in_list: Match any string in the list.
        starts: Starts-with match.
    """

    contains: Optional[str] = None
    ends: Optional[str] = None
    equals: Optional[str] = None
    in_list: Optional[List[str]] = None
    starts: Optional[str] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.contains is not None:
            result["contains"] = self.contains
        if self.ends is not None:
            result["ends"] = self.ends
        if self.equals is not None:
            result["equals"] = self.equals
        if self.in_list is not None:
            result["in"] = self.in_list
        if self.starts is not None:
            result["starts"] = self.starts
        return result if result else None


@dataclass
class IntegerExpression:
    """
    Integer expression for flexible integer filtering.

    Attributes:
        eq: Exact integer match.
        gt: Greater than.
        gte: Greater than or equal.
        lt: Less than.
        lte: Less than or equal.
        in_list: Match any integer in the list.
        between: Match between two integers.
    """

    eq: Optional[int] = None
    gt: Optional[int] = None
    gte: Optional[int] = None
    lt: Optional[int] = None
    lte: Optional[int] = None
    in_list: Optional[List[int]] = None
    between: Optional[List[int]] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.eq is not None:
            result["eq"] = self.eq
        if self.gt is not None:
            result["gt"] = self.gt
        if self.gte is not None:
            result["gte"] = self.gte
        if self.lt is not None:
            result["lt"] = self.lt
        if self.lte is not None:
            result["lte"] = self.lte
        if self.in_list is not None:
            result["in"] = self.in_list
        if self.between is not None:
            result["between"] = self.between
        return result if result else None


@dataclass
class StringArrayExpression:
    """
    String array expression for array field filtering.

    Attributes:
        contains_any: Match if array contains any of the specified strings.
    """

    contains_any: Optional[List[str]] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.contains_any is not None:
            return {"containsAny": self.contains_any}
        return None


# ============================================================================
# Resource Query Filters
# ============================================================================


@dataclass
class ResourceQueryFilter:
    """
    Filter for resource queries.

    Attributes:
        id: Filter by resource ID.
        name: Filter by resource name.
        status: Filter by resource status.
        resource_type: Filter by resource type.
        cloud_provider: Filter by cloud provider.
        cloud_region: Filter by cloud region.
        platform_os: Filter by platform OS.
    """

    id: Optional[StringExpression] = None
    name: Optional[StringExpression] = None
    status: Optional[StringExpression] = None
    resource_type: Optional[StringExpression] = None
    cloud_provider: Optional[StringExpression] = None
    cloud_region: Optional[StringExpression] = None
    platform_os: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        for attr, key in [
            ("id", "id"),
            ("name", "name"),
            ("status", "status"),
            ("resource_type", "resourceType"),
            ("cloud_provider", "cloudProvider"),
            ("cloud_region", "cloudRegion"),
            ("platform_os", "platformOs"),
        ]:
            val = getattr(self, attr)
            if val is not None:
                d = val.as_dict()
                if d:
                    result[key] = d
        return result if result else None


@dataclass
class ResourceQueryOrderBy:
    """
    Ordering options for resource queries.

    Attributes:
        name: Sort direction for resource name.
    """

    name: Optional[SortDirection] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.name is not None:
            return {"name": self.name.value}
        return None


# ============================================================================
# Resource Group Filters
# ============================================================================


@dataclass
class ResourceGroupsFilter:
    """
    Filter for resource group queries.

    Attributes:
        id: Filter by resource group ID.
        name: Filter by resource group name.
        resource_hostname: Filter by resource hostname.
        resource_id: Filter by resource ID.
    """

    id: Optional[StringExpression] = None
    name: Optional[StringExpression] = None
    resource_hostname: Optional[StringExpression] = None
    resource_id: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        for attr, key in [
            ("id", "id"),
            ("name", "name"),
            ("resource_hostname", "resourceHostname"),
            ("resource_id", "resourceId"),
        ]:
            val = getattr(self, attr)
            if val is not None:
                d = val.as_dict()
                if d:
                    result[key] = d
        return result if result else None


# ============================================================================
# Policy Rule Filters
# ============================================================================


@dataclass
class PolicyRuleFilter:
    """
    Filter for policy rule queries.

    Attributes:
        id: Filter by policy rule ID.
        name: Filter by policy rule name.
        action: Filter by policy action.
    """

    id: Optional[StringExpression] = None
    name: Optional[StringExpression] = None
    action: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        for attr, key in [
            ("id", "id"),
            ("name", "name"),
            ("action", "action"),
        ]:
            val = getattr(self, attr)
            if val is not None:
                d = val.as_dict()
                if d:
                    result[key] = d
        return result if result else None


# ============================================================================
# App Zone Filters
# ============================================================================


@dataclass
class AppZoneFilter:
    """
    Filter for app zone queries.

    Attributes:
        id: Filter by app zone ID.
        app_zone_name: Filter by app zone name.
        description: Filter by description.
    """

    id: Optional[StringExpression] = None
    app_zone_name: Optional[StringExpression] = None
    description: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        for attr, key in [
            ("id", "id"),
            ("app_zone_name", "appZoneName"),
            ("description", "description"),
        ]:
            val = getattr(self, attr)
            if val is not None:
                d = val.as_dict()
                if d:
                    result[key] = d
        return result if result else None


@dataclass
class AppZoneQueryOrderBy:
    """
    Ordering options for app zone queries.

    Attributes:
        app_zone_name: Sort direction for app zone name.
    """

    app_zone_name: Optional[str] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.app_zone_name is not None:
            return {"appZoneName": self.app_zone_name}
        return None


# ============================================================================
# App Catalog Filters
# ============================================================================


@dataclass
class AppCatalogQueryFilter:
    """
    Filter for app catalog queries.

    Attributes:
        id: Filter by app catalog ID.
        name: Filter by app catalog name.
        category: Filter by category.
    """

    id: Optional[StringExpression] = None
    name: Optional[StringExpression] = None
    category: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        for attr, key in [
            ("id", "id"),
            ("name", "name"),
            ("category", "category"),
        ]:
            val = getattr(self, attr)
            if val is not None:
                d = val.as_dict()
                if d:
                    result[key] = d
        return result if result else None


@dataclass
class AppCatalogQueryOrderBy:
    """
    Ordering options for app catalog queries.

    Attributes:
        name: Sort direction for name.
        category: Sort direction for category.
        creation_time: Sort direction for creation time.
        modified_time: Sort direction for modified time.
    """

    name: Optional[SortDirection] = None
    category: Optional[SortDirection] = None
    creation_time: Optional[SortDirection] = None
    modified_time: Optional[SortDirection] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.name is not None:
            result["name"] = self.name.value
        if self.category is not None:
            result["category"] = self.category.value
        if self.creation_time is not None:
            result["creationTime"] = self.creation_time.value
        if self.modified_time is not None:
            result["modifiedTime"] = self.modified_time.value
        return result if result else None


# ============================================================================
# Tag Filters
# ============================================================================


@dataclass
class NamespaceFilter:
    """
    Filter for tag namespace queries.

    Attributes:
        name: Filter by namespace name.
        origin: Filter by namespace origin.
    """

    name: Optional[StringExpression] = None
    origin: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.name is not None:
            d = self.name.as_dict()
            if d:
                result["name"] = d
        if self.origin is not None:
            d = self.origin.as_dict()
            if d:
                result["origin"] = d
        return result if result else None


@dataclass
class NamespaceQueryOrderBy:
    """
    Ordering options for namespace queries.

    Attributes:
        name: Sort direction for namespace name.
    """

    name: Optional[SortDirection] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.name is not None:
            return {"name": self.name.value}
        return None


@dataclass
class TagKeyFilter:
    """
    Filter for tag key queries.

    Attributes:
        key_name: Filter by tag key name.
        value_name: Filter by tag value name.
    """

    key_name: Optional[StringExpression] = None
    value_name: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        result = {}
        if self.key_name is not None:
            d = self.key_name.as_dict()
            if d:
                result["keyName"] = d
        if self.value_name is not None:
            d = self.value_name.as_dict()
            if d:
                result["valueName"] = d
        return result if result else None


@dataclass
class TagKeyQueryOrderBy:
    """
    Ordering options for tag key queries.

    Attributes:
        name: Sort direction for tag key name.
    """

    name: Optional[SortDirection] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.name is not None:
            return {"name": self.name.value}
        return None


@dataclass
class TagValueFilter:
    """
    Filter for tag value queries.

    Attributes:
        name: Filter by tag value name.
    """

    name: Optional[StringExpression] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.name is not None:
            d = self.name.as_dict()
            if d:
                return {"name": d}
        return None


@dataclass
class TagValueQueryOrderBy:
    """
    Ordering options for tag value queries.

    Attributes:
        name: Sort direction for tag value name.
    """

    name: Optional[SortDirection] = None

    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Convert to dictionary for GraphQL variables."""
        if self.name is not None:
            return {"name": self.name.value}
        return None


__all__ = [
    "StringExpression",
    "IntegerExpression",
    "StringArrayExpression",
    "ResourceQueryFilter",
    "ResourceQueryOrderBy",
    "ResourceGroupsFilter",
    "PolicyRuleFilter",
    "AppZoneFilter",
    "AppZoneQueryOrderBy",
    "AppCatalogQueryFilter",
    "AppCatalogQueryOrderBy",
    "NamespaceFilter",
    "NamespaceQueryOrderBy",
    "TagKeyFilter",
    "TagKeyQueryOrderBy",
    "TagValueFilter",
    "TagValueQueryOrderBy",
]
