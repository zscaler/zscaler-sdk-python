# flake8: noqa
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

from typing import Any, Dict, List, Optional
from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject
from zscaler.zia.models import common as common


class IPSSignatureRules(ZscalerObject):
    """
    A class for IPSSignatureRules objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the IPSSignatureRules model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id: Optional[Any] = config["id"] if "id" in config else None
            self.name: Optional[Any] = config["name"] if "name" in config else None
            self.rule_text: Optional[Any] = config["ruleText"] if "ruleText" in config else None
            self.description: Optional[Any] = config["description"] if "description" in config else None
            if "category" in config:
                if isinstance(config["category"], common.CommonIDNameTag):
                    self.category: Optional[common.CommonIDNameTag] = config["category"]
                elif config["category"] is not None:
                    self.category = common.CommonIDNameTag(config["category"])
                else:
                    self.category = None
            else:
                self.category: Optional[common.CommonIDNameTag] = None

            self.enabled: Optional[Any] = config["enabled"] if "enabled" in config else None
            self.deleted: Optional[Any] = config["deleted"] if "deleted" in config else None
            self.promote_time: Optional[Any] = config["promoteTime"] if "promoteTime" in config else None
            self.rule_text_mod_time: Optional[Any] = config["ruleTextModTime"] if "ruleTextModTime" in config else None
            self.dynamic_validation_submitted: Optional[Any] = (
                config["dynamicValidationSubmitted"] if "dynamicValidationSubmitted" in config else None
            )
            self.dynamic_validation_rejected: Optional[Any] = (
                config["dynamicValidationRejected"] if "dynamicValidationRejected" in config else None
            )
            self.dynamic_validation_succeeded: Optional[Any] = (
                config["dynamicValidationSucceeded"] if "dynamicValidationSucceeded" in config else None
            )
            self.disabled_from_zscm: Optional[Any] = config["disabledFromZSCM"] if "disabledFromZSCM" in config else None
            self.dynamic_val_reject_code: Optional[Any] = (
                config["dynamicValRejectCode"] if "dynamicValRejectCode" in config else None
            )
        else:
            self.id: Optional[Any] = None
            self.name: Optional[Any] = None
            self.rule_text: Optional[Any] = None
            self.description: Optional[Any] = None
            self.category: Optional[Any] = None
            self.enabled: Optional[Any] = None
            self.deleted: Optional[Any] = None
            self.promote_time: Optional[Any] = None
            self.rule_text_mod_time: Optional[Any] = None
            self.dynamic_validation_submitted: Optional[Any] = None
            self.dynamic_validation_rejected: Optional[Any] = None
            self.dynamic_validation_succeeded: Optional[Any] = None
            self.disabled_from_zscm: Optional[Any] = None
            self.dynamic_val_reject_code: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "ruleText": self.rule_text,
            "description": self.description,
            "category": self.category,
            "enabled": self.enabled,
            "deleted": self.deleted,
            "promoteTime": self.promote_time,
            "ruleTextModTime": self.rule_text_mod_time,
            "dynamicValidationSubmitted": self.dynamic_validation_submitted,
            "dynamicValidationRejected": self.dynamic_validation_rejected,
            "dynamicValidationSucceeded": self.dynamic_validation_succeeded,
            "disabledFromZSCM": self.disabled_from_zscm,
            "dynamicValRejectCode": self.dynamic_val_reject_code,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ValidateIPSRuleText(ZscalerObject):
    """
    A class for ValidateIPSRuleText objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ValidateIPSRuleText model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.status: Optional[Any] = config["status"] if "status" in config else None
            self.err_position: Optional[Any] = config["errPosition"] if "errPosition" in config else None
            self.err_msg: Optional[Any] = config["errMsg"] if "errMsg" in config else None
            self.err_parameter: Optional[Any] = config["errParameter"] if "errParameter" in config else None
            self.err_suggestion: Optional[Any] = config["errSuggestion"] if "errSuggestion" in config else None
            self.id_list: Optional[Any] = config["idList"] if "idList" in config else None
            self.sub_ids_map: Optional[Any] = config["subIdsMap"] if "subIdsMap" in config else None
        else:
            self.status: Optional[Any] = None
            self.err_position: Optional[Any] = None
            self.err_msg: Optional[Any] = None
            self.err_parameter: Optional[Any] = None
            self.err_suggestion: Optional[Any] = None
            self.id_list: Optional[Any] = None
            self.sub_ids_map: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "errPosition": self.err_position,
            "errMsg": self.err_msg,
            "errParameter": self.err_parameter,
            "errSuggestion": self.err_suggestion,
            "idList": self.id_list,
            "subIdsMap": self.sub_ids_map,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IPSSignatureImport(ZscalerObject):
    """
    A class for IPSSignatureImport objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the IPSSignatureImport model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.status: Optional[Any] = config["status"] if "status" in config else None
            self.total_records_added: Optional[Any] = config["totalRecordsAdded"] if "totalRecordsAdded" in config else None
            self.total_records_deleted: Optional[Any] = (
                config["totalRecordsDeleted"] if "totalRecordsDeleted" in config else None
            )
            self.total_records_updated: Optional[Any] = (
                config["totalRecordsUpdated"] if "totalRecordsUpdated" in config else None
            )
            self.failed_records: List[FailedRecord] = ZscalerCollection.form_list(
                config["failedRecords"] if "failedRecords" in config else [], FailedRecord
            )
            self.processed_records: Optional[Any] = config["processedRecords"] if "processedRecords" in config else None
            self.total_records_in_import: Optional[Any] = (
                config["totalRecordsInImport"] if "totalRecordsInImport" in config else None
            )
            self.errors: List[Error] = ZscalerCollection.form_list(config["errors"] if "errors" in config else [], Error)
            self.percent_complete: Optional[Any] = config["percentComplete"] if "percentComplete" in config else None
            self.error_code: Optional[Any] = config["errorCode"] if "errorCode" in config else None
        else:
            self.status: Optional[Any] = None
            self.total_records_added: Optional[Any] = None
            self.total_records_deleted: Optional[Any] = None
            self.total_records_updated: Optional[Any] = None
            self.failed_records: List[FailedRecord] = []
            self.processed_records: Optional[Any] = None
            self.total_records_in_import: Optional[Any] = None
            self.errors: List[Error] = []
            self.percent_complete: Optional[Any] = None
            self.error_code: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "totalRecordsAdded": self.total_records_added,
            "totalRecordsDeleted": self.total_records_deleted,
            "totalRecordsUpdated": self.total_records_updated,
            "failedRecords": self.failed_records,
            "processedRecords": self.processed_records,
            "totalRecordsInImport": self.total_records_in_import,
            "errors": self.errors,
            "percentComplete": self.percent_complete,
            "errorCode": self.error_code,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class FailedRecord(ZscalerObject):
    """
    A class for FailedRecord objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the FailedRecord model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.error_code: Optional[Any] = config["errorCode"] if "errorCode" in config else None
            self.name: Optional[Any] = config["name"] if "name" in config else None
            self.action: Optional[Any] = config["action"] if "action" in config else None
            self.description: Optional[Any] = config["description"] if "description" in config else None
        else:
            self.error_code: Optional[Any] = None
            self.name: Optional[Any] = None
            self.action: Optional[Any] = None
            self.description: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "errorCode": self.error_code,
            "name": self.name,
            "action": self.action,
            "description": self.description,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Error(ZscalerObject):
    """
    A class for Error objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Error model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.error_code: Optional[Any] = config["errorCode"] if "errorCode" in config else None
            self.description: Optional[Any] = config["description"] if "description" in config else None
        else:
            self.error_code: Optional[Any] = None
            self.description: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"errorCode": self.error_code, "description": self.description}
        parent_req_format.update(current_obj_format)
        return parent_req_format
