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

# AUTO-GENERATED! DO NOT EDIT FILE DIRECTLY
# SEE CONTRIBUTOR DOCUMENTATION
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class OAuth2UserCode(ZscalerObject):
    """
    A class for OAuth2UserCode objects.
    """

    def __init__(self, config=None):
        """
        Initialize the OAuth2UserCode model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.component_group_id = config["componentGroupId"] \
                if "componentGroupId" in config else None
            self.config_cloud_name = config["configCloudName"] \
                if "configCloudName" in config else None
            self.enrollment_server = config["enrollmentServer"] \
                if "enrollmentServer" in config else None
            self.nonce_association_type = config["nonceAssociationType"] \
                if "nonceAssociationType" in config else None
            self.tenant_id = config["tenantId"] \
                if "tenantId" in config else None
            self.user_codes = ZscalerCollection.form_list(
                config["userCodes"] if "userCodes" in config else [], str
            )
            self.zcomponent_id = config["zcomponentId"] \
                if "zcomponentId" in config else None
        else:
            self.component_group_id = None
            self.config_cloud_name = None
            self.enrollment_server = None
            self.nonce_association_type = None
            self.tenant_id = None
            self.user_codes = []
            self.zcomponent_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "componentGroupId": self.component_group_id,
            "configCloudName": self.config_cloud_name,
            "enrollmentServer": self.enrollment_server,
            "nonceAssociationType": self.nonce_association_type,
            "tenantId": self.tenant_id,
            "userCodes": self.user_codes,
            "zcomponentId": self.zcomponent_id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
