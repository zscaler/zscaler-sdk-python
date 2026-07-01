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
from zscaler.zcell.models import sim_handling as sim_handling


class SimHandling(ZscalerObject):
    """
    A class representing a SimHandling object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.icc_id = config["iccId"] if "iccId" in config else None
            self.tag_ids = ZscalerCollection.form_list(config["tagIds"] if "tagIds" in config else [], str)
        else:
            self.icc_id = None
            self.tag_ids = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iccId": self.icc_id,
            "tagIds": self.tag_ids,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimData(ZscalerObject):
    """
    A class representing a SimData object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.iccid = config["iccid"] if "iccid" in config else None
            self.entity_id = config["entityId"] if "entityId" in config else None
            self.imei = config["imei"] if "imei" in config else None
            self.imsi = config["imsi"] if "imsi" in config else None
            self.msisdn = config["msisdn"] if "msisdn" in config else None
            self.status = config["status"] if "status" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by_user_id = config["modifiedByUserId"] if "modifiedByUserId" in config else None
            self.eid = config["eid"] if "eid" in config else None
            self.profile_name = config["profileName"] if "profileName" in config else None
            self.is_imported = config["isImported"] if "isImported" in config else False
            self.api_sim_id = config["apiSimId"] if "apiSimId" in config else None
            self.location_country = config["locationCountry"] if "locationCountry" in config else None
            self.mvno_customer_id = config["mvnoCustomerId"] if "mvnoCustomerId" in config else None
            self.ip_address = ZscalerCollection.form_list(config["ipAddress"] if "ipAddress" in config else [], str)
            self.apn = config["apn"] if "apn" in config else None
            self.activated_date = config["activatedDate"] if "activatedDate" in config else None
            self.location_mno = config["locationMno"] if "locationMno" in config else None
            self.network_status = config["networkStatus"] if "networkStatus" in config else None
            self.last_session_updated_at = config["lastSessionUpdatedAt"] if "lastSessionUpdatedAt" in config else None
            self.data_authorize_imei = config["dataAuthorizeImei"] if "dataAuthorizeImei" in config else False
            self.data_authorize_imei_value = config["dataAuthorizeImeiValue"] if "dataAuthorizeImeiValue" in config else None
            self.sim_lat = config["simLat"] if "simLat" in config else None
            self.sim_lng = config["simLng"] if "simLng" in config else None
            if "simLocInfo" in config:
                if isinstance(config["simLocInfo"], sim_handling.JsonNode):
                    self.sim_loc_info = config["simLocInfo"]
                elif config["simLocInfo"] is not None:
                    self.sim_loc_info = sim_handling.JsonNode(config["simLocInfo"])
                else:
                    self.sim_loc_info = None
            else:
                self.sim_loc_info = None
            self.event_session_id = config["eventSessionId"] if "eventSessionId" in config else None
            self.tac_id = config["tacId"] if "tacId" in config else None
            self.brand_name = config["brandName"] if "brandName" in config else None
            self.marketing_name = config["marketingName"] if "marketingName" in config else None
            self.device_type = config["deviceType"] if "deviceType" in config else None
            self.model_name = config["modelName"] if "modelName" in config else None
            self.operating_system = config["operatingSystem"] if "operatingSystem" in config else None
            self.band_details = config["bandDetails"] if "bandDetails" in config else None
            self.form_factor = config["formFactor"] if "formFactor" in config else None
            self.assigned_to = config["assignedTo"] if "assignedTo" in config else None
            self.tag_ids = ZscalerCollection.form_list(config["tagIds"] if "tagIds" in config else [], str)
            self.tags = ZscalerCollection.form_list(config["tags"] if "tags" in config else [], str)
            self.entity_name = config["entityName"] if "entityName" in config else None
            self.usage = config["usage"] if "usage" in config else None
            self.usage_val = config["usageVal"] if "usageVal" in config else None
        else:
            self.iccid = None
            self.entity_id = None
            self.imei = None
            self.imsi = None
            self.msisdn = None
            self.status = None
            self.creation_time = None
            self.modified_by_user_id = None
            self.eid = None
            self.profile_name = None
            self.is_imported = False
            self.api_sim_id = None
            self.location_country = None
            self.mvno_customer_id = None
            self.ip_address = []
            self.apn = None
            self.activated_date = None
            self.location_mno = None
            self.network_status = None
            self.last_session_updated_at = None
            self.data_authorize_imei = False
            self.data_authorize_imei_value = None
            self.sim_lat = None
            self.sim_lng = None
            self.sim_loc_info = None
            self.event_session_id = None
            self.tac_id = None
            self.brand_name = None
            self.marketing_name = None
            self.device_type = None
            self.model_name = None
            self.operating_system = None
            self.band_details = None
            self.form_factor = None
            self.assigned_to = None
            self.tag_ids = []
            self.tags = []
            self.entity_name = None
            self.usage = None
            self.usage_val = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iccid": self.iccid,
            "entityId": self.entity_id,
            "imei": self.imei,
            "imsi": self.imsi,
            "msisdn": self.msisdn,
            "status": self.status,
            "creationTime": self.creation_time,
            "modifiedByUserId": self.modified_by_user_id,
            "eid": self.eid,
            "profileName": self.profile_name,
            "isImported": self.is_imported,
            "apiSimId": self.api_sim_id,
            "locationCountry": self.location_country,
            "mvnoCustomerId": self.mvno_customer_id,
            "ipAddress": self.ip_address,
            "apn": self.apn,
            "activatedDate": self.activated_date,
            "locationMno": self.location_mno,
            "networkStatus": self.network_status,
            "lastSessionUpdatedAt": self.last_session_updated_at,
            "dataAuthorizeImei": self.data_authorize_imei,
            "dataAuthorizeImeiValue": self.data_authorize_imei_value,
            "simLat": self.sim_lat,
            "simLng": self.sim_lng,
            "simLocInfo": self.sim_loc_info,
            "eventSessionId": self.event_session_id,
            "tacId": self.tac_id,
            "brandName": self.brand_name,
            "marketingName": self.marketing_name,
            "deviceType": self.device_type,
            "modelName": self.model_name,
            "operatingSystem": self.operating_system,
            "bandDetails": self.band_details,
            "formFactor": self.form_factor,
            "assignedTo": self.assigned_to,
            "tagIds": self.tag_ids,
            "tags": self.tags,
            "entityName": self.entity_name,
            "usage": self.usage,
            "usageVal": self.usage_val,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimDataSearchRequest(ZscalerObject):
    """
    A class representing a SimDataSearchRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.iccid = ZscalerCollection.form_list(
                config["iccid"] if "iccid" in config else [], sim_handling.SanitizedString50
            )
            if "status" in config:
                if isinstance(config["status"], sim_handling.SanitizedString20):
                    self.status = config["status"]
                elif config["status"] is not None:
                    self.status = sim_handling.SanitizedString20(config["status"])
                else:
                    self.status = None
            else:
                self.status = None
            if "networkStatus" in config:
                if isinstance(config["networkStatus"], sim_handling.SanitizedString20):
                    self.network_status = config["networkStatus"]
                elif config["networkStatus"] is not None:
                    self.network_status = sim_handling.SanitizedString20(config["networkStatus"])
                else:
                    self.network_status = None
            else:
                self.network_status = None
            self.ip_address = ZscalerCollection.form_list(
                config["ipAddress"] if "ipAddress" in config else [], sim_handling.SanitizedString20
            )
            if "locationCountry" in config:
                if isinstance(config["locationCountry"], sim_handling.SanitizedString50):
                    self.location_country = config["locationCountry"]
                elif config["locationCountry"] is not None:
                    self.location_country = sim_handling.SanitizedString50(config["locationCountry"])
                else:
                    self.location_country = None
            else:
                self.location_country = None
            self.tag = ZscalerCollection.form_list(config["tag"] if "tag" in config else [], sim_handling.SanitizedString50)
            if "deviceType" in config:
                if isinstance(config["deviceType"], sim_handling.SanitizedString255):
                    self.device_type = config["deviceType"]
                elif config["deviceType"] is not None:
                    self.device_type = sim_handling.SanitizedString255(config["deviceType"])
                else:
                    self.device_type = None
            else:
                self.device_type = None
            if "brandName" in config:
                if isinstance(config["brandName"], sim_handling.SanitizedString255):
                    self.brand_name = config["brandName"]
                elif config["brandName"] is not None:
                    self.brand_name = sim_handling.SanitizedString255(config["brandName"])
                else:
                    self.brand_name = None
            else:
                self.brand_name = None
            if "marketingName" in config:
                if isinstance(config["marketingName"], sim_handling.SanitizedString255):
                    self.marketing_name = config["marketingName"]
                elif config["marketingName"] is not None:
                    self.marketing_name = sim_handling.SanitizedString255(config["marketingName"])
                else:
                    self.marketing_name = None
            else:
                self.marketing_name = None
            if "modelName" in config:
                if isinstance(config["modelName"], sim_handling.SanitizedString255):
                    self.model_name = config["modelName"]
                elif config["modelName"] is not None:
                    self.model_name = sim_handling.SanitizedString255(config["modelName"])
                else:
                    self.model_name = None
            else:
                self.model_name = None
            if "formFactor" in config:
                if isinstance(config["formFactor"], sim_handling.SanitizedString20):
                    self.form_factor = config["formFactor"]
                elif config["formFactor"] is not None:
                    self.form_factor = sim_handling.SanitizedString20(config["formFactor"])
                else:
                    self.form_factor = None
            else:
                self.form_factor = None
            if "imeiStatus" in config:
                if isinstance(config["imeiStatus"], sim_handling.SimImeiStatusEnum):
                    self.imei_status = config["imeiStatus"]
                elif config["imeiStatus"] is not None:
                    self.imei_status = sim_handling.SimImeiStatusEnum(config["imeiStatus"])
                else:
                    self.imei_status = None
            else:
                self.imei_status = None
        else:
            self.iccid = []
            self.status = None
            self.network_status = None
            self.ip_address = []
            self.location_country = None
            self.tag = []
            self.device_type = None
            self.brand_name = None
            self.marketing_name = None
            self.model_name = None
            self.form_factor = None
            self.imei_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iccid": [item.request_format() for item in (self.iccid or [])],
            "status": self.status,
            "networkStatus": self.network_status,
            "ipAddress": [item.request_format() for item in (self.ip_address or [])],
            "locationCountry": self.location_country,
            "tag": [item.request_format() for item in (self.tag or [])],
            "deviceType": self.device_type,
            "brandName": self.brand_name,
            "marketingName": self.marketing_name,
            "modelName": self.model_name,
            "formFactor": self.form_factor,
            "imeiStatus": self.imei_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimLockRequest(ZscalerObject):
    """
    A class representing a SimLockRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.data_authorize = config["dataAuthorize"] if "dataAuthorize" in config else False
            self.sim_lock_details = ZscalerCollection.form_list(
                config["simLockDetails"] if "simLockDetails" in config else [], sim_handling.SimLockDetail
            )
        else:
            self.data_authorize = False
            self.sim_lock_details = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "dataAuthorize": self.data_authorize,
            "simLockDetails": [item.request_format() for item in (self.sim_lock_details or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimDataResponse(ZscalerObject):
    """
    A class representing a SimDataResponse object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.page_details = config["pageDetails"] if "pageDetails" in config else None
            self.total_usage = config["totalUsage"] if "totalUsage" in config else None
        else:
            self.page_details = None
            self.total_usage = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "pageDetails": self.page_details,
            "totalUsage": self.total_usage,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimUpdateRequest(ZscalerObject):
    """
    A class representing a SimUpdateRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            if "status" in config:
                if isinstance(config["status"], sim_handling.SimStatusEnum):
                    self.status = config["status"]
                elif config["status"] is not None:
                    self.status = sim_handling.SimStatusEnum(config["status"])
                else:
                    self.status = None
            else:
                self.status = None
            self.iccid = ZscalerCollection.form_list(config["iccid"] if "iccid" in config else [], str)
            self.reason = config["reason"] if "reason" in config else None
        else:
            self.status = None
            self.iccid = []
            self.reason = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "iccid": self.iccid,
            "reason": self.reason,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class GetActivationCodeResponse(ZscalerObject):
    """
    A class representing a GetActivationCodeResponse object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.iccid = config["iccid"] if "iccid" in config else None
            self.activation_code = config["activationCode"] if "activationCode" in config else None
            self.qr_code = config["qrCode"] if "qrCode" in config else None
        else:
            self.iccid = None
            self.activation_code = None
            self.qr_code = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iccid": self.iccid,
            "activationCode": self.activation_code,
            "qrCode": self.qr_code,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SimAssignRequest(ZscalerObject):
    """
    A class representing a SimAssignRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.assignment = config["assignment"] if "assignment" in config else None
        else:
            self.assignment = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "assignment": self.assignment,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class RefreshEsimState(ZscalerObject):
    """
    A class representing a RefreshEsimState object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.esim_state = config["esimState"] if "esimState" in config else None
        else:
            self.esim_state = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "esimState": self.esim_state,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
