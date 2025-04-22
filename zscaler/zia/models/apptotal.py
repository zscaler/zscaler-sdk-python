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


class AppTotal(ZscalerObject):
    """
    A class for App Total 3rd-Party App Governance API objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.name = config["name"] if "name" in config else None
            self.publisher_name = (
                config["publisher"]["name"] if "publisher" in config and "name" in config["publisher"] else None
            )
            self.publisher_description = (
                config["publisher"]["description"] if "publisher" in config and "description" in config["publisher"] else None
            )
            self.publisher_site_url = (
                config["publisher"]["siteUrl"] if "publisher" in config and "siteUrl" in config["publisher"] else None
            )
            self.publisher_logo_url = (
                config["publisher"]["logoUrl"] if "publisher" in config and "logoUrl" in config["publisher"] else None
            )
            self.platform = config["platform"] if "platform" in config else None
            self.description = config["description"] if "description" in config else None
            self.redirect_urls = ZscalerCollection.form_list(config["redirectUrls"] if "redirectUrls" in config else [], str)
            self.website_urls = ZscalerCollection.form_list(config["websiteUrls"] if "websiteUrls" in config else [], str)
            self.categories = ZscalerCollection.form_list(config["categories"] if "categories" in config else [], str)
            self.tags = ZscalerCollection.form_list(config["tags"] if "tags" in config else [], str)
            self.permission_level = config["permissionLevel"] if "permissionLevel" in config else None
            self.risk_score = config["riskScore"] if "riskScore" in config else None
            self.risk = config["risk"] if "risk" in config else None
            self.external_ids = ZscalerCollection.form_list(config["externalIds"] if "externalIds" in config else [], dict)
            self.client_id = config["clientId"] if "clientId" in config else None
            self.permissions = ZscalerCollection.form_list(config["permissions"] if "permissions" in config else [], dict)
            self.compliance = ZscalerCollection.form_list(config["compliance"] if "compliance" in config else [], str)
            self.data_retention = config["dataRetention"] if "dataRetention" in config else None
            self.client_type = config["clientType"] if "clientType" in config else None
            self.logo_url = config["logoUrl"] if "logoUrl" in config else None
            self.privacy_policy_url = config["privacyPolicyUrl"] if "privacyPolicyUrl" in config else None
            self.terms_of_service_url = config["termsOfServiceUrl"] if "termsOfServiceUrl" in config else None
            self.marketplace_url = config["marketplaceUrl"] if "marketplaceUrl" in config else None
            self.marketplace_data_stars = (
                config["marketplaceData"]["stars"]
                if "marketplaceData" in config and "stars" in config["marketplaceData"]
                else None
            )
            self.marketplace_data_downloads = (
                config["marketplaceData"]["downloads"]
                if "marketplaceData" in config and "downloads" in config["marketplaceData"]
                else None
            )
            self.marketplace_data_reviews = (
                config["marketplaceData"]["reviews"]
                if "marketplaceData" in config and "reviews" in config["marketplaceData"]
                else None
            )
            self.platform_verified = config["platformVerified"] if "platformVerified" in config else None
            self.canonic_verified = config["canonicVerified"] if "canonicVerified" in config else None
            self.developer_email = config["developerEmail"] if "developerEmail" in config else None
            self.consent_screenshot = config["consentScreenshot"] if "consentScreenshot" in config else None
            self.ip_addresses = ZscalerCollection.form_list(config["ipAddresses"] if "ipAddresses" in config else [], dict)
            self.extracted_urls = ZscalerCollection.form_list(
                config["extractedUrls"] if "extractedUrls" in config else [], str
            )
            self.extracted_api_calls = ZscalerCollection.form_list(
                config["extractedApiCalls"] if "extractedApiCalls" in config else [], str
            )
            self.vulnerabilities = ZscalerCollection.form_list(
                config["vulnerabilities"] if "vulnerabilities" in config else [], dict
            )
            self.api_activities = ZscalerCollection.form_list(
                config["apiActivities"] if "apiActivities" in config else [], dict
            )
            self.risks = ZscalerCollection.form_list(config["risks"] if "risks" in config else [], dict)
            self.insights = ZscalerCollection.form_list(config["insights"] if "insights" in config else [], dict)
            self.instances = ZscalerCollection.form_list(config["instances"] if "instances" in config else [], dict)
        else:
            self.name = None
            self.publisher_name = None
            self.publisher_description = None
            self.publisher_site_url = None
            self.publisher_logo_url = None
            self.platform = None
            self.description = None
            self.redirect_urls = []
            self.website_urls = []
            self.categories = []
            self.tags = []
            self.permission_level = None
            self.risk_score = None
            self.risk = None
            self.external_ids = []
            self.client_id = None
            self.permissions = []
            self.compliance = []
            self.data_retention = None
            self.client_type = None
            self.logo_url = None
            self.privacy_policy_url = None
            self.terms_of_service_url = None
            self.marketplace_url = None
            self.marketplace_data_stars = None
            self.marketplace_data_downloads = None
            self.marketplace_data_reviews = None
            self.platform_verified = None
            self.canonic_verified = None
            self.developer_email = None
            self.consent_screenshot = None
            self.ip_addresses = []
            self.extracted_urls = []
            self.extracted_api_calls = []
            self.vulnerabilities = []
            self.api_activities = []
            self.risks = []
            self.insights = []
            self.instances = []

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "publisher": {
                "name": self.publisher_name,
                "description": self.publisher_description,
                "siteUrl": self.publisher_site_url,
                "logoUrl": self.publisher_logo_url,
            },
            "platform": self.platform,
            "description": self.description,
            "redirectUrls": self.redirect_urls,
            "websiteUrls": self.website_urls,
            "categories": self.categories,
            "tags": self.tags,
            "permissionLevel": self.permission_level,
            "riskScore": self.risk_score,
            "risk": self.risk,
            "externalIds": self.external_ids,
            "clientId": self.client_id,
            "permissions": self.permissions,
            "compliance": self.compliance,
            "dataRetention": self.data_retention,
            "clientType": self.client_type,
            "logoUrl": self.logo_url,
            "privacyPolicyUrl": self.privacy_policy_url,
            "termsOfServiceUrl": self.terms_of_service_url,
            "marketplaceUrl": self.marketplace_url,
            "marketplaceData": {
                "stars": self.marketplace_data_stars,
                "downloads": self.marketplace_data_downloads,
                "reviews": self.marketplace_data_reviews,
            },
            "platformVerified": self.platform_verified,
            "canonicVerified": self.canonic_verified,
            "developerEmail": self.developer_email,
            "consentScreenshot": self.consent_screenshot,
            "ipAddresses": self.ip_addresses,
            "extractedUrls": self.extracted_urls,
            "extractedApiCalls": self.extracted_api_calls,
            "vulnerabilities": self.vulnerabilities,
            "apiActivities": self.api_activities,
            "risks": self.risks,
            "insights": self.insights,
            "instances": self.instances,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppTotalSearch(ZscalerObject):
    """
    A class for App Total Search 3rd-Party App Governance API objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.count = config["count"] if "count" in config else None
            self.current_page = config["currentPage"] if "currentPage" in config else None

            self.data = []
            if "data" in config and isinstance(config["data"], list):
                for item in config["data"]:
                    self.data.append(
                        {
                            "result": {
                                "appId": item["result"]["appId"] if "result" in item and "appId" in item["result"] else None,
                                "name": item["result"]["name"] if "result" in item and "name" in item["result"] else None,
                                "provider": (
                                    item["result"]["provider"] if "result" in item and "provider" in item["result"] else None
                                ),
                                "publisher": (
                                    item["result"]["publisher"] if "result" in item and "publisher" in item["result"] else None
                                ),
                            }
                        }
                    )
        else:
            self.count = None
            self.current_page = None
            self.data = []

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {"count": self.count, "currentPage": self.current_page, "data": self.data}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AppViewAppsResponse(ZscalerObject):
    """
    A class representing a High Risk App object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.created_at = config["createdAt"] if "createdAt" in config else None

            # Handling the spec dictionary
            self.spec_map = config["spec"]["map"] if "spec" in config and "map" in config["spec"] else None
        else:
            self.id = None
            self.name = None
            self.created_by = None
            self.created_at = None
            self.spec_map = None

    def request_format(self):
        return {
            "id": self.id,
            "name": self.name,
            "createdBy": self.created_by,
            "createdAt": self.created_at,
            "spec": {"map": self.spec_map} if self.spec_map else None,
        }
