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


class DomainProfiles(ZscalerObject):
    """
    A class for DomainProfiles objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DomainProfiles model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.profile_id = config["profileId"] \
                if "profileId" in config else None
            self.profile_name = config["profileName"] \
                if "profileName" in config else None
            self.include_company_domains = config["includeCompanyDomains"] \
                if "includeCompanyDomains" in config else None
            self.include_subdomains = config["includeSubdomains"] \
                if "includeSubdomains" in config else None
            self.description = config["description"] \
                if "description" in config else None

            self.custom_domains = ZscalerCollection.form_list(
                config["customDomains"] if "customDomains" in config else [], str
            )
            self.predefined_email_domains = ZscalerCollection.form_list(
                config["predefinedEmailDomains"] if "predefinedEmailDomains" in config else [], str
            )
        else:
            self.profile_id = None
            self.profile_name = None
            self.include_company_domains = None
            self.include_subdomains = None
            self.description = None
            self.custom_domains = []
            self.predefined_email_domains = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "profileId": self.profile_id,
            "profileName": self.profile_name,
            "includeCompanyDomains": self.include_company_domains,
            "includeSubdomains": self.include_subdomains,
            "description": self.description,
            "customDomains": self.custom_domains,
            "predefinedEmailDomains": self.predefined_email_domains
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class QuarantineTombstoneTemplate(ZscalerObject):
    """
    A class for QuarantineTombstoneTemplate objects.
    """

    def __init__(self, config=None):
        """
        Initialize the QuarantineTombstoneTemplate model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.description = config["description"] \
                if "description" in config else None

        else:
            self.id = None
            self.name = None
            self.description = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CasbEmailLabel(ZscalerObject):
    """
    A class for CasbEmailLabel objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CasbEmailLabel model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.label_desc = config["labelDesc"] \
                if "labelDesc" in config else None
            self.label_color = config["labelColor"] \
                if "labelColor" in config else None
            self.label_deleted = config["labelDeleted"] \
                if "labelDeleted" in config else None
        else:
            self.id = None
            self.name = None
            self.label_desc = None
            self.label_color = None
            self.label_deleted = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "labelDesc": self.label_desc,
            "labelColor": self.label_color,
            "labelDeleted": self.label_deleted,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CasbTenant(ZscalerObject):
    """
    A class for CasbTenant objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CasbTenant model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.tenant_id = config["tenantId"] \
                if "tenantId" in config else None
            self.enterprise_tenant_id = config["enterpriseTenantId"] \
                if "enterpriseTenantId" in config else None
            self.tenant_name = config["tenantName"] \
                if "tenantName" in config else None
            self.saas_application = config["saasApplication"] \
                if "saasApplication" in config else None

            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.last_tenant_validation_time = config["lastTenantValidationTime"] \
                if "lastTenantValidationTime" in config else None
            self.tenant_deleted = config["tenantDeleted"] \
                if "tenantDeleted" in config else None
            self.tenant_webhook_enabled = config["tenantWebhookEnabled"] \
                if "tenantWebhookEnabled" in config else None
            self.re_auth = config["reAuth"] \
                if "reAuth" in config else None
            self.status = ZscalerCollection.form_list(
                config["status"] if "status" in config else [], str
            )
            self.features_supported = ZscalerCollection.form_list(
                config["featuresSupported"] if "featuresSupported" in config else [], str
            )
            if "zscalerAppTenantId" in config:
                if isinstance(config["zscalerAppTenantId"], common.CommonBlocks):
                    self.zscaler_app_tenant_id = config["zscalerAppTenantId"]
                elif config["zscalerAppTenantId"] is not None:
                    self.zscaler_app_tenant_id = common.CommonBlocks(config["zscalerAppTenantId"])
                else:
                    self.zscaler_app_tenant_id = None
            else:
                self.zscaler_app_tenant_id = None
        else:
            self.tenant_id = None
            self.enterprise_tenant_id = None
            self.zscaler_app_tenant_id = None
            self.tenant_name = None
            self.saas_application = None
            self.status = []
            self.modified_time = None
            self.last_tenant_validation_time = None
            self.tenant_deleted = None
            self.tenant_webhook_enabled = None
            self.re_auth = None
            self.features_supported = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "tenantId": self.tenant_id,
            "enterpriseTenantId": self.enterprise_tenant_id,
            "zscalerAppTenantId": self.zscaler_app_tenant_id,
            "tenantName": self.tenant_name,
            "saasApplication": self.saas_application,
            "status": self.status,
            "modifiedTime": self.modified_time,
            "lastTenantValidationTime": self.last_tenant_validation_time,
            "tenantDeleted": self.tenant_deleted,
            "tenantWebhookEnabled": self.tenant_webhook_enabled,
            "reAuth": self.re_auth,
            "featuresSupported": self.features_supported
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
