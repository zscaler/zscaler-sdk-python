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

from typing import Dict, List, Optional, Any, Union
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class ContentHash(ZscalerObject):
    """
    A class representing the ContentHash.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ContentHash model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.hash_type = config["hashType"] if "hashType" in config else None
            self.hash_value = config["hashValue"] if "hashValue" in config else None
        else:
            self.hash_type = None
            self.hash_value = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "hashType": self.hash_type,
            "hashValue": self.hash_value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DetectorResponse(ZscalerObject):
    """
    A class representing the DetectorResponse.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the DetectorResponse model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.status_code = config["statusCode"] if "statusCode" in config else None
            self.error_msg = config["errorMsg"] if "errorMsg" in config else None
            self.triggered = config["triggered"] if "triggered" in config else None
            self.action = config["action"] if "action" in config else None
            self.latency = config["latency"] if "latency" in config else None
            self.device_type = config["deviceType"] if "deviceType" in config else None
            self.details = config["details"] if "details" in config else None
            self.severity = config["severity"] if "severity" in config else None

            if "contentHash" in config:
                if isinstance(config["contentHash"], ContentHash):
                    self.content_hash = config["contentHash"]
                elif config["contentHash"] is not None:
                    self.content_hash = ContentHash(config["contentHash"])
                else:
                    self.content_hash = None
            else:
                self.content_hash = None
        else:
            self.status_code = None
            self.error_msg = None
            self.triggered = None
            self.action = None
            self.latency = None
            self.device_type = None
            self.details = None
            self.content_hash = None
            self.severity = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "statusCode": self.status_code,
            "errorMsg": self.error_msg,
            "triggered": self.triggered,
            "action": self.action,
            "latency": self.latency,
            "deviceType": self.device_type,
            "details": self.details,
            "contentHash": self.content_hash.request_format() if self.content_hash else None,
            "severity": self.severity,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class RateLimitThrottlingDetail(ZscalerObject):
    """
    A class representing the RateLimitThrottlingDetail.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the RateLimitThrottlingDetail model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.rlc_id = config["rlcId"] if "rlcId" in config else None
            self.metric = config["metric"] if "metric" in config else None
            self.retry_after_millis = config["retryAfterMillis"] if "retryAfterMillis" in config else None
        else:
            self.rlc_id = None
            self.metric = None
            self.retry_after_millis = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "rlcId": self.rlc_id,
            "metric": self.metric,
            "retryAfterMillis": self.retry_after_millis,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExecuteDetectionsPolicyRequest(ZscalerObject):
    """
    A class representing the ExecuteDetectionsPolicyRequest.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ExecuteDetectionsPolicyRequest model based on API response.

        Args:
            config (dict): A dictionary representing the request.
        """
        super().__init__(config)
        if config:
            self.transaction_id = config["transactionId"] if "transactionId" in config else None
            self.content = config["content"] if "content" in config else None
            self.direction = config["direction"] if "direction" in config else None
            self.policy_id = config["policyId"] if "policyId" in config else None
        else:
            self.transaction_id = None
            self.content = None
            self.direction = None
            self.policy_id = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "transactionId": self.transaction_id,
            "content": self.content,
            "direction": self.direction,
            "policyId": self.policy_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExecuteDetectionsPolicyResponse(ZscalerObject):
    """
    A class representing the ExecuteDetectionsPolicyResponse.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ExecuteDetectionsPolicyResponse model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.transaction_id = config["transactionId"] if "transactionId" in config else None
            self.status_code = config["statusCode"] if "statusCode" in config else None
            self.error_msg = config["errorMsg"] if "errorMsg" in config else None
            self.detector_error_count = config["detectorErrorCount"] if "detectorErrorCount" in config else None
            self.action = config["action"] if "action" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.direction = config["direction"] if "direction" in config else None

            # Handle detectorResponses as a dictionary of DetectorResponse objects
            self.detector_responses = {}
            if "detectorResponses" in config and config["detectorResponses"]:
                for key, value in config["detectorResponses"].items():
                    if isinstance(value, DetectorResponse):
                        self.detector_responses[key] = value
                    elif value is not None:
                        self.detector_responses[key] = DetectorResponse(value)

            # Handle throttlingDetails as a list
            self.throttling_details = ZscalerCollection.form_list(
                config["throttlingDetails"] if "throttlingDetails" in config else [],
                RateLimitThrottlingDetail
            )
        else:
            self.transaction_id = None
            self.status_code = None
            self.error_msg = None
            self.detector_error_count = None
            self.action = None
            self.severity = None
            self.direction = None
            self.detector_responses = {}
            self.throttling_details = []

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()

        # Convert detector_responses dict
        detector_responses_dict = {}
        if self.detector_responses:
            for key, value in self.detector_responses.items():
                if isinstance(value, DetectorResponse):
                    detector_responses_dict[key] = value.request_format()
                else:
                    detector_responses_dict[key] = value

        current_obj_format = {
            "transactionId": self.transaction_id,
            "statusCode": self.status_code,
            "errorMsg": self.error_msg,
            "detectorErrorCount": self.detector_error_count,
            "action": self.action,
            "severity": self.severity,
            "direction": self.direction,
            "detectorResponses": detector_responses_dict,
            "throttlingDetails": [
                item.request_format() if isinstance(item, RateLimitThrottlingDetail) else item
                for item in self.throttling_details
            ] if self.throttling_details else [],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DasResolveAndExecuteDetectionsPolicyRequest(ZscalerObject):
    """
    A class representing the DasResolveAndExecuteDetectionsPolicyRequest.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the DasResolveAndExecuteDetectionsPolicyRequest model based on API response.

        Args:
            config (dict): A dictionary representing the request.
        """
        super().__init__(config)
        if config:
            self.transaction_id = config["transactionId"] if "transactionId" in config else None
            self.content = config["content"] if "content" in config else None
            self.direction = config["direction"] if "direction" in config else None
        else:
            self.transaction_id = None
            self.content = None
            self.direction = None

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "transactionId": self.transaction_id,
            "content": self.content,
            "direction": self.direction,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ResolveAndExecuteDetectionsPolicyResponse(ZscalerObject):
    """
    A class representing the ResolveAndExecuteDetectionsPolicyResponse.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the ResolveAndExecuteDetectionsPolicyResponse model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.transaction_id = config["transactionId"] if "transactionId" in config else None
            self.status_code = config["statusCode"] if "statusCode" in config else None
            self.error_msg = config["errorMsg"] if "errorMsg" in config else None
            self.detector_error_count = config["detectorErrorCount"] if "detectorErrorCount" in config else None
            self.action = config["action"] if "action" in config else None
            self.severity = config["severity"] if "severity" in config else None
            self.direction = config["direction"] if "direction" in config else None
            self.policy_id = config["policyId"] if "policyId" in config else None
            self.policy_name = config["policyName"] if "policyName" in config else None
            self.policy_version = config["policyVersion"] if "policyVersion" in config else None

            # Handle detectorResponses as a dictionary of DetectorResponse objects
            self.detector_responses = {}
            if "detectorResponses" in config and config["detectorResponses"]:
                for key, value in config["detectorResponses"].items():
                    if isinstance(value, DetectorResponse):
                        self.detector_responses[key] = value
                    elif value is not None:
                        self.detector_responses[key] = DetectorResponse(value)

            # Handle throttlingDetails as a list
            self.throttling_details = ZscalerCollection.form_list(
                config["throttlingDetails"] if "throttlingDetails" in config else [],
                RateLimitThrottlingDetail
            )
        else:
            self.transaction_id = None
            self.status_code = None
            self.error_msg = None
            self.detector_error_count = None
            self.action = None
            self.severity = None
            self.direction = None
            self.policy_id = None
            self.policy_name = None
            self.policy_version = None
            self.detector_responses = {}
            self.throttling_details = []

    def request_format(self) -> Dict[str, Any]:
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()

        # Convert detector_responses dict
        detector_responses_dict = {}
        if self.detector_responses:
            for key, value in self.detector_responses.items():
                if isinstance(value, DetectorResponse):
                    detector_responses_dict[key] = value.request_format()
                else:
                    detector_responses_dict[key] = value

        current_obj_format = {
            "transactionId": self.transaction_id,
            "statusCode": self.status_code,
            "errorMsg": self.error_msg,
            "detectorErrorCount": self.detector_error_count,
            "action": self.action,
            "severity": self.severity,
            "direction": self.direction,
            "policyId": self.policy_id,
            "policyName": self.policy_name,
            "policyVersion": self.policy_version,
            "detectorResponses": detector_responses_dict,
            "throttlingDetails": [
                item.request_format() if isinstance(item, RateLimitThrottlingDetail) else item
                for item in self.throttling_details
            ] if self.throttling_details else [],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
