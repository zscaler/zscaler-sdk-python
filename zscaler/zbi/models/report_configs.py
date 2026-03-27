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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject
from zscaler.zbi.models.custom_apps import CustomApp


def _get(config, snake_key, camel_key):
    """Look up a key in both snake_case (raw API) and camelCase
    (after form_response_body) formats."""
    if snake_key in config:
        return config[snake_key]
    if camel_key in config:
        return config[camel_key]
    return None


class DeliveryInformation(ZscalerObject):
    """A class for report delivery information objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.delivery_method = _get(config, "delivery_method", "deliveryMethod")
            self.emails = ZscalerCollection.form_list(config["emails"] if "emails" in config else [], str)
        else:
            self.delivery_method = None
            self.emails = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "delivery_method": self.delivery_method,
            "emails": self.emails,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ScheduleParams(ZscalerObject):
    """A class for report schedule parameter objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.timezone = config["timezone"] if "timezone" in config else None
            self.frequency = config["frequency"] if "frequency" in config else None
            self.weekday = config["weekday"] if "weekday" in config else None
        else:
            self.timezone = None
            self.frequency = None
            self.weekday = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "timezone": self.timezone,
            "frequency": self.frequency,
            "weekday": self.weekday,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class BackfillParams(ZscalerObject):
    """A class for report backfill parameter objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.timezone = config["timezone"] if "timezone" in config else None
            self.stime = config["stime"] if "stime" in config else None
            self.etime = config["etime"] if "etime" in config else None
        else:
            self.timezone = None
            self.stime = None
            self.etime = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "timezone": self.timezone,
            "stime": self.stime,
            "etime": self.etime,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ReportConfig(ZscalerObject):
    """A class for Report Configuration objects."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.sub_type = _get(config, "sub_type", "subType")
            self.enabled = config["enabled"] if "enabled" in config else None
            self.status = config["status"] if "status" in config else None
            self.next_runtime = _get(config, "nextRuntime", "nextRuntime")

            ids_val = _get(config, "custom_ids", "customIds")
            self.custom_ids = ZscalerCollection.form_list(ids_val if ids_val else [], int)

            di_val = _get(
                config,
                "delivery_information",
                "deliveryInformation",
            )
            if di_val:
                self.delivery_information = ZscalerCollection.form_list(di_val, DeliveryInformation)
            else:
                self.delivery_information = []

            sp_val = _get(config, "schedule_params", "scheduleParams")
            if sp_val:
                self.schedule_params = ScheduleParams(sp_val)
            else:
                self.schedule_params = None

            bp_val = _get(config, "backfill_params", "backfillParams")
            if bp_val:
                self.backfill_params = BackfillParams(bp_val)
            else:
                self.backfill_params = None

            ca_val = _get(config, "custom_apps", "customApps")
            if ca_val:
                self.custom_apps = ZscalerCollection.form_list(ca_val, CustomApp)
            else:
                self.custom_apps = []
        else:
            self.id = None
            self.name = None
            self.sub_type = None
            self.enabled = None
            self.custom_ids = []
            self.status = None
            self.next_runtime = None
            self.delivery_information = []
            self.schedule_params = None
            self.backfill_params = None
            self.custom_apps = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "sub_type": self.sub_type,
            "enabled": self.enabled,
            "custom_ids": self.custom_ids,
            "delivery_information": [
                d.request_format() if hasattr(d, "request_format") else d for d in (self.delivery_information or [])
            ],
            "schedule_params": (
                self.schedule_params.request_format()
                if self.schedule_params and hasattr(self.schedule_params, "request_format")
                else self.schedule_params
            ),
            "backfill_params": (
                self.backfill_params.request_format()
                if self.backfill_params and hasattr(self.backfill_params, "request_format")
                else self.backfill_params
            ),
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
