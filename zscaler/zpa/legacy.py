from __future__ import annotations

import logging
import os
import urllib.parse
from typing import Optional, Dict, Any, Tuple, Type, TYPE_CHECKING

import requests

from zscaler import __version__
from zscaler.cache.cache import Cache
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.constants import ZPA_BASE_URLS, DEV_AUTH_URL
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    is_token_expired,
)
from zscaler.logger import setup_logging
from zscaler.errors.response_checker import check_response_for_error

# Import all ZPA API classes for type hints only (to avoid circular imports)
if TYPE_CHECKING:
    from zscaler.zpa.customer_controller import CustomerControllerAPI
    from zscaler.zpa.app_segment_by_type import ApplicationSegmentByTypeAPI
    from zscaler.zpa.application_segment import ApplicationSegmentAPI
    from zscaler.zpa.app_segments_ba import ApplicationSegmentBAAPI
    from zscaler.zpa.app_segments_ba_v2 import AppSegmentsBAV2API
    from zscaler.zpa.app_segments_inspection import AppSegmentsInspectionAPI
    from zscaler.zpa.app_segments_pra import AppSegmentsPRAAPI
    from zscaler.zpa.app_connector_groups import AppConnectorGroupAPI
    from zscaler.zpa.app_connectors import AppConnectorControllerAPI
    from zscaler.zpa.app_connector_schedule import AppConnectorScheduleAPI
    from zscaler.zpa.servers import AppServersAPI
    from zscaler.zpa.cbi_banner import CBIBannerAPI
    from zscaler.zpa.cbi_certificate import CBICertificateAPI
    from zscaler.zpa.cbi_profile import CBIProfileAPI
    from zscaler.zpa.cbi_region import CBIRegionAPI
    from zscaler.zpa.cbi_zpa_profile import CBIZPAProfileAPI
    from zscaler.zpa.certificates import CertificatesAPI
    from zscaler.zpa.cloud_connector_groups import CloudConnectorGroupsAPI
    from zscaler.zpa.customer_version_profile import CustomerVersionProfileAPI
    from zscaler.zpa.emergency_access import EmergencyAccessAPI
    from zscaler.zpa.enrollment_certificates import EnrollmentCertificateAPI
    from zscaler.zpa.idp import IDPControllerAPI
    from zscaler.zpa.app_protection import InspectionControllerAPI
    from zscaler.zpa.machine_groups import MachineGroupsAPI
    from zscaler.zpa.microtenants import MicrotenantsAPI
    from zscaler.zpa.lss import LSSConfigControllerAPI
    from zscaler.zpa.policies import PolicySetControllerAPI
    from zscaler.zpa.posture_profiles import PostureProfilesAPI
    from zscaler.zpa.pra_approval import PRAApprovalAPI
    from zscaler.zpa.pra_console import PRAConsoleAPI
    from zscaler.zpa.pra_credential import PRACredentialAPI
    from zscaler.zpa.pra_credential_pool import PRACredentialPoolAPI
    from zscaler.zpa.pra_portal import PRAPortalAPI
    from zscaler.zpa.provisioning import ProvisioningKeyAPI
    from zscaler.zpa.segment_groups import SegmentGroupsAPI
    from zscaler.zpa.server_groups import ServerGroupsAPI
    from zscaler.zpa.service_edges import ServiceEdgeControllerAPI
    from zscaler.zpa.service_edge_group import ServiceEdgeGroupAPI
    from zscaler.zpa.service_edge_schedule import ServiceEdgeScheduleAPI
    from zscaler.zpa.saml_attributes import SAMLAttributesAPI
    from zscaler.zpa.scim_groups import SCIMGroupsAPI
    from zscaler.zpa.scim_attributes import ScimAttributeHeaderAPI
    from zscaler.zpa.trusted_networks import TrustedNetworksAPI
    from zscaler.zpa.role_controller import RoleControllerAPI
    from zscaler.zpa.administrator_controller import AdministratorControllerAPI
    from zscaler.zpa.admin_sso_controller import AdminSSOControllerAPI
    from zscaler.zpa.client_settings import ClientSettingsAPI
    from zscaler.zpa.c2c_ip_ranges import IPRangesAPI
    from zscaler.zpa.api_keys import ApiKeysAPI
    from zscaler.zpa.customer_domain import CustomerDomainControllerAPI
    from zscaler.zpa.private_cloud_group import PrivateCloudGroupAPI
    from zscaler.zpa.private_cloud_controller import PrivateCloudControllerAPI
    from zscaler.zpa.user_portal_controller import UserPortalControllerAPI
    from zscaler.zpa.user_portal_link import UserPortalLinkAPI
    from zscaler.zpa.npn_client_controller import NPNClientControllerAPI
    from zscaler.zpa.config_override_controller import ConfigOverrideControllerAPI
    from zscaler.zpa.branch_connector_group import BranchConnectorGroupAPI
    from zscaler.zpa.branch_connectors import BranchConnectorControllerAPI
    from zscaler.zpa.browser_protection import BrowserProtectionProfileAPI
    from zscaler.zpa.zia_customer_config import ZIACustomerConfigAPI
    from zscaler.zpa.customer_dr_tool import CustomerDRToolVersionAPI
    from zscaler.zpa.extranet_resource import ExtranetResourceAPI
    from zscaler.zpa.cloud_connector_controller import CloudConnectorControllerAPI
    from zscaler.zpa.managed_browser_profile import ManagedBrowserProfileAPI
    from zscaler.zpa.oauth2_user_code import OAuth2UserCodeAPI
    from zscaler.zpa.stepup_auth_level import StepUpAuthLevelAPI
    from zscaler.zpa.user_portal_aup import UserPortalAUPAPI
    from zscaler.zpa.location_controller import LocationControllerAPI
    from zscaler.zpa.workload_tag_group import WorkloadTagGroupAPI

setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class LegacyZPAClientHelper:
    """A Controller to access Endpoints in the Zscaler Private Access (ZPA) API.

    The ZPA object stores the session token and simplifies access to API interfaces within ZPA.

    Attributes:
        client_id (str): The ZPA API client ID generated from the ZPA console.
        client_secret (str): The ZPA API client secret generated from the ZPA console.
        customer_id (str): The ZPA tenant ID found in the Administration > Company menu in the ZPA console.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``production``
            * ``beta``
            * ``gov``
            * ``govus``
            * ``zpatwo``
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        customer_id: str,
        cloud: str,
        microtenant_id: Optional[str] = None,
        partner_id: Optional[str] = None,
        timeout: int = 240,
        cache: Optional[Cache] = None,
        fail_safe: bool = False,
        request_executor_impl: Optional[Type] = None,
    ) -> None:
        from zscaler.request_executor import RequestExecutor

        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            get_limit=20,  # Allow 20 GET requests per 10 seconds
            post_put_delete_limit=10,  # Allow 10 POST/PUT/DELETE requests per 10 seconds
            get_freq=10,  # Adjust GET frequency
            post_put_delete_freq=10,  # Adjust POST/PUT/DELETE frequency
        )

        if cloud not in ZPA_BASE_URLS:
            valid_clouds = ", ".join(ZPA_BASE_URLS.keys())
            raise ValueError(
                f"The provided ZPA_CLOUD value '{cloud}' is not supported. "
                f"Please use one of the following supported values: {valid_clouds}"
            )

        self.baseurl = ZPA_BASE_URLS.get(cloud, ZPA_BASE_URLS["PRODUCTION"])
        self.timeout = timeout
        self.client_id = client_id
        self.client_secret = client_secret
        self.customer_id = customer_id
        self.cloud = cloud
        self.microtenant_id = microtenant_id or os.getenv("ZPA_MICROTENANT_ID")
        self.partner_id = partner_id or os.getenv("ZSCALER_PARTNER_ID")
        self.fail_safe = fail_safe

        cache_enabled = os.environ.get("ZSCALER_CLIENT_CACHE_ENABLED", "true").lower() == "true"
        self.cache = NoOpCache()
        if cache is None and cache_enabled:
            ttl = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTL", 3600))
            tti = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTI", 1800))
            self.cache = ZscalerCache(ttl=ttl, tti=tti)
        elif isinstance(cache, Cache):
            self.cache = cache

        # Create request executor
        self.config = {
            "client": {
                "customerId": self.customer_id,
                "microtenantId": self.microtenant_id or "",
                "partnerId": self.partner_id or "",
                "cloud": self.cloud,
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": 3},
                "cache": {
                    "enabled": cache_enabled,
                },
            }
        }
        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, zpa_legacy_client=self)

        ua = UserAgent()
        self.user_agent = ua.get_user_agent_string()
        self.access_token = None
        self.headers = {}
        self.refreshToken()

    def refreshToken(self) -> None:
        if not self.access_token or is_token_expired(self.access_token):
            response = self.login()
            if response is None or response.status_code > 299 or not response.json():
                logger.error("Failed to login using provided credentials, response: %s", response)
                raise Exception("Failed to login using provided credentials.")
            self.access_token = response.json().get("access_token")
            self.headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": self.user_agent,
            }
            # Add x-partner-id header if partnerId is provided
            if self.partner_id:
                self.headers["x-partner-id"] = self.partner_id

    def login(self) -> Optional[requests.Response]:
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        try:
            url = f"{self.baseurl}/signin"
            if self.cloud == "DEV":
                url = DEV_AUTH_URL + "?grant_type=CLIENT_CREDENTIALS"
            data = urllib.parse.urlencode(params)

            resp = requests.post(url, data=data, headers=headers, timeout=self.timeout)

            logger.info("Login attempt with status: %d", resp.status_code)
            # centralized error parsing
            _, err = check_response_for_error(url, resp, resp.text)
            if err:
                raise err

            logger.info("Login attempt with status: %d", resp.status_code)
            return resp
        except Exception as e:
            logger.error("Login failed due to an exception: %s", str(e))
            return None

    def get_base_url(self, endpoint: str) -> str:
        return self.baseurl

    def send(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Sends a request using the legacy client.

        Args:
            method (str): The HTTP method (GET, POST, PUT, DELETE).
            path (str): The API path.
            json (dict): Request payload.
            params (dict): URL query parameters.

        Returns:
            Tuple[requests.Response, dict]: Response object and request details.
        """
        try:
            base_url = f"{self.baseurl}{path}"

            headers = self.headers.copy()
            headers.update(self.request_executor.get_custom_headers())
            if not headers.get("Authorization"):
                self.refreshToken()
                # Re-copy headers after refreshToken() to include x-partner-id if it was added
                headers = self.headers.copy()
                headers.update(self.request_executor.get_custom_headers())
                headers["Authorization"] = f"Bearer {self.access_token}"

            response = requests.request(
                method=method,
                url=base_url,
                headers=headers,
                json=json,
                params=params,
                timeout=self.timeout,
            )

            _, err = check_response_for_error(base_url, response, response.text)
            if err:
                raise err

            logger.info("Legacy client request executed successfully. "
                        "Status: %d, URL: %s", response.status_code, base_url)

            return response, {
                "method": method,
                "url": base_url,
                "params": params or {},
                "headers": headers,
                "json": json or {},
            }

        except requests.RequestException as error:
            logger.error(f"Error sending request: {error}")
            raise ValueError(f"Request execution failed: {error}")

    def set_session(self, session: Any) -> None:
        """Dummy method for compatibility with the request executor."""
        self._session = session

    @property
    def customer_controller(self) -> CustomerControllerAPI:
        """
        The interface object for the :ref:`ZPA Auth Domains interface <zpa-customer_controller>`.

        """
        from zscaler.zpa.customer_controller import CustomerControllerAPI

        return CustomerControllerAPI(self.request_executor, self.config)

    @property
    def servers(self) -> AppServersAPI:
        """
        The interface object for the :ref:`ZPA Application Servers interface <zpa-app_servers>`.

        """
        from zscaler.zpa.servers import AppServersAPI

        return AppServersAPI(self.request_executor, self.config)

    @property
    def app_segment_by_type(self) -> ApplicationSegmentByTypeAPI:
        """
        The interface object for the :ref:`ZPA Application Segments By Type interface <zpa-app_segment_by_type>`.

        """
        from zscaler.zpa.app_segment_by_type import ApplicationSegmentByTypeAPI

        return ApplicationSegmentByTypeAPI(self.request_executor, self.config)

    @property
    def application_segment(self) -> ApplicationSegmentAPI:
        """
        The interface object for the :ref:`ZPA Application Segments interface <zpa-application_segment>`.

        """
        from zscaler.zpa.application_segment import ApplicationSegmentAPI

        return ApplicationSegmentAPI(self.request_executor, self.config)

    @property
    def app_segments_ba(self) -> ApplicationSegmentBAAPI:
        """
        The interface object for the :ref:`ZPA Application Segments BA interface <zpa-app_segments_ba>`.

        """
        from zscaler.zpa.app_segments_ba import ApplicationSegmentBAAPI

        return ApplicationSegmentBAAPI(self.request_executor, self.config)

    @property
    def app_segments_ba_v2(self) -> AppSegmentsBAV2API:
        """
        The interface object for the :ref:`ZPA Application Segments BA V2 interface <zpa-app_segments_ba_v2>`.

        """
        from zscaler.zpa.app_segments_ba_v2 import AppSegmentsBAV2API

        return AppSegmentsBAV2API(self.request_executor, self.config)

    @property
    def app_segments_pra(self) -> AppSegmentsPRAAPI:
        """
        The interface object for the :ref:`ZPA Application Segments PRA interface <zpa-app_segments_pra>`.

        """
        from zscaler.zpa.app_segments_pra import AppSegmentsPRAAPI

        return AppSegmentsPRAAPI(self.request_executor, self.config)

    @property
    def app_segments_inspection(self) -> AppSegmentsInspectionAPI:
        """
        The interface object for the :ref:`ZPA Application Segments PRA interface <zpa-app_segments_inspection>`.

        """
        from zscaler.zpa.app_segments_inspection import AppSegmentsInspectionAPI

        return AppSegmentsInspectionAPI(self.request_executor, self.config)

    @property
    def app_connector_groups(self) -> AppConnectorGroupAPI:
        """
        The interface object for the :ref:`ZPA App Connector Groups interface <zpa-app_connector_groups>`.

        """
        from zscaler.zpa.app_connector_groups import AppConnectorGroupAPI

        return AppConnectorGroupAPI(self.request_executor, self.config)

    @property
    def app_connector_schedule(self) -> AppConnectorScheduleAPI:
        """
        The interface object for the :ref:`ZPA App Connector Groups interface <zpa-app_connector_schedule>`.

        """
        from zscaler.zpa.app_connector_schedule import AppConnectorScheduleAPI

        return AppConnectorScheduleAPI(self.request_executor, self.config)

    @property
    def connectors(self) -> AppConnectorControllerAPI:
        """
        The interface object for the :ref:`ZPA Connectors interface <zpa-connectors>`.

        """
        from zscaler.zpa.app_connectors import AppConnectorControllerAPI

        return AppConnectorControllerAPI(self.request_executor, self.config)

    @property
    def cbi_banner(self) -> CBIBannerAPI:
        """
        The interface object for the :ref:`ZPA Cloud Browser Isolation Banner interface <zpa-cbi_banner>`.

        """
        from zscaler.zpa.cbi_banner import CBIBannerAPI

        return CBIBannerAPI(self.request_executor, self.config)

    @property
    def cbi_certificate(self) -> CBICertificateAPI:
        """
        The interface object for the :ref:`ZPA Cloud Browser Isolation Certificate interface <zpa-cbi_certificate>`.

        """
        from zscaler.zpa.cbi_certificate import CBICertificateAPI

        return CBICertificateAPI(self.request_executor, self.config)

    @property
    def cbi_profile(self) -> CBIProfileAPI:
        """
        The interface object for the :ref:`ZPA Cloud Browser Isolation Profile interface <zpa-cbi_profile>`.

        """
        from zscaler.zpa.cbi_profile import CBIProfileAPI

        return CBIProfileAPI(self.request_executor, self.config)

    @property
    def cbi_region(self) -> CBIRegionAPI:
        """
        The interface object for the :ref:`ZPA Cloud Browser Isolation Region interface <zpa-cbi_region>`.

        """
        from zscaler.zpa.cbi_region import CBIRegionAPI

        return CBIRegionAPI(self.request_executor, self.config)

    @property
    def cbi_zpa_profile(self) -> CBIZPAProfileAPI:
        """
        The interface object for the :ref:`ZPA Cloud Browser Isolation ZPA Profile interface <zpa-cbi_zpa_profile>`.

        """
        from zscaler.zpa.cbi_zpa_profile import CBIZPAProfileAPI

        return CBIZPAProfileAPI(self.request_executor, self.config)

    @property
    def certificates(self) -> CertificatesAPI:
        """
        The interface object for the :ref:`ZPA Browser Access Certificates interface <zpa-certificates>`.

        """
        from zscaler.zpa.certificates import CertificatesAPI

        return CertificatesAPI(self.request_executor, self.config)

    @property
    def cloud_connector_groups(self) -> CloudConnectorGroupsAPI:
        """
        The interface object for the :ref:`ZPA Cloud Connector Groups interface <zpa-cloud_connector_groups>`.

        """
        from zscaler.zpa.cloud_connector_groups import CloudConnectorGroupsAPI

        return CloudConnectorGroupsAPI(self.request_executor, self.config)

    @property
    def customer_version_profile(self) -> CustomerVersionProfileAPI:
        """
        The interface object for the :ref:`ZPA Customer Version profile interface <zpa-customer_version_profile>`.

        """
        from zscaler.zpa.customer_version_profile import CustomerVersionProfileAPI

        return CustomerVersionProfileAPI(self.request_executor, self.config)

    @property
    def emergency_access(self) -> EmergencyAccessAPI:
        """
        The interface object for the :ref:`ZPA Emergency Access interface <zpa-emergency_access>`.

        """
        from zscaler.zpa.emergency_access import EmergencyAccessAPI

        return EmergencyAccessAPI(self.request_executor, self.config)

    @property
    def enrollment_certificates(self) -> EnrollmentCertificateAPI:
        """
        The interface object for the :ref:`ZPA Enrollment Certificate interface <zpa-enrollment_certificates>`.

        """
        from zscaler.zpa.enrollment_certificates import EnrollmentCertificateAPI

        return EnrollmentCertificateAPI(self.request_executor, self.config)

    @property
    def idp(self) -> IDPControllerAPI:
        """
        The interface object for the :ref:`ZPA IDP interface <zpa-idp>`.

        """
        from zscaler.zpa.idp import IDPControllerAPI

        return IDPControllerAPI(self.request_executor, self.config)

    @property
    def app_protection(self) -> InspectionControllerAPI:
        """
        The interface object for the :ref:`ZPA Inspection interface <zpa-app_protection>`.

        """
        from zscaler.zpa.app_protection import InspectionControllerAPI

        return InspectionControllerAPI(self.request_executor, self.config)

    @property
    def lss(self) -> LSSConfigControllerAPI:
        """
        The interface object for the :ref:`ZIA Log Streaming Service Config interface <zpa-lss>`.

        """
        from zscaler.zpa.lss import LSSConfigControllerAPI

        return LSSConfigControllerAPI(self.request_executor, self.config)

    @property
    def machine_groups(self) -> MachineGroupsAPI:
        """
        The interface object for the :ref:`ZPA Machine Groups interface <zpa-machine_groups>`.

        """
        from zscaler.zpa.machine_groups import MachineGroupsAPI

        return MachineGroupsAPI(self.request_executor, self.config)

    @property
    def microtenants(self) -> MicrotenantsAPI:
        """
        The interface object for the :ref:`ZPA Microtenants interface <zpa-microtenants>`.

        """
        from zscaler.zpa.microtenants import MicrotenantsAPI

        return MicrotenantsAPI(self.request_executor, self.config)

    @property
    def policies(self) -> PolicySetControllerAPI:
        """
        The interface object for the :ref:`ZPA Policy Sets interface <zpa-policies>`.

        """
        from zscaler.zpa.policies import PolicySetControllerAPI

        return PolicySetControllerAPI(self.request_executor, self.config)

    @property
    def posture_profiles(self) -> PostureProfilesAPI:
        """
        The interface object for the :ref:`ZPA Posture Profiles interface <zpa-posture_profiles>`.

        """
        from zscaler.zpa.posture_profiles import PostureProfilesAPI

        return PostureProfilesAPI(self.request_executor, self.config)

    @property
    def pra_approval(self) -> PRAApprovalAPI:
        """
        The interface object for the :ref:`ZPA Privileged Remote Access Approval interface <zpa-pra_approval>`.

        """
        from zscaler.zpa.pra_approval import PRAApprovalAPI

        return PRAApprovalAPI(self.request_executor, self.config)

    @property
    def pra_console(self) -> PRAConsoleAPI:
        """
        The interface object for the :ref:`ZPA Privileged Remote Access Console interface <zpa-pra_console>`.

        """
        from zscaler.zpa.pra_console import PRAConsoleAPI

        return PRAConsoleAPI(self.request_executor, self.config)

    @property
    def pra_credential(self) -> PRACredentialAPI:
        """
        The interface object for the :ref:`ZPA Privileged Remote Access Credential interface <zpa-pra_credential>`.

        """
        from zscaler.zpa.pra_credential import PRACredentialAPI

        return PRACredentialAPI(self.request_executor, self.config)

    @property
    def pra_credential_pool(self) -> PRACredentialPoolAPI:
        """
        The interface object for the :ref:`ZPA Privileged Remote Access Credential pool interface <zpa-pra_credential_pool>`.

        """
        from zscaler.zpa.pra_credential_pool import PRACredentialPoolAPI

        return PRACredentialPoolAPI(self.request_executor, self.config)

    @property
    def pra_portal(self) -> PRAPortalAPI:
        """
        The interface object for the :ref:`ZPA Privileged Remote Access Portal interface <zpa-pra_portal>`.

        """
        from zscaler.zpa.pra_portal import PRAPortalAPI

        return PRAPortalAPI(self.request_executor, self.config)

    @property
    def provisioning(self) -> ProvisioningKeyAPI:
        """
        The interface object for the :ref:`ZPA Provisioning interface <zpa-provisioning>`.

        """
        from zscaler.zpa.provisioning import ProvisioningKeyAPI

        return ProvisioningKeyAPI(self.request_executor, self.config)

    @property
    def saml_attributes(self) -> SAMLAttributesAPI:
        """
        The interface object for the :ref:`ZPA SAML Attributes interface <zpa-saml_attributes>`.

        """
        from zscaler.zpa.saml_attributes import SAMLAttributesAPI

        return SAMLAttributesAPI(self.request_executor, self.config)

    @property
    def scim_attributes(self) -> ScimAttributeHeaderAPI:
        """
        The interface object for the :ref:`ZPA SCIM Attributes interface <zpa-scim_attributes>`.

        """
        from zscaler.zpa.scim_attributes import ScimAttributeHeaderAPI

        return ScimAttributeHeaderAPI(self.request_executor, self.config)

    @property
    def scim_groups(self) -> SCIMGroupsAPI:
        """
        The interface object for the :ref:`ZPA SCIM Groups interface <zpa-scim_groups>`.

        """
        from zscaler.zpa.scim_groups import SCIMGroupsAPI

        return SCIMGroupsAPI(self.request_executor, self.config)

    @property
    def segment_groups(self) -> SegmentGroupsAPI:
        """
        The interface object for the :ref:`ZPA Segment Groups interface <zpa-segment_groups>`.

        """
        from zscaler.zpa.segment_groups import SegmentGroupsAPI

        return SegmentGroupsAPI(self.request_executor, self.config)

    @property
    def server_groups(self) -> ServerGroupsAPI:
        """
        The interface object for the :ref:`ZPA Server Groups interface <zpa-server_groups>`.

        """
        from zscaler.zpa.server_groups import ServerGroupsAPI

        return ServerGroupsAPI(self.request_executor, self.config)

    @property
    def service_edges(self) -> ServiceEdgeControllerAPI:
        """
        The interface object for the :ref:`ZPA Service Edges interface <zpa-service_edges>`.

        """
        from zscaler.zpa.service_edges import ServiceEdgeControllerAPI

        return ServiceEdgeControllerAPI(self.request_executor, self.config)

    @property
    def service_edge_group(self) -> ServiceEdgeGroupAPI:
        """
        The interface object for the :ref:`ZPA Service Edge Groups interface <zpa-service_edge_group>`.

        """
        from zscaler.zpa.service_edge_group import ServiceEdgeGroupAPI

        return ServiceEdgeGroupAPI(self.request_executor, self.config)

    @property
    def service_edge_schedule(self) -> ServiceEdgeScheduleAPI:
        """
        The interface object for the :ref:`ZPA Service Edge Groups interface <zpa-service_edge_schedule>`.

        """
        from zscaler.zpa.service_edge_schedule import ServiceEdgeScheduleAPI

        return ServiceEdgeScheduleAPI(self.request_executor, self.config)

    @property
    def trusted_networks(self) -> TrustedNetworksAPI:
        """
        The interface object for the :ref:`ZPA Trusted Networks interface <zpa-trusted_networks>`.

        """
        from zscaler.zpa.trusted_networks import TrustedNetworksAPI

        return TrustedNetworksAPI(self.request_executor, self.config)

    @property
    def administrator_controller(self) -> AdministratorControllerAPI:
        """
        The interface object for the :ref:`ZPA Administrator Controller interface <zpa-administrator_controller>`.

        """
        from zscaler.zpa.administrator_controller import AdministratorControllerAPI

        return AdministratorControllerAPI(self.request_executor, self.config)

    @property
    def admin_sso_controller(self) -> AdminSSOControllerAPI:
        """
        The interface object for the :ref:`ZPA Admin SSL Login Controller interface <zpa-admin_sso_controller>`.

        """
        from zscaler.zpa.admin_sso_controller import AdminSSOControllerAPI

        return AdminSSOControllerAPI(self.request_executor, self.config)

    @property
    def role_controller(self) -> RoleControllerAPI:
        """
        The interface object for the :ref:`ZPA Role Controller interface <zpa-role_controller>`.

        """
        from zscaler.zpa.role_controller import RoleControllerAPI

        return RoleControllerAPI(self.request_executor, self.config)

    @property
    def client_settings(self) -> ClientSettingsAPI:
        """
        The interface object for the :ref:`ZPA Client Setting interface <zpa-client_settings>`.

        """
        from zscaler.zpa.client_settings import ClientSettingsAPI

        return ClientSettingsAPI(self.request_executor, self.config)

    @property
    def c2c_ip_ranges(self) -> IPRangesAPI:
        """
        The interface object for the :ref:`ZPA C2C IP Range Controller interface <zpa-c2c_ip_ranges>`.

        """
        from zscaler.zpa.c2c_ip_ranges import IPRangesAPI

        return IPRangesAPI(self.request_executor, self.config)

    @property
    def api_keys(self) -> ApiKeysAPI:
        """
        The interface object for the :ref:`ZPA API Key Controller interface <zpa-api_keys>`.

        """
        from zscaler.zpa.api_keys import ApiKeysAPI

        return ApiKeysAPI(self.request_executor, self.config)

    @property
    def customer_domain(self) -> CustomerDomainControllerAPI:
        """
        The interface object for the :ref:`ZPA Customer Domain Controller interface <zpa-customer_domain>`.

        """
        from zscaler.zpa.customer_domain import CustomerDomainControllerAPI

        return CustomerDomainControllerAPI(self.request_executor, self.config)

    @property
    def private_cloud_group(self) -> PrivateCloudGroupAPI:
        """
        The interface object for the :ref:`ZPA Private Cloud Controller Group interface <zpa-private_cloud_group>`.

        """
        from zscaler.zpa.private_cloud_group import PrivateCloudGroupAPI

        return PrivateCloudGroupAPI(self.request_executor, self.config)

    @property
    def private_cloud_controller(self) -> PrivateCloudControllerAPI:
        """
        The interface object for the :ref:`ZPA Private Cloud Controller interface <zpa-private_cloud_controller>`.

        """
        from zscaler.zpa.private_cloud_controller import PrivateCloudControllerAPI

        return PrivateCloudControllerAPI(self.request_executor, self.config)

    @property
    def user_portal_controller(self) -> UserPortalControllerAPI:
        """
        The interface object for the :ref:`ZPA User Portal Controller interface <zpa-user_portal_controller>`.

        """

        from zscaler.zpa.user_portal_controller import UserPortalControllerAPI

        return UserPortalControllerAPI(self.request_executor, self.config)

    @property
    def user_portal_link(self) -> UserPortalLinkAPI:
        """
        The interface object for the :ref:`ZPA User Portal Link interface <zpa-user_portal_link>`.

        """

        from zscaler.zpa.user_portal_link import UserPortalLinkAPI

        return UserPortalLinkAPI(self.request_executor, self.config)

    @property
    def npn_client_controller(self) -> NPNClientControllerAPI:
        """
        The interface object for the :ref:`ZPA VPN Connected Users interface <zpa-npn_client_controller>`.

        """

        from zscaler.zpa.npn_client_controller import NPNClientControllerAPI

        return NPNClientControllerAPI(self.request_executor, self.config)

    @property
    def config_override_controller(self) -> ConfigOverrideControllerAPI:
        """
        The interface object for the :ref:`ZPA Config Override interface <zpa-config_override_controller>`.

        """

        from zscaler.zpa.config_override_controller import ConfigOverrideControllerAPI

        return ConfigOverrideControllerAPI(self.request_executor, self.config)

    @property
    def branch_connector_group(self) -> BranchConnectorGroupAPI:
        """
        The interface object for the :ref:`ZPA Branch Connector Group interface <zpa-branch-connector-group>`.

        """

        from zscaler.zpa.branch_connector_group import BranchConnectorGroupAPI

        return BranchConnectorGroupAPI(self.request_executor, self.config)

    @property
    def branch_connectors(self) -> BranchConnectorControllerAPI:
        """
        The interface object for the :ref:`ZPA Branch Connectors interface <zpa-branch-connectors>`.

        """

        from zscaler.zpa.branch_connectors import BranchConnectorControllerAPI

        return BranchConnectorControllerAPI(self.request_executor, self.config)

    @property
    def browser_protection(self) -> BrowserProtectionProfileAPI:
        """
        The interface object for the :ref:`ZPA Browser Protection Profile interface <zpa-browser-protection>`.

        """

        from zscaler.zpa.browser_protection import BrowserProtectionProfileAPI

        return BrowserProtectionProfileAPI(self.request_executor, self.config)

    @property
    def zia_customer_config(self) -> ZIACustomerConfigAPI:
        """
        The interface object for the :ref:`ZIA Customer Config interface <zpa-zia-customer-config>`.

        """

        from zscaler.zpa.zia_customer_config import ZIACustomerConfigAPI

        return ZIACustomerConfigAPI(self.request_executor, self.config)

    @property
    def customer_dr_tool(self) -> CustomerDRToolVersionAPI:
        """
        The interface object for the :ref:`ZPA Customer DR Tool Version interface <zpa-customer-dr-tool>`.

        """

        from zscaler.zpa.customer_dr_tool import CustomerDRToolVersionAPI

        return CustomerDRToolVersionAPI(self.request_executor, self.config)

    @property
    def extranet_resource(self) -> ExtranetResourceAPI:
        """
        The interface object for the :ref:`ZPA Extranet Resource interface <zpa-extranet_resource>`.

        """
        from zscaler.zpa.extranet_resource import ExtranetResourceAPI

        return ExtranetResourceAPI(self.request_executor, self.config)

    @property
    def cloud_connector_controller(self) -> CloudConnectorControllerAPI:
        """
        The interface object for the :ref:`ZPA Cloud Connector Controller interface <zpa-cloud_connector_controller>`.

        """
        from zscaler.zpa.cloud_connector_controller import CloudConnectorControllerAPI

        return CloudConnectorControllerAPI(self.request_executor, self.config)

    @property
    def managed_browser_profile(self) -> ManagedBrowserProfileAPI:
        """
        The interface object for the :ref:`ZPA Managed Browser Profile interface <zpa-managed_browser_profile>`.

        """
        from zscaler.zpa.managed_browser_profile import ManagedBrowserProfileAPI

        return ManagedBrowserProfileAPI(self.request_executor, self.config)

    @property
    def oauth2_user_code(self) -> OAuth2UserCodeAPI:
        """
        The interface object for the :ref:`ZPA OAuth2 User Code interface <zpa-oauth2_user_code>`.

        """
        from zscaler.zpa.oauth2_user_code import OAuth2UserCodeAPI

        return OAuth2UserCodeAPI(self.request_executor, self.config)

    @property
    def stepup_auth_level(self) -> StepUpAuthLevelAPI:
        """
        The interface object for the :ref:`ZPA Step Up Auth Level interface <zpa-stepup_auth_level>`.

        """
        from zscaler.zpa.stepup_auth_level import StepUpAuthLevelAPI

        return StepUpAuthLevelAPI(self.request_executor, self.config)

    @property
    def user_portal_aup(self) -> UserPortalAUPAPI:
        """
        The interface object for the :ref:`ZPA User Portal AUP interface <zpa-user_portal_aup>`.

        """
        from zscaler.zpa.user_portal_aup import UserPortalAUPAPI

        return UserPortalAUPAPI(self.request_executor, self.config)

    @property
    def location_controller(self) -> LocationControllerAPI:
        """
        The interface object for the :ref:`ZPA Location Controller interface <zpa-location_controller>`.

        """
        from zscaler.zpa.location_controller import LocationControllerAPI

        return LocationControllerAPI(self.request_executor, self.config)

    @property
    def workload_tag_group(self) -> WorkloadTagGroupAPI:
        """
        The interface object for the :ref:`ZPA Workload Tag Group interface <zpa-workload_tag_group>`.

        """
        from zscaler.zpa.workload_tag_group import WorkloadTagGroupAPI

        return WorkloadTagGroupAPI(self.request_executor, self.config)

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
