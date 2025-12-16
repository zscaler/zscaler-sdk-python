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

from typing import Dict, Any, List, Optional
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class WebReportEntry(ZscalerObject):
    """
    A single entry in a web traffic report.

    Attributes:
        name: The name/label of the entry (e.g., location name).
        total: The total count or value.
        trend: Optional trend data points.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.name: Optional[str] = config.get("name")
            self.total: Optional[int] = config.get("total")
            self.trend: Optional[List[Dict[str, Any]]] = config.get("trend")
        else:
            self.name = None
            self.total = None
            self.trend = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "total": self.total,
            "trend": self.trend,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class WebReportEntryWithId(ZscalerObject):
    """
    A web traffic report entry that includes an ID.

    Attributes:
        id: The unique identifier.
        name: The name/label of the entry.
        total: The total count or value.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id: Optional[int] = config.get("id")
            self.name: Optional[str] = config.get("name")
            self.total: Optional[int] = config.get("total")
        else:
            self.id = None
            self.name = None
            self.total = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "total": self.total,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TrendDataPoint(ZscalerObject):
    """
    A single data point in a trend series.

    Attributes:
        time_stamp: The timestamp in epoch milliseconds.
        value: The value at this time point.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.time_stamp: Optional[int] = config.get("time_stamp")
            self.value: Optional[int] = config.get("value")
        else:
            self.time_stamp = None
            self.value = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "time_stamp": self.time_stamp,
            "value": self.value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CyberSecurityIncident(ZscalerObject):
    """
    A cybersecurity incident entry.

    Attributes:
        app: The application name involved.
        name: The incident name.
        total: The total count.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.app: Optional[str] = config.get("app")
            self.name: Optional[str] = config.get("name")
            self.total: Optional[int] = config.get("total")
        else:
            self.app = None
            self.name = None
            self.total = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "app": self.app,
            "name": self.name,
            "total": self.total,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CasbIncident(ZscalerObject):
    """
    A CASB (Cloud Access Security Broker) incident entry.

    Attributes:
        time_stamp: The timestamp of the incident in epoch milliseconds.
        policy: The policy that triggered the incident.
        incident_type: The type of incident (DLP, MALWARE).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.time_stamp: Optional[int] = config.get("time_stamp")
            self.policy: Optional[str] = config.get("policy")
            self.incident_type: Optional[str] = config.get("incident_type")
        else:
            self.time_stamp = None
            self.policy = None
            self.incident_type = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "time_stamp": self.time_stamp,
            "policy": self.policy,
            "incident_type": self.incident_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IoTDeviceStat(ZscalerObject):
    """
    IoT device statistics entry.

    Attributes:
        category: The device category.
        type: The device type.
        device_count: The number of devices.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.category: Optional[str] = config.get("category")
            self.type: Optional[str] = config.get("type")
            self.device_count: Optional[int] = config.get("device_count")
        else:
            self.category = None
            self.type = None
            self.device_count = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "category": self.category,
            "type": self.type,
            "device_count": self.device_count,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ShadowITApp(ZscalerObject):
    """
    A Shadow IT discovered application.

    Attributes:
        name: The application name.
        total: The total usage count.
        risk_score: The risk score (if available).
        category: The application category (if available).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.name: Optional[str] = config.get("name")
            self.total: Optional[int] = config.get("total")
            self.risk_score: Optional[int] = config.get("risk_score")
            self.category: Optional[str] = config.get("category")
        else:
            self.name = None
            self.total = None
            self.risk_score = None
            self.category = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "total": self.total,
            "risk_score": self.risk_score,
            "category": self.category,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class FirewallReportEntry(ZscalerObject):
    """
    A firewall traffic report entry.

    Attributes:
        name: The entry name (e.g., action type).
        total: The total count.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.name: Optional[str] = config.get("name")
            self.total: Optional[int] = config.get("total")
        else:
            self.name = None
            self.total = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "total": self.total,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


# Export all common types
__all__ = [
    "WebReportEntry",
    "WebReportEntryWithId",
    "TrendDataPoint",
    "CyberSecurityIncident",
    "CasbIncident",
    "IoTDeviceStat",
    "ShadowITApp",
    "FirewallReportEntry",
]
