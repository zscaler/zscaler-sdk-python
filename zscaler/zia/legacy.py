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
from zscaler.logger import setup_logging
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import obfuscate_api_key

# Setup the logger
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

    def __init__(self, cloud, timeout=240, cache=None, fail_safe=False, **kw):
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
        self.request_executor = RequestExecutor(self.config, self.cache, zia_legacy_client=self)

    def extractJSessionIDFromHeaders(self, header):
        session_id_str = header.get("Set-Cookie", "")

        if not session_id_str:
            raise ValueError("no Set-Cookie header received")

        regex = re.compile(r"JSESSIONID=(.*?);")
        result = regex.search(session_id_str)

        if not result:
            raise ValueError("couldn't find JSESSIONID in header value")

        return result.group(1)

    def is_session_expired(self):
        if self.auth_details is None:
            return True
        now = datetime.datetime.now()
        if self.auth_details["passwordExpiryTime"] > 0 and (self.session_refreshed - self.session_timeout_offset < now):
            return True
        return False

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

        url = f"{self.url}/api/v1/authenticatedSession"  # Correct path
        resp = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)

        if resp.status_code != 200:
            logger.error(f"Authentication failed: {resp.status_code}, {resp.text}")
            raise ValueError("Failed to authenticate with ZIA API")

        # Extract JSESSIONID
        self.session_id = self.extractJSessionIDFromHeaders(resp.headers)
        if not self.session_id:
            raise ValueError("Failed to extract JSESSIONID from authentication response")

        self.session_refreshed = datetime.datetime.now()
        self.auth_details = resp.json()
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

        # Prepare headers
        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent.update(headers or {})
        headers_with_user_agent["Cookie"] = f"JSESSIONID={self.session_id}"

        attempts = 0
        while attempts < 5:
            try:
                # Refresh session if expired
                if self.is_session_expired():
                    logger.warning("Session expired. Refreshing...")
                    self.authenticate()

                # Execute the request
                resp = requests.request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    headers=headers_with_user_agent,
                    timeout=self.timeout,
                )

                if resp.status_code == 429:  # Handle rate-limiting
                    sleep_time = int(resp.headers.get("Retry-After", 2))
                    logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                    sleep(sleep_time)
                    attempts += 1
                    continue

                if resp.status_code in [401, 403]:  # Authentication failure
                    logger.error("Authentication failed, refreshing session.")
                    self.authenticate()
                    continue

                if resp.status_code >= 400:
                    logger.error(f"Request failed: {resp.status_code}, {resp.text}")
                    raise ValueError(f"Request failed with status {resp.status_code}")

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
        The interface object for the :ref:`ZIA Cloud App Control <zia-cloudappcontrol>`.

        """
        from zscaler.zia.cloudappcontrol import CloudAppControlAPI

        return CloudAppControlAPI(self.request_executor)

    @property
    def cloud_applications(self):
        """
        The interface object for the :ref:`ZIA Cloud App Control <zia-cloud_applications>`.

        """
        from zscaler.zia.cloud_applications import CloudApplicationsAPI

        return CloudApplicationsAPI(self.request_executor)

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
    def traffic_gre_tunnel(self):
        """
        The interface object for the :ref:`ZIA Traffic Forwarding interface <zia-traffic_gre_tunnel>`.

        """
        from zscaler.zia.traffic_gre_tunnels import TrafficForwardingGRETunnelAPI

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
