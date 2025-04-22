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


class PostureProfile(ZscalerObject):
    """
    A class representing a Posture Profile object.
    """

    def __init__(self, config=None):
        """
        Initialize the PostureProfile object with optional fields and nested object handling.

        Args:
            config (dict, optional): A dictionary containing posture profile data.
        """
        super().__init__(config)
        if config:
            # Handle optional fields
            self.id = config["id"] if config and "id" in config else None
            self.modified_time = config["modifiedTime"] if config and "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if config and "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if config and "modifiedBy" in config else None
            self.name = config["name"] if config and "name" in config else None
            self.posture_udid = config["postureUdid"] if config and "postureUdid" in config else None

            self.apply_to_machine_tunnel_enabled = (
                config["applyToMachineTunnelEnabled"] if config and "applyToMachineTunnelEnabled" in config else False
            )
            self.crl_check_enabled = config["crlCheckEnabled"] if config and "crlCheckEnabled" in config else False
            self.non_exportable_private_key_enabled = (
                config["nonExportablePrivateKeyEnabled"] if config and "nonExportablePrivateKeyEnabled" in config else False
            )

            self.root_cert = config["rootCert"] if config and "rootCert" in config else None

            self.posture_type = config["postureType"] if config and "postureType" in config else None

            self.zscaler_cloud = config["zscalerCloud"] if config and "zscalerCloud" in config else None

            self.master_customer_id = config["masterCustomerId"] if config and "masterCustomerId" in config else None

            self.zscaler_customer_id = config["zscalerCustomerId"] if config and "zscalerCustomerId" in config else None

            self.platform = ZscalerCollection.form_list(config["platform"] if "platform" in config else [], str)

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.name = None
            self.posture_udid = None
            self.apply_to_machine_tunnel_enabled = False
            self.crl_check_enabled = False
            self.non_exportable_private_key_enabled = False
            self.zscaler_cloud = None
            self.platform = None
            self.master_customer_id = None
            self.zscaler_customer_id = None
            self.posture_type = None
            self.root_cert = None

    def request_format(self):
        """
        Prepare the object in a format suitable for sending as a request payload.

        Returns:
            dict: A dictionary representing the posture profile for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "postureUdid": self.posture_udid,
            "applyToMachineTunnelEnabled": self.apply_to_machine_tunnel_enabled,
            "crlCheckEnabled": self.crl_check_enabled,
            "nonExportablePrivateKeyEnabled": self.non_exportable_private_key_enabled,
            "zscalerCloud": self.zscaler_cloud,
            "platform": self.platform,
            "masterCustomerId": self.master_customer_id,
            "zscalerCustomerId": self.zscaler_customer_id,
            "postureType": self.posture_type,
            "rootCert	": self.root_cert,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
