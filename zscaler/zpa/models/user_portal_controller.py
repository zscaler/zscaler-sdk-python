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


class UserPortalController(ZscalerObject):
    """
    A class for User Portal Controller objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Userportalcontroller model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.certificate_id = config["certificateId"] \
                if "certificateId" in config else None
            self.certificate_name = config["certificateName"] \
                if "certificateName" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.domain = config["domain"] \
                if "domain" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.ext_domain = config["extDomain"] \
                if "extDomain" in config else None
            self.ext_domain_name = config["extDomainName"] \
                if "extDomainName" in config else None
            self.ext_domain_translation = config["extDomainTranslation"] \
                if "extDomainTranslation" in config else None
            self.ext_label = config["extLabel"] \
                if "extLabel" in config else None
            self.getc_name = config["getcName"] \
                if "getcName" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.image_data = config["imageData"] \
                if "imageData" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.microtenant_id = config["microtenantId"] \
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] \
                if "microtenantName" in config else None
            self.user_notification = config["userNotification"] \
                if "userNotification" in config else None
            self.user_notification_enabled = config["userNotificationEnabled"] \
                if "userNotificationEnabled" in config else None
            self.managed_by_zs = config["managedByZs"] \
                if "managedByZs" in config else None
        else:
            self.certificate_id = None
            self.certificate_name = None
            self.creation_time = None
            self.description = None
            self.domain = None
            self.enabled = None
            self.ext_domain = None
            self.ext_domain_name = None
            self.ext_domain_translation = None
            self.ext_label = None
            self.getc_name = None
            self.id = None
            self.image_data = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.user_notification = None
            self.user_notification_enabled = None
            self.managed_by_zs = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "certificateId": self.certificate_id,
            "certificateName": self.certificate_name,
            "creationTime": self.creation_time,
            "description": self.description,
            "domain": self.domain,
            "enabled": self.enabled,
            "extDomain": self.ext_domain,
            "extDomainName": self.ext_domain_name,
            "extDomainTranslation": self.ext_domain_translation,
            "extLabel": self.ext_label,
            "getcName": self.getc_name,
            "id": self.id,
            "imageData": self.image_data,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "userNotification": self.user_notification,
            "userNotificationEnabled": self.user_notification_enabled,
            "managedByZs": self.managed_by_zs
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
