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


class ConfigOverrideController(ZscalerObject):
    """
    A class for Config Override Controller objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Config Override Controller model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.broker_name = config["brokerName"] \
                if "brokerName" in config else None
            self.config_key = config["configKey"] \
                if "configKey" in config else None
            self.config_value = config["configValue"] \
                if "configValue" in config else None
            self.config_value_int = config["configValueInt"] \
                if "configValueInt" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.customer_id = config["customerId"] \
                if "customerId" in config else None
            self.customer_name = config["customerName"] \
                if "customerName" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.target_gid = config["targetGid"] \
                if "targetGid" in config else None
            self.target_name = config["targetName"] \
                if "targetName" in config else None
            self.target_type = config["targetType"] \
                if "targetType" in config else None
        else:
            self.broker_name = None
            self.config_key = None
            self.config_value = None
            self.config_value_int = None
            self.creation_time = None
            self.customer_id = None
            self.customer_name = None
            self.description = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.target_gid = None
            self.target_name = None
            self.target_type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "brokerName": self.broker_name,
            "configKey": self.config_key,
            "configValue": self.config_value,
            "configValueInt": self.config_value_int,
            "creationTime": self.creation_time,
            "customerId": self.customer_id,
            "customerName": self.customer_name,
            "description": self.description,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "targetGid": self.target_gid,
            "targetName": self.target_name,
            "targetType": self.target_type
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
