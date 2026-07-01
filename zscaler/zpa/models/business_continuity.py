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
from zscaler.zpa.models import idp as idp


class BusinessContinuity(ZscalerObject):
    """
    A class representing a BusinessContinuity object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.ba_auth_domain_cert_id = config["baAuthDomainCertId"] if "baAuthDomainCertId" in config else None
            self.ba_auth_domain_cert_name = config["baAuthDomainCertName"] if "baAuthDomainCertName" in config else None
            self.backup_basedir = config["backupBasedir"] if "backupBasedir" in config else None
            self.backup_enabled = config["backupEnabled"] if "backupEnabled" in config else False
            self.backup_max_allowed_num = config["backupMaxAllowedNum"] if "backupMaxAllowedNum" in config else None
            self.backup_schedule_type = config["backupScheduleType"] if "backupScheduleType" in config else None
            self.backup_schedule_value = config["backupScheduleValue"] if "backupScheduleValue" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.encrypt_saml_response = config["encryptSamlResponse"] if "encryptSamlResponse" in config else False
            self.id = config["id"] if "id" in config else None
            self.idp_cert = config["idpCert"] if "idpCert" in config else None
            self.idp_entity_id = config["idpEntityId"] if "idpEntityId" in config else None
            self.idp_login_url = config["idpLoginUrl"] if "idpLoginUrl" in config else None
            self.max_allowed_down_time = config["maxAllowedDownTime"] if "maxAllowedDownTime" in config else None
            self.max_allowed_down_time_unit = config["maxAllowedDownTimeUnit"] if "maxAllowedDownTimeUnit" in config else None
            self.max_allowed_switch_time = config["maxAllowedSwitchTime"] if "maxAllowedSwitchTime" in config else None
            self.max_allowed_switch_time_unit = (
                config["maxAllowedSwitchTimeUnit"] if "maxAllowedSwitchTimeUnit" in config else None
            )
            if "metaData" in config:
                if isinstance(config["metaData"], idp.ServiceProvider):
                    self.meta_data = config["metaData"]
                elif config["metaData"] is not None:
                    self.meta_data = idp.ServiceProvider(config["metaData"])
                else:
                    self.meta_data = None
            else:
                self.meta_data = None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.new_user_support = config["newUserSupport"] if "newUserSupport" in config else False
            self.offline_domain = config["offlineDomain"] if "offlineDomain" in config else None
            self.read_only = config["readOnly"] if "readOnly" in config else False
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.site_s_p_cert_id = config["siteSPCertId"] if "siteSPCertId" in config else None
            self.site_s_p_cert_name = config["siteSPCertName"] if "siteSPCertName" in config else None
            self.sitec_preferred = config["sitecPreferred"] if "sitecPreferred" in config else False
            self.sitesp_c_a_certificate = config["sitespCACertificate"] if "sitespCACertificate" in config else None
            self.sitesp_c_a_private_key = config["sitespCAPrivateKey"] if "sitespCAPrivateKey" in config else None
            self.sitesp_certificate = config["sitespCertificate"] if "sitespCertificate" in config else None
            self.sitesp_encryption_certificate = (
                config["sitespEncryptionCertificate"] if "sitespEncryptionCertificate" in config else None
            )
            self.sitesp_private_key = config["sitespPrivateKey"] if "sitespPrivateKey" in config else None
            self.sitesp_signing_certificate = (
                config["sitespSigningCertificate"] if "sitespSigningCertificate" in config else None
            )
            self.sitesp_signing_private_key = (
                config["sitespSigningPrivateKey"] if "sitespSigningPrivateKey" in config else None
            )
            self.switch_time_enabled = config["switchTimeEnabled"] if "switchTimeEnabled" in config else False
            self.use_existing_idp = config["useExistingIdp"] if "useExistingIdp" in config else False
            self.user_idps_meta_data = ZscalerCollection.form_list(
                config["userIdpsMetaData"] if "userIdpsMetaData" in config else [], idp.ServiceProvider
            )
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else False
        else:
            self.ba_auth_domain_cert_id = None
            self.ba_auth_domain_cert_name = None
            self.backup_basedir = None
            self.backup_enabled = False
            self.backup_max_allowed_num = None
            self.backup_schedule_type = None
            self.backup_schedule_value = None
            self.creation_time = None
            self.encrypt_saml_response = False
            self.id = None
            self.idp_cert = None
            self.idp_entity_id = None
            self.idp_login_url = None
            self.max_allowed_down_time = None
            self.max_allowed_down_time_unit = None
            self.max_allowed_switch_time = None
            self.max_allowed_switch_time_unit = None
            self.meta_data = None
            self.modified_by = None
            self.modified_time = None
            self.new_user_support = False
            self.offline_domain = None
            self.read_only = False
            self.restriction_type = None
            self.site_s_p_cert_id = None
            self.site_s_p_cert_name = None
            self.sitec_preferred = False
            self.sitesp_c_a_certificate = None
            self.sitesp_c_a_private_key = None
            self.sitesp_certificate = None
            self.sitesp_encryption_certificate = None
            self.sitesp_private_key = None
            self.sitesp_signing_certificate = None
            self.sitesp_signing_private_key = None
            self.switch_time_enabled = False
            self.use_existing_idp = False
            self.user_idps_meta_data = []
            self.zscaler_managed = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "baAuthDomainCertId": self.ba_auth_domain_cert_id,
            "baAuthDomainCertName": self.ba_auth_domain_cert_name,
            "backupBasedir": self.backup_basedir,
            "backupEnabled": self.backup_enabled,
            "backupMaxAllowedNum": self.backup_max_allowed_num,
            "backupScheduleType": self.backup_schedule_type,
            "backupScheduleValue": self.backup_schedule_value,
            "creationTime": self.creation_time,
            "encryptSamlResponse": self.encrypt_saml_response,
            "id": self.id,
            "idpCert": self.idp_cert,
            "idpEntityId": self.idp_entity_id,
            "idpLoginUrl": self.idp_login_url,
            "maxAllowedDownTime": self.max_allowed_down_time,
            "maxAllowedDownTimeUnit": self.max_allowed_down_time_unit,
            "maxAllowedSwitchTime": self.max_allowed_switch_time,
            "maxAllowedSwitchTimeUnit": self.max_allowed_switch_time_unit,
            "metaData": self.meta_data,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "newUserSupport": self.new_user_support,
            "offlineDomain": self.offline_domain,
            "readOnly": self.read_only,
            "restrictionType": self.restriction_type,
            "siteSPCertId": self.site_s_p_cert_id,
            "siteSPCertName": self.site_s_p_cert_name,
            "sitecPreferred": self.sitec_preferred,
            "sitespCACertificate": self.sitesp_c_a_certificate,
            "sitespCAPrivateKey": self.sitesp_c_a_private_key,
            "sitespCertificate": self.sitesp_certificate,
            "sitespEncryptionCertificate": self.sitesp_encryption_certificate,
            "sitespPrivateKey": self.sitesp_private_key,
            "sitespSigningCertificate": self.sitesp_signing_certificate,
            "sitespSigningPrivateKey": self.sitesp_signing_private_key,
            "switchTimeEnabled": self.switch_time_enabled,
            "useExistingIdp": self.use_existing_idp,
            "userIdpsMetaData": [item.request_format() for item in (self.user_idps_meta_data or [])],
            "zscalerManaged": self.zscaler_managed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
