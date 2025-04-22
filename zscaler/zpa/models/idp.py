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
from zscaler.zpa.models import certificates as certificates


class IDPController(ZscalerObject):
    """
    A class for IDPController objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IDPController model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.admin_sp_signing_cert_id = config["adminSpSigningCertId"] if "adminSpSigningCertId" in config else None
            self.auto_provision = config["autoProvision"] if "autoProvision" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.delta = config["delta"] if "delta" in config else None
            self.description = config["description"] if "description" in config else None
            self.disable_saml_based_policy = config["disableSamlBasedPolicy"] if "disableSamlBasedPolicy" in config else None
            self.enable_arbitrary_auth_domains = (
                config["enableArbitraryAuthDomains"] if "enableArbitraryAuthDomains" in config else None
            )
            self.enable_scim_based_policy = config["enableScimBasedPolicy"] if "enableScimBasedPolicy" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.force_auth = config["forceAuth"] if "forceAuth" in config else None
            self.iam_idp_id = config["iamIdpId"] if "iamIdpId" in config else None
            self.idp_entity_id = config["idpEntityId"] if "idpEntityId" in config else None
            self.login_hint = config["loginHint"] if "loginHint" in config else None
            self.login_name_attribute = config["loginNameAttribute"] if "loginNameAttribute" in config else None
            self.login_url = config["loginUrl"] if "loginUrl" in config else None
            self.migration_detail = config["migrationDetail"] if "migrationDetail" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.one_identity_enabled = config["oneIdentityEnabled"] if "oneIdentityEnabled" in config else None
            self.reauth_on_user_update = config["reauthOnUserUpdate"] if "reauthOnUserUpdate" in config else None
            self.redirect_binding = config["redirectBinding"] if "redirectBinding" in config else None
            self.scim_enabled = config["scimEnabled"] if "scimEnabled" in config else None
            self.scim_service_provider_endpoint = (
                config["scimServiceProviderEndpoint"] if "scimServiceProviderEndpoint" in config else None
            )
            self.scim_shared_secret_exists = config["scimSharedSecretExists"] if "scimSharedSecretExists" in config else None
            self.sign_saml_request = config["signSamlRequest"] if "signSamlRequest" in config else None

            self.use_custom_sp_metadata = config["useCustomSPMetadata"] if "useCustomSPMetadata" in config else None

            self.user_sp_signing_cert_id = config["userSpSigningCertId"] if "userSpSigningCertId" in config else None

            self.domain_list = ZscalerCollection.form_list(config["domainList"] if "domainList" in config else [], str)

            self.sso_type = ZscalerCollection.form_list(config["ssoType"] if "ssoType" in config else [], str)

            self.certificates = ZscalerCollection.form_list(
                config["certificates"] if "certificates" in config else [], certificates.Certificate
            )

            if "adminMetadata" in config:
                if isinstance(config["adminMetadata"], ServiceProvider):
                    self.admin_metadata = config["adminMetadata"]
                elif config["adminMetadata"] is not None:
                    self.admin_metadata = ServiceProvider(config["adminMetadata"])
                else:
                    self.admin_metadata = None
            else:
                self.admin_metadata = None

            if "userMetadata" in config:
                if isinstance(config["userMetadata"], ServiceProvider):
                    self.user_metadata = config["userMetadata"]
                elif config["userMetadata"] is not None:
                    self.user_metadata = ServiceProvider(config["userMetadata"])
                else:
                    self.user_metadata = None
            else:
                self.user_metadata = None

        else:
            self.admin_metadata = None
            self.user_metadata = None
            self.admin_sp_signing_cert_id = None
            self.auto_provision = None
            self.certificates = []
            self.creation_time = None
            self.delta = None
            self.description = None
            self.disable_saml_based_policy = None
            self.domain_list = ZscalerCollection.form_list([], str)
            self.enable_arbitrary_auth_domains = None
            self.enable_scim_based_policy = None
            self.enabled = None
            self.force_auth = None
            self.iam_idp_id = None
            self.id = None
            self.idp_entity_id = None
            self.login_hint = None
            self.login_name_attribute = None
            self.login_url = None
            self.migration_detail = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.one_identity_enabled = None
            self.reauth_on_user_update = None
            self.redirect_binding = None
            self.scim_enabled = None
            self.scim_service_provider_endpoint = None
            self.scim_shared_secret_exists = None
            self.sign_saml_request = None
            self.sso_type = ZscalerCollection.form_list([], str)
            self.use_custom_sp_metadata = None
            self.user_sp_signing_cert_id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "adminMetadata": self.admin_metadata,
            "userMetadata": self.user_metadata,
            "adminSpSigningCertId": self.admin_sp_signing_cert_id,
            "autoProvision": self.auto_provision,
            "certificates": self.certificates,
            "creationTime": self.creation_time,
            "delta": self.delta,
            "description": self.description,
            "disableSamlBasedPolicy": self.disable_saml_based_policy,
            "domainList": self.domain_list,
            "enableArbitraryAuthDomains": self.enable_arbitrary_auth_domains,
            "enableScimBasedPolicy": self.enable_scim_based_policy,
            "enabled": self.enabled,
            "forceAuth": self.force_auth,
            "iamIdpId": self.iam_idp_id,
            "id": self.id,
            "idpEntityId": self.idp_entity_id,
            "loginHint": self.login_hint,
            "loginNameAttribute": self.login_name_attribute,
            "loginUrl": self.login_url,
            "migrationDetail": self.migration_detail,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "oneIdentityEnabled": self.one_identity_enabled,
            "reauthOnUserUpdate": self.reauth_on_user_update,
            "redirectBinding": self.redirect_binding,
            "scimEnabled": self.scim_enabled,
            "scimServiceProviderEndpoint": self.scim_service_provider_endpoint,
            "scimSharedSecretExists": self.scim_shared_secret_exists,
            "signSamlRequest": self.sign_saml_request,
            "ssoType": self.sso_type,
            "useCustomSPMetadata": self.use_custom_sp_metadata,
            "userSpSigningCertId": self.user_sp_signing_cert_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ServiceProvider(ZscalerObject):
    """
    A class for ServiceProvider objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the ServiceProvider model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.certificate_url = config["certificateUrl"] if "certificateUrl" in config else None
            self.sp_base_url = config["spBaseUrl"] if "spBaseUrl" in config else None
            self.sp_entity_id = config["spEntityId"] if "spEntityId" in config else False
            self.sp_metadata_url = config["spMetadataUrl"] if "spMetadataUrl" in config else False
            self.sp_post_url = config["spPostUrl"] if "spPostUrl" in config else False

        else:
            self.certificate_url = None
            self.sp_base_url = None
            self.sp_entity_id = None
            self.sp_metadata_url = None
            self.sp_post_url = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "certificateUrl": self.certificate_url,
            "spBaseUrl": self.sp_base_url,
            "spEntityId": self.sp_entity_id,
            "spMetadataUrl": self.sp_metadata_url,
            "spPostUrl": self.sp_post_url,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
