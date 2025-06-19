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

import datetime
import logging
import os
import re
from time import sleep

import requests
from zscaler import __version__
from zscaler.cache.cache import Cache
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import obfuscate_api_key
from zscaler.logger import setup_logging
from zscaler.errors.response_checker import check_response_for_error

setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class LegacyZIAClientHelper:
    """
    A Controller to access Endpoints in the Zscaler Internet Access (ZIA) API.

    The ZIA object stores the session token and simplifies access to CRUD options within the ZIA platform.

    Attributes:
        api_key (str): The ZIA API key generated from the ZIA console.
        username (str): The ZIA administrator username.
        password (str): The ZIA administrator password.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``zscaler``
            * ``zscloud``
            * ``zscalerbeta``
            * ``zspreview``
            * ``zscalerone``
            * ``zscalertwo``
            * ``zscalerthree``
            * ``zscalergov``
            * ``zscalerten``

        override_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Internet Access"
    _build = __version__
    _env_base = "ZIA"
    url = "https://zsapi.zscaler.net"
    env_cloud = "zscaler"

    def __init__(self, cloud, timeout=240, cache=None, fail_safe=False, request_executor_impl=None, **kw):
        from zscaler.request_executor import RequestExecutor

        self.api_key = kw.get("api_key", os.getenv(f"{self._env_base}_API_KEY"))
        self.username = kw.get("username", os.getenv(f"{self._env_base}_USERNAME"))
        self.password = kw.get("password", os.getenv(f"{self._env_base}_PASSWORD"))
        # The 'cloud' parameter should have precedence over environment variables
        self.env_cloud = cloud or kw.get("cloud") or os.getenv(f"{self._env_base}_CLOUD")
        if not self.env_cloud:
            raise ValueError(
                f"Cloud environment must be set via the 'cloud' argument or the {self._env_base}_CLOUD environment variable."
            )

        # URL construction
        if cloud == "zspreview":
            self.url = f"https://admin.{self.env_cloud}.net"
        else:
            # Use override URL if provided, else construct the URL
            self.url = (
                kw.get("override_url") or os.getenv(f"{self._env_base}_OVERRIDE_URL") or f"https://zsapi.{self.env_cloud}.net"
            )

        self.conv_box = True
        self.sandbox_token = kw.get("sandbox_token") or os.getenv(f"{self._env_base}_SANDBOX_TOKEN")
        self.timeout = timeout
        self.fail_safe = fail_safe
        cache_enabled = os.environ.get("ZSCALER_CLIENT_CACHE_ENABLED", "false").lower() == "true"
        self.cache = NoOpCache()
        if cache is None and cache_enabled:
            ttl = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTL", 3600))
            tti = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTI", 1800))
            self.cache = ZscalerCache(ttl=ttl, tti=tti)
        elif isinstance(cache, Cache):
            self.cache = cache

        # Initialize user-agent
        ua = UserAgent()
        self.user_agent = ua.get_user_agent_string()
        # Initialize rate limiter
        # You may want to adjust these parameters as per your rate limit configuration
        self.rate_limiter = RateLimiter(
            get_limit=2,  # Adjust as per actual limit
            post_put_delete_limit=2,  # Adjust as per actual limit
            get_freq=2,  # Adjust as per actual frequency (in seconds)
            post_put_delete_freq=2,  # Adjust as per actual frequency (in seconds)
        )
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        self.session_timeout_offset = datetime.timedelta(minutes=5)
        self.session_refreshed = None
        self.auth_details = None
        self.session_id = None
        self.authenticate()

        # Create request executor
        self.config = {
            "client": {
                "cloud": self.env_cloud,
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": 3},
                "cache": {"enabled": True},
            }
        }
        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, zia_legacy_client=self)

    def extractJSessionIDFromHeaders(self, header):
        session_id_str = header.get("Set-Cookie", "")

        if not session_id_str:
            raise ValueError("no Set-Cookie header received")

        regex = re.compile(r"JSESSIONID=(.*?);")
        result = regex.search(session_id_str)

        if not result:
            raise ValueError("couldn't find JSESSIONID in header value")

        return result.group(1)

    def is_session_expired(self) -> bool:
        """
        Checks whether the current session is expired.

        Returns:
            bool: True if the session is expired or if the session details are missing.
        """
        # no session yet → force login
        if self.auth_details is None or self.session_refreshed is None:
            return True

        # ZIA returns expiry as epoch-milliseconds in `passwordExpiryTime`
        expiry_ms = self.auth_details.get("passwordExpiryTime", 0)
        if expiry_ms <= 0:
            return False

        expiry_time = datetime.datetime.fromtimestamp(expiry_ms / 1000)
        safety_window = self.session_timeout_offset
        return datetime.datetime.utcnow() >= (expiry_time - safety_window)

    def authenticate(self):
        """
        Creates a ZIA authentication session and sets the JSESSIONID.
        """
        api_key_chars = list(self.api_key)
        api_obf = obfuscate_api_key(api_key_chars)

        payload = {
            "apiKey": api_obf["key"],
            "username": self.username,
            "password": self.password,
            "timestamp": api_obf["timestamp"],
        }

        url = f"{self.url}/api/v1/authenticatedSession"
        resp = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)

        parsed_response, err = check_response_for_error(url, resp, resp.text)
        if err:
            raise err

        self.session_id = self.extractJSessionIDFromHeaders(resp.headers)
        if not self.session_id:
            raise ValueError("Failed to extract JSESSIONID from authentication response")

        self.session_refreshed = datetime.datetime.now()
        self.auth_details = parsed_response
        logger.info("Authentication successful. JSESSIONID set.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("deauthenticating...")
        self.deauthenticate()

    def deauthenticate(self):
        """
        Ends the ZIA authentication session.
        """
        logout_url = self.url + "/api/v1/authenticatedSession"

        headers = self.headers.copy()
        headers.update({"Cookie": f"JSESSIONID={self.session_id}"})
        headers.update(self.request_executor.get_custom_headers())
        try:
            response = requests.delete(logout_url, headers=headers, timeout=self.timeout)
            if response.status_code == 204:
                self.session_id = None
                self.auth_details = None
                return True
            else:
                return False
        except requests.RequestException as e:
            return False

    def get_base_url(self, endpoint):
        return self.url

    def send(self, method, path, json=None, params=None, data=None, headers=None):
        """
        Send a request to the ZIA API using JSESSIONID-based authentication.

        Args:
            method (str): The HTTP method.
            path (str): API endpoint path.
            json (dict, optional): Request payload. Defaults to None.
            params (dict, optional): URL query parameters. Defaults to None.
            data (dict, optional): Raw request data. Defaults to None.
            headers (dict, optional): Additional request headers. Defaults to None.

        Returns:
            requests.Response: Response object from the request.
        """
        url = f"{self.url}/{path.lstrip('/')}"
        attempts = 0

        while attempts < 5:
            try:
                if self.is_session_expired():
                    logger.warning("Session expired. Refreshing...")
                    self.authenticate()

                # Always refresh session cookie
                headers_with_user_agent = self.headers.copy()
                headers_with_user_agent.update(headers or {})
                headers_with_user_agent["Cookie"] = f"JSESSIONID={self.session_id}"

                resp = requests.request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    headers=headers_with_user_agent,
                    timeout=self.timeout,
                )

                if resp.status_code == 429:
                    sleep_time = int(resp.headers.get("Retry-After", 2))
                    logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                    sleep(sleep_time)
                    attempts += 1
                    continue

                _, err = check_response_for_error(url, resp, resp.text)
                if err:
                    raise err

                # return parsed_response, {
                return resp, {
                    "method": method,
                    "url": url,
                    "params": params or {},
                    "headers": headers_with_user_agent,
                    "json": json or {},
                }

            except requests.RequestException as e:
                logger.error(f"Request to {url} failed: {e}")
                if attempts == 4:
                    raise
                logger.warning(f"Retrying... ({attempts + 1}/5)")
                attempts += 1
                sleep(5)

        raise ValueError("Request execution failed after maximum retries.")

    def set_session(self, session):
        """Dummy method for compatibility with the request executor."""
        self._session = session

    @property
    def activate(self):
        """
        The interface object for the :ref:`ZIA Activation interface <zia-activate>`.

        """
        from zscaler.zia.activate import ActivationAPI

        return ActivationAPI(self.request_executor)

    @property
    def admin_roles(self):
        """
        The interface object for the :ref:`ZIA Admin and Role Management interface <zia-admin_roles>`.

        """
        from zscaler.zia.admin_roles import AdminRolesAPI

        return AdminRolesAPI(self.request_executor)

    @property
    def admin_users(self):
        """
        The interface object for the :ref:`ZIA Admin Users interface <zia-admin_users>`.

        """
        from zscaler.zia.admin_users import AdminUsersAPI

        return AdminUsersAPI(self.request_executor)

    @property
    def audit_logs(self):
        """
        The interface object for the :ref:`ZIA Admin Audit Logs interface <zia-audit_logs>`.

        """
        from zscaler.zia.audit_logs import AuditLogsAPI

        return AuditLogsAPI(self.request_executor)

    @property
    def apptotal(self):
        """
        The interface object for the :ref:`ZIA AppTotal interface <zia-apptotal>`.

        """
        from zscaler.zia.apptotal import AppTotalAPI

        return AppTotalAPI(self.request_executor)

    @property
    def advanced_settings(self):
        """
        The interface object for the :ref:`ZIA Advanced Settings interface <zia-advanced_settings>`.

        """
        from zscaler.zia.advanced_settings import AdvancedSettingsAPI

        return AdvancedSettingsAPI(self.request_executor)

    @property
    def atp_policy(self):
        """
        The interface object for the :ref:`ZIA Advanced Settings interface <zia-advanced_settings>`.

        """
        from zscaler.zia.atp_policy import ATPPolicyAPI

        return ATPPolicyAPI(self.request_executor)

    @property
    def authentication_settings(self):
        """
        The interface object for the :ref:`ZIA Authentication Security Settings interface <zia-authentication_settings>`.

        """
        from zscaler.zia.authentication_settings import AuthenticationSettingsAPI

        return AuthenticationSettingsAPI(self.request_executor)

    @property
    def cloudappcontrol(self):
        """
        The interface object for the :ref:`ZIA Cloud App Control interface <zia-cloudappcontrol>`.

        """
        from zscaler.zia.cloudappcontrol import CloudAppControlAPI

        return CloudAppControlAPI(self.request_executor)

    @property
    def casb_dlp_rules(self):
        """
        The interface object for the :ref:`ZIA Casb DLP Rules interface <zia-casb_dlp_rules>`.

        """
        from zscaler.zia.casb_dlp_rules import CasbdDlpRulesAPI

        return CasbdDlpRulesAPI(self.request_executor)

    @property
    def casb_malware_rules(self):
        """
        The interface object for the :ref:`ZIA Casb Malware Rules interface <zia-casb_malware_rules>`.

        """

        from zscaler.zia.casb_malware_rules import CasbMalwareRulesAPI

        return CasbMalwareRulesAPI(self.request_executor)

    @property
    def cloud_applications(self):
        """
        The interface object for the :ref:`ZIA Cloud App Control <zia-cloud_applications>`.

        """
        from zscaler.zia.cloud_applications import CloudApplicationsAPI

        return CloudApplicationsAPI(self.request_executor)

    @property
    def shadow_it_report(self):
        """
        The interface object for the :ref:`ZIA Shadow IT Report <zia-shadow_it_report>`.

        """
        from zscaler.zia.shadow_it_report import ShadowITAPI

        return ShadowITAPI(self.request_executor)

    @property
    def cloud_browser_isolation(self):
        """
        The interface object for the :ref:`ZIA Cloud Browser Isolation Profile <zia-cloud_browser_isolation>`.

        """
        from zscaler.zia.cloud_browser_isolation import CBIProfileAPI

        return CBIProfileAPI(self.request_executor)

    @property
    def cloud_nss(self):
        """
        The interface object for the :ref:`ZIA Cloud NSS interface <zia-cloud_nss>`.

        """
        from zscaler.zia.cloud_nss import CloudNSSAPI

        return CloudNSSAPI(self.request_executor)

    @property
    def cloud_firewall_dns(self):
        """
        The interface object for the :ref:`ZIA Firewall DNS Policies interface <zia-cloud_firewall_dns>`.

        """
        from zscaler.zia.cloud_firewall_dns import FirewallDNSRulesAPI

        return FirewallDNSRulesAPI(self.request_executor)

    @property
    def cloud_firewall_ips(self):
        """
        The interface object for the :ref:`ZIA Firewall IPS Policies interface <zia-cloud_firewall_ips>`.

        """
        from zscaler.zia.cloud_firewall_ips import FirewallIPSRulesAPI

        return FirewallIPSRulesAPI(self.request_executor)

    @property
    def cloud_firewall_rules(self):
        """
        The interface object for the :ref:`ZIA Firewall Policies interface <zia-cloud_firewall_rules>`.

        """
        from zscaler.zia.cloud_firewall_rules import FirewallPolicyAPI

        return FirewallPolicyAPI(self.request_executor)

    @property
    def cloud_firewall(self):
        """
        The interface object for the :ref:`ZIA Cloud Firewall resources interface <zia-cloud_firewall>`.

        """
        from zscaler.zia.cloud_firewall import FirewallResourcesAPI

        return FirewallResourcesAPI(self.request_executor)

    @property
    def dlp_dictionary(self):
        """
        The interface object for the :ref:`ZIA DLP Dictionaries interface <zia-dlp_dictionary>`.

        """
        from zscaler.zia.dlp_dictionary import DLPDictionaryAPI

        return DLPDictionaryAPI(self.request_executor)

    @property
    def dlp_engine(self):
        """
        The interface object for the :ref:`ZIA DLP Engine interface <zia-dlp_engine>`.

        """
        from zscaler.zia.dlp_engine import DLPEngineAPI

        return DLPEngineAPI(self.request_executor)

    @property
    def dlp_web_rules(self):
        """
        The interface object for the :ref:`ZIA DLP Web Rules interface <zia-dlp_web_rules>`.

        """
        from zscaler.zia.dlp_web_rules import DLPWebRuleAPI

        return DLPWebRuleAPI(self.request_executor)

    @property
    def dlp_templates(self):
        """
        The interface object for the :ref:`ZIA DLP Templates interface <zia-dlp_templates>`.

        """
        from zscaler.zia.dlp_templates import DLPTemplatesAPI

        return DLPTemplatesAPI(self.request_executor)

    @property
    def dlp_resources(self):
        """
        The interface object for the :ref:`ZIA DLP Resources interface <zia-dlp_resources>`.

        """
        from zscaler.zia.dlp_resources import DLPResourcesAPI

        return DLPResourcesAPI(self.request_executor)

    @property
    def device_management(self):
        """
        The interface object for the :ref:`ZIA Device Management interface <zia-device_management>`.

        """
        from zscaler.zia.device_management import DeviceManagementAPI

        return DeviceManagementAPI(self.request_executor)

    @property
    def end_user_notification(self):
        """
        The interface object for the :ref:`ZIA End user Notification interface <zia-end_user_notification>`.

        """
        from zscaler.zia.end_user_notification import EndUserNotificationAPI

        return EndUserNotificationAPI(self.request_executor)

    @property
    def ipv6_config(self):
        """
        The interface object for the :ref:`ZIA Traffic IPV6 Configuration <zia-ipv6_config>`.

        """
        from zscaler.zia.ipv6_config import TrafficIPV6ConfigAPI

        return TrafficIPV6ConfigAPI(self.request_executor)

    @property
    def file_type_control_rule(self):
        """
        The interface object for the :ref:`ZIA File Type Control Rule interface <zia-file_type_control_rule>`.

        """
        from zscaler.zia.file_type_control_rule import FileTypeControlRuleAPI

        return FileTypeControlRuleAPI(self.request_executor)

    @property
    def locations(self):
        """
        The interface object for the :ref:`ZIA Locations interface <zia-locations>`.

        """
        from zscaler.zia.locations import LocationsAPI

        return LocationsAPI(self.request_executor)

    @property
    def malware_protection_policy(self):
        """
        The interface object for the :ref:`ZIA Malware Protection Policy interface <zia-malware_protection_policy>`.

        """
        from zscaler.zia.malware_protection_policy import MalwareProtectionPolicyAPI

        return MalwareProtectionPolicyAPI(self.request_executor)

    @property
    def organization_information(self):
        """
        The interface object for the :ref:`ZIA Organization Information interface <zia-organization_information>`.

        """
        from zscaler.zia.organization_information import OrganizationInformationAPI

        return OrganizationInformationAPI(self.request_executor)

    @property
    def pac_files(self):
        """
        The interface object for the :ref:`ZIA Pac Files interface <zia-pac_files>`.

        """
        from zscaler.zia.pac_files import PacFilesAPI

        return PacFilesAPI(self.request_executor)

    @property
    def policy_export(self):
        """
        The interface object for the :ref:`ZIA Policy Export interface <zia-policy_export>`.

        """
        from zscaler.zia.policy_export import PolicyExportAPI

        return PolicyExportAPI(self.request_executor)

    @property
    def remote_assistance(self):
        """
        The interface object for the ZIA Remote Assistance interface.
        """
        from zscaler.zia.remote_assistance import RemoteAssistanceAPI

        return RemoteAssistanceAPI(self.request_executor)

    @property
    def rule_labels(self):
        """
        The interface object for the ZIA Rule Labels interface.
        """
        from zscaler.zia.rule_labels import RuleLabelsAPI

        return RuleLabelsAPI(self.request_executor)

    @property
    def sandbox(self):
        """
        The interface object for the :ref:`ZIA Cloud Sandbox interface <zia-sandbox>`.

        """
        from zscaler.zia.sandbox import CloudSandboxAPI

        return CloudSandboxAPI(self.request_executor)

    @property
    def sandbox_rules(self):
        """
        The interface object for the :ref:`ZIA Sandbox Rules interface <zia-sandbox_rules>`.

        """
        from zscaler.zia.sandbox_rules import SandboxRulesAPI

        return SandboxRulesAPI(self.request_executor)

    @property
    def security_policy_settings(self):
        """
        The interface object for the :ref:`ZIA Security Policy Settings interface <zia-security_policy_settings>`.

        """
        from zscaler.zia.security_policy_settings import SecurityPolicyAPI

        return SecurityPolicyAPI(self.request_executor)

    @property
    def ssl_inspection_rules(self):
        """
        The interface object for the :ref:`ZIA SSL Inspection Rules interface <zia-security_policy_settings>`.

        """
        from zscaler.zia.ssl_inspection_rules import SSLInspectionAPI

        return SSLInspectionAPI(self.request_executor)

    @property
    def traffic_extranet(self):
        """
        The interface object for the :ref:`ZIA Extranet interface <zia-traffic_extranet>`.

        """
        from zscaler.zia.traffic_extranet import TrafficExtranetAPI

        return TrafficExtranetAPI(self.request_executor)

    @property
    def gre_tunnel(self):
        """
        The interface object for the :ref:`ZIA Traffic GRE Tunnel interface <zia-gre_tunnel>`.

        """
        from zscaler.zia.gre_tunnel import TrafficForwardingGRETunnelAPI

        return TrafficForwardingGRETunnelAPI(self.request_executor)

    @property
    def traffic_vpn_credentials(self):
        """
        The interface object for the :ref:`ZIA Traffic VPN Credential interface <zia-traffic_vpn_credentials>`.

        """
        from zscaler.zia.traffic_vpn_credentials import TrafficVPNCredentialAPI

        return TrafficVPNCredentialAPI(self.request_executor)

    @property
    def traffic_static_ip(self):
        """
        The interface object for the :ref:`ZIA Traffic Static IP interface <zia-traffic_static_ip>`.

        """
        from zscaler.zia.traffic_static_ip import TrafficStaticIPAPI

        return TrafficStaticIPAPI(self.request_executor)

    @property
    def url_categories(self):
        """
        The interface object for the :ref:`ZIA URL Categories interface <zia-url_categories>`.

        """
        from zscaler.zia.url_categories import URLCategoriesAPI

        return URLCategoriesAPI(self.request_executor)

    @property
    def url_filtering(self):
        """
        The interface object for the :ref:`ZIA URL Filtering interface <zia-url_filtering>`.

        """
        from zscaler.zia.url_filtering import URLFilteringAPI

        return URLFilteringAPI(self.request_executor)

    @property
    def user_management(self):
        """
        The interface object for the :ref:`ZIA User Management interface <zia-user_management>`.

        """
        from zscaler.zia.user_management import UserManagementAPI

        return UserManagementAPI(self.request_executor)

    @property
    def zpa_gateway(self):
        """
        The interface object for the :ref:`ZPA Gateway <zia-zpa_gateway>`.

        """
        from zscaler.zia.zpa_gateway import ZPAGatewayAPI

        return ZPAGatewayAPI(self.request_executor)

    @property
    def workload_groups(self):
        """
        The interface object for the :ref:`ZIA Workload Groups <zia-workload_groups>`.

        """
        from zscaler.zia.workload_groups import WorkloadGroupsAPI

        return WorkloadGroupsAPI(self.request_executor)

    @property
    def system_audit(self):
        """
        The interface object for the :ref:`ZIA System Audit interface <zia-system_audit>`.

        """
        from zscaler.zia.system_audit import SystemAuditReportAPI

        return SystemAuditReportAPI(self.request_executor)

    @property
    def iot_report(self):
        """
        The interface object for the :ref:`ZIA IOT Report interface <zia-iot_report>`.

        """
        from zscaler.zia.iot_report import IOTReportAPI

        return IOTReportAPI(self.request_executor)

    @property
    def mobile_threat_settings(self):
        """
        The interface object for the :ref:`ZIA Mobile Threat Settings interface <zia-mobile_threat_settings>`.

        """
        from zscaler.zia.mobile_threat_settings import MobileAdvancedSettingsAPI

        return MobileAdvancedSettingsAPI(self.request_executor)

    @property
    def dns_gatways(self):
        """
        The interface object for the :ref:`ZIA DNS Gateway interface <zia-dns_gatways>`.

        """
        from zscaler.zia.dns_gatways import DNSGatewayAPI

        return DNSGatewayAPI(self.request_executor)

    @property
    def alert_subscriptions(self):
        """
        The interface object for the :ref:`ZIA Alert Subscriptions interface <zia-alert_subscriptions>`.

        """
        from zscaler.zia.alert_subscriptions import AlertSubscriptionsAPI

        return AlertSubscriptionsAPI(self.request_executor)

    @property
    def bandwidth_classes(self):
        """
        The interface object for the :ref:`ZIA Bandwidth Classes interface <zia-bandwidth_classes>`.

        """
        from zscaler.zia.bandwidth_classes import BandwidthClassesAPI

        return BandwidthClassesAPI(self.request_executor)

    @property
    def bandwidth_control_rules(self):
        """
        The interface object for the :ref:`ZIA Bandwidth Control Rule interface <zia-bandwidth_control_rules>`.

        """
        from zscaler.zia.bandwidth_control_rules import BandwidthControlRulesAPI

        return BandwidthControlRulesAPI(self.request_executor)

    @property
    def risk_profiles(self):
        """
        The interface object for the :ref:`ZIA Risk Profiles interface <zia-risk_profiles>`.

        """
        from zscaler.zia.risk_profiles import RiskProfilesAPI

        return RiskProfilesAPI(self.request_executor)

    @property
    def cloud_app_instances(self):
        """
        The interface object for the :ref:`ZIA Cloud Application Instances interface <zia-cloud_app_instances>`.

        """
        from zscaler.zia.cloud_app_instances import CloudApplicationInstancesAPI

        return CloudApplicationInstancesAPI(self.request_executor)

    @property
    def tenancy_restriction_profile(self):
        """
        The interface object for the :ref:`ZIA Tenant Restriction Profile interface <zia-tenancy_restriction_profile>`.

        """
        from zscaler.zia.tenancy_restriction_profile import TenancyRestrictionProfileAPI

        return TenancyRestrictionProfileAPI(self.request_executor)

    @property
    def time_intervals(self):
        """
        The interface object for the :ref:`ZIA Time Intervals interface <zia-time_intervals>`.

        """
        from zscaler.zia.time_intervals import TimeIntervalsAPI

        return TimeIntervalsAPI(self.request_executor)

    @property
    def ftp_control_policy(self):
        """
        The interface object for the :ref:`ZIA FTP Control Policy interface <zia-ftp_control_policy>`.

        """
        from zscaler.zia.ftp_control_policy import FTPControlPolicyAPI

        return FTPControlPolicyAPI(self.request_executor)

    @property
    def proxies(self):
        """
        The interface object for the :ref:`ZIA Proxies interface <zia-proxies>`.

        """
        from zscaler.zia.proxies import ProxiesAPI

        return ProxiesAPI(self.request_executor)

    @property
    def dedicated_ip_gateways(self):
        """
        The interface object for the :ref:`ZIA Dedicated IP Gateways interface <zia-dedicated_ip_gateways>`.

        """
        from zscaler.zia.dedicated_ip_gateways import DedicatedIPGatewaysAPI

        return DedicatedIPGatewaysAPI(self.request_executor)

    @property
    def traffic_datacenters(self):
        """
        The interface object for the :ref:`ZIA Traffic Datacenters interface <zia-traffic_datacenters>`.

        """
        from zscaler.zia.traffic_datacenters import TrafficDatacentersAPI

        return TrafficDatacentersAPI(self.request_executor)

    @property
    def nss_servers(self):
        """
        The interface object for the :ref:`ZIA NSS Servers interface <zia-nss_servers>`.

        """
        from zscaler.zia.nss_servers import NssServersAPI

        return NssServersAPI(self.request_executor)

    @property
    def nat_control_policy(self):
        """
        The interface object for the :ref:`ZIA NAT Control Policy interface <zia-nat_control_policy>`.

        """

        from zscaler.zia.nat_control_policy import NatControlPolicyAPI

        return NatControlPolicyAPI(self.request_executor)

    @property
    def vzen_clusters(self):
        """
        The interface object for the :ref:`Virtual ZEN Clusters interface <zia-vzen_clusters>`.

        """

        from zscaler.zia.vzen_clusters import VZENClustersAPI

        return VZENClustersAPI(self.request_executor)

    @property
    def browser_control_settings(self):
        """
        The interface object for the :ref:`Browser Control Settings interface <zia-browser_control_settings>`.

        """

        from zscaler.zia.browser_control_settings import BrowserControlSettingsPI

        return BrowserControlSettingsPI(self.request_executor)

    @property
    def saas_security_api(self):
        """
        The interface object for the :ref:`ZIA SaaS Security API interface <zia-saas_security_api>`.

        """

        from zscaler.zia.saas_security_api import SaaSSecurityAPI

        return SaaSSecurityAPI(self.request_executor)

    """
    Misc
    """

    def set_custom_headers(self, headers):
        self.request_executor.set_custom_headers(headers)

    def clear_custom_headers(self):
        self.request_executor.clear_custom_headers()

    def get_custom_headers(self):
        return self.request_executor.get_custom_headers()

    def get_default_headers(self):
        return self.request_executor.get_default_headers()
