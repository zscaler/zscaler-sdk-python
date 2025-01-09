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

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection
from zscaler.zpa.models.application_segment_pra import ApplicationSegmentPRA

class PrivilegedRemoteAccessPortal(ZscalerObject):
    """
    A class representing the Privileged Remote Access Portal.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"]\
                if "id" in config else None
            self.name = config["name"]\
                if "name" in config else None
            self.enabled = config["enabled"]\
                if "enabled" in config else True
            self.description = config["description"]\
                if "description" in config else None
            self.certificate_id = config["certificateId"]\
                if "certificateId" in config else None
            self.certificate_name = config["certificateName"]\
                if "certificateName" in config else None
            self.cname = config["cName"]\
                if "cName" in config else None
            self.domain = config["domain"]\
                if "domain" in config else None
            self.user_notification = config["userNotification"]\
                if "userNotification" in config else None
            self.user_notification_enabled = config["userNotificationEnabled"]\
                if "userNotificationEnabled" in config else False
            self.microtenant_id = config["microtenantId"]\
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"]\
                if "microtenantName" in config else "Default"
        else:
            self.id = None
            self.name = None
            self.enabled = True
            self.description = None
            self.certificate_id = None
            self.certificate_name = None
            self.cname = None
            self.domain = None
            self.user_notification = None
            self.user_notification_enabled = False
            self.microtenant_id = None
            self.microtenant_name = "Default"

    def request_format(self):
        """
        Formats the PRA portal data into a dictionary suitable for API requests.
        """
        return {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
            "certificateId": self.certificate_id,
            "certificateName": self.certificate_name,
            "cName": self.cname,
            "domain": self.domain,
            "userNotification": self.user_notification,
            "userNotificationEnabled": self.user_notification_enabled,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
