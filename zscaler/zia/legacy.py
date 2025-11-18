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

from __future__ import annotations

import datetime
import logging
import os
import re
import time
import uuid
from time import sleep
from typing import Optional, Dict, Any, Tuple, Type, TYPE_CHECKING

import requests
from zscaler import __version__
from zscaler.cache.cache import Cache
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import obfuscate_api_key
from zscaler.logger import setup_logging, dump_request, dump_response
from zscaler.errors.response_checker import check_response_for_error

setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")

# Import all ZIA API classes for type hints only (to avoid circular imports)
if TYPE_CHECKING:
    from zscaler.zia.activate import ActivationAPI
    from zscaler.zia.admin_roles import AdminRolesAPI
    from zscaler.zia.admin_users import AdminUsersAPI
    from zscaler.zia.audit_logs import AuditLogsAPI
    from zscaler.zia.apptotal import AppTotalAPI
    from zscaler.zia.advanced_settings import AdvancedSettingsAPI
    from zscaler.zia.atp_policy import ATPPolicyAPI
    from zscaler.zia.authentication_settings import AuthenticationSettingsAPI
    from zscaler.zia.cloudappcontrol import CloudAppControlAPI
    from zscaler.zia.casb_dlp_rules import CasbdDlpRulesAPI
    from zscaler.zia.casb_malware_rules import CasbMalwareRulesAPI
    from zscaler.zia.cloud_applications import CloudApplicationsAPI
    from zscaler.zia.shadow_it_report import ShadowITAPI
    from zscaler.zia.cloud_browser_isolation import CBIProfileAPI
    from zscaler.zia.cloud_nss import CloudNSSAPI
    from zscaler.zia.cloud_firewall_dns import FirewallDNSRulesAPI
    from zscaler.zia.cloud_firewall_ips import FirewallIPSRulesAPI
    from zscaler.zia.cloud_firewall_rules import FirewallPolicyAPI
    from zscaler.zia.cloud_firewall import FirewallResourcesAPI
    from zscaler.zia.dlp_dictionary import DLPDictionaryAPI
    from zscaler.zia.dlp_engine import DLPEngineAPI
    from zscaler.zia.dlp_web_rules import DLPWebRuleAPI
    from zscaler.zia.dlp_templates import DLPTemplatesAPI
    from zscaler.zia.dlp_resources import DLPResourcesAPI
    from zscaler.zia.device_management import DeviceManagementAPI
    from zscaler.zia.end_user_notification import EndUserNotificationAPI
    from zscaler.zia.ipv6_config import TrafficIPV6ConfigAPI
    from zscaler.zia.file_type_control_rule import FileTypeControlRuleAPI
    from zscaler.zia.locations import LocationsAPI
    from zscaler.zia.malware_protection_policy import MalwareProtectionPolicyAPI
    from zscaler.zia.organization_information import OrganizationInformationAPI
    from zscaler.zia.pac_files import PacFilesAPI
    from zscaler.zia.policy_export import PolicyExportAPI
    from zscaler.zia.remote_assistance import RemoteAssistanceAPI
    from zscaler.zia.rule_labels import RuleLabelsAPI
    from zscaler.zia.sandbox import CloudSandboxAPI
    from zscaler.zia.sandbox_rules import SandboxRulesAPI
    from zscaler.zia.security_policy_settings import SecurityPolicyAPI
    from zscaler.zia.ssl_inspection_rules import SSLInspectionAPI
    from zscaler.zia.traffic_extranet import TrafficExtranetAPI
    from zscaler.zia.gre_tunnel import TrafficForwardingGRETunnelAPI
    from zscaler.zia.traffic_vpn_credentials import TrafficVPNCredentialAPI
    from zscaler.zia.traffic_static_ip import TrafficStaticIPAPI
    from zscaler.zia.url_categories import URLCategoriesAPI
    from zscaler.zia.url_filtering import URLFilteringAPI
    from zscaler.zia.user_management import UserManagementAPI
    from zscaler.zia.zpa_gateway import ZPAGatewayAPI
    from zscaler.zia.workload_groups import WorkloadGroupsAPI
    from zscaler.zia.system_audit import SystemAuditReportAPI
    from zscaler.zia.iot_report import IOTReportAPI
    from zscaler.zia.mobile_threat_settings import MobileAdvancedSettingsAPI
    from zscaler.zia.dns_gatways import DNSGatewayAPI
    from zscaler.zia.alert_subscriptions import AlertSubscriptionsAPI
    from zscaler.zia.bandwidth_classes import BandwidthClassesAPI
    from zscaler.zia.bandwidth_control_rules import BandwidthControlRulesAPI
    from zscaler.zia.risk_profiles import RiskProfilesAPI
    from zscaler.zia.cloud_app_instances import CloudApplicationInstancesAPI
    from zscaler.zia.tenancy_restriction_profile import TenancyRestrictionProfileAPI
    from zscaler.zia.time_intervals import TimeIntervalsAPI
    from zscaler.zia.ftp_control_policy import FTPControlPolicyAPI
    from zscaler.zia.proxies import ProxiesAPI
    from zscaler.zia.dedicated_ip_gateways import DedicatedIPGatewaysAPI
    from zscaler.zia.traffic_datacenters import TrafficDatacentersAPI
    from zscaler.zia.nss_servers import NssServersAPI
    from zscaler.zia.nat_control_policy import NatControlPolicyAPI
    from zscaler.zia.vzen_clusters import VZENClustersAPI
    from zscaler.zia.vzen_nodes import VZENNodesAPI
    from zscaler.zia.browser_control_settings import BrowserControlSettingsPI
    from zscaler.zia.saas_security_api import SaaSSecurityAPI
    from zscaler.zia.cloud_to_cloud_ir import CloudToCloudIRAPI
    from zscaler.zia.traffic_capture import TrafficCaptureAPI


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

        session_safety_margin (int):
            Safety margin in seconds before the 5-minute session idle timeout to proactively refresh
            the session. Default is 30 seconds (refreshes at 4.5 minutes). Cannot exceed 5 minutes.

        use_session_validation (bool):
            Whether to use the new session idle timeout validation (default: True) or legacy
            passwordExpiryTime validation (False). The new behavior is recommended for the 5-minute
            session timeout requirement.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Internet Access"
    _build = __version__
    _env_base = "ZIA"
    url = "https://zsapi.zscaler.net"
    env_cloud = "zscaler"

    def __init__(
        self,
        cloud: str,
        timeout: int = 240,
        cache: Optional[Cache] = None,
        fail_safe: bool = False,
        request_executor_impl: Optional[Type] = None,
        session_safety_margin: int = 30,
        use_session_validation: bool = True,
        **kw: Any
    ) -> None:
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
        self.partner_id = kw.get("partner_id") or os.getenv("ZSCALER_PARTNER_ID")
        self.timeout = timeout
        self.fail_safe = fail_safe

        # Session management configuration
        env_safety_margin = os.getenv(f"{self._env_base}_SESSION_SAFETY_MARGIN")
        if env_safety_margin is not None:
            self.session_safety_margin = int(env_safety_margin)
        else:
            self.session_safety_margin = kw.get("session_safety_margin", session_safety_margin)

        # Ensure session_safety_margin has a default value if None
        if self.session_safety_margin is None:
            self.session_safety_margin = 30  # Default 30 seconds

        self.max_idle_time = datetime.timedelta(minutes=5) - datetime.timedelta(seconds=self.session_safety_margin)
        self.last_activity = None
        self.use_session_validation = kw.get("use_session_validation", use_session_validation) or os.getenv(
            f"{self._env_base}_USE_SESSION_VALIDATION", "true").lower() == "true"

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
        # Add x-partner-id header if partnerId is provided
        if self.partner_id:
            self.headers["x-partner-id"] = self.partner_id
        self.session_timeout_offset = datetime.timedelta(minutes=5)
        self.session_refreshed = None
        self.auth_details = None
        self.session_id = None
        self.authenticate()

        # Create request executor
        self.config = {
            "client": {
                "cloud": self.env_cloud,
                "partnerId": self.partner_id or "",
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": 3},
                "cache": {"enabled": True},
            }
        }
        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, zia_legacy_client=self)

    def extractJSessionIDFromHeaders(self, header: Dict[str, str]) -> str:
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
        Checks whether the current session is expired using passwordExpiryTime.
        This maintains backward compatibility.
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

    def is_session_idle_expired(self) -> bool:
        """
        Checks if the session has been idle for too long (approaching 5-minute limit).
        This is the new default behavior for session idle timeout.
        """
        if self.last_activity is None:
            return True

        idle_duration = datetime.datetime.utcnow() - self.last_activity
        return idle_duration >= self.max_idle_time

    def validate_session_status(self) -> bool:
        """
        Actively checks session status via GET /api/v1/authenticatedSession.
        Returns True if session is valid, False if expired.
        """
        try:
            url = f"{self.url}/api/v1/authenticatedSession"
            headers = self.headers.copy()
            headers["Cookie"] = f"JSESSIONID={self.session_id}"

            response = requests.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 200:
                # Session is still valid, update last activity
                self.last_activity = datetime.datetime.utcnow()
                return True
            else:
                # Session expired or invalid
                return False

        except Exception as e:
            logger.warning(f"Session validation failed: {e}")
            return False

    def ensure_valid_session(self) -> None:
        """
        Ensures the session is valid before making API calls.
        Uses the configured validation strategy.
        """
        if self.use_session_validation:
            # New default behavior: check session idle timeout
            if self.is_session_idle_expired():
                logger.info("Session approaching idle timeout, refreshing...")
                self.authenticate()
                return

            # Actively validate session status
            if not self.validate_session_status():
                logger.info("Session validation failed, refreshing...")
                self.authenticate()
                return
        else:
            # Legacy behavior: use passwordExpiryTime
            if self.is_session_expired():
                logger.info("Session expired based on passwordExpiryTime, refreshing...")
                self.authenticate()
                return

        # Update last activity time
        self.last_activity = datetime.datetime.utcnow()

    def authenticate(self) -> None:
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
        method = "POST"
        request_uuid = str(uuid.uuid4())
        start_time = time.time()

        # Log authentication request using the same formatting as regular API calls
        dump_request(logger, url, method, payload, {}, self.headers, request_uuid)

        resp = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)

        # Log authentication response using the same formatting as regular API calls
        dump_response(logger, url, method, resp, {}, request_uuid, start_time)

        parsed_response, err = check_response_for_error(url, resp, resp.text)
        if err:
            raise err

        self.session_id = self.extractJSessionIDFromHeaders(resp.headers)
        if not self.session_id:
            raise ValueError("Failed to extract JSESSIONID from authentication response")

        self.session_refreshed = datetime.datetime.now()
        self.auth_details = parsed_response
        self.last_activity = datetime.datetime.utcnow()  # Set initial activity time
        logger.info("Authentication successful. JSESSIONID set.")

    def __enter__(self) -> "LegacyZIAClientHelper":
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        logger.debug("deauthenticating...")
        self.deauthenticate()

    def deauthenticate(self) -> bool:
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

    def get_base_url(self, endpoint: str) -> str:
        return self.url

    def send(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[requests.Response, Dict[str, Any]]:
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
                # Ensure session is valid before making any request
                self.ensure_valid_session()

                # Always refresh session cookie
                headers_with_user_agent = self.headers.copy()
                headers_with_user_agent.update(headers or {})
                headers_with_user_agent["Cookie"] = f"JSESSIONID={self.session_id}"

                # Special handling for PAC file validation endpoint
                if "/pacFiles/validate" in path:
                    # For PAC validation, send as raw data without any modification
                    resp = requests.request(
                        method=method,
                        url=url,
                        data=data,  # Send as raw data, not JSON
                        params=params,
                        headers=headers_with_user_agent,
                        timeout=self.timeout,
                    )
                else:
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

    def set_session(self, session: Any) -> None:
        """Dummy method for compatibility with the request executor."""
        self._session = session

    @property
    def activate(self) -> "ActivationAPI":
        """
        The interface object for the :ref:`ZIA Activation interface <zia-activate>`.

        """
        from zscaler.zia.activate import ActivationAPI

        return ActivationAPI(self.request_executor)

    @property
    def admin_roles(self) -> "AdminRolesAPI":
        """
        The interface object for the :ref:`ZIA Admin and Role Management interface <zia-admin_roles>`.

        """
        from zscaler.zia.admin_roles import AdminRolesAPI

        return AdminRolesAPI(self.request_executor)

    @property
    def admin_users(self) -> "AdminUsersAPI":
        """
        The interface object for the :ref:`ZIA Admin Users interface <zia-admin_users>`.

        """
        from zscaler.zia.admin_users import AdminUsersAPI

        return AdminUsersAPI(self.request_executor)

    @property
    def audit_logs(self) -> "AuditLogsAPI":
        """
        The interface object for the :ref:`ZIA Admin Audit Logs interface <zia-audit_logs>`.

        """
        from zscaler.zia.audit_logs import AuditLogsAPI

        return AuditLogsAPI(self.request_executor)

    @property
    def apptotal(self) -> "AppTotalAPI":
        """
        The interface object for the :ref:`ZIA AppTotal interface <zia-apptotal>`.

        """
        from zscaler.zia.apptotal import AppTotalAPI

        return AppTotalAPI(self.request_executor)

    @property
    def advanced_settings(self) -> "AdvancedSettingsAPI":
        """
        The interface object for the :ref:`ZIA Advanced Settings interface <zia-advanced_settings>`.

        """
        from zscaler.zia.advanced_settings import AdvancedSettingsAPI

        return AdvancedSettingsAPI(self.request_executor)

    @property
    def atp_policy(self) -> "ATPPolicyAPI":
        """
        The interface object for the :ref:`ZIA Advanced Settings interface <zia-advanced_settings>`.

        """
        from zscaler.zia.atp_policy import ATPPolicyAPI

        return ATPPolicyAPI(self.request_executor)

    @property
    def authentication_settings(self) -> "AuthenticationSettingsAPI":
        """
        The interface object for the :ref:`ZIA Authentication Security Settings interface <zia-authentication_settings>`.

        """
        from zscaler.zia.authentication_settings import AuthenticationSettingsAPI

        return AuthenticationSettingsAPI(self.request_executor)

    @property
    def cloudappcontrol(self) -> "CloudAppControlAPI":
        """
        The interface object for the :ref:`ZIA Cloud App Control interface <zia-cloudappcontrol>`.

        """
        from zscaler.zia.cloudappcontrol import CloudAppControlAPI

        return CloudAppControlAPI(self.request_executor)

    @property
    def casb_dlp_rules(self) -> "CasbdDlpRulesAPI":
        """
        The interface object for the :ref:`ZIA Casb DLP Rules interface <zia-casb_dlp_rules>`.

        """
        from zscaler.zia.casb_dlp_rules import CasbdDlpRulesAPI

        return CasbdDlpRulesAPI(self.request_executor)

    @property
    def casb_malware_rules(self) -> "CasbMalwareRulesAPI":
        """
        The interface object for the :ref:`ZIA Casb Malware Rules interface <zia-casb_malware_rules>`.

        """

        from zscaler.zia.casb_malware_rules import CasbMalwareRulesAPI

        return CasbMalwareRulesAPI(self.request_executor)

    @property
    def cloud_applications(self) -> "CloudApplicationsAPI":
        """
        The interface object for the :ref:`ZIA Cloud App Control <zia-cloud_applications>`.

        """
        from zscaler.zia.cloud_applications import CloudApplicationsAPI

        return CloudApplicationsAPI(self.request_executor)

    @property
    def shadow_it_report(self) -> "ShadowITAPI":
        """
        The interface object for the :ref:`ZIA Shadow IT Report <zia-shadow_it_report>`.

        """
        from zscaler.zia.shadow_it_report import ShadowITAPI

        return ShadowITAPI(self.request_executor)

    @property
    def cloud_browser_isolation(self) -> "CBIProfileAPI":
        """
        The interface object for the :ref:`ZIA Cloud Browser Isolation Profile <zia-cloud_browser_isolation>`.

        """
        from zscaler.zia.cloud_browser_isolation import CBIProfileAPI

        return CBIProfileAPI(self.request_executor)

    @property
    def cloud_nss(self) -> "CloudNSSAPI":
        """
        The interface object for the :ref:`ZIA Cloud NSS interface <zia-cloud_nss>`.

        """
        from zscaler.zia.cloud_nss import CloudNSSAPI

        return CloudNSSAPI(self.request_executor)

    @property
    def cloud_firewall_dns(self) -> "FirewallDNSRulesAPI":
        """
        The interface object for the :ref:`ZIA Firewall DNS Policies interface <zia-cloud_firewall_dns>`.

        """
        from zscaler.zia.cloud_firewall_dns import FirewallDNSRulesAPI

        return FirewallDNSRulesAPI(self.request_executor)

    @property
    def cloud_firewall_ips(self) -> "FirewallIPSRulesAPI":
        """
        The interface object for the :ref:`ZIA Firewall IPS Policies interface <zia-cloud_firewall_ips>`.

        """
        from zscaler.zia.cloud_firewall_ips import FirewallIPSRulesAPI

        return FirewallIPSRulesAPI(self.request_executor)

    @property
    def cloud_firewall_rules(self) -> "FirewallPolicyAPI":
        """
        The interface object for the :ref:`ZIA Firewall Policies interface <zia-cloud_firewall_rules>`.

        """
        from zscaler.zia.cloud_firewall_rules import FirewallPolicyAPI

        return FirewallPolicyAPI(self.request_executor)

    @property
    def cloud_firewall(self) -> "FirewallResourcesAPI":
        """
        The interface object for the :ref:`ZIA Cloud Firewall resources interface <zia-cloud_firewall>`.

        """
        from zscaler.zia.cloud_firewall import FirewallResourcesAPI

        return FirewallResourcesAPI(self.request_executor)

    @property
    def dlp_dictionary(self) -> "DLPDictionaryAPI":
        """
        The interface object for the :ref:`ZIA DLP Dictionaries interface <zia-dlp_dictionary>`.

        """
        from zscaler.zia.dlp_dictionary import DLPDictionaryAPI

        return DLPDictionaryAPI(self.request_executor)

    @property
    def dlp_engine(self) -> "DLPEngineAPI":
        """
        The interface object for the :ref:`ZIA DLP Engine interface <zia-dlp_engine>`.

        """
        from zscaler.zia.dlp_engine import DLPEngineAPI

        return DLPEngineAPI(self.request_executor)

    @property
    def dlp_web_rules(self) -> "DLPWebRuleAPI":
        """
        The interface object for the :ref:`ZIA DLP Web Rules interface <zia-dlp_web_rules>`.

        """
        from zscaler.zia.dlp_web_rules import DLPWebRuleAPI

        return DLPWebRuleAPI(self.request_executor)

    @property
    def dlp_templates(self) -> "DLPTemplatesAPI":
        """
        The interface object for the :ref:`ZIA DLP Templates interface <zia-dlp_templates>`.

        """
        from zscaler.zia.dlp_templates import DLPTemplatesAPI

        return DLPTemplatesAPI(self.request_executor)

    @property
    def dlp_resources(self) -> "DLPResourcesAPI":
        """
        The interface object for the :ref:`ZIA DLP Resources interface <zia-dlp_resources>`.

        """
        from zscaler.zia.dlp_resources import DLPResourcesAPI

        return DLPResourcesAPI(self.request_executor)

    @property
    def device_management(self) -> "DeviceManagementAPI":
        """
        The interface object for the :ref:`ZIA Device Management interface <zia-device_management>`.

        """
        from zscaler.zia.device_management import DeviceManagementAPI

        return DeviceManagementAPI(self.request_executor)

    @property
    def end_user_notification(self) -> "EndUserNotificationAPI":
        """
        The interface object for the :ref:`ZIA End user Notification interface <zia-end_user_notification>`.

        """
        from zscaler.zia.end_user_notification import EndUserNotificationAPI

        return EndUserNotificationAPI(self.request_executor)

    @property
    def ipv6_config(self) -> "TrafficIPV6ConfigAPI":
        """
        The interface object for the :ref:`ZIA Traffic IPV6 Configuration <zia-ipv6_config>`.

        """
        from zscaler.zia.ipv6_config import TrafficIPV6ConfigAPI

        return TrafficIPV6ConfigAPI(self.request_executor)

    @property
    def file_type_control_rule(self) -> "FileTypeControlRuleAPI":
        """
        The interface object for the :ref:`ZIA File Type Control Rule interface <zia-file_type_control_rule>`.

        """
        from zscaler.zia.file_type_control_rule import FileTypeControlRuleAPI

        return FileTypeControlRuleAPI(self.request_executor)

    @property
    def locations(self) -> "LocationsAPI":
        """
        The interface object for the :ref:`ZIA Locations interface <zia-locations>`.

        """
        from zscaler.zia.locations import LocationsAPI

        return LocationsAPI(self.request_executor)

    @property
    def malware_protection_policy(self) -> "MalwareProtectionPolicyAPI":
        """
        The interface object for the :ref:`ZIA Malware Protection Policy interface <zia-malware_protection_policy>`.

        """
        from zscaler.zia.malware_protection_policy import MalwareProtectionPolicyAPI

        return MalwareProtectionPolicyAPI(self.request_executor)

    @property
    def organization_information(self) -> "OrganizationInformationAPI":
        """
        The interface object for the :ref:`ZIA Organization Information interface <zia-organization_information>`.

        """
        from zscaler.zia.organization_information import OrganizationInformationAPI

        return OrganizationInformationAPI(self.request_executor)

    @property
    def pac_files(self) -> "PacFilesAPI":
        """
        The interface object for the :ref:`ZIA Pac Files interface <zia-pac_files>`.

        """
        from zscaler.zia.pac_files import PacFilesAPI

        return PacFilesAPI(self.request_executor)

    @property
    def policy_export(self) -> "PolicyExportAPI":
        """
        The interface object for the :ref:`ZIA Policy Export interface <zia-policy_export>`.

        """
        from zscaler.zia.policy_export import PolicyExportAPI

        return PolicyExportAPI(self.request_executor)

    @property
    def remote_assistance(self) -> "RemoteAssistanceAPI":
        """
        The interface object for the ZIA Remote Assistance interface.
        """
        from zscaler.zia.remote_assistance import RemoteAssistanceAPI

        return RemoteAssistanceAPI(self.request_executor)

    @property
    def rule_labels(self) -> "RuleLabelsAPI":
        """
        The interface object for the ZIA Rule Labels interface.
        """
        from zscaler.zia.rule_labels import RuleLabelsAPI

        return RuleLabelsAPI(self.request_executor)

    @property
    def sandbox(self) -> "CloudSandboxAPI":
        """
        The interface object for the :ref:`ZIA Cloud Sandbox interface <zia-sandbox>`.

        """
        from zscaler.zia.sandbox import CloudSandboxAPI

        return CloudSandboxAPI(self.request_executor)

    @property
    def sandbox_rules(self) -> "SandboxRulesAPI":
        """
        The interface object for the :ref:`ZIA Sandbox Rules interface <zia-sandbox_rules>`.

        """
        from zscaler.zia.sandbox_rules import SandboxRulesAPI

        return SandboxRulesAPI(self.request_executor)

    @property
    def security_policy_settings(self) -> "SecurityPolicyAPI":
        """
        The interface object for the :ref:`ZIA Security Policy Settings interface <zia-security_policy_settings>`.

        """
        from zscaler.zia.security_policy_settings import SecurityPolicyAPI

        return SecurityPolicyAPI(self.request_executor)

    @property
    def ssl_inspection_rules(self) -> "SSLInspectionAPI":
        """
        The interface object for the :ref:`ZIA SSL Inspection Rules interface <zia-security_policy_settings>`.

        """
        from zscaler.zia.ssl_inspection_rules import SSLInspectionAPI

        return SSLInspectionAPI(self.request_executor)

    @property
    def traffic_extranet(self) -> "TrafficExtranetAPI":
        """
        The interface object for the :ref:`ZIA Extranet interface <zia-traffic_extranet>`.

        """
        from zscaler.zia.traffic_extranet import TrafficExtranetAPI

        return TrafficExtranetAPI(self.request_executor)

    @property
    def gre_tunnel(self) -> "TrafficForwardingGRETunnelAPI":
        """
        The interface object for the :ref:`ZIA Traffic GRE Tunnel interface <zia-gre_tunnel>`.

        """
        from zscaler.zia.gre_tunnel import TrafficForwardingGRETunnelAPI

        return TrafficForwardingGRETunnelAPI(self.request_executor)

    @property
    def traffic_vpn_credentials(self) -> "TrafficVPNCredentialAPI":
        """
        The interface object for the :ref:`ZIA Traffic VPN Credential interface <zia-traffic_vpn_credentials>`.

        """
        from zscaler.zia.traffic_vpn_credentials import TrafficVPNCredentialAPI

        return TrafficVPNCredentialAPI(self.request_executor)

    @property
    def traffic_static_ip(self) -> "TrafficStaticIPAPI":
        """
        The interface object for the :ref:`ZIA Traffic Static IP interface <zia-traffic_static_ip>`.

        """
        from zscaler.zia.traffic_static_ip import TrafficStaticIPAPI

        return TrafficStaticIPAPI(self.request_executor)

    @property
    def url_categories(self) -> "URLCategoriesAPI":
        """
        The interface object for the :ref:`ZIA URL Categories interface <zia-url_categories>`.

        """
        from zscaler.zia.url_categories import URLCategoriesAPI

        return URLCategoriesAPI(self.request_executor)

    @property
    def url_filtering(self) -> "URLFilteringAPI":
        """
        The interface object for the :ref:`ZIA URL Filtering interface <zia-url_filtering>`.

        """
        from zscaler.zia.url_filtering import URLFilteringAPI

        return URLFilteringAPI(self.request_executor)

    @property
    def user_management(self) -> "UserManagementAPI":
        """
        The interface object for the :ref:`ZIA User Management interface <zia-user_management>`.

        """
        from zscaler.zia.user_management import UserManagementAPI

        return UserManagementAPI(self.request_executor)

    @property
    def zpa_gateway(self) -> "ZPAGatewayAPI":
        """
        The interface object for the :ref:`ZPA Gateway <zia-zpa_gateway>`.

        """
        from zscaler.zia.zpa_gateway import ZPAGatewayAPI

        return ZPAGatewayAPI(self.request_executor)

    @property
    def workload_groups(self) -> "WorkloadGroupsAPI":
        """
        The interface object for the :ref:`ZIA Workload Groups <zia-workload_groups>`.

        """
        from zscaler.zia.workload_groups import WorkloadGroupsAPI

        return WorkloadGroupsAPI(self.request_executor)

    @property
    def system_audit(self) -> "SystemAuditReportAPI":
        """
        The interface object for the :ref:`ZIA System Audit interface <zia-system_audit>`.

        """
        from zscaler.zia.system_audit import SystemAuditReportAPI

        return SystemAuditReportAPI(self.request_executor)

    @property
    def iot_report(self) -> "IOTReportAPI":
        """
        The interface object for the :ref:`ZIA IOT Report interface <zia-iot_report>`.

        """
        from zscaler.zia.iot_report import IOTReportAPI

        return IOTReportAPI(self.request_executor)

    @property
    def mobile_threat_settings(self) -> "MobileAdvancedSettingsAPI":
        """
        The interface object for the :ref:`ZIA Mobile Threat Settings interface <zia-mobile_threat_settings>`.

        """
        from zscaler.zia.mobile_threat_settings import MobileAdvancedSettingsAPI

        return MobileAdvancedSettingsAPI(self.request_executor)

    @property
    def dns_gatways(self) -> "DNSGatewayAPI":
        """
        The interface object for the :ref:`ZIA DNS Gateway interface <zia-dns_gatways>`.

        """
        from zscaler.zia.dns_gatways import DNSGatewayAPI

        return DNSGatewayAPI(self.request_executor)

    @property
    def alert_subscriptions(self) -> "AlertSubscriptionsAPI":
        """
        The interface object for the :ref:`ZIA Alert Subscriptions interface <zia-alert_subscriptions>`.

        """
        from zscaler.zia.alert_subscriptions import AlertSubscriptionsAPI

        return AlertSubscriptionsAPI(self.request_executor)

    @property
    def bandwidth_classes(self) -> "BandwidthClassesAPI":
        """
        The interface object for the :ref:`ZIA Bandwidth Classes interface <zia-bandwidth_classes>`.

        """
        from zscaler.zia.bandwidth_classes import BandwidthClassesAPI

        return BandwidthClassesAPI(self.request_executor)

    @property
    def bandwidth_control_rules(self) -> "BandwidthControlRulesAPI":
        """
        The interface object for the :ref:`ZIA Bandwidth Control Rule interface <zia-bandwidth_control_rules>`.

        """
        from zscaler.zia.bandwidth_control_rules import BandwidthControlRulesAPI

        return BandwidthControlRulesAPI(self.request_executor)

    @property
    def risk_profiles(self) -> "RiskProfilesAPI":
        """
        The interface object for the :ref:`ZIA Risk Profiles interface <zia-risk_profiles>`.

        """
        from zscaler.zia.risk_profiles import RiskProfilesAPI

        return RiskProfilesAPI(self.request_executor)

    @property
    def cloud_app_instances(self) -> "CloudApplicationInstancesAPI":
        """
        The interface object for the :ref:`ZIA Cloud Application Instances interface <zia-cloud_app_instances>`.

        """
        from zscaler.zia.cloud_app_instances import CloudApplicationInstancesAPI

        return CloudApplicationInstancesAPI(self.request_executor)

    @property
    def tenancy_restriction_profile(self) -> "TenancyRestrictionProfileAPI":
        """
        The interface object for the :ref:`ZIA Tenant Restriction Profile interface <zia-tenancy_restriction_profile>`.

        """
        from zscaler.zia.tenancy_restriction_profile import TenancyRestrictionProfileAPI

        return TenancyRestrictionProfileAPI(self.request_executor)

    @property
    def time_intervals(self) -> "TimeIntervalsAPI":
        """
        The interface object for the :ref:`ZIA Time Intervals interface <zia-time_intervals>`.

        """
        from zscaler.zia.time_intervals import TimeIntervalsAPI

        return TimeIntervalsAPI(self.request_executor)

    @property
    def ftp_control_policy(self) -> "FTPControlPolicyAPI":
        """
        The interface object for the :ref:`ZIA FTP Control Policy interface <zia-ftp_control_policy>`.

        """
        from zscaler.zia.ftp_control_policy import FTPControlPolicyAPI

        return FTPControlPolicyAPI(self.request_executor)

    @property
    def proxies(self) -> "ProxiesAPI":
        """
        The interface object for the :ref:`ZIA Proxies interface <zia-proxies>`.

        """
        from zscaler.zia.proxies import ProxiesAPI

        return ProxiesAPI(self.request_executor)

    @property
    def dedicated_ip_gateways(self) -> "DedicatedIPGatewaysAPI":
        """
        The interface object for the :ref:`ZIA Dedicated IP Gateways interface <zia-dedicated_ip_gateways>`.

        """
        from zscaler.zia.dedicated_ip_gateways import DedicatedIPGatewaysAPI

        return DedicatedIPGatewaysAPI(self.request_executor)

    @property
    def traffic_datacenters(self) -> "TrafficDatacentersAPI":
        """
        The interface object for the :ref:`ZIA Traffic Datacenters interface <zia-traffic_datacenters>`.

        """
        from zscaler.zia.traffic_datacenters import TrafficDatacentersAPI

        return TrafficDatacentersAPI(self.request_executor)

    @property
    def nss_servers(self) -> "NssServersAPI":
        """
        The interface object for the :ref:`ZIA NSS Servers interface <zia-nss_servers>`.

        """
        from zscaler.zia.nss_servers import NssServersAPI

        return NssServersAPI(self.request_executor)

    @property
    def nat_control_policy(self) -> "NatControlPolicyAPI":
        """
        The interface object for the :ref:`ZIA NAT Control Policy interface <zia-nat_control_policy>`.

        """

        from zscaler.zia.nat_control_policy import NatControlPolicyAPI

        return NatControlPolicyAPI(self.request_executor)

    @property
    def vzen_clusters(self) -> "VZENClustersAPI":
        """
        The interface object for the :ref:`Virtual ZEN Clusters interface <zia-vzen_clusters>`.

        """

        from zscaler.zia.vzen_clusters import VZENClustersAPI

        return VZENClustersAPI(self.request_executor)

    @property
    def vzen_nodes(self) -> "VZENNodesAPI":
        """
        The interface object for the :ref:`Virtual ZEN Nodes interface <zia-vzen_nodes>`.

        """

        from zscaler.zia.vzen_nodes import VZENNodesAPI

        return VZENNodesAPI(self.request_executor)

    @property
    def browser_control_settings(self) -> "BrowserControlSettingsPI":
        """
        The interface object for the :ref:`Browser Control Settings interface <zia-browser_control_settings>`.

        """

        from zscaler.zia.browser_control_settings import BrowserControlSettingsPI

        return BrowserControlSettingsPI(self.request_executor)

    @property
    def saas_security_api(self) -> "SaaSSecurityAPI":
        """
        The interface object for the :ref:`ZIA SaaS Security API interface <zia-saas_security_api>`.

        """

        from zscaler.zia.saas_security_api import SaaSSecurityAPI

        return SaaSSecurityAPI(self.request_executor)

    @property
    def cloud_to_cloud_ir(self) -> "CloudToCloudIRAPI":
        """
        The interface object for the :ref:`ZIA Cloud-to-Cloud DLP Incident Receiver API interface <zia-cloud_to_cloud_ir>`.

        """

        from zscaler.zia.cloud_to_cloud_ir import CloudToCloudIRAPI

        return CloudToCloudIRAPI(self.request_executor)

    @property
    def traffic_capture(self) -> "TrafficCaptureAPI":
        """
        The interface object for the :ref:`ZIA Traffic Capture API interface <zia-traffic_capture>`.

        """

        from zscaler.zia.traffic_capture import TrafficCaptureAPI

        return TrafficCaptureAPI(self.request_executor)

    """
    Misc
    """

    def set_custom_headers(self, headers: Dict[str, str]) -> None:
        self.request_executor.set_custom_headers(headers)

    def clear_custom_headers(self) -> None:
        self.request_executor.clear_custom_headers()

    def get_custom_headers(self) -> Dict[str, str]:
        return self.request_executor.get_custom_headers()

    def get_default_headers(self) -> Dict[str, str]:
        return self.request_executor.get_default_headers()
