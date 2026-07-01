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
from zscaler.zcell.models import anomaly_policy as anomaly_policy


class AuditDataHandling(ZscalerObject):
    """
    A class for Audit Data Handling objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Audit Data Handling model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by_user_id = config["modifiedByUserId"] if "modifiedByUserId" in config else None
            self.audit_operation_type = config["auditOperationType"] if "auditOperationType" in config else None
            self.object_type = config["objectType"] if "objectType" in config else None
            self.object_name = config["objectName"] if "objectName" in config else None
            self.object_id = config["objectId"] if "objectId" in config else None
            self.customer_id = config["customerId"] if "customerId" in config else None
            self.jwt_key_id = config["jwtKeyId"] if "jwtKeyId" in config else None

            if "oldData" in config:
                if isinstance(config["oldData"], AuditPolicyData):
                    self.old_data = config["oldData"]
                elif config["oldData"] is not None:
                    self.old_data = AuditPolicyData(config["oldData"])
                else:
                    self.old_data = None
            else:
                self.old_data = None

            if "newData" in config:
                if isinstance(config["newData"], AuditPolicyData):
                    self.new_data = config["newData"]
                elif config["newData"] is not None:
                    self.new_data = AuditPolicyData(config["newData"])
                else:
                    self.new_data = None
            else:
                self.new_data = None

            self.visibility = config["visibility"] if "visibility" in config else None
        else:
            self.id = None
            self.creation_time = None
            self.modified_by_user_id = None
            self.audit_operation_type = None
            self.object_type = None
            self.object_name = None
            self.object_id = None
            self.customer_id = None
            self.jwt_key_id = None
            self.old_data = None
            self.new_data = None
            self.visibility = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "creationTime": self.creation_time,
            "modifiedByUserId": self.modified_by_user_id,
            "auditOperationType": self.audit_operation_type,
            "objectType": self.object_type,
            "objectName": self.object_name,
            "objectId": self.object_id,
            "customerId": self.customer_id,
            "jwtKeyId": self.jwt_key_id,
            "oldData": self.old_data,
            "newData": self.new_data,
            "visibility": self.visibility,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AuditPolicyData(ZscalerObject):
    """
    A class for Audit Policy Data objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Audit Policy Data model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.zs_tid = config["zsTid"] if "zsTid" in config else None
            self.deleted = config["deleted"] if "deleted" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None

            if "jsonData" in config:
                if isinstance(config["jsonData"], anomaly_policy.JsonData):
                    self.json_data = config["jsonData"]
                elif config["jsonData"] is not None:
                    self.json_data = anomaly_policy.JsonData(config["jsonData"])
                else:
                    self.json_data = None
            else:
                self.json_data = None

            self.enabled_at = config["enabledAt"] if "enabledAt" in config else None
            self.policy_name = config["policyName"] if "policyName" in config else None
            self.policy_type = config["policyType"] if "policyType" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.running_status = config["runningStatus"] if "runningStatus" in config else None
            self.modified_by_user_id = config["modifiedByUserId"] if "modifiedByUserId" in config else None
            self.sim_location_group_ids = ZscalerCollection.form_list(
                config["simLocationGroupIds"] if "simLocationGroupIds" in config else [], int
            )
        else:
            self.zs_tid = None
            self.deleted = None
            self.enabled = None
            self.json_data = None
            self.enabled_at = None
            self.policy_name = None
            self.policy_type = None
            self.creation_time = None
            self.modified_time = None
            self.running_status = None
            self.modified_by_user_id = None
            self.sim_location_group_ids = []

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "zsTid": self.zs_tid,
            "deleted": self.deleted,
            "enabled": self.enabled,
            "jsonData": self.json_data,
            "enabledAt": self.enabled_at,
            "policyName": self.policy_name,
            "policyType": self.policy_type,
            "creationTime": self.creation_time,
            "modifiedTime": self.modified_time,
            "runningStatus": self.running_status,
            "modifiedByUserId": self.modified_by_user_id,
            "simLocationGroupIds": self.sim_location_group_ids,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AuditDataRequest(ZscalerObject):
    """
    A class for Audit Data Request objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Audit Data Request model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_by_user_id = config["modifiedByUserId"] if "modifiedByUserId" in config else None
            self.start_date = config["startDate"] if "startDate" in config else None
            self.end_date = config["endDate"] if "endDate" in config else None
            self.operation_type = config["operationType"] if "operationType" in config else None
            self.object_type = config["objectType"] if "objectType" in config else None
            self.object_name = config["objectName"] if "objectName" in config else None
            self.object_id = config["objectId"] if "objectId" in config else None
            self.visibility = config["visibility"] if "visibility" in config else None
            self.customer_id = config["customerId"] if "customerId" in config else None
        else:
            self.id = None
            self.modified_by_user_id = None
            self.start_date = None
            self.end_date = None
            self.operation_type = None
            self.object_type = None
            self.object_name = None
            self.object_id = None
            self.visibility = None
            self.customer_id = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedByUserId": self.modified_by_user_id,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "operationType": self.operation_type,
            "objectType": self.object_type,
            "objectName": self.object_name,
            "objectId": self.object_id,
            "visibility": self.visibility,
            "customerId": self.customer_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AuditMetadata(ZscalerObject):
    """
    A class for Audit Metadata objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Audit Metadata model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.operations = ZscalerCollection.form_list(config["operations"] if "operations" in config else [], str)
            self.object_types = ZscalerCollection.form_list(config["objectTypes"] if "objectTypes" in config else [], str)
        else:
            self.operations = []
            self.object_types = []

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "operations": self.operations,
            "objectTypes": self.object_types,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
