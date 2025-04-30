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
from zscaler.zia.models import common


class CloudApplicationInstances(ZscalerObject):
    """
    A class for CloudApplicationInstances objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CloudApplicationInstances model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.instance_id = config["instanceId"] if "instanceId" in config else None

            self.instance_type = config["instanceType"] if "instanceType" in config else None

            self.instance_name = config["instanceName"] if "instanceName" in config else None

            self.modified_at = config["modifiedAt"] if "modifiedAt" in config else None

            self.instance_identifiers = ZscalerCollection.form_list(
                config["instanceIdentifiers"] if "instanceIdentifiers" in config else [], InstanceIdentifiers
            )

            if "modifiedBy" in config:
                if isinstance(config["modifiedBy"], common.CommonBlocks):
                    self.modified_by = config["modifiedBy"]
                elif config["modifiedBy"] is not None:
                    self.modified_by = common.CommonBlocks(config["modifiedBy"])
                else:
                    self.modified_by = None
            else:
                self.modified_by = None
        else:
            self.instance_id = None
            self.instance_type = None
            self.instance_name = None
            self.modified_by = None
            self.modified_at = None
            self.instance_identifiers = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "instanceId": self.instance_id,
            "instanceType": self.instance_type,
            "instanceName": self.instance_name,
            "modifiedBy": self.modified_by,
            "modifiedAt": self.modified_at,
            "instanceIdentifiers": self.instance_identifiers,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class InstanceIdentifiers(ZscalerObject):
    """
    A class for InstanceIdentifiers objects.
    """

    def __init__(self, config=None):
        """
        Initialize the InstanceIdentifiers model based on API response.

        Args:
            config (dict): A dictionary representing the Instance Identifiers configuration.
        """
        super().__init__(config)

        if config:
            self.instance_id = config["instanceId"] if "instanceId" in config else None

            self.instance_identifier = config["instanceIdentifier"] if "instanceIdentifier" in config else None

            self.instance_identifier_name = config["instanceIdentifierName"] if "instanceIdentifierName" in config else None

            self.identifier_type = config["identifierType"] if "identifierType" in config else None

            self.modified_at = config["modifiedAt"] if "modifiedAt" in config else None

            if "modifiedBy" in config:
                if isinstance(config["modifiedBy"], common.CommonBlocks):
                    self.modified_by = config["modifiedBy"]
                elif config["modifiedBy"] is not None:
                    self.modified_by = common.CommonBlocks(config["modifiedBy"])
                else:
                    self.modified_by = None
            else:
                self.modified_by = None
        else:
            self.instance_id = None
            self.instance_identifier = None
            self.instance_identifier_name = None
            self.identifier_type = None
            self.modified_at = None
            self.modified_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "instanceId": self.instance_id,
            "instanceIdentifier": self.instance_identifier,
            "identifierType": self.identifier_type,
            "modifiedAt": self.modified_at,
            "modifiedBy": self.modified_by,
            "instanceIdentifierName": self.instance_identifier_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
