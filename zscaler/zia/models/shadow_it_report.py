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


class ShadowITReport(ZscalerObject):
    """
    A class representing a Shadow IT Report object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.duration = config["duration"] if "duration" in config else None
            self.app_name = config["appName"] if "appName" in config else None

            # Handling simple lists
            self.application = ZscalerCollection.form_list(config["application"] if "application" in config else [], str)
            self.application_category = ZscalerCollection.form_list(
                config["applicationCategory"] if "applicationCategory" in config else [], str
            )
            self.risk_index = ZscalerCollection.form_list(config["riskIndex"] if "riskIndex" in config else [], int)
            self.sanctioned_state = ZscalerCollection.form_list(
                config["sanctionedState"] if "sanctionedState" in config else [], str
            )
            self.employees = ZscalerCollection.form_list(config["employees"] if "employees" in config else [], str)
            self.source_ip_restriction = ZscalerCollection.form_list(
                config["sourceIpRestriction"] if "sourceIpRestriction" in config else [], str
            )
            self.mfa_support = ZscalerCollection.form_list(config["mfaSupport"] if "mfaSupport" in config else [], str)
            self.admin_audit_logs = ZscalerCollection.form_list(
                config["adminAuditLogs"] if "adminAuditLogs" in config else [], str
            )
            self.had_breach_in_last_3_years = ZscalerCollection.form_list(
                config["hadBreachInLast3Years"] if "hadBreachInLast3Years" in config else [], str
            )
            self.have_poor_items_of_service = ZscalerCollection.form_list(
                config["havePoorItemsOfService"] if "havePoorItemsOfService" in config else [], str
            )
            self.password_strength = ZscalerCollection.form_list(
                config["passwordStrength"] if "passwordStrength" in config else [], str
            )
            self.ssl_pinned = ZscalerCollection.form_list(config["sslPinned"] if "sslPinned" in config else [], str)
            self.evasive = ZscalerCollection.form_list(config["evasive"] if "evasive" in config else [], str)
            self.have_https_security_header_support = ZscalerCollection.form_list(
                config["haveHTTPSecurityHeaderSupport"] if "haveHTTPSecurityHeaderSupport" in config else [], str
            )
            self.dns_caa_policy = ZscalerCollection.form_list(config["dnsCAAPolicy"] if "dnsCAAPolicy" in config else [], str)
            self.have_weak_cipher_support = ZscalerCollection.form_list(
                config["haveWeakCipherSupport"] if "haveWeakCipherSupport" in config else [], str
            )
            self.ssl_certification_validity = ZscalerCollection.form_list(
                config["sslCertificationValidity"] if "sslCertificationValidity" in config else [], str
            )
            self.malware_scanning_content = ZscalerCollection.form_list(
                config["malwareScanningContent"] if "malwareScanningContent" in config else [], str
            )
            self.file_sharing = ZscalerCollection.form_list(config["fileSharing"] if "fileSharing" in config else [], str)
            self.remote_access_screen_sharing = ZscalerCollection.form_list(
                config["remoteAccessScreenSharing"] if "remoteAccessScreenSharing" in config else [], str
            )
            self.sender_policy_framework = ZscalerCollection.form_list(
                config["senderPolicyFramework"] if "senderPolicyFramework" in config else [], str
            )
            self.domain_keys_identified_mail = ZscalerCollection.form_list(
                config["domainKeysIdentifiedMail"] if "domainKeysIdentifiedMail" in config else [], str
            )
            self.domain_based_message_authentication = ZscalerCollection.form_list(
                config["domainBasedMessageAuthentication"] if "domainBasedMessageAuthentication" in config else [], str
            )
            self.vulnerable_disclosure_program = ZscalerCollection.form_list(
                config["vulnerableDisclosureProgram"] if "vulnerableDisclosureProgram" in config else [], str
            )
            self.waf_support = ZscalerCollection.form_list(config["wafSupport"] if "wafSupport" in config else [], str)
            self.vulnerability = ZscalerCollection.form_list(config["vulnerability"] if "vulnerability" in config else [], str)
            self.valid_ssl_certificate = ZscalerCollection.form_list(
                config["validSSLCertificate"] if "validSSLCertificate" in config else [], str
            )
            self.data_encryption_in_transit = ZscalerCollection.form_list(
                config["dataEncryptionInTransit"] if "dataEncryptionInTransit" in config else [], str
            )
            self.vulnerable_to_heart_bleed = ZscalerCollection.form_list(
                config["vulnerableToHeartBleed"] if "vulnerableToHeartBleed" in config else [], str
            )
            self.vulnerable_to_poodle = ZscalerCollection.form_list(
                config["vulnerableToPoodle"] if "vulnerableToPoodle" in config else [], str
            )
            self.vulnerable_to_logjam = ZscalerCollection.form_list(
                config["vulnerableToLogJam"] if "vulnerableToLogJam" in config else [], str
            )
            self.ssl_cert_key_algo = ZscalerCollection.form_list(
                config["sslCertKeyAlgo"] if "sslCertKeyAlgo" in config else [], str
            )

            # Handling nested objects with lists
            self.order = (
                {
                    "on": config["order"]["on"] if "order" in config and "on" in config["order"] else None,
                    "by": config["order"]["by"] if "order" in config and "by" in config["order"] else None,
                }
                if "order" in config
                else None
            )

            # Handling nested object for certKeySize and supportedCertifications
            self.cert_key_size = (
                {
                    "operation": (
                        config["certKeySize"]["operation"]
                        if "certKeySize" in config and "operation" in config["certKeySize"]
                        else None
                    ),
                    "value": (
                        ZscalerCollection.form_list(config["certKeySize"]["value"], str)
                        if "certKeySize" in config and "value" in config["certKeySize"]
                        else []
                    ),
                }
                if "certKeySize" in config
                else None
            )

            self.supported_certifications = (
                {
                    "operation": (
                        config["supportedCertifications"]["operation"]
                        if "supportedCertifications" in config and "operation" in config["supportedCertifications"]
                        else None
                    ),
                    "value": (
                        ZscalerCollection.form_list(config["supportedCertifications"]["value"], str)
                        if "supportedCertifications" in config and "value" in config["supportedCertifications"]
                        else []
                    ),
                }
                if "supportedCertifications" in config
                else None
            )

            # Handling lists of objects for dataConsumed
            self.data_consumed = (
                [{"min": data["min"], "max": data["max"]} for data in config["dataConsumed"]]
                if "dataConsumed" in config
                else []
            )

        else:
            # Defaults when config is None
            self.duration = None
            self.app_name = None
            self.application = []
            self.application_category = []
            self.risk_index = []
            self.sanctioned_state = []
            self.employees = []
            self.source_ip_restriction = []
            self.mfa_support = []
            self.admin_audit_logs = []
            self.had_breach_in_last_3_years = []
            self.have_poor_items_of_service = []
            self.password_strength = []
            self.ssl_pinned = []
            self.evasive = []
            self.have_https_security_header_support = []
            self.dns_caa_policy = []
            self.have_weak_cipher_support = []
            self.ssl_certification_validity = []
            self.malware_scanning_content = []
            self.file_sharing = []
            self.remote_access_screen_sharing = []
            self.sender_policy_framework = []
            self.domain_keys_identified_mail = []
            self.domain_based_message_authentication = []
            self.vulnerable_disclosure_program = []
            self.waf_support = []
            self.vulnerability = []
            self.valid_ssl_certificate = []
            self.data_encryption_in_transit = []
            self.vulnerable_to_heart_bleed = []
            self.vulnerable_to_poodle = []
            self.vulnerable_to_logjam = []
            self.ssl_cert_key_algo = []
            self.order = None
            self.cert_key_size = None
            self.supported_certifications = None
            self.data_consumed = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "duration": self.duration,
            "appName": self.app_name,
            "application": self.application,
            "applicationCategory": self.application_category,
            "riskIndex": self.risk_index,
            "sanctionedState": self.sanctioned_state,
            "employees": self.employees,
            "sourceIpRestriction": self.source_ip_restriction,
            "mfaSupport": self.mfa_support,
            "adminAuditLogs": self.admin_audit_logs,
            "hadBreachInLast3Years": self.had_breach_in_last_3_years,
            "havePoorItemsOfService": self.have_poor_items_of_service,
            "passwordStrength": self.password_strength,
            "sslPinned": self.ssl_pinned,
            "evasive": self.evasive,
            "haveHTTPSecurityHeaderSupport": self.have_https_security_header_support,
            "dnsCAAPolicy": self.dns_caa_policy,
            "haveWeakCipherSupport": self.have_weak_cipher_support,
            "sslCertificationValidity": self.ssl_certification_validity,
            "malwareScanningContent": self.malware_scanning_content,
            "fileSharing": self.file_sharing,
            "remoteAccessScreenSharing": self.remote_access_screen_sharing,
            "senderPolicyFramework": self.sender_policy_framework,
            "domainKeysIdentifiedMail": self.domain_keys_identified_mail,
            "domainBasedMessageAuthentication": self.domain_based_message_authentication,
            "vulnerableDisclosureProgram": self.vulnerable_disclosure_program,
            "wafSupport": self.waf_support,
            "vulnerability": self.vulnerability,
            "validSSLCertificate": self.valid_ssl_certificate,
            "dataEncryptionInTransit": self.data_encryption_in_transit,
            "vulnerableToHeartBleed": self.vulnerable_to_heart_bleed,
            "vulnerableToPoodle": self.vulnerable_to_poodle,
            "vulnerableToLogJam": self.vulnerable_to_logjam,
            "sslCertKeyAlgo": self.ssl_cert_key_algo,
            "order": self.order,
            "certKeySize": self.cert_key_size,
            "supportedCertifications": self.supported_certifications,
            "dataConsumed": self.data_consumed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CloudapplicationsAndTags(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        self.id = config["id"] if "id" in config else None
        self.name = config["name"] if "name" in config else None

    def request_format(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class CloudApplicationBulkUpdate(ZscalerObject):
    """
    A class representing the payload for the bulk update of Cloud Applications.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.sanctioned_state = config["sanctionedState"] if "sanctionedState" in config else None

            self.application_ids = ZscalerCollection.form_list(
                config["applicationIds"] if "applicationIds" in config else [], int
            )

            self.custom_tags = ZscalerCollection.form_list(
                config["customTags"] if "customTags" in config else [], CloudapplicationsAndTags
            )
        else:
            self.sanctioned_state = None
            self.application_ids = []
            self.custom_tags = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "sanctionedState": self.sanctioned_state,
            "applicationIds": self.application_ids,
            "customTags": [tag.request_format() for tag in self.custom_tags],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
