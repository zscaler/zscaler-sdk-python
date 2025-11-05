# This file shows the complete ZPA Service with ALL type hints added
# Copy this to replace zscaler/zpa/zpa_service.py

from typing import Dict, Any
from zscaler.request_executor import RequestExecutor
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


class ZPAService:
    """ZPA Service client, exposing various ZPA APIs."""

    def __init__(self, request_executor: RequestExecutor, config: Dict[str, Any]) -> None:
        self._request_executor: RequestExecutor = request_executor
        self._config: Dict[str, Any] = config

    @property
    def customer_controller(self) -> CustomerControllerAPI:
        """The interface object for the :ref:`ZPA Auth Domains interface <zpa-customer_controller>`."""
        return CustomerControllerAPI(self._request_executor, self._config)

    @property
    def app_segment_by_type(self) -> ApplicationSegmentByTypeAPI:
        """The interface object for the :ref:`ZPA Application Segments By Type interface <zpa-app_segment_by_type>`."""
        return ApplicationSegmentByTypeAPI(self._request_executor, self._config)

    @property
    def application_segment(self) -> ApplicationSegmentAPI:
        """The interface object for the :ref:`ZPA Application Segments interface <zpa-application_segment>`."""
        return ApplicationSegmentAPI(self._request_executor, self._config)

    @property
    def app_segments_ba(self) -> ApplicationSegmentBAAPI:
        """The interface object for the :ref:`ZPA Application Segments BA interface <zpa-app_segments_ba>`."""
        return ApplicationSegmentBAAPI(self._request_executor, self._config)

    @property
    def app_segments_ba_v2(self) -> AppSegmentsBAV2API:
        """The interface object for the :ref:`ZPA Application Segments BA V2 interface <zpa-app_segments_ba_v2>`."""
        return AppSegmentsBAV2API(self._request_executor, self._config)

    @property
    def app_segments_pra(self) -> AppSegmentsPRAAPI:
        """The interface object for the :ref:`ZPA Application Segments PRA interface <zpa-app_segments_pra>`."""
        return AppSegmentsPRAAPI(self._request_executor, self._config)

    @property
    def app_segments_inspection(self) -> AppSegmentsInspectionAPI:
        """The interface object for the :ref:`ZPA Application Segments PRA interface <zpa-app_segments_inspection>`."""
        return AppSegmentsInspectionAPI(self._request_executor, self._config)

    @property
    def cbi_banner(self) -> CBIBannerAPI:
        """The interface object for the :ref:`ZPA Cloud Browser Isolation Banner interface <zpa-cbi_banner>`."""
        return CBIBannerAPI(self._request_executor, self._config)

    @property
    def cbi_certificate(self) -> CBICertificateAPI:
        """The interface object for the :ref:`ZPA Cloud Browser Isolation Certificate interface <zpa-cbi_certificate>`."""
        return CBICertificateAPI(self._request_executor, self._config)

    @property
    def cbi_profile(self) -> CBIProfileAPI:
        """The interface object for the :ref:`ZPA Cloud Browser Isolation Profile interface <zpa-cbi_profile>`."""
        return CBIProfileAPI(self._request_executor, self._config)

    @property
    def cbi_region(self) -> CBIRegionAPI:
        """The interface object for the :ref:`ZPA Cloud Browser Isolation Region interface <zpa-cbi_region>`."""
        return CBIRegionAPI(self._request_executor, self._config)

    @property
    def cbi_zpa_profile(self) -> CBIZPAProfileAPI:
        """The interface object for the :ref:`ZPA Cloud Browser Isolation ZPA Profile interface <zpa-cbi_zpa_profile>`."""
        return CBIZPAProfileAPI(self._request_executor, self._config)

    @property
    def certificates(self) -> CertificatesAPI:
        """The interface object for the :ref:`ZPA Browser Access Certificates interface <zpa-certificates>`."""
        return CertificatesAPI(self._request_executor, self._config)

    @property
    def customer_version_profile(self) -> CustomerVersionProfileAPI:
        """The interface object for the :ref:`ZPA Customer Version profile interface <zpa-customer_version_profile>`."""
        return CustomerVersionProfileAPI(self._request_executor, self._config)

    @property
    def cloud_connector_groups(self) -> CloudConnectorGroupsAPI:
        """The interface object for the :ref:`ZPA Cloud Connector Groups interface <zpa-cloud_connector_groups>`."""
        return CloudConnectorGroupsAPI(self._request_executor, self._config)

    @property
    def app_connector_groups(self) -> AppConnectorGroupAPI:
        """The interface object for the :ref:`ZPA App Connector Groups interface <zpa-app_connector_groups>`."""
        return AppConnectorGroupAPI(self._request_executor, self._config)

    @property
    def app_connectors(self) -> AppConnectorControllerAPI:
        """The interface object for the :ref:`ZPA Connectors interface <zpa-app_connectors>`."""
        return AppConnectorControllerAPI(self._request_executor, self._config)

    @property
    def app_connector_schedule(self) -> AppConnectorScheduleAPI:
        """The interface object for the :ref:`ZPA App Connector Groups interface <zpa-app_connector_schedule>`."""
        return AppConnectorScheduleAPI(self._request_executor, self._config)

    @property
    def emergency_access(self) -> EmergencyAccessAPI:
        """The interface object for the :ref:`ZPA Emergency Access interface <zpa-emergency_access>`."""
        return EmergencyAccessAPI(self._request_executor, self._config)

    @property
    def enrollment_certificates(self) -> EnrollmentCertificateAPI:
        """The interface object for the :ref:`ZPA Enrollment Certificate interface <zpa-enrollment_certificates>`."""
        return EnrollmentCertificateAPI(self._request_executor, self._config)

    @property
    def idp(self) -> IDPControllerAPI:
        """The interface object for the :ref:`ZPA IDP interface <zpa-idp>`."""
        return IDPControllerAPI(self._request_executor, self._config)

    @property
    def app_protection(self) -> InspectionControllerAPI:
        """The interface object for the :ref:`ZPA Inspection interface <zpa-app_protection>`."""
        return InspectionControllerAPI(self._request_executor, self._config)

    @property
    def lss(self) -> LSSConfigControllerAPI:
        """The interface object for the :ref:`ZIA Log Streaming Service Config interface <zpa-lss>`."""
        return LSSConfigControllerAPI(self._request_executor, self._config)

    @property
    def machine_groups(self) -> MachineGroupsAPI:
        """The interface object for the :ref:`ZPA Machine Groups interface <zpa-machine_groups>`."""
        return MachineGroupsAPI(self._request_executor, self._config)

    @property
    def microtenants(self) -> MicrotenantsAPI:
        """The interface object for the :ref:`ZPA Microtenants interface <zpa-microtenants>`."""
        return MicrotenantsAPI(self._request_executor, self._config)

    @property
    def policies(self) -> PolicySetControllerAPI:
        """The interface object for the :ref:`ZPA Policy Sets interface <zpa-policies>`."""
        return PolicySetControllerAPI(self._request_executor, self._config)

    @property
    def posture_profiles(self) -> PostureProfilesAPI:
        """The interface object for the :ref:`ZPA Posture Profiles interface <zpa-posture_profiles>`."""
        return PostureProfilesAPI(self._request_executor, self._config)

    @property
    def pra_approval(self) -> PRAApprovalAPI:
        """The interface object for the :ref:`ZPA Privileged Remote Access Approval interface <zpa-pra_approval>`."""
        return PRAApprovalAPI(self._request_executor, self._config)

    @property
    def pra_console(self) -> PRAConsoleAPI:
        """The interface object for the :ref:`ZPA Privileged Remote Access Console interface <zpa-pra_console>`."""
        return PRAConsoleAPI(self._request_executor, self._config)

    @property
    def pra_credential(self) -> PRACredentialAPI:
        """The interface object for the :ref:`ZPA Privileged Remote Access Credential interface <zpa-pra_credential>`."""
        return PRACredentialAPI(self._request_executor, self._config)

    @property
    def pra_credential_pool(self) -> PRACredentialPoolAPI:
        """
        The interface object for the :ref:`ZPA Privileged Remote Access Credential pool interface <zpa-pra_credential_pool>`.
        """
        return PRACredentialPoolAPI(self._request_executor, self._config)

    @property
    def pra_portal(self) -> PRAPortalAPI:
        """The interface object for the :ref:`ZPA Privileged Remote Access Portal interface <zpa-pra_portal>`."""
        return PRAPortalAPI(self._request_executor, self._config)

    @property
    def provisioning(self) -> ProvisioningKeyAPI:
        """The interface object for the :ref:`ZPA Provisioning interface <zpa-provisioning>`."""
        return ProvisioningKeyAPI(self._request_executor, self._config)

    @property
    def saml_attributes(self) -> SAMLAttributesAPI:
        """The interface object for the :ref:`ZPA SAML Attributes interface <zpa-saml_attributes>`."""
        return SAMLAttributesAPI(self._request_executor, self._config)

    @property
    def scim_attributes(self) -> ScimAttributeHeaderAPI:
        """The interface object for the :ref:`ZPA SCIM Attributes interface <zpa-scim_attributes>`."""
        return ScimAttributeHeaderAPI(self._request_executor, self._config)

    @property
    def scim_groups(self) -> SCIMGroupsAPI:
        """The interface object for the :ref:`ZPA SCIM Groups interface <zpa-scim_groups>`."""
        return SCIMGroupsAPI(self._request_executor, self._config)

    @property
    def segment_groups(self) -> SegmentGroupsAPI:
        """The interface object for the :ref:`ZPA Segment Groups interface <zpa-segment_groups>`."""
        return SegmentGroupsAPI(self._request_executor, self._config)

    @property
    def server_groups(self) -> ServerGroupsAPI:
        """The interface object for the :ref:`ZPA Server Groups interface <zpa-server_groups>`."""
        return ServerGroupsAPI(self._request_executor, self._config)

    @property
    def servers(self) -> AppServersAPI:
        """The interface object for the :ref:`ZPA Application Servers interface <zpa-app_servers>`."""
        return AppServersAPI(self._request_executor, self._config)

    @property
    def service_edges(self) -> ServiceEdgeControllerAPI:
        """The interface object for the :ref:`ZPA Service Edges interface <zpa-service_edges>`."""
        return ServiceEdgeControllerAPI(self._request_executor, self._config)

    @property
    def service_edge_group(self) -> ServiceEdgeGroupAPI:
        """The interface object for the :ref:`ZPA Service Edge Groups interface <zpa-service_edge_group>`."""
        return ServiceEdgeGroupAPI(self._request_executor, self._config)

    @property
    def service_edge_schedule(self) -> ServiceEdgeScheduleAPI:
        """The interface object for the :ref:`ZPA Service Edge Groups interface <zpa-service_edge_schedule>`."""
        return ServiceEdgeScheduleAPI(self._request_executor, self._config)

    @property
    def trusted_networks(self) -> TrustedNetworksAPI:
        """The interface object for the :ref:`ZPA Trusted Networks interface <zpa-trusted_networks>`."""
        return TrustedNetworksAPI(self._request_executor, self._config)

    @property
    def administrator_controller(self) -> AdministratorControllerAPI:
        """The interface object for the :ref:`ZPA Administrator Controller interface <zpa-administrator_controller>`."""
        return AdministratorControllerAPI(self._request_executor, self._config)

    @property
    def admin_sso_controller(self) -> AdminSSOControllerAPI:
        """The interface object for the :ref:`ZPA Admin SSL Login Controller interface <zpa-admin_sso_controller>`."""
        return AdminSSOControllerAPI(self._request_executor, self._config)

    @property
    def role_controller(self) -> RoleControllerAPI:
        """The interface object for the :ref:`ZPA Role Controller interface <zpa-role_controller>`."""
        return RoleControllerAPI(self._request_executor, self._config)

    @property
    def client_settings(self) -> ClientSettingsAPI:
        """The interface object for the :ref:`ZPA Client Setting interface <zpa-client_settings>`."""
        return ClientSettingsAPI(self._request_executor, self._config)

    @property
    def c2c_ip_ranges(self) -> IPRangesAPI:
        """The interface object for the :ref:`ZPA C2C IP Range Controller interface <zpa-c2c_ip_ranges>`."""
        return IPRangesAPI(self._request_executor, self._config)

    @property
    def api_keys(self) -> ApiKeysAPI:
        """The interface object for the :ref:`ZPA API Key Controller interface <zpa-api_keys>`."""
        return ApiKeysAPI(self._request_executor, self._config)

    @property
    def customer_domain(self) -> CustomerDomainControllerAPI:
        """The interface object for the :ref:`ZPA Customer Domain Controller interface <zpa-customer_domain>`."""
        return CustomerDomainControllerAPI(self._request_executor, self._config)

    @property
    def private_cloud_group(self) -> PrivateCloudGroupAPI:
        """The interface object for the :ref:`ZPA Private Cloud Controller Group interface <zpa-private_cloud_group>`."""
        return PrivateCloudGroupAPI(self._request_executor, self._config)

    @property
    def private_cloud_controller(self) -> PrivateCloudControllerAPI:
        """The interface object for the :ref:`ZPA Private Cloud Controller interface <zpa-private_cloud_controller>`."""
        return PrivateCloudControllerAPI(self._request_executor, self._config)

    @property
    def user_portal_controller(self) -> UserPortalControllerAPI:
        """The interface object for the :ref:`ZPA User Portal Controller interface <zpa-user_portal_controller>`."""
        return UserPortalControllerAPI(self._request_executor, self._config)

    @property
    def user_portal_link(self) -> UserPortalLinkAPI:
        """The interface object for the :ref:`ZPA User Portal Link interface <zpa-user_portal_link>`."""
        return UserPortalLinkAPI(self._request_executor, self._config)

    @property
    def npn_client_controller(self) -> NPNClientControllerAPI:
        """The interface object for the :ref:`ZPA VPN Connected Users interface <zpa-npn_client_controller>`."""
        return NPNClientControllerAPI(self._request_executor, self._config)

    @property
    def config_override_controller(self) -> ConfigOverrideControllerAPI:
        """The interface object for the :ref:`ZPA Config Override interface <zpa-config_override_controller>`."""
        return ConfigOverrideControllerAPI(self._request_executor, self._config)

    @property
    def branch_connector_group(self) -> BranchConnectorGroupAPI:
        """The interface object for the :ref:`ZPA Branch Connector Group interface <zpa-branch_connector_group>`."""
        return BranchConnectorGroupAPI(self._request_executor, self._config)

    @property
    def branch_connectors(self) -> BranchConnectorControllerAPI:
        """The interface object for the :ref:`ZPA Branch Connectors interface <zpa-branch_connectors>`."""
        return BranchConnectorControllerAPI(self._request_executor, self._config)

    @property
    def browser_protection(self) -> BrowserProtectionProfileAPI:
        """The interface object for the :ref:`ZPA Browser Protection Profile interface <zpa-browser-protection>`."""
        return BrowserProtectionProfileAPI(self._request_executor, self._config)

    @property
    def zia_customer_config(self) -> ZIACustomerConfigAPI:
        """The interface object for the :ref:`ZIA Customer Config interface <zpa-zia-customer-config>`."""
        return ZIACustomerConfigAPI(self._request_executor, self._config)

    @property
    def customer_dr_tool(self) -> CustomerDRToolVersionAPI:
        """The interface object for the :ref:`ZPA Customer DR Tool Version interface <zpa-customer-dr-tool>`."""
        return CustomerDRToolVersionAPI(self._request_executor, self._config)

    @property
    def extranet_resource(self) -> ExtranetResourceAPI:
        """The interface object for the :ref:`ZPA Extranet Resource interface <zpa-extranet_resource>`."""
        return ExtranetResourceAPI(self._request_executor, self._config)

    @property
    def cloud_connector_controller(self) -> CloudConnectorControllerAPI:
        """The interface object for the :ref:`ZPA Cloud Connector Controller interface <zpa-cloud_connector_controller>`."""
        return CloudConnectorControllerAPI(self._request_executor, self._config)

    @property
    def managed_browser_profile(self) -> ManagedBrowserProfileAPI:
        """The interface object for the :ref:`ZPA Managed Browser Profile interface <zpa-managed_browser_profile>`."""
        return ManagedBrowserProfileAPI(self._request_executor, self._config)

    @property
    def oauth2_user_code(self) -> OAuth2UserCodeAPI:
        """The interface object for the :ref:`ZPA OAuth2 User Code interface <zpa-oauth2_user_code>`."""
        return OAuth2UserCodeAPI(self._request_executor, self._config)

    @property
    def stepup_auth_level(self) -> StepUpAuthLevelAPI:
        """The interface object for the :ref:`ZPA Step Up Auth Level interface <zpa-stepup_auth_level>`."""
        return StepUpAuthLevelAPI(self._request_executor, self._config)

    @property
    def user_portal_aup(self) -> UserPortalAUPAPI:
        """The interface object for the :ref:`ZPA User Portal AUP interface <zpa-user_portal_aup>`."""
        return UserPortalAUPAPI(self._request_executor, self._config)

    @property
    def location_controller(self) -> LocationControllerAPI:
        """The interface object for the :ref:`ZPA Location Controller interface <zpa-location_controller>`."""
        return LocationControllerAPI(self._request_executor, self._config)

    @property
    def workload_tag_group(self) -> WorkloadTagGroupAPI:
        """The interface object for the :ref:`ZPA Workload Tag Group interface <zpa-workload_tag_group>`."""
        return WorkloadTagGroupAPI(self._request_executor, self._config)
