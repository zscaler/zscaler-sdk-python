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


class OrganizationInformation(ZscalerObject):
    """
    A class for Organizationinformation objects.
    """

    def __init__(self, config=None):
        """
        Initialize the OrganizationInformation model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.org_id = config["orgId"] if "orgId" in config else None
            self.name = config["name"] if "name" in config else None
            self.hq_location = config["hqLocation"] if "hqLocation" in config else None
            self.domains = ZscalerCollection.form_list(config["domains"] if "domains" in config else [], str)
            self.geo_location = config["geoLocation"] if "geoLocation" in config else None
            self.industry_vertical = config["industryVertical"] if "industryVertical" in config else None
            self.addr_line1 = config["addrLine1"] if "addrLine1" in config else None
            self.addr_line2 = config["addrLine2"] if "addrLine2" in config else None
            self.city = config["city"] if "city" in config else None
            self.state = config["state"] if "state" in config else None
            self.zipcode = config["zipcode"] if "zipcode" in config else None
            self.country = config["country"] if "country" in config else None
            self.employee_count = config["employeeCount"] if "employeeCount" in config else None
            self.language = config["language"] if "language" in config else None
            self.timezone = config["timezone"] if "timezone" in config else None
            self.alert_timer = config["alertTimer"] if "alertTimer" in config else None
            self.pdomain = config["pdomain"] if "pdomain" in config else None
            self.internal_company = config["internalCompany"] if "internalCompany" in config else None
            self.primary_technical_contactcontact_type = (
                config["primaryTechnicalContactcontactType"] if "primaryTechnicalContactcontactType" in config else None
            )
            self.primary_technical_contact_name = (
                config["primaryTechnicalContactName"] if "primaryTechnicalContactName" in config else None
            )
            self.primary_technical_contact_title = (
                config["primaryTechnicalContactTitle"] if "primaryTechnicalContactTitle" in config else None
            )
            self.primary_technical_contact_email = (
                config["primaryTechnicalContactEmail"] if "primaryTechnicalContactEmail" in config else None
            )
            self.primary_technical_contact_phone = (
                config["primaryTechnicalContactPhone"] if "primaryTechnicalContactPhone" in config else None
            )
            self.primary_technical_contact_alt_phone = (
                config["primaryTechnicalContactAltPhone"] if "primaryTechnicalContactAltPhone" in config else None
            )
            self.primary_technical_contact_insights_href = (
                config["primaryTechnicalContactInsightsHref"] if "primaryTechnicalContactInsightsHref" in config else None
            )
            self.secondary_technical_contactcontact_type = (
                config["secondaryTechnicalContactcontactType"] if "secondaryTechnicalContactcontactType" in config else None
            )
            self.secondary_technical_contact_name = (
                config["secondaryTechnicalContactName"] if "secondaryTechnicalContactName" in config else None
            )
            self.secondary_technical_contact_title = (
                config["secondaryTechnicalContactTitle"] if "secondaryTechnicalContactTitle" in config else None
            )
            self.secondary_technical_contact_email = (
                config["secondaryTechnicalContactEmail"] if "secondaryTechnicalContactEmail" in config else None
            )
            self.secondary_technical_contact_phone = (
                config["secondaryTechnicalContactPhone"] if "secondaryTechnicalContactPhone" in config else None
            )
            self.secondary_technical_contact_alt_phone = (
                config["secondaryTechnicalContactAltPhone"] if "secondaryTechnicalContactAltPhone" in config else None
            )
            self.secondary_technical_contact_insights_href = (
                config["secondaryTechnicalContactInsightsHref"] if "secondaryTechnicalContactInsightsHref" in config else None
            )
            self.primary_billing_contactcontact_type = (
                config["primaryBillingContactcontactType"] if "primaryBillingContactcontactType" in config else None
            )
            self.primary_billing_contact_name = (
                config["primaryBillingContactName"] if "primaryBillingContactName" in config else None
            )
            self.primary_billing_contact_title = (
                config["primaryBillingContactTitle"] if "primaryBillingContactTitle" in config else None
            )
            self.primary_billing_contact_email = (
                config["primaryBillingContactEmail"] if "primaryBillingContactEmail" in config else None
            )
            self.primary_billing_contact_phone = (
                config["primaryBillingContactPhone"] if "primaryBillingContactPhone" in config else None
            )
            self.primary_billing_contact_alt_phone = (
                config["primaryBillingContactAltPhone"] if "primaryBillingContactAltPhone" in config else None
            )
            self.primary_billing_contact_insights_href = (
                config["primaryBillingContactInsightsHref"] if "primaryBillingContactInsightsHref" in config else None
            )
            self.secondary_billing_contactcontact_type = (
                config["secondaryBillingContactcontactType"] if "secondaryBillingContactcontactType" in config else None
            )
            self.secondary_billing_contact_name = (
                config["secondaryBillingContactName"] if "secondaryBillingContactName" in config else None
            )
            self.secondary_billing_contact_title = (
                config["secondaryBillingContactTitle"] if "secondaryBillingContactTitle" in config else None
            )
            self.secondary_billing_contact_email = (
                config["secondaryBillingContactEmail"] if "secondaryBillingContactEmail" in config else None
            )
            self.secondary_billing_contact_phone = (
                config["secondaryBillingContactPhone"] if "secondaryBillingContactPhone" in config else None
            )
            self.secondary_billing_contact_alt_phone = (
                config["secondaryBillingContactAltPhone"] if "secondaryBillingContactAltPhone" in config else None
            )
            self.secondary_billing_contact_insights_href = (
                config["secondaryBillingContactInsightsHref"] if "secondaryBillingContactInsightsHref" in config else None
            )
            self.primary_business_contactcontact_type = (
                config["primaryBusinessContactcontactType"] if "primaryBusinessContactcontactType" in config else None
            )
            self.primary_business_contact_name = (
                config["primaryBusinessContactName"] if "primaryBusinessContactName" in config else None
            )
            self.primary_business_contact_title = (
                config["primaryBusinessContactTitle"] if "primaryBusinessContactTitle" in config else None
            )
            self.primary_business_contact_email = (
                config["primaryBusinessContactEmail"] if "primaryBusinessContactEmail" in config else None
            )
            self.primary_business_contact_phone = (
                config["primaryBusinessContactPhone"] if "primaryBusinessContactPhone" in config else None
            )
            self.primary_business_contact_alt_phone = (
                config["primaryBusinessContactAltPhone"] if "primaryBusinessContactAltPhone" in config else None
            )
            self.primary_business_contact_insights_href = (
                config["primaryBusinessContactInsightsHref"] if "primaryBusinessContactInsightsHref" in config else None
            )
            self.secondary_business_contactcontact_type = (
                config["secondaryBusinessContactcontactType"] if "secondaryBusinessContactcontactType" in config else None
            )
            self.secondary_business_contact_name = (
                config["secondaryBusinessContactName"] if "secondaryBusinessContactName" in config else None
            )
            self.secondary_business_contact_title = (
                config["secondaryBusinessContactTitle"] if "secondaryBusinessContactTitle" in config else None
            )
            self.secondary_business_contact_email = (
                config["secondaryBusinessContactEmail"] if "secondaryBusinessContactEmail" in config else None
            )
            self.secondary_business_contact_phone = (
                config["secondaryBusinessContactPhone"] if "secondaryBusinessContactPhone" in config else None
            )
            self.secondary_business_contact_alt_phone = (
                config["secondaryBusinessContactAltPhone"] if "secondaryBusinessContactAltPhone" in config else None
            )
            self.secondary_business_contact_insights_href = (
                config["secondaryBusinessContactInsightsHref"] if "secondaryBusinessContactInsightsHref" in config else None
            )
            self.exec_insights_href = config["execInsightsHref"] if "execInsightsHref" in config else None
            self.legacy_insights_report_was_enabled = (
                config["legacyInsightsReportWasEnabled"] if "legacyInsightsReportWasEnabled" in config else None
            )
            self.logo_base64_data = config["logoBase64Data"] if "logoBase64Data" in config else None
            self.logo_mime_type = config["logoMimeType"] if "logoMimeType" in config else None
            self.cloud_name = config["cloudName"] if "cloudName" in config else None
            self.external_email_portal = config["externalEmailPortal"] if "externalEmailPortal" in config else None
            self.zpa_tenant_id = config["zpaTenantId"] if "zpaTenantId" in config else None
            self.zpa_tenant_cloud = config["zpaTenantCloud"] if "zpaTenantCloud" in config else None
            self.customer_contact_inherit = config["customerContactInherit"] if "customerContactInherit" in config else None
        else:
            self.org_id = None
            self.name = None
            self.hq_location = None
            self.domains = []
            self.geo_location = None
            self.industry_vertical = None
            self.addr_line1 = None
            self.addr_line2 = None
            self.city = None
            self.state = None
            self.zipcode = None
            self.country = None
            self.employee_count = None
            self.language = None
            self.timezone = None
            self.alert_timer = None
            self.pdomain = None
            self.internal_company = None
            self.primary_technical_contactcontact_type = None
            self.primary_technical_contact_name = None
            self.primary_technical_contact_title = None
            self.primary_technical_contact_email = None
            self.primary_technical_contact_phone = None
            self.primary_technical_contact_alt_phone = None
            self.primary_technical_contact_insights_href = None
            self.secondary_technical_contactcontact_type = None
            self.secondary_technical_contact_name = None
            self.secondary_technical_contact_title = None
            self.secondary_technical_contact_email = None
            self.secondary_technical_contact_phone = None
            self.secondary_technical_contact_alt_phone = None
            self.secondary_technical_contact_insights_href = None
            self.primary_billing_contactcontact_type = None
            self.primary_billing_contact_name = None
            self.primary_billing_contact_title = None
            self.primary_billing_contact_email = None
            self.primary_billing_contact_phone = None
            self.primary_billing_contact_alt_phone = None
            self.primary_billing_contact_insights_href = None
            self.secondary_billing_contactcontact_type = None
            self.secondary_billing_contact_name = None
            self.secondary_billing_contact_title = None
            self.secondary_billing_contact_email = None
            self.secondary_billing_contact_phone = None
            self.secondary_billing_contact_alt_phone = None
            self.secondary_billing_contact_insights_href = None
            self.primary_business_contactcontact_type = None
            self.primary_business_contact_name = None
            self.primary_business_contact_title = None
            self.primary_business_contact_email = None
            self.primary_business_contact_phone = None
            self.primary_business_contact_alt_phone = None
            self.primary_business_contact_insights_href = None
            self.secondary_business_contactcontact_type = None
            self.secondary_business_contact_name = None
            self.secondary_business_contact_title = None
            self.secondary_business_contact_email = None
            self.secondary_business_contact_phone = None
            self.secondary_business_contact_alt_phone = None
            self.secondary_business_contact_insights_href = None
            self.exec_insights_href = None
            self.legacy_insights_report_was_enabled = None
            self.logo_base64_data = None
            self.logo_mime_type = None
            self.cloud_name = None
            self.external_email_portal = None
            self.zpa_tenant_id = None
            self.zpa_tenant_cloud = None
            self.customer_contact_inherit = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "orgId": self.org_id,
            "name": self.name,
            "hqLocation": self.hq_location,
            "domains": self.domains,
            "geoLocation": self.geo_location,
            "industryVertical": self.industry_vertical,
            "addrLine1": self.addr_line1,
            "addrLine2": self.addr_line2,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "country": self.country,
            "employeeCount": self.employee_count,
            "language": self.language,
            "timezone": self.timezone,
            "alertTimer": self.alert_timer,
            "pdomain": self.pdomain,
            "internalCompany": self.internal_company,
            "primaryTechnicalContactcontactType": self.primary_technical_contactcontact_type,
            "primaryTechnicalContactName": self.primary_technical_contact_name,
            "primaryTechnicalContactTitle": self.primary_technical_contact_title,
            "primaryTechnicalContactEmail": self.primary_technical_contact_email,
            "primaryTechnicalContactPhone": self.primary_technical_contact_phone,
            "primaryTechnicalContactAltPhone": self.primary_technical_contact_alt_phone,
            "primaryTechnicalContactInsightsHref": self.primary_technical_contact_insights_href,
            "secondaryTechnicalContactcontactType": self.secondary_technical_contactcontact_type,
            "secondaryTechnicalContactName": self.secondary_technical_contact_name,
            "secondaryTechnicalContactTitle": self.secondary_technical_contact_title,
            "secondaryTechnicalContactEmail": self.secondary_technical_contact_email,
            "secondaryTechnicalContactPhone": self.secondary_technical_contact_phone,
            "secondaryTechnicalContactAltPhone": self.secondary_technical_contact_alt_phone,
            "secondaryTechnicalContactInsightsHref": self.secondary_technical_contact_insights_href,
            "primaryBillingContactcontactType": self.primary_billing_contactcontact_type,
            "primaryBillingContactName": self.primary_billing_contact_name,
            "primaryBillingContactTitle": self.primary_billing_contact_title,
            "primaryBillingContactEmail": self.primary_billing_contact_email,
            "primaryBillingContactPhone": self.primary_billing_contact_phone,
            "primaryBillingContactAltPhone": self.primary_billing_contact_alt_phone,
            "primaryBillingContactInsightsHref": self.primary_billing_contact_insights_href,
            "secondaryBillingContactcontactType": self.secondary_billing_contactcontact_type,
            "secondaryBillingContactName": self.secondary_billing_contact_name,
            "secondaryBillingContactTitle": self.secondary_billing_contact_title,
            "secondaryBillingContactEmail": self.secondary_billing_contact_email,
            "secondaryBillingContactPhone": self.secondary_billing_contact_phone,
            "secondaryBillingContactAltPhone": self.secondary_billing_contact_alt_phone,
            "secondaryBillingContactInsightsHref": self.secondary_billing_contact_insights_href,
            "primaryBusinessContactcontactType": self.primary_business_contactcontact_type,
            "primaryBusinessContactName": self.primary_business_contact_name,
            "primaryBusinessContactTitle": self.primary_business_contact_title,
            "primaryBusinessContactEmail": self.primary_business_contact_email,
            "primaryBusinessContactPhone": self.primary_business_contact_phone,
            "primaryBusinessContactAltPhone": self.primary_business_contact_alt_phone,
            "primaryBusinessContactInsightsHref": self.primary_business_contact_insights_href,
            "secondaryBusinessContactcontactType": self.secondary_business_contactcontact_type,
            "secondaryBusinessContactName": self.secondary_business_contact_name,
            "secondaryBusinessContactTitle": self.secondary_business_contact_title,
            "secondaryBusinessContactEmail": self.secondary_business_contact_email,
            "secondaryBusinessContactPhone": self.secondary_business_contact_phone,
            "secondaryBusinessContactAltPhone": self.secondary_business_contact_alt_phone,
            "secondaryBusinessContactInsightsHref": self.secondary_business_contact_insights_href,
            "execInsightsHref": self.exec_insights_href,
            "legacyInsightsReportWasEnabled": self.legacy_insights_report_was_enabled,
            "logoBase64Data": self.logo_base64_data,
            "logoMimeType": self.logo_mime_type,
            "cloudName": self.cloud_name,
            "externalEmailPortal": self.external_email_portal,
            "zpaTenantId": self.zpa_tenant_id,
            "zpaTenantCloud": self.zpa_tenant_cloud,
            "customerContactInherit": self.customer_contact_inherit,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class OrganizationSubscription(ZscalerObject):
    """
    A class for OrganizationSubscription objects.
    """

    def __init__(self, config=None):
        """
        Initialize the OrganizationSubscription model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.status = config["status"] if "status" in config else None
            self.state = config["state"] if "state" in config else None
            self.licenses = config["licenses"] if "licenses" in config else None
            self.start_date = config["startDate"] if "startDate" in config else None
            self.str_start_date = config["strStartDate"] if "strStartDate" in config else None
            self.str_end_date = config["strEndDate"] if "strEndDate" in config else None
            self.end_date = config["endDate"] if "endDate" in config else None
            self.sku = config["sku"] if "sku" in config else None
            self.cell_count = config["cellCount"] if "cellCount" in config else None
            self.updated_at_timestamp = config["updatedAtTimestamp"] if "updatedAtTimestamp" in config else None
            self.subscribed = config["subscribed"] if "subscribed" in config else None
        else:
            self.id = None
            self.status = None
            self.state = None
            self.licenses = None
            self.start_date = None
            self.str_start_date = None
            self.str_end_date = None
            self.end_date = None
            self.sku = None
            self.cell_count = None
            self.updated_at_timestamp = None
            self.subscribed = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "status": self.status,
            "state": self.state,
            "licenses": self.licenses,
            "startDate": self.start_date,
            "strStartDate": self.str_start_date,
            "strEndDate": self.str_end_date,
            "endDate": self.end_date,
            "sku": self.sku,
            "cellCount": self.cell_count,
            "updatedAtTimestamp": self.updated_at_timestamp,
            "subscribed": self.subscribed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class OrganizationInformationLite(ZscalerObject):
    """
    A class for OrganizationInformationLite objects.
    """

    def __init__(self, config=None):
        """
        Initialize the OrganizationInformationLite model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.org_id = config["orgId"] if "orgId" in config else None
            self.name = config["name"] if "name" in config else None
            self.cloud_name = config["cloudName"] if "cloudName" in config else None
            self.domains = ZscalerCollection.form_list(config["domains"] if "domains" in config else [], str)
            self.language = config["language"] if "language" in config else None
            self.timezone = config["timezone"] if "timezone" in config else None
            self.org_disabled = config["orgDisabled"] if "orgDisabled" in config else None
        else:
            self.org_id = None
            self.name = None
            self.cloud_name = None
            self.domains = []
            self.language = None
            self.timezone = None
            self.org_disabled = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "orgId": self.org_id,
            "name": self.name,
            "cloudName": self.cloud_name,
            "domains": self.domains,
            "language": self.language,
            "timezone": self.timezone,
            "orgDisabled": self.org_disabled,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
