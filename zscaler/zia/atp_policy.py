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
from zscaler.zia.models.advanced_threat_settings import AdvancedThreatProtectionSettings
from zscaler.utils import format_url


class ATPPolicyAPI(APIClient):
    """
    A Client object for the Advanced Threat Protection Policy resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_atp_settings(self) -> tuple:
        """
        Retrieves the current advanced settings configured in the ZIA Admin Portal.

        This method makes a GET request to the ZIA Admin API and returns detailed advanced settings,
        including various bypass rules, DNS optimization configurations, and traffic control settings.

        Returns:
            tuple: A tuple containing:
                - AdvancedSettings: The current advanced settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current advanced settings:

            >>> settings, response, err = client.zia.advanced_settings.get_advanced_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/advancedThreatSettings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = AdvancedThreatProtectionSettings(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_atp_settings(self, **kwargs) -> tuple:
        """
        Updates advanced threat protection settings in the ZIA Admin Portal.

        This method pushes updated advanced threat protection policy settings.

        Args:
            settings (:obj:`AdvancedThreatProtectionSettings`):
                An instance of `AdvancedThreatProtectionSettings` containing the updated configuration.

                Supported attributes:
                    - risk_tolerance (int): Defines the maximum risk score allowed.
                    - risk_tolerance_capture (bool): Captures traffic exceeding risk tolerance.
                    - cmd_ctl_server_blocked (bool): Blocks command & control servers.
                    - cmd_ctl_server_capture (bool): Captures traffic to command & control servers.
                    - cmd_ctl_traffic_blocked (bool): Blocks command & control traffic.
                    - cmd_ctl_traffic_capture (bool): Captures command & control traffic.
                    - malware_sites_blocked (bool): Blocks malware sites.
                    - malware_sites_capture (bool): Captures malware site traffic.
                    - active_x_blocked (bool): Blocks ActiveX controls.
                    - active_x_capture (bool): Captures ActiveX control usage.
                    - browser_exploits_blocked (bool): Blocks browser exploits.
                    - browser_exploits_capture (bool): Captures browser exploit attempts.
                    - file_format_vulnerabilities_blocked (bool): Blocks file format vulnerabilities.
                    - file_format_vulnerabilities_capture (bool): Captures file format vulnerability attempts.
                    - known_phishing_sites_blocked (bool): Blocks known phishing sites.
                    - known_phishing_sites_capture (bool): Captures known phishing site traffic.
                    - suspected_phishing_sites_blocked (bool): Blocks suspected phishing sites.
                    - suspected_phishing_sites_capture (bool): Captures suspected phishing site traffic.
                    - blocked_countries (list[str]): Countries blocked for traffic.
                    - block_countries_capture (bool): Captures traffic from blocked countries.
                    - bit_torrent_blocked (bool): Blocks BitTorrent traffic.
                    - bit_torrent_capture (bool): Captures BitTorrent traffic.
                    - tor_blocked (bool): Blocks Tor network access.
                    - tor_capture (bool): Captures Tor network traffic.
                    - google_talk_blocked (bool): Blocks Google Talk usage.
                    - google_talk_capture (bool): Captures Google Talk usage traffic.
                    - ssh_tunnelling_blocked (bool): Blocks SSH tunneling.
                    - ssh_tunnelling_capture (bool): Captures SSH tunneling traffic.
                    - crypto_mining_blocked (bool): Blocks cryptocurrency mining.
                    - crypto_mining_capture (bool): Captures cryptocurrency mining attempts.
                    - ad_spyware_sites_blocked (bool): Blocks adware and spyware sites.
                    - ad_spyware_sites_capture (bool): Captures traffic to adware and spyware sites.
                    - alert_for_unknown_or_suspicious_c2_traffic (bool): Alerts for suspicious command & control traffic.
                    - dga_domains_blocked (bool): Blocks domains generated by DGA (Domain Generation Algorithms).
                    - dga_domains_capture (bool): Captures traffic to DGA domains.
                    - malicious_urls_capture (bool): Captures traffic to malicious URLs.

        Returns:
            tuple: A tuple containing:
                - AdvancedThreatProtectionSettings: The updated advanced threat protection policy settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, `None`.

        Examples:
            Update advanced threat protection settings by blocking specific threats:

            >>> settings, response, err = client.zia.atp_policy.get_atp_settings()
            >>> if not err:
            ...     settings.cmd_ctl_server_blocked = True
            ...     settings.malware_sites_blocked = True
            ...     updated_settings, response, err = client.zia.atp_policy.update_atp_settings(settings)
            ...     if not err:
            ...         print(f"Updated Malware Sites Blocked: {updated_settings.malware_sites_blocked}")
            ...     else:
            ...         print(f"Failed to update settings: {err}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/advancedThreatSettings
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AdvancedThreatProtectionSettings)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = AdvancedThreatProtectionSettings(self.form_response_body(response.get_body()))
            else:
                result = AdvancedThreatProtectionSettings()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_atp_security_exceptions(self) -> tuple:
        """
        Retrieves a list of URLs bypassed in ATP security exceptions.

        Returns:
            tuple: A tuple containing:
                - list[str]: List of bypassed URLs.
                - Response: The raw HTTP response from the API.
                - error: Error details if the request fails.

        Examples:
            >>> bypass_urls, response, err = client.zia.atp_policy.get_atp_security_exceptions()
            >>> if not err:
            ...     print("Bypassed URLs:", bypass_urls)
        """

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/securityExceptions
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            bypass_urls = response.get_body().get("bypassUrls", [])
            if not isinstance(bypass_urls, list):
                raise ValueError("Unexpected response format: bypassUrls should be a list.")
            return (bypass_urls, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_atp_security_exceptions(self, bypass_urls: list[str]) -> tuple:
        """
        Updates the list of bypassed URLs in ATP security exceptions.

        Args:
            bypass_urls (list[str]): The list of URLs to bypass ATP security checks.

        Returns:
            tuple: A tuple containing:
                - list[str]: Updated list of bypassed URLs.
                - Response: The raw HTTP response from the API.
                - error: Error details if the request fails.

        Examples:
            >>> bypass_urls = ["example.com", "test.com"]
            >>> updated_urls, response, err = client.zia.atp_policy.update_atp_security_exceptions(bypass_urls)
            >>> if not err:
            ...     print("Updated URLs:", updated_urls)
        """

        if not isinstance(bypass_urls, list):
            raise TypeError("bypass_urls must be a list of strings.")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/securityExceptions
            """
        )

        payload = {"bypassUrls": bypass_urls}

        request, error = self._request_executor.create_request(http_method, api_url, payload)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            updated_bypass_urls = response.get_body().get("bypassUrls", [])
            if not isinstance(updated_bypass_urls, list):
                raise ValueError("Unexpected response format: bypassUrls should be a list.")
            return (updated_bypass_urls, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_atp_malicious_urls(self) -> tuple:
        """
        Retrieves the malicious URLs added to the denylist in the Advanced Threat Protection (ATP) policy

        Returns:
            tuple: A tuple containing:
                - list[str]: List of malicious URLs.
                - Response: The raw HTTP response from the API.
                - error: Error details if the request fails.

        Examples:
            >>> malicious_urls, response, err = client.zia.atp_policy.get_atp_malicious_urls()
            >>> if not err:
            ...     print("Malicious URLs:", malicious_urls)
        """

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/maliciousUrls
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            malicious_urls = response.get_body().get("maliciousUrls", [])
            if not isinstance(malicious_urls, list):
                raise ValueError("Unexpected response format: maliciousUrls should be a list.")
            return (malicious_urls, response, None)
        except Exception as ex:
            return (None, response, ex)

    def add_atp_malicious_urls(self, malicious_urls: list) -> tuple:
        """
        Adds the provided malicious URLs to the deny list.

        Args:
            malicious_urls (list of str): A list of malicious URLs to be added to the deny list.

        Returns:
            tuple: A tuple containing (updated list of malicious URLs, Response, error)

        Raises:
            ValueError: If the malicious_urls list is empty.

        Examples:
            Add a single URL:
                >>> updated_malicious_urls, response, error = zia.atp_policy.add_atp_malicious_urls(["malicious-site.com"])

            Add multiple URLs:
                >>> malicious_urls = ["malicious-site1.com", "malicious-site2.com"]
                >>> updated_malicious_urls, response, error = zia.atp_policy.add_atp_malicious_urls(malicious_urls)
        """
        if not malicious_urls:
            return (None, None, ValueError("The URL list cannot be empty."))

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/maliciousUrls?action=ADD_TO_LIST
            """
        )

        payload = {"maliciousUrls": malicious_urls}

        # Prepare request body and headers
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, payload, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        return self.get_atp_malicious_urls()

    def delete_atp_malicious_urls(self, malicious_urls: list) -> tuple:
        """
        Removes the specified malicious URLs from the deny list.

        Note:
            The malicious_urls list must include at least one URL already present in the deny list.
            The API does not allow an empty list.

        Args:
            malicious_urls (list of str): A list of malicious URLs to be removed from the deny list.

        Returns:
            tuple: A tuple containing (updated list of malicious URLs, Response, error)

        Raises:
            ValueError: If the malicious_urls list is empty.

        Examples:
            Remove a single URL:
                >>> updated_malicious_urls, response, error = zia.atp_policy.delete_atp_malicious_urls(["malicious-site.com"])

            Remove multiple URLs:
                >>> malicious_urls = ["malicious-site1.com", "malicious-site2.com"]
                >>> updated_malicious_urls, response, error = zia.atp_policy.delete_atp_malicious_urls(malicious_urls)
        """
        if not malicious_urls:
            return (None, None, ValueError("The URL list cannot be empty."))

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /cyberThreatProtection/maliciousUrls?action=REMOVE_FROM_LIST
            """
        )

        payload = {"maliciousUrls": malicious_urls}

        # Prepare request body and headers
        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, payload, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        return self.get_atp_malicious_urls()
