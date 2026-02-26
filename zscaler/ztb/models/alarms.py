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

from typing import Dict, List, Optional, Any
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class Alarm(ZscalerObject):
    """
    A class for individual ZTB Alarm objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.alarm_id = config["alarmId"] if "alarmId" in config else None
            self.description = config["description"] if "description" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.status = config["status"] if "status" in config else None
            self.service = config["service"] if "service" in config else None
            self.recommended_action = config["recommendedAction"] if "recommendedAction" in config else None
            self.action_taken_time = config["actionTakenTime"] if "actionTakenTime" in config else None
            self.action_taken_user = config["actionTakenUser"] if "actionTakenUser" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None
            self.gateway_id = config["gatewayId"] if "gatewayId" in config else None
            self.gateway_name = config["gatewayName"] if "gatewayName" in config else None
            self.network_id = config["networkId"] if "networkId" in config else None
            self.network_name = config["networkName"] if "networkName" in config else None
            self.site_id = config["siteId"] if "siteId" in config else None
            self.site_name = config["siteName"] if "siteName" in config else None
        else:
            self.alarm_id = None
            self.description = None
            self.severity = None
            self.status = None
            self.service = None
            self.recommended_action = None
            self.action_taken_time = None
            self.action_taken_user = None
            self.created_at = None
            self.gateway_id = None
            self.gateway_name = None
            self.network_id = None
            self.network_name = None
            self.site_id = None
            self.site_name = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "alarmId": self.alarm_id,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "service": self.service,
            "recommendedAction": self.recommended_action,
            "actionTakenTime": self.action_taken_time,
            "actionTakenUser": self.action_taken_user,
            "createdAt": self.created_at,
            "gatewayId": self.gateway_id,
            "gatewayName": self.gateway_name,
            "networkId": self.network_id,
            "networkName": self.network_name,
            "siteId": self.site_id,
            "siteName": self.site_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlarmResult(ZscalerObject):
    """
    A class for the ``result`` block inside the ZTB Alarm response envelope.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.total_alarms_count = config["totalAlarmsCount"] if "totalAlarmsCount" in config else 0
            self.alarms = ZscalerCollection.form_list(
                config["alarms"] if "alarms" in config else [], Alarm
            )
        else:
            self.total_alarms_count = 0
            self.alarms = []

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "totalAlarmsCount": self.total_alarms_count,
            "alarms": [alarm.request_format() for alarm in (self.alarms or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AlarmResponse(ZscalerObject):
    """
    A class for the top-level ZTB Alarm API response envelope.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)

        if config:
            self.status_code = config["statusCode"] if "statusCode" in config else None
            self.message = config["message"] if "message" in config else None
            self.detail = config["detail"] if "detail" in config else None
            self.error_code = config["errorCode"] if "errorCode" in config else None
            self.request_key = config["requestKey"] if "requestKey" in config else None

            if "result" in config:
                if isinstance(config["result"], AlarmResult):
                    self.result = config["result"]
                elif config["result"] is not None:
                    self.result = AlarmResult(config["result"])
                else:
                    self.result = None
            else:
                self.result = None
        else:
            self.status_code = None
            self.message = None
            self.detail = None
            self.error_code = None
            self.request_key = None
            self.result = None

    def request_format(self) -> Dict[str, Any]:
        parent_req_format = super().request_format()
        current_obj_format = {
            "statusCode": self.status_code,
            "message": self.message,
            "detail": self.detail,
            "errorCode": self.error_code,
            "requestKey": self.request_key,
            "result": self.result.request_format() if self.result else None,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
