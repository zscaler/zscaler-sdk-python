# flake8: noqa
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

from typing import Any, Dict, List, Optional

from pydash.strings import camel_case

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


def _get(config: dict, snake_key: str, default=None):
    """Get from config with camelCase or snake_case fallback."""
    if not config:
        return default
    v = config.get(snake_key)
    if v is not None:
        return v
    return config.get(camel_case(snake_key), default)


# ---------------------------------------------------------------------------
# GET /api/v2/devices/active - active device row
# ---------------------------------------------------------------------------


class ActiveDevice(ZscalerObject):
    """Active device from list."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id = _get(config, "id")
            self.site_id = _get(config, "site_id")
            self.hostname = _get(config, "hostname")
            self.type = _get(config, "type")
            self.tags = _get(config, "tags")
            self.location = _get(config, "location")
            self.ip_address = _get(config, "ip_address")
            self.mac = _get(config, "mac")
            self.groups = _get(config, "groups")
            self.ad_users = _get(config, "ad_users")
            self.start = _get(config, "start")
            self.end = _get(config, "end")
            self.vendor = _get(config, "vendor")
            self.last_timestamp = _get(config, "last_timestamp")
            self.command = _get(config, "command")
            self.finger_banks = config.get("finger_banks") or config.get("fingerBanks")
            self.created_at = _get(config, "created_at")
            self.updated_at = _get(config, "updated_at")
            self.is_quarantined = _get(config, "is_quarantined")
            self.posture_score = _get(config, "posture_score")
            self.protection = _get(config, "protection")
            self.status = _get(config, "status")
            self.status_error = _get(config, "status_error")
            self.assignment_type = _get(config, "assignment_type")
            self.network_name = _get(config, "network_name")
            self.network_display_name = _get(config, "network_display_name")
            self.capability = _get(config, "capability")
        else:
            self.id = None
            self.site_id = None
            self.hostname = None
            self.type = None
            self.tags = None
            self.location = None
            self.ip_address = None
            self.mac = None
            self.groups = None
            self.ad_users = None
            self.start = None
            self.end = None
            self.vendor = None
            self.last_timestamp = None
            self.command = None
            self.finger_banks = None
            self.created_at = None
            self.updated_at = None
            self.is_quarantined = None
            self.posture_score = None
            self.protection = None
            self.status = None
            self.status_error = None
            self.assignment_type = None
            self.network_name = None
            self.network_display_name = None
            self.capability = None


# ---------------------------------------------------------------------------
# GET /api/v3/device/operating-systems - OS row
# ---------------------------------------------------------------------------


class OSVersionItem(ZscalerObject):
    """Version item in OS row."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.devices = _get(config, "devices")
            self.first_seen = _get(config, "first_seen")
            self.last_seen = _get(config, "last_seen")
            self.version = _get(config, "version")
        else:
            self.devices = None
            self.first_seen = None
            self.last_seen = None
            self.version = None


class OperatingSystemRow(ZscalerObject):
    """OS row from operating-systems list."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.devices = _get(config, "devices")
            self.first_seen = _get(config, "first_seen")
            self.last_seen = _get(config, "last_seen")
            self.os_name = _get(config, "os_name")
            self.versions = ZscalerCollection.form_list(config.get("versions") or [], OSVersionItem)
        else:
            self.devices = None
            self.first_seen = None
            self.last_seen = None
            self.os_name = None
            self.versions = []


# ---------------------------------------------------------------------------
# GET /api/v3/device/{group} - group by row
# ---------------------------------------------------------------------------


class GroupByRow(ZscalerObject):
    """Row from device group-by response."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.count = _get(config, "count")
            self.name = _get(config, "name")
        else:
            self.count = None
            self.name = None


# ---------------------------------------------------------------------------
# GET /api/v2/devices/tags - Tags response
# ---------------------------------------------------------------------------


class DeviceTags(ZscalerObject):
    """Response from GET /api/v2/devices/tags."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            raw_tags = config.get("Tags") or config.get("tags") or []
            self.tags = raw_tags if isinstance(raw_tags, list) else []
            self.cluster_token = _get(config, "cluster_token")
            self.token = _get(config, "token")
        else:
            self.tags = []
            self.cluster_token = None
            self.token = None


# ---------------------------------------------------------------------------
# GET /api/v3/device/filters/{field}/values - Filter values
# ---------------------------------------------------------------------------


class DeviceFilterValues(ZscalerObject):
    """Response from GET /api/v3/device/filters/{field}/values."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.count = _get(config, "count")
            self.values = config.get("values") or config.get("Values") or []
        else:
            self.count = None
            self.values = []


# ---------------------------------------------------------------------------
# Device details (v2 and v3) - use dict for flexibility; nested structures vary
# ---------------------------------------------------------------------------
