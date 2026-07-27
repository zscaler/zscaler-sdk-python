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


class Policies(ZscalerObject):
    """
    A class for Policies objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Policies model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.version = config["version"] if "version" in config else None
            self.description = config["description"] if "description" in config else None
            self.create_time_millis = config["createTimeMillis"] if "createTimeMillis" in config else None
            self.update_time_millis = config["updateTimeMillis"] if "updateTimeMillis" in config else None
            self.input_detector_policies = ZscalerCollection.form_list(
                config["inputDetectorPolicies"] if "inputDetectorPolicies" in config else [], InputDetectorPolicy
            )
            self.output_detector_policies = ZscalerCollection.form_list(
                config["outputDetectorPolicies"] if "outputDetectorPolicies" in config else [], InputDetectorPolicy
            )
        else:
            self.id = None
            self.name = None
            self.version = None
            self.description = None
            self.create_time_millis = None
            self.update_time_millis = None
            self.input_detector_policies = []
            self.output_detector_policies = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "createTimeMillis": self.create_time_millis,
            "updateTimeMillis": self.update_time_millis,
            "inputDetectorPolicies": [item.request_format() for item in (self.input_detector_policies or [])],
            "outputDetectorPolicies": [item.request_format() for item in (self.output_detector_policies or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class InputDetectorPolicy(ZscalerObject):
    """
    A class for InputDetectorPolicy objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the InputDetectorPolicy model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.detector = config["detector"] if "detector" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.severity = config["severity"] if "severity" in config else None

            if "configuration" in config:
                if isinstance(config["configuration"], Configuration):
                    self.configuration = config["configuration"]
                elif config["configuration"] is not None:
                    self.configuration = Configuration(config["configuration"])
                else:
                    self.configuration = None
            else:
                self.configuration = None
        else:
            self.detector = None
            self.enabled = None
            self.severity = None
            self.configuration = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "detector": self.detector,
            "enabled": self.enabled,
            "severity": self.severity,
            "configuration": self.configuration,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Configuration(ZscalerObject):
    """
    A class for Configuration objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Configuration model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.action = config["action"] if "action" in config else None
            self.threshold = config["threshold"] if "threshold" in config else None
            self.anonymization = config["anonymization"] if "anonymization" in config else None
            self.default_action = config["defaultAction"] if "defaultAction" in config else None
            self.replace_with_masked_content = (
                config["replaceWithMaskedContent"] if "replaceWithMaskedContent" in config else None
            )
            self.entities = ZscalerCollection.form_list(config["entities"] if "entities" in config else [], Entity)
        else:
            self.action = None
            self.threshold = None
            self.anonymization = None
            self.default_action = None
            self.replace_with_masked_content = None
            self.entities = []

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "threshold": self.threshold,
            "anonymization": self.anonymization,
            "defaultAction": self.default_action,
            "replaceWithMaskedContent": self.replace_with_masked_content,
            "entities": [item.request_format() for item in (self.entities or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Entity(ZscalerObject):
    """
    A class for Entity objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Entity model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.action = config["action"] if "action" in config else None
            self.entity_type = config["entityType"] if "entityType" in config else None
        else:
            self.action = None
            self.entity_type = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "entityType": self.entity_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
