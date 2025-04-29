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


class RiskProfiles(ZscalerObject):
    """
    A class for RiskProfiles objects.
    """

    def __init__(self, config=None):
        """
        Initialize the RiskProfiles model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.profile_name = config["profileName"] if "profileName" in config else None
            self.profile_type = config["profileType"] if "profileType" in config else None
            self.risk_index = ZscalerCollection.form_list(config["riskIndex"] if "riskIndex" in config else [], str)
            self.status = config["status"] if "status" in config else None
            self.exclude_certificates = config["excludeCertificates"] if "excludeCertificates" in config else None
            self.certifications = ZscalerCollection.form_list(
                config["certifications"] if "certifications" in config else [], str
            )
            self.poor_items_of_service = config["poorItemsOfService"] if "poorItemsOfService" in config else None
            self.admin_audit_logs = config["adminAuditLogs"] if "adminAuditLogs" in config else None
            self.data_breach = config["dataBreach"] if "dataBreach" in config else None
            self.source_ip_restrictions = config["sourceIpRestrictions"] if "sourceIpRestrictions" in config else None
            self.mfa_support = config["mfaSupport"] if "mfaSupport" in config else None
            self.ssl_pinned = config["sslPinned"] if "sslPinned" in config else None
            self.http_security_headers = config["httpSecurityHeaders"] if "httpSecurityHeaders" in config else None
            self.evasive = config["evasive"] if "evasive" in config else None
            self.dns_caa_policy = config["dnsCaaPolicy"] if "dnsCaaPolicy" in config else None
            self.weak_cipher_support = config["weakCipherSupport"] if "weakCipherSupport" in config else None
            self.password_strength = config["passwordStrength"] if "passwordStrength" in config else None
            self.ssl_cert_validity = config["sslCertValidity"] if "sslCertValidity" in config else None
            self.vulnerability = config["vulnerability"] if "vulnerability" in config else None
            self.malware_scanning_for_content = (
                config["malwareScanningForContent"] if "malwareScanningForContent" in config else None
            )
            self.file_sharing = config["fileSharing"] if "fileSharing" in config else None
            self.ssl_cert_key_size = config["sslCertKeySize"] if "sslCertKeySize" in config else None
            self.vulnerable_to_heart_bleed = config["vulnerableToHeartBleed"] if "vulnerableToHeartBleed" in config else None
            self.vulnerable_to_log_jam = config["vulnerableToLogJam"] if "vulnerableToLogJam" in config else None
            self.vulnerable_to_poodle = config["vulnerableToPoodle"] if "vulnerableToPoodle" in config else None
            self.vulnerability_disclosure = config["vulnerabilityDisclosure"] if "vulnerabilityDisclosure" in config else None
            self.support_for_waf = config["supportForWaf"] if "supportForWaf" in config else None
            self.remote_screen_sharing = config["remoteScreenSharing"] if "remoteScreenSharing" in config else None
            self.sender_policy_framework = config["senderPolicyFramework"] if "senderPolicyFramework" in config else None
            self.domain_keys_identified_mail = (
                config["domainKeysIdentifiedMail"] if "domainKeysIdentifiedMail" in config else None
            )
            self.domain_based_message_auth = config["domainBasedMessageAuth"] if "domainBasedMessageAuth" in config else None
            self.data_encryption_in_transit = ZscalerCollection.form_list(
                config["dataEncryptionInTransit"] if "dataEncryptionInTransit" in config else [], str
            )
            self.last_mod_time = config["lastModTime"] if "lastModTime" in config else None
            self.create_time = config["createTime"] if "createTime" in config else None
            if "modifiedBy" in config:
                if isinstance(config["modifiedBy"], common.CommonBlocks):
                    self.modified_by = config["modifiedBy"]
                elif config["modifiedBy"] is not None:
                    self.modified_by = common.CommonBlocks(config["modifiedBy"])
                else:
                    self.modified_by = None
            else:
                self.modified_by = None
            self.custom_tags = ZscalerCollection.form_list(config["customTags"] if "customTags" in config else [], str)
        else:
            self.id = None
            self.profile_name = None
            self.profile_type = None
            self.risk_index = ZscalerCollection.form_list([], str)
            self.status = None
            self.exclude_certificates = None
            self.certifications = ZscalerCollection.form_list([], str)
            self.poor_items_of_service = None
            self.admin_audit_logs = None
            self.data_breach = None
            self.source_ip_restrictions = None
            self.mfa_support = None
            self.ssl_pinned = None
            self.http_security_headers = None
            self.evasive = None
            self.dns_caa_policy = None
            self.weak_cipher_support = None
            self.password_strength = None
            self.ssl_cert_validity = None
            self.vulnerability = None
            self.malware_scanning_for_content = None
            self.file_sharing = None
            self.ssl_cert_key_size = None
            self.vulnerable_to_heart_bleed = None
            self.vulnerable_to_log_jam = None
            self.vulnerable_to_poodle = None
            self.vulnerability_disclosure = None
            self.support_for_waf = None
            self.remote_screen_sharing = None
            self.sender_policy_framework = None
            self.domain_keys_identified_mail = None
            self.domain_based_message_auth = None
            self.data_encryption_in_transit = ZscalerCollection.form_list([], str)
            self.last_mod_time = None
            self.create_time = None
            self.modified_by = None
            self.custom_tags = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "profileName": self.profile_name,
            "profileType": self.profile_type,
            "riskIndex": self.risk_index,
            "status": self.status,
            "excludeCertificates": self.exclude_certificates,
            "certifications": self.certifications,
            "poorItemsOfService": self.poor_items_of_service,
            "adminAuditLogs": self.admin_audit_logs,
            "dataBreach": self.data_breach,
            "sourceIpRestrictions": self.source_ip_restrictions,
            "mfaSupport": self.mfa_support,
            "sslPinned": self.ssl_pinned,
            "httpSecurityHeaders": self.http_security_headers,
            "evasive": self.evasive,
            "dnsCaaPolicy": self.dns_caa_policy,
            "weakCipherSupport": self.weak_cipher_support,
            "passwordStrength": self.password_strength,
            "sslCertValidity": self.ssl_cert_validity,
            "vulnerability": self.vulnerability,
            "malwareScanningForContent": self.malware_scanning_for_content,
            "fileSharing": self.file_sharing,
            "sslCertKeySize": self.ssl_cert_key_size,
            "vulnerableToHeartBleed": self.vulnerable_to_heart_bleed,
            "vulnerableToLogJam": self.vulnerable_to_log_jam,
            "vulnerableToPoodle": self.vulnerable_to_poodle,
            "vulnerabilityDisclosure": self.vulnerability_disclosure,
            "supportForWaf": self.support_for_waf,
            "remoteScreenSharing": self.remote_screen_sharing,
            "senderPolicyFramework": self.sender_policy_framework,
            "domainKeysIdentifiedMail": self.domain_keys_identified_mail,
            "domainBasedMessageAuth": self.domain_based_message_auth,
            "dataEncryptionInTransit": self.data_encryption_in_transit,
            "lastModTime": self.last_mod_time,
            "createTime": self.create_time,
            "modifiedBy": self.modified_by,
            "customTags": self.custom_tags,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
