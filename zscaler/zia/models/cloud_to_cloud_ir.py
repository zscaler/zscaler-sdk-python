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


class CloudToCloudIR(ZscalerObject):
    """
    A class for Cloud-to-Cloud Incident Forwarding objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Cloud-to-Cloud Incident Forwarding model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None

            self.last_tenant_validation_time = config["lastTenantValidationTime"] \
                if "lastTenantValidationTime" in config else None

            if "lastValidationMsg" in config:
                if isinstance(config["lastValidationMsg"], LastValidationMsg):
                    self.last_validation_msg = config["lastValidationMsg"]
                elif config["lastValidationMsg"] is not None:
                    self.last_validation_msg = LastValidationMsg(config["lastValidationMsg"])
                else:
                    self.last_validation_msg = None
            else:
                self.last_validation_msg = None

            self.status = ZscalerCollection.form_list(
                config["status"] if "status" in config else [], str
            )

            if "onboardableEntity" in config:
                if isinstance(config["onboardableEntity"], OnboardableEntity):
                    self.onboardable_entity = config["onboardableEntity"]
                elif config["onboardableEntity"] is not None:
                    self.onboardable_entity = OnboardableEntity(config["onboardableEntity"])
                else:
                    self.onboardable_entity = None
            else:
                self.onboardable_entity = None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None
        else:
            self.id = None
            self.name = None
            self.status = ZscalerCollection.form_list([], str)
            self.modified_time = None
            self.last_modified_by = None
            self.last_tenant_validation_time = None
            self.last_validation_msg = None
            self.onboardable_entity = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "modifiedTime": self.modified_time,
            "lastModifiedBy": self.last_modified_by,
            "lastTenantValidationTime": self.last_tenant_validation_time,
            "lastValidationMsg": self.last_validation_msg,
            "onboardableEntity": self.onboardable_entity
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TenantAuthorizationInfo(ZscalerObject):
    """
    A class for Tenant Authorization Info objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Tenant Authorization Info model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.access_token = config["accessToken"] \
                if "accessToken" in config else None
            self.bot_token = config["botToken"] \
                if "botToken" in config else None
            self.redirect_url = config["redirectUrl"] \
                if "redirectUrl" in config else None
            self.type = config["type"] \
                if "type" in config else None
            self.env = config["env"] \
                if "env" in config else None
            self.temp_auth_code = config["tempAuthCode"] \
                if "tempAuthCode" in config else None
            self.subdomain = config["subdomain"] \
                if "subdomain" in config else None
            self.apicp = config["apicp"] \
                if "apicp" in config else None
            self.client_id = config["clientId"] \
                if "clientId" in config else None
            self.client_secret = config["clientSecret"] \
                if "clientSecret" in config else None
            self.secret_token = config["secretToken"] \
                if "secretToken" in config else None
            self.user_name = config["userName"] \
                if "userName" in config else None
            self.user_pwd = config["userPwd"] \
                if "userPwd" in config else None
            self.instance_url = config["instanceUrl"] \
                if "instanceUrl" in config else None
            self.role_arn = config["roleArn"] \
                if "roleArn" in config else None
            self.quarantine_bucket_name = config["quarantineBucketName"] \
                if "quarantineBucketName" in config else None
            self.cloud_trail_bucket_name = config["cloudTrailBucketName"] \
                if "cloudTrailBucketName" in config else None
            self.bot_id = config["botId"] \
                if "botId" in config else None
            self.org_api_key = config["orgApiKey"] \
                if "orgApiKey" in config else None
            self.external_id = config["externalId"] \
                if "externalId" in config else None
            self.enterprise_id = config["enterpriseId"] \
                if "enterpriseId" in config else None
            self.cred_json = config["credJson"] \
                if "credJson" in config else None
            self.role = config["role"] \
                if "role" in config else None
            self.organization_id = config["organizationId"] \
                if "organizationId" in config else None
            self.workspace_name = config["workspaceName"] \
                if "workspaceName" in config else None
            self.workspace_id = config["workspaceId"] \
                if "workspaceId" in config else None
            self.qtn_channel_url = config["qtnChannelUrl"] \
                if "qtnChannelUrl" in config else None
            self.features_supported = ZscalerCollection.form_list(
                config["featuresSupported"] if "featuresSupported" in config else [], str
            )
            self.mal_qtn_lib_name = config["malQtnLibName"] \
                if "malQtnLibName" in config else None
            self.dlp_qtn_lib_name = config["dlpQtnLibName"] \
                if "dlpQtnLibName" in config else None
            self.credentials = config["credentials"] \
                if "credentials" in config else None
            self.token_endpoint = config["tokenEndpoint"] \
                if "tokenEndpoint" in config else None
            self.rest_api_endpoint = config["restApiEndpoint"] \
                if "restApiEndpoint" in config else None

            self.qtn_info_cleared = config["qtnInfoCleared"] \
                if "qtnInfoCleared" in config else None

            self.qtn_info = ZscalerCollection.form_list(
                config["qtnInfo"] if "qtnInfo" in config else [], QtnInfo
            )

            self.smir_bucket_config = ZscalerCollection.form_list(
                config["smirBucketConfig"] if "smirBucketConfig" in config else [], SmirBucketConfig
            )
        else:
            self.access_token = None
            self.bot_token = None
            self.redirect_url = None
            self.type = None
            self.env = None
            self.temp_auth_code = None
            self.subdomain = None
            self.apicp = None
            self.client_id = None
            self.client_secret = None
            self.secret_token = None
            self.user_name = None
            self.user_pwd = None
            self.instance_url = None
            self.role_arn = None
            self.quarantine_bucket_name = None
            self.cloud_trail_bucket_name = None
            self.bot_id = None
            self.org_api_key = None
            self.external_id = None
            self.enterprise_id = None
            self.cred_json = None
            self.role = None
            self.organization_id = None
            self.workspace_name = None
            self.workspace_id = None
            self.qtn_channel_url = None
            self.features_supported = []
            self.mal_qtn_lib_name = None
            self.dlp_qtn_lib_name = None
            self.credentials = None
            self.token_endpoint = None
            self.rest_api_endpoint = None
            self.smir_bucket_config = []
            self.qtn_info = []
            self.qtn_info_cleared = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "accessToken": self.access_token,
            "botToken": self.bot_token,
            "redirectUrl": self.redirect_url,
            "type": self.type,
            "env": self.env,
            "tempAuthCode": self.temp_auth_code,
            "subdomain": self.subdomain,
            "apicp": self.apicp,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "secretToken": self.secret_token,
            "userName": self.user_name,
            "userPwd": self.user_pwd,
            "instanceUrl": self.instance_url,
            "roleArn": self.role_arn,
            "quarantineBucketName": self.quarantine_bucket_name,
            "cloudTrailBucketName": self.cloud_trail_bucket_name,
            "botId": self.bot_id,
            "orgApiKey": self.org_api_key,
            "externalId": self.external_id,
            "enterpriseId": self.enterprise_id,
            "credJson": self.cred_json,
            "role": self.role,
            "organizationId": self.organization_id,
            "workspaceName": self.workspace_name,
            "workspaceId": self.workspace_id,
            "qtnChannelUrl": self.qtn_channel_url,
            "featuresSupported": self.features_supported,
            "malQtnLibName": self.mal_qtn_lib_name,
            "dlpQtnLibName": self.dlp_qtn_lib_name,
            "credentials": self.credentials,
            "tokenEndpoint": self.token_endpoint,
            "restApiEndpoint": self.rest_api_endpoint,
            "smirBucketConfig": self.smir_bucket_config,
            "qtnInfo": self.qtn_info,
            "qtnInfoCleared": self.qtn_info_cleared,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class OnboardableEntity(ZscalerObject):
    """
    A class for OnboardableEntity objects.
    """

    def __init__(self, config=None):
        """
        Initialize the OnboardableEntity model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.type = config["type"] \
                if "type" in config else None
            self.application = config["application"] \
                if "application" in config else None
            self.enterprise_tenant_id = config["enterpriseTenantId"] \
                if "enterpriseTenantId" in config else None

            if "tenantAuthorizationInfo" in config:
                if isinstance(config["tenantAuthorizationInfo"], TenantAuthorizationInfo):
                    self.tenant_authorization_info = config["tenantAuthorizationInfo"]
                elif config["tenantAuthorizationInfo"] is not None:
                    self.tenant_authorization_info = TenantAuthorizationInfo(config["tenantAuthorizationInfo"])
                else:
                    self.tenant_authorization_info = None
            else:
                self.tenant_authorization_info = None

            if "zscalerAppTenantId" in config:
                if isinstance(config["zscalerAppTenantId"], common.CommonBlocks):
                    self.zscaler_app_tenant_id = config["zscalerAppTenantId"]
                elif config["zscalerAppTenantId"] is not None:
                    self.zscaler_app_tenant_id = common.CommonBlocks(config["zscalerAppTenantId"])
                else:
                    self.zscaler_app_tenant_id = None
            else:
                self.zscaler_app_tenant_id = None

            if "lastValidationMsg" in config:
                if isinstance(config["lastValidationMsg"], LastValidationMsg):
                    self.last_validation_msg = config["lastValidationMsg"]
                elif config["lastValidationMsg"] is not None:
                    self.last_validation_msg = LastValidationMsg(config["lastValidationMsg"])
                else:
                    self.last_validation_msg = None
            else:
                self.last_validation_msg = None
        else:
            self.id = None
            self.name = None
            self.type = None
            self.application = None
            self.tenant_authorization_info = None
            self.zscaler_app_tenant_id = None
            self.enterprise_tenant_id = None
            self.last_validation_msg = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "application": self.application,
            "tenantAuthorizationInfo": self.tenant_authorization_info,
            "zscalerAppTenantId": self.zscaler_app_tenant_id,
            "enterpriseTenantId": self.enterprise_tenant_id,
            "lastValidationMsg": self.last_validation_msg,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SmirBucketConfig(ZscalerObject):
    """
    A class for SmirBucketConfig objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SmirBucketConfig model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.url = config["url"] \
                if "url" in config else None
            self.status = config["status"] \
                if "status" in config else None
        else:
            self.id = None
            self.name = None
            self.url = None
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class QtnInfo(ZscalerObject):
    """
    A class for QtnInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the QtnInfo model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.admin_id = config["adminId"] \
                if "adminId" in config else None
            self.qtn_folder_path = config["qtnFolderPath"] \
                if "qtnFolderPath" in config else None
            self.mod_time = config["modTime"] \
                if "modTime" in config else None
        else:
            self.admin_id = None
            self.qtn_folder_path = None
            self.mod_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "adminId": self.admin_id,
            "qtnFolderPath": self.qtn_folder_path,
            "modTime": self.mod_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LastValidationMsg(ZscalerObject):
    """
    A class for LastValidationMsg objects.
    """

    def __init__(self, config=None):
        """
        Initialize the LastValidationMsg model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.error_msg = config["errorMsg"] \
                if "errorMsg" in config else None
            self.error_code = config["errorCode"] \
                if "errorCode" in config else None
        else:
            self.error_msg = None
            self.error_code = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "errorMsg": self.error_msg,
            "errorCode": self.error_code,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
