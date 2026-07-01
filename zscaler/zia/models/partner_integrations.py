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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class IntegrationPartner(ZscalerObject):
    """
    A class representing a IntegrationPartner object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.type = config["type"] if "type" in config else None
        else:
            self.id = None
            self.name = None
            self.type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CrowdStrikeEndpoint(ZscalerObject):
    """
    A class representing a CrowdStrikeEndpoint object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.crowd_strike_response = ZscalerCollection.form_list(
                config["crowdStrikeResponse"] if "crowdStrikeResponse" in config else [],
                CrowdStrikeEndpointResponseCrowdStrike,
            )
            if "crowdStrikePagination" in config:
                if isinstance(config["crowdStrikePagination"], CrowdStrikeEndpointResponseCrowdStrikePagination):
                    self.crowd_strike_pagination = config["crowdStrikePagination"]
                elif config["crowdStrikePagination"] is not None:
                    self.crowd_strike_pagination = CrowdStrikeEndpointResponseCrowdStrikePagination(
                        config["crowdStrikePagination"]
                    )
                else:
                    self.crowd_strike_pagination = None
            else:
                self.crowd_strike_pagination = None
            self.crowd_strike_errors = ZscalerCollection.form_list(
                config["crowdStrikeErrors"] if "crowdStrikeErrors" in config else [],
                CrowdStrikeEndpointResponseCrowdStrikeErrors,
            )
        else:
            self.crowd_strike_response = []
            self.crowd_strike_pagination = None
            self.crowd_strike_errors = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "crowdStrikeResponse": [item.request_format() for item in (self.crowd_strike_response or [])],
            "crowdStrikePagination": self.crowd_strike_pagination,
            "crowdStrikeErrors": [item.request_format() for item in (self.crowd_strike_errors or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MicrosoftDefenderEndpoint(ZscalerObject):
    """
    A class representing a MicrosoftDefenderEndpoint object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.response = ZscalerCollection.form_list(
                config["response"] if "response" in config else [], MicrosoftDefenderEndpointResponse
            )
            self.status = config["status"] if "status" in config else None
            self.offset = config["offset"] if "offset" in config else None
            self.sha1 = config["sha1"] if "sha1" in config else None
            self.total_count = config["totalCount"] if "totalCount" in config else None
            if "actionResponse" in config:
                if isinstance(config["actionResponse"], MicrosoftDefenderEndpointResponseAction):
                    self.action_response = config["actionResponse"]
                elif config["actionResponse"] is not None:
                    self.action_response = MicrosoftDefenderEndpointResponseAction(config["actionResponse"])
                else:
                    self.action_response = None
            else:
                self.action_response = None
            if "error" in config:
                if isinstance(config["error"], MicrosoftDefenderEndpointResponseError):
                    self.error = config["error"]
                elif config["error"] is not None:
                    self.error = MicrosoftDefenderEndpointResponseError(config["error"])
                else:
                    self.error = None
            else:
                self.error = None
        else:
            self.response = []
            self.status = None
            self.offset = None
            self.sha1 = None
            self.total_count = None
            self.action_response = None
            self.error = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "response": [item.request_format() for item in (self.response or [])],
            "status": self.status,
            "offset": self.offset,
            "sha1": self.sha1,
            "totalCount": self.total_count,
            "actionResponse": self.action_response,
            "error": self.error,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SandboxMd5Detail(ZscalerObject):
    """
    A class representing a SandboxMd5Detail object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.threat_name = config["threatName"] if "threatName" in config else None
            self.sandbox_category = config["sandboxCategory"] if "sandboxCategory" in config else None
            self.sandbox_score = config["sandboxScore"] if "sandboxScore" in config else None
            self.file_type = config["fileType"] if "fileType" in config else None
            self.file_size = config["fileSize"] if "fileSize" in config else None
            self.md5 = config["md5"] if "md5" in config else None
            self.sha1 = config["sha1"] if "sha1" in config else None
            self.sha256 = config["sha256"] if "sha256" in config else None
            self.ssdeep = config["ssdeep"] if "ssdeep" in config else None
            self.threat_link = config["threatLink"] if "threatLink" in config else None
            self.message = config["message"] if "message" in config else None
            self.origin_language = config["originLanguage"] if "originLanguage" in config else None
            self.origin_country = config["originCountry"] if "originCountry" in config else None
        else:
            self.threat_name = None
            self.sandbox_category = None
            self.sandbox_score = None
            self.file_type = None
            self.file_size = None
            self.md5 = None
            self.sha1 = None
            self.sha256 = None
            self.ssdeep = None
            self.threat_link = None
            self.message = None
            self.origin_language = None
            self.origin_country = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "threatName": self.threat_name,
            "sandboxCategory": self.sandbox_category,
            "sandboxScore": self.sandbox_score,
            "fileType": self.file_type,
            "fileSize": self.file_size,
            "md5": self.md5,
            "sha1": self.sha1,
            "sha256": self.sha256,
            "ssdeep": self.ssdeep,
            "threatLink": self.threat_link,
            "message": self.message,
            "originLanguage": self.origin_language,
            "originCountry": self.origin_country,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CrowdStrikeEndpointResponseCrowdStrike(ZscalerObject):
    """
    A class representing a CrowdStrikeEndpointResponseCrowdStrike object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.end_point_link = config["endPointLink"] if "endPointLink" in config else None
            self.device_id = config["device_id"] if "device_id" in config else None
            self.system_product_name = config["system_product_name"] if "system_product_name" in config else None
            self.hostname = config["hostname"] if "hostname" in config else None
            self.local_ip = config["local_ip"] if "local_ip" in config else None
            self.external_ip = config["external_ip"] if "external_ip" in config else None
            self.mac_address = config["mac_address"] if "mac_address" in config else None
            self.os_version = config["os_version"] if "os_version" in config else None
            self.status = config["status"] if "status" in config else None
            self.file_status = config["file_status"] if "file_status" in config else None
            self.platform_name = config["platform_name"] if "platform_name" in config else None
            self.first_seen = config["first_seen"] if "first_seen" in config else None
            self.last_seen = config["last_seen"] if "last_seen" in config else None
        else:
            self.end_point_link = None
            self.device_id = None
            self.system_product_name = None
            self.hostname = None
            self.local_ip = None
            self.external_ip = None
            self.mac_address = None
            self.os_version = None
            self.status = None
            self.file_status = None
            self.platform_name = None
            self.first_seen = None
            self.last_seen = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "endPointLink": self.end_point_link,
            "device_id": self.device_id,
            "system_product_name": self.system_product_name,
            "hostname": self.hostname,
            "local_ip": self.local_ip,
            "external_ip": self.external_ip,
            "mac_address": self.mac_address,
            "os_version": self.os_version,
            "status": self.status,
            "file_status": self.file_status,
            "platform_name": self.platform_name,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CrowdStrikeEndpointResponseCrowdStrikePagination(ZscalerObject):
    """
    A class representing a CrowdStrikeEndpointResponseCrowdStrikePagination object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.offset = config["offset"] if "offset" in config else None
            self.limit = config["limit"] if "limit" in config else None
            self.total = config["total"] if "total" in config else None
            self.next_page = config["next_page"] if "next_page" in config else None
        else:
            self.offset = None
            self.limit = None
            self.total = None
            self.next_page = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "offset": self.offset,
            "limit": self.limit,
            "total": self.total,
            "next_page": self.next_page,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CrowdStrikeEndpointResponseCrowdStrikeErrors(ZscalerObject):
    """
    A class representing a CrowdStrikeEndpointResponseCrowdStrikeErrors object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.message = config["message"] if "message" in config else None
            self.code = config["code"] if "code" in config else None
        else:
            self.message = None
            self.code = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "message": self.message,
            "code": self.code,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MicrosoftDefenderEndpointResponse(ZscalerObject):
    """
    A class representing a MicrosoftDefenderEndpointResponse object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.machine_id = config["machineId"] if "machineId" in config else None
            self.hostname = config["hostname"] if "hostname" in config else None
            self.internal_ip = config["internalIp"] if "internalIp" in config else None
            self.external_ip = config["externalIp"] if "externalIp" in config else None
            self.os_version = config["osVersion"] if "osVersion" in config else None
            self.action = config["action"] if "action" in config else None
            self.last_seen_date_time = config["lastSeenDateTime"] if "lastSeenDateTime" in config else None
            self.first_seen_date_time = config["firstSeenDateTime"] if "firstSeenDateTime" in config else None
            self.file_status = config["fileStatus"] if "fileStatus" in config else None
            self.end_point_status = config["endPointStatus"] if "endPointStatus" in config else None
        else:
            self.machine_id = None
            self.hostname = None
            self.internal_ip = None
            self.external_ip = None
            self.os_version = None
            self.action = None
            self.last_seen_date_time = None
            self.first_seen_date_time = None
            self.file_status = None
            self.end_point_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "machineId": self.machine_id,
            "hostname": self.hostname,
            "internalIp": self.internal_ip,
            "externalIp": self.external_ip,
            "osVersion": self.os_version,
            "action": self.action,
            "lastSeenDateTime": self.last_seen_date_time,
            "firstSeenDateTime": self.first_seen_date_time,
            "fileStatus": self.file_status,
            "endPointStatus": self.end_point_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MicrosoftDefenderEndpointResponseAction(ZscalerObject):
    """
    A class representing a MicrosoftDefenderEndpointResponseAction object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.machine_id = config["machineId"] if "machineId" in config else None
            self.hostname = config["hostname"] if "hostname" in config else None
            self.internal_ip = config["internalIp"] if "internalIp" in config else None
            self.external_ip = config["externalIp"] if "externalIp" in config else None
            self.os_version = config["osVersion"] if "osVersion" in config else None
            self.action = config["action"] if "action" in config else None
            self.last_seen_date_time = config["lastSeenDateTime"] if "lastSeenDateTime" in config else None
            self.first_seen_date_time = config["firstSeenDateTime"] if "firstSeenDateTime" in config else None
            self.file_status = config["fileStatus"] if "fileStatus" in config else None
            self.end_point_status = config["endPointStatus"] if "endPointStatus" in config else None
        else:
            self.machine_id = None
            self.hostname = None
            self.internal_ip = None
            self.external_ip = None
            self.os_version = None
            self.action = None
            self.last_seen_date_time = None
            self.first_seen_date_time = None
            self.file_status = None
            self.end_point_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "machineId": self.machine_id,
            "hostname": self.hostname,
            "internalIp": self.internal_ip,
            "externalIp": self.external_ip,
            "osVersion": self.os_version,
            "action": self.action,
            "lastSeenDateTime": self.last_seen_date_time,
            "firstSeenDateTime": self.first_seen_date_time,
            "fileStatus": self.file_status,
            "endPointStatus": self.end_point_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class MicrosoftDefenderEndpointResponseError(ZscalerObject):
    """
    A class representing a MicrosoftDefenderEndpointResponseError object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.error_message = config["errorMessage"] if "errorMessage" in config else None
            self.error_code = config["errorCode"] if "errorCode" in config else None
        else:
            self.error_message = None
            self.error_code = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "errorMessage": self.error_message,
            "errorCode": self.error_code,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
