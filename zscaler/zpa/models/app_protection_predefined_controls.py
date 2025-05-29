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
from zscaler.zpa.models import app_protection_predefined_controls as app_protection_predefined_controls
from zscaler.zpa.models import common as common


class PredefinedInspectionControlResource(ZscalerObject):
    """
    A class for PredefinedInspectionControlResource objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PredefinedInspectionControlResource model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        # Initialize as empty list to ensure it's always iterable
        self._items = []

        if config:
            self.control_group = config.get("controlGroup")
            self.default_group = config.get("defaultGroup")

            # Store the raw config for iteration purposes
            if isinstance(config, list):
                self._items = config
            elif isinstance(config, dict):
                self._items = [config]

            self.predefined_inspection_controls = ZscalerCollection.form_list(
                config.get("predefinedInspectionControls", []),
                PredefinedInspectionControls,
            )
        else:
            self.control_group = None
            self.default_group = None
            self.predefined_inspection_controls = []

    def __iter__(self):
        """
        Make the object iterable, yielding either the raw items or the processed objects.
        """
        for item in self._items:
            if isinstance(item, dict):
                yield PredefinedInspectionControlResource(item)
            else:
                yield item

    def __len__(self):
        """Return the length of the underlying items."""
        return len(self._items)

    def __getitem__(self, index):
        """Support index-based access."""
        if isinstance(index, int):
            if 0 <= index < len(self._items):
                item = self._items[index]
                if isinstance(item, dict):
                    return PredefinedInspectionControlResource(item)
                return item
            raise IndexError("Index out of range")
        elif isinstance(index, str):
            # Maintain backward compatibility with string attribute access
            if hasattr(self, index):
                return getattr(self, index)
            raise KeyError(f"'{index}' not found in {self.__class__.__name__}")
        else:
            raise TypeError(f"Invalid index type: {type(index)}")

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "controlGroup": self.control_group,
            "defaultGroup": self.default_group,
            "predefinedInspectionControls": self.predefined_inspection_controls,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PredefinedInspectionControls(ZscalerObject):
    """
    A class for PredefinedInspectionControls objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PredefinedInspectionControls model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None

            self.name = config["name"] if "name" in config else None

            self.description = config["description"] if "description" in config else None

            self.action = config["action"] if "action" in config else None

            self.action_value = config["actionValue"] if "actionValue" in config else None

            self.attachment = config["attachment"] if "attachment" in config else None

            self.control_group = config["controlGroup"] if "controlGroup" in config else None

            self.control_number = config["controlNumber"] if "controlNumber" in config else None

            self.control_type = config["controlType"] if "controlType" in config else None

            self.creation_time = config["creationTime"] if "creationTime" in config else None

            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None

            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None

            self.default_action = config["defaultAction"] if "defaultAction" in config else None

            self.default_action_value = config["defaultActionValue"] if "defaultActionValue" in config else None

            self.paranoia_level = config["paranoiaLevel"] if "paranoiaLevel" in config else None

            self.protocol_type = config["protocolType"] if "protocolType" in config else None

            self.severity = config["severity"] if "severity" in config else None

            self.version = config["version"] if "version" in config else None

            self.associated_inspection_profile_names = ZscalerCollection.form_list(
                config["associatedInspectionProfileNames"] if "associatedInspectionProfileNames" in config else [],
                common.CommonIDName,
            )

            if "controlException" in config:
                if isinstance(config["controlException"], common.InspectionControlException):
                    self.control_exception = config["controlException"]
                elif config["controlException"] is not None:
                    self.control_exception = common.InspectionControlException(config["controlException"])
                else:
                    self.control_exception = None
            else:
                self.control_exception = None

        else:
            self.id = None
            self.name = None
            self.description = None
            self.action = None
            self.action_value = None
            self.attachment = None
            self.associated_inspection_profile_names = []
            self.control_exception = None
            self.control_group = None
            self.control_number = None
            self.control_type = None
            self.creation_time = None
            self.modified_by = None
            self.modified_time = None
            self.default_action = None
            self.default_action_value = None
            self.paranoia_level = None
            self.protocol_type = None
            self.severity = None
            self.version = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "action": self.action,
            "actionValue": self.action_value,
            "attachment": self.attachment,
            "associatedInspectionProfileNames": self.associated_inspection_profile_names,
            "controlException": self.control_exception,
            "controlGroup": self.control_group,
            "controlNumber": self.control_number,
            "controlType": self.control_type,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "defaultAction": self.default_action,
            "defaultActionValue": self.default_action_value,
            "paranoiaLevel": self.paranoia_level,
            "protocolType": self.protocol_type,
            "severity": self.severity,
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
