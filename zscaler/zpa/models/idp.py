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

class IDP(ZscalerObject):
    """
    A class for Identity Provider (IDP) objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        
        # Defensive programming for each key's presence
        self.id = config["id"]\
            if config and "id" in config else None
        self.modified_time = config["modifiedTime"]\
            if config and "modifiedTime" in config else None
        self.creation_time = config["creationTime"]\
            if config and "creationTime" in config else None
        self.modified_by = config["modifiedBy"]\
            if config and "modifiedBy" in config else None
        self.name = config["name"]\
            if config and "name" in config else None
        
        # Handle certificates as a list of dictionaries
        self.certificates = [
            {
                "cName": cert.get("cName"),
                "serialNo": cert.get("serialNo"),
                "certificate": cert.get("certificate"),
                "validFromInSec": cert.get("validFromInSec"),
                "validToInSec": cert.get("validToInSec"),
            }
            for cert in config.get("certificates", []) if config
        ]
        
        self.login_url = config["loginUrl"]\
            if config and "loginUrl" in config else None
        self.idp_entity_id = config["idpEntityId"]\
            if config and "idpEntityId" in config else None
        self.auto_provision = config["autoProvision"]\
            if config and "autoProvision" in config else "0"
        self.sign_saml_request = config["signSamlRequest"]\
            if config and "signSamlRequest" in config else "1"
        self.sso_type = config["ssoType"]\
            if config and "ssoType" in config else []
        self.domain_list = config["domainList"]\
            if config and "domainList" in config else []
        self.use_custom_sp_metadata = config["useCustomSPMetadata"]\
            if config and "useCustomSPMetadata" in config else False
        self.scim_enabled = config["scimEnabled"]\
            if config and "scimEnabled" in config else False
        self.enable_scim_based_policy = config["enableScimBasedPolicy"]\
            if config and "enableScimBasedPolicy" in config else False
        self.disable_saml_based_policy = config["disableSamlBasedPolicy"]\
            if config and "disableSamlBasedPolicy" in config else False
        self.reauth_on_user_update = config["reauthOnUserUpdate"]\
            if config and "reauthOnUserUpdate" in config else False
        self.admin_sp_signing_cert_id = config["adminSpSigningCertId"]\
            if config and "adminSpSigningCertId" in config else "0"
        self.enable_arbitrary_auth_domains = config["enableArbitraryAuthDomains"]\
            if config and "enableArbitraryAuthDomains" in config else "0"
        
        # Handle adminMetadata if available
        self.admin_metadata = {
            "spEntityId": config["adminMetadata"].get("spEntityId"),
            "spPostUrl": config["adminMetadata"].get("spPostUrl"),
            "certificateUrl": config["adminMetadata"].get("certificateUrl"),
            "spMetadataUrl": config["adminMetadata"].get("spMetadataUrl"),
            "spBaseUrl": config["adminMetadata"].get("spBaseUrl"),
        } if config and "adminMetadata" in config else None
        
        self.one_identity_enabled = config["oneIdentityEnabled"]\
            if config and "oneIdentityEnabled" in config else False
        self.scim_service_provider_endpoint = config["scimServiceProviderEndpoint"]\
            if config and "scimServiceProviderEndpoint" in config else None
        self.scim_shared_secret_exists = config["scimSharedSecretExists"]\
            if config and "scimSharedSecretExists" in config else False
        self.force_auth = config["forceAuth"]\
            if config and "forceAuth" in config else False
        self.login_hint = config["loginHint"]\
            if config and "loginHint" in config else True
        self.enabled = config["enabled"]\
            if config and "enabled" in config else True
        self.delta = config["delta"]\
            if config and "delta" in config else None
        self.redirect_binding = config["redirectBinding"]\
            if config and "redirectBinding" in config else False

        # Handle userMetadata if available
        self.user_metadata = {
            "spEntityId": config["userMetadata"].get("spEntityId"),
            "spPostUrl": config["userMetadata"].get("spPostUrl"),
            "certificateUrl": config["userMetadata"].get("certificateUrl"),
            "spMetadataUrl": config["userMetadata"].get("spMetadataUrl"),
            "spBaseUrl": config["userMetadata"].get("spBaseUrl"),
        } if config and "userMetadata" in config else None

    def request_format(self):
        """
        Formats the IDP data into a dictionary suitable for API requests.
        """
        return {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "name": self.name,
            "certificates": [
                {
                    "cName": cert.get("cName"),
                    "serialNo": cert.get("serialNo"),
                    "certificate": cert.get("certificate"),
                    "validFromInSec": cert.get("validFromInSec"),
                    "validToInSec": cert.get("validToInSec"),
                }
                for cert in self.certificates
            ],
            "loginUrl": self.login_url,
            "idpEntityId": self.idp_entity_id,
            "autoProvision": self.auto_provision,
            "signSamlRequest": self.sign_saml_request,
            "ssoType": self.sso_type,
            "domainList": self.domain_list,
            "useCustomSPMetadata": self.use_custom_sp_metadata,
            "scimEnabled": self.scim_enabled,
            "enableScimBasedPolicy": self.enable_scim_based_policy,
            "disableSamlBasedPolicy": self.disable_saml_based_policy,
            "reauthOnUserUpdate": self.reauth_on_user_update,
            "adminSpSigningCertId": self.admin_sp_signing_cert_id,
            "enableArbitraryAuthDomains": self.enable_arbitrary_auth_domains,
            "adminMetadata": self.admin_metadata,
            "oneIdentityEnabled": self.one_identity_enabled,
            "scimServiceProviderEndpoint": self.scim_service_provider_endpoint,
            "scimSharedSecretExists": self.scim_shared_secret_exists,
            "forceAuth": self.force_auth,
            "loginHint": self.login_hint,
            "enabled": self.enabled,
            "delta": self.delta,
            "redirectBinding": self.redirect_binding,
            "userMetadata": self.user_metadata,
        }
