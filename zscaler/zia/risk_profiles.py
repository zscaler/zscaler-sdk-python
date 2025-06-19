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
from zscaler.zia.models.risk_profiles import RiskProfiles
from zscaler.utils import format_url


class RiskProfilesAPI(APIClient):
    """
    A Client object for the Risk Profiles resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_risk_profiles(self, query_params=None) -> tuple:
        """
        Retrieves the cloud application risk profile

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of risk profile  instances, Response, error)

        Examples:
            List risk profile :

            >>> profile_list, _, error = client.zia.risk_profiles.list_risk_profiles(
                query_params={'search': 'Profile01'})
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
            /riskProfiles
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(RiskProfiles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_risk_profiles_lite(self) -> tuple:
        """
        Retrieves the cloud application risk profile lite

        Args:
            N/A

        Returns:
            tuple: A tuple containing (risk profile lite instance, Response, error).

        Examples:
            List risk profile :

            >>> profile_list, _, error = client.zia.risk_profiles.list_risk_profiles()
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
            /riskProfiles/lite
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RiskProfiles)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(RiskProfiles(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_risk_profile(self, profile_id: int) -> tuple:
        """
        Fetches a specific risk profile by ID.

        Args:
            profile_id (int): The unique identifier for the risk profile.

        Returns:
            tuple: A tuple containing (Risk Profile instance, Response, error).

        Examples:
            Print a specific Risk Profile

            >>> fetched_profile, _, error = client.zia.risk_profiles.get_risk_profile(
                '1254654')
            >>> if error:
            ...     print(f"Error fetching Risk Profile by ID: {error}")
            ...     return
            ... print(f"Fetched Risk Profile by ID: {fetched_profile.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /riskProfiles/{profile_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RiskProfiles)
        if error:
            return (None, response, error)

        try:
            result = RiskProfiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_risk_profile(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Risk Profile.

        Keyword Args:
            profile_name (str): Cloud application risk profile name.
            profile_type (str): Risk profile type. Supported Value: CLOUD_APPLICATIONS.
            risk_index (list[int]): Risk index scores assigned to cloud applications.
            status (str): Application status. Values: UN_SANCTIONED, SANCTIONED, ANY.
            exclude_certificates (int): Whether to include (0) or exclude (1) certificates.
            certifications (list[str]): List of certifications for the profile.
                Supported Values: `CSA_STAR`, `ISO_27001`, `HIPAA`, `FISMA`, `FEDRAMP`,
                                    `SOC2`, `ISO_27018`, `PCI_DSS`, `ISO_27017`, `SOC1`,
                                    `SOC3`, `GDPR`, `CCPA`, `FERPA`, `COPPA`, `HITECH`,
                                    `EU_US_SWISS_PRIVACY_SHIELD`, `EU_US_PRIVACY_SHIELD_FRAMEWORK`,
                                    `CISP`, `AICPA`, `FIPS`, `SAFE_BIOPHARMA`, `ISAE_3000`,
                                    `SSAE_18`, `NIST`, `ISO_14001`, `SOC`, `TRUSTE`,
                                    `ISO_26262`, `ISO_20252`, `RGPD`, `ISO_20243`, `JIS_Q_27001`
                                    `ISO_10002`, `JIS_Q_15001_2017`, `ISMAP`, `GAAP`,
            poor_items_of_service (str): Filters apps based on questionable terms/conditions in legal agreements.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            admin_audit_logs (str): Support for admin activity audit logs.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            data_breach (str): History of reported data breaches.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            source_ip_restrictions (str): Ability to restrict access by source IPs.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            mfa_support (str): Support for multi-factor authentication (MFA).
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            ssl_pinned (str): Use of pinned SSL certificates for traffic validation.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            http_security_headers (str): Implementation of standard security headers.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            evasive (str): Support for anonymous or evasive access methods.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            dns_caa_policy (str): DNS Certification Authority Authorization (CAA) policy.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            weak_cipher_support (str): Support for weak ciphers with small key sizes.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            password_strength (str): Password strength rating under Hosting Info.
                Supported Values: `ANY`, `GOOD`, `POOR`, `UN_KNOWN`
            ssl_cert_validity (str): Validity period of SSL certificates.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            vulnerability (str): Support for mitigating known CVE vulnerabilities.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            malware_scanning_for_content (str): Content malware scanning capabilities.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            file_sharing (str): Support for file sharing features.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            ssl_cert_key_size (str): Key size of SSL certificates. Example: BITS_2048.
                Supported Values: `ANY`, `UN_KNOWN`, `BITS_2048`, `BITS_256`, `BITS_3072`, `BITS_384`,
                    `BITS_4096`, `BITS_1024`,`BITS_8192`
            vulnerable_to_heart_bleed (str): Vulnerability to Heartbleed attack.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            vulnerable_to_log_jam (str): Vulnerability to Logjam attack.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            vulnerable_to_poodle (str): Vulnerability to POODLE attack.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            vulnerability_disclosure (str): Policy for disclosing vulnerabilities.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            support_for_waf (str): Support for Web Application Firewalls (WAFs).
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            remote_screen_sharing (str): Remote screen sharing feature support.
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            sender_policy_framework (str): Support for Sender Policy Framework (SPF).
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            domain_keys_identified_mail (str): Support for DomainKeys Identified Mail (DKIM).
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            domain_based_message_auth (str): Support for Domain-Based Message Authentication (DMARC).
                Supported Values: `ANY`, `YES`, `NO`, `UN_KNOWN`
            data_encryption_in_transit (list[str]): Encryption methods for data in transit.
                Supported Values: `ANY`, `UN_KNOWN`, `TLSV1_0`, `TLSV1_1`, `TLSV1_2`, `TLSV1_3`,
                    `SSLV2`, `SSLV3`
            custom_tags (list[dict]): List of custom tags for inclusion or exclusion.

        Returns:
            tuple: A tuple containing the added Risk Profile object, response, and error.

        Examples:
            Add a new Risk Profile :

            >>> added_profile, _, error = client.zia.risk_profiles.add_risk_profile(
            ... profile_name=f"RiskProfile_{random.randint(1000, 10000)}",
            ... status="SANCTIONED",
            ... risk_index=[1, 2, 3, 4, 5],
            ... custom_tags=[],
            ... certifications=["AICPA", "CCPA", "CISP"],
            ... password_strength="GOOD",
            ... poor_items_of_service="YES",
            ... admin_audit_logs="YES",
            ... data_breach="YES",
            ... source_ip_restrictions="YES",
            ... file_sharing="YES",
            ... mfa_support="YES",
            ... ssl_pinned="YES",
            ... data_encryption_in_transit=[
            ...     "SSLV2", "SSLV3", "TLSV1_0", "TLSV1_1", "TLSV1_2", "TLSV1_3", "UN_KNOWN"
            ... ],
            ... http_security_headers="YES",
            ... evasive="YES",
            ... dns_caa_policy="YES",
            ... ssl_cert_validity="YES",
            ... weak_cipher_support="YES",
            ... vulnerability="YES",
            ... vulnerable_to_heart_bleed="YES",
            ... ssl_cert_key_size="BITS_2048",
            ... vulnerable_to_poodle="YES",
            ... support_for_waf="YES",
            ... vulnerability_disclosure="YES",
            ... domain_keys_identified_mail="YES",
            ... malware_scanning_for_content="YES",
            ... domain_based_message_auth="YES",
            ... sender_policy_framework="YES",
            ... remote_screen_sharing="YES",
            ... vulnerable_to_log_jam="YES",
            ... profile_type="CLOUD_APPLICATIONS",
            ... )
            >>> if error:
            ...     print(f"Error adding risk profile: {error}")
            ...     return
            ... print(f"Risk profile added successfully: {added_profile.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /riskProfiles
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RiskProfiles)
        if error:
            return (None, response, error)

        try:
            result = RiskProfiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_risk_profile(self, profile_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Risk Profile.

        Args:
            profile_id (int): The unique ID for the Risk Profile.

        Returns:
            tuple: A tuple containing the updated Risk Profile, response, and error.

        Examples:
            Add a new Risk Profile :

            >>> update_profile, _, error = client.zia.risk_profiles.add_risk_profile(
            ... profile_id='876868'
            ... profile_name=f"RiskProfile_{random.randint(1000, 10000)}",
            ... status="SANCTIONED",
            ... risk_index=[1, 2, 3, 4, 5],
            ... custom_tags=[],
            ... certifications=["AICPA", "CCPA", "CISP"],
            ... password_strength="GOOD",
            ... poor_items_of_service="YES",
            ... admin_audit_logs="YES",
            ... data_breach="YES",
            ... source_ip_restrictions="YES",
            ... file_sharing="YES",
            ... mfa_support="YES",
            ... ssl_pinned="YES",
            ... data_encryption_in_transit=[
            ...     "SSLV2", "SSLV3", "TLSV1_0", "TLSV1_1", "TLSV1_2", "TLSV1_3", "UN_KNOWN"
            ... ],
            ... http_security_headers="YES",
            ... evasive="YES",
            ... dns_caa_policy="YES",
            ... ssl_cert_validity="YES",
            ... weak_cipher_support="YES",
            ... vulnerability="YES",
            ... vulnerable_to_heart_bleed="YES",
            ... ssl_cert_key_size="BITS_2048",
            ... vulnerable_to_poodle="YES",
            ... support_for_waf="YES",
            ... vulnerability_disclosure="YES",
            ... domain_keys_identified_mail="YES",
            ... malware_scanning_for_content="YES",
            ... domain_based_message_auth="YES",
            ... sender_policy_framework="YES",
            ... remote_screen_sharing="YES",
            ... vulnerable_to_log_jam="YES",
            ... profile_type="CLOUD_APPLICATIONS",
            ... )
            >>> if error:
            ...     print(f"Error adding risk profile: {error}")
            ...     return
            ... print(f"Risk profile added successfully: {update_profile.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /riskProfiles/{profile_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, RiskProfiles)
        if error:
            return (None, response, error)

        try:
            result = RiskProfiles(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_risk_profile(self, profile_id: int) -> tuple:
        """
        Deletes the specified Risk Profile.

        Args:
            profile_id (str): The unique identifier of the Risk Profile.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            List risk profile :

            >>> _, _, error = client.zia.risk_profiles.delete_risk_profile('73459')
            >>> if error:
            ...     print(f"Error deleting risk profile: {error}")
            ...     return
            ... print(f"Risk profile with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /riskProfiles/{profile_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
