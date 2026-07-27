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

from typing import Any, Dict, Optional

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class EndpointDlpResourceGroups(ZscalerObject):
    """
    A class for EndpointDlpResourceGroups objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the EndpointDlpResourceGroups model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.channel = config["channel"] if "channel" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.resource_count = config["resourceCount"] if "resourceCount" in config else None
            self.resources = ZscalerCollection.form_list(config["resources"] if "resources" in config else [], Resource)
        else:
            self.id = None
            self.channel = None
            self.name = None
            self.description = None
            self.resource_count = None
            self.resources = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "channel": self.channel,
            "name": self.name,
            "description": self.description,
            "resourceCount": self.resource_count,
            "resources": [item.request_format() for item in (self.resources or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Resource(ZscalerObject):
    """
    A class for Resource objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Resource model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.channel = config["channel"] if "channel" in config else None
            self.is_predefined = config["isPredefined"] if "isPredefined" in config else None
            self.network_drive_type = config["networkDriveType"] if "networkDriveType" in config else None
            self.description = config["description"] if "description" in config else None
            self.server_name = config["serverName"] if "serverName" in config else None
            self.app_id = config["appId"] if "appId" in config else None
            self.network_drives = ZscalerCollection.form_list(
                config["networkDrives"] if "networkDrives" in config else [], NetworkDrive
            )

            if "printer" in config:
                if isinstance(config["printer"], Printer):
                    self.printer = config["printer"]
                elif config["printer"] is not None:
                    self.printer = Printer(config["printer"])
                else:
                    self.printer = None
            else:
                self.printer = None

            if "removableStorage" in config:
                if isinstance(config["removableStorage"], RemovableStorage):
                    self.removable_storage = config["removableStorage"]
                elif config["removableStorage"] is not None:
                    self.removable_storage = RemovableStorage(config["removableStorage"])
                else:
                    self.removable_storage = None
            else:
                self.removable_storage = None

            if "application" in config:
                if isinstance(config["application"], Application):
                    self.application = config["application"]
                elif config["application"] is not None:
                    self.application = Application(config["application"])
                else:
                    self.application = None
            else:
                self.application = None
        else:
            self.id = None
            self.name = None
            self.channel = None
            self.is_predefined = None
            self.network_drive_type = None
            self.description = None
            self.server_name = None
            self.app_id = None
            self.network_drives = []
            self.printer = None
            self.removable_storage = None
            self.application = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "channel": self.channel,
            "isPredefined": self.is_predefined,
            "networkDriveType": self.network_drive_type,
            "description": self.description,
            "serverName": self.server_name,
            "appId": self.app_id,
            "networkDrives": [item.request_format() for item in (self.network_drives or [])],
            "printer": self.printer,
            "removableStorage": self.removable_storage,
            "application": self.application,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Printer(ZscalerObject):
    """
    A class for Printer objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Printer model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.unc = config["unc"] if "unc" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.domain = config["domain"] if "domain" in config else None
        else:
            self.unc = None
            self.ip_address = None
            self.domain = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "unc": self.unc,
            "ipAddress": self.ip_address,
            "domain": self.domain,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NetworkDrive(ZscalerObject):
    """
    A class for NetworkDrive objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the NetworkDrive model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.network_path = config["networkPath"] if "networkPath" in config else None
        else:
            self.network_path = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "networkPath": self.network_path,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class RemovableStorage(ZscalerObject):
    """
    A class for RemovableStorage objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the RemovableStorage model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.vendor_id = config["vendorId"] if "vendorId" in config else None
            self.product_id = config["productId"] if "productId" in config else None
            self.serial_number = config["serialNumber"] if "serialNumber" in config else None
        else:
            self.vendor_id = None
            self.product_id = None
            self.serial_number = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "vendorId": self.vendor_id,
            "productId": self.product_id,
            "serialNumber": self.serial_number,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Application(ZscalerObject):
    """
    A class for Application objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Application model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.os_type = config["osType"] if "osType" in config else None
            self.file_name = config["fileName"] if "fileName" in config else None
            self.original_file_name = config["originalFileName"] if "originalFileName" in config else None
            self.bundle_id = config["bundleID"] if "bundleID" in config else None
            self.digitally_signed = config["digitallySigned"] if "digitallySigned" in config else None
        else:
            self.os_type = None
            self.file_name = None
            self.original_file_name = None
            self.bundle_id = None
            self.digitally_signed = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "osType": self.os_type,
            "fileName": self.file_name,
            "originalFileName": self.original_file_name,
            "bundleID": self.bundle_id,
            "digitallySigned": self.digitally_signed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
