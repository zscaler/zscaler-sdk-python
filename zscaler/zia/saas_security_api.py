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

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.saas_security_api import DomainProfiles
from zscaler.zia.models.saas_security_api import QuarantineTombstoneTemplate
from zscaler.zia.models.saas_security_api import CasbEmailLabel
from zscaler.zia.models.saas_security_api import CasbTenant
from zscaler.utils import format_url


class SaaSSecurityAPI(APIClient):
    """
    A Client object for the SaaS Security API resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_domain_profiles_lite(self) -> tuple:
        """
        Retrieves the domain profile summary

            See the
            `Domain Profiles API reference:
            <https://help.zscaler.com/zia/saas-security-api#/domainProfiles/lite-get>`_
            for details

        Args:
            N/A

        Returns:
            tuple: A tuple containing (domain profiles lite instance, Response, error).

        Examples:
            List domain profiles :

            >>> profile_list, _, error = client.zia.saas_security_api.list_domain_profiles_lite()
            >>> if error:
            ...     print(f"Error listing profiles: {error}")
            ...     return
            ... print(f"Total profiles found: {len(profile_list)}")
            ... for profile in profile_list:
            ...     print(profile.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /domainProfiles/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, DomainProfiles)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(DomainProfiles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_quarantine_tombstone_lite(self) -> tuple:
        """
        Retrieves the templates for the tombstone file created when a file is quarantined

            See the
            `Quarantine Tombstone File Template API reference:
            <https://help.zscaler.com/zia/saas-security-api#/quarantineTombstoneTemplate/lite-get>`_
            for details

        Args:
            N/A

        Returns:
            tuple: A tuple containing (tombstone file lite instance, Response, error).

        Examples:
            List tombstone templates :

            >>> template_list, _, error = client.zia.saas_security_api.list_quarantine_tombstone_lite()
            >>> if error:
            ...     print(f"Error listing templates: {error}")
            ...     return
            ... print(f"Total profiles found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /quarantineTombstoneTemplate/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, QuarantineTombstoneTemplate)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(QuarantineTombstoneTemplate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_casb_email_label_lite(self) -> tuple:
        """
        Retrieves the email labels generated for the SaaS Security API policies in a user's email account

            See the
            `Email Labels API reference:
            <https://help.zscaler.com/zia/saas-security-api#/casbEmailLabel/lite-get>`_
            for details

        Args:
            N/A

        Returns:
            tuple: A tuple containing (email labels lite instance, Response, error).

        Examples:
            List email label :

            >>> label_list, _, error = client.zia.saas_security_api.list_casb_email_label_lite()
            >>> if error:
            ...     print(f"Error listing labels: {error}")
            ...     return
            ... print(f"Total labels found: {len(label_list)}")
            ... for label in label_list:
            ...     print(label.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbEmailLabel/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CasbEmailLabel)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CasbEmailLabel(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_casb_tenant_lite(self, query_params=None) -> tuple:
        """
        Retrieves the email labels generated for the SaaS Security API policies in a user's email account

            See the
            `SaaS Application Tenants API reference:
            <https://help.zscaler.com/zia/saas-security-api#/casbTenant/lite-get>`_
            for details

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.active_only]`` {bool}: Indicates that the tenant is in use.
                ``[query_params.include_deleted]`` {bool}: Indicates that the tenant is deleted
                ``[query_params.scan_config_tenants_only]`` {bool}: Specifies the tenant which the scan is already configured
                ``[query_params.include_bucket_ready_s3_tenants]`` {bool}: For the AWS S3 SaaS application

                ``[query_params.filter_by_feature]`` {list[str]}: Filters the SaaS application tenant by feature

                    See the
                    `SaaS Application Tenants API reference:
                    <https://help.zscaler.com/zia/saas-security-api#/casbTenant/lite-get>`_
                    for details

                ``[query_params.app]`` {bool}: Specifies the sanctioned SaaS application

                    See the
                    `SaaS Application Tenants API reference:
                    <https://help.zscaler.com/zia/saas-security-api#/casbTenant/lite-get>`_
                    for details

                ``[query_params.app_type]`` {str}: Specifies the SaaS application type

                Supported Values: `ANY`, `FILE`, `EMAIL`, `CRM`, `ITSM`,
                    `COLLAB`, `REPO`, `STORAGE`, `TP_APP`, `GENAI`, `MISC`

        Returns:
            tuple: A tuple containing (SaaS Application Tenants lite instance, Response, error).

        Examples:
            List SaaS Application Tenant :

            >>> tenant_list, _, error = client.zia.saas_security_api.list_casb_tenant_lite(
                query_params={'active_only': True}
            )
            >>> if error:
            ...     print(f"Error listing saas tenants: {error}")
            ...     return
            ... print(f"Total tenants found: {len(tenant_list)}")
            ... for tenant in tenant_list:
            ...     print(tenant.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /casbTenant/lite
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CasbTenant)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CasbTenant(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
