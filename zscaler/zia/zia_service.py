from zscaler.request_executor import RequestExecutor
from zscaler.zia.activate import ActivationAPI
from zscaler.zia.advanced_settings import AdvancedSettingsAPI
from zscaler.zia.atp_policy import ATPPolicyAPI
from zscaler.zia.admin_roles import AdminRolesAPI
from zscaler.zia.admin_users import AdminUsersAPI
from zscaler.zia.apptotal import AppTotalAPI
from zscaler.zia.audit_logs import AuditLogsAPI
from zscaler.zia.authentication_settings import AuthenticationSettingsAPI
from zscaler.zia.cloudappcontrol import CloudAppControlAPI
from zscaler.zia.cloud_applications import CloudApplicationsAPI
from zscaler.zia.cloud_nss import CloudNSSAPI
from zscaler.zia.isolation_profile import CBIProfileAPI
from zscaler.zia.sandbox import CloudSandboxAPI
from zscaler.zia.dlp_dictionary import DLPDictionaryAPI
from zscaler.zia.dlp_engine import DLPEngineAPI
from zscaler.zia.dlp_web_rules import DLPWebRuleAPI
from zscaler.zia.dlp_templates import DLPTemplates
from zscaler.zia.dlp_resources import DLPResourcesAPI
from zscaler.zia.device_management import DeviceManagementAPI
from zscaler.zia.endusernotification import EndUserNotificationAPI
from zscaler.zia.file_type_control_rule import FileTypeControlRuleAPI
from zscaler.zia.cloud_firewall_dns import FirewallDNSRulesAPI
from zscaler.zia.cloud_firewall_ips import FirewallIPSRulesAPI
from zscaler.zia.cloud_firewall_rules import FirewallPolicyAPI
from zscaler.zia.forwarding_control import ForwardingControlAPI
from zscaler.zia.malware_protection_policy import MalwareProtectionPolicyAPI
from zscaler.zia.locations import LocationsAPI
from zscaler.zia.organization_information import OrganizationInformationAPI
from zscaler.zia.pac_files import PacFilesAPI
from zscaler.zia.remoteassistance import RemoteAssistanceAPI
from zscaler.zia.rule_labels import RuleLabelsAPI
from zscaler.zia.sandbox_rules import SandboxRulesAPI
from zscaler.zia.security_policy_settings import SecurityPolicyAPI
from zscaler.zia.intermediate_certificates import IntermediateCertsAPI
from zscaler.zia.traffic_gre_tunnels import TrafficForwardingGRETunnelAPI
from zscaler.zia.traffic_vpn_credentials import TrafficVPNCredentialAPI
from zscaler.zia.traffic_static_ip import TrafficStaticIPAPI
from zscaler.zia.url_categories import URLCategoriesAPI
from zscaler.zia.url_filtering import URLFilteringAPI
from zscaler.zia.user_management import UserManagementAPI
from zscaler.zia.workload_groups import WorkloadGroupsAPI
from zscaler.zia.zpa_gateway import ZPAGatewayAPI


class ZIAService:
    """ZIA Service client, exposing various ZIA APIs."""

    def __init__(self, request_executor: RequestExecutor):
        # Ensure the service gets the request executor from the Client object
        self._request_executor = request_executor

    @property
    def activate(self):
        """
        The interface object for the :ref:`ZIA Activation interface <zia-activate>`.

        """
        return ActivationAPI(self)

    @property
    def admin_roles(self):
        """
        The interface object for the :ref:`ZIA Admin and Role Management interface <zia-admin_roles>`.

        """
        return AdminRolesAPI(self._request_executor)

    @property
    def admin_users(self):
        """
        The interface object for the :ref:`ZIA Admin Users interface <zia-admin_users>`.

        """
        return AdminUsersAPI(self._request_executor)

    @property
    def audit_logs(self):
        """
        The interface object for the :ref:`ZIA Admin Audit Logs interface <zia-audit_logs>`.

        """
        return AuditLogsAPI(self._request_executor)

    @property
    def apptotal(self):
        """
        The interface object for the :ref:`ZIA AppTotal interface <zia-apptotal>`.

        """
        return AppTotalAPI(self._request_executor)

    @property
    def advanced_settings(self):
        """
        The interface object for the :ref:`ZIA Advanced Settings interface <zia-advanced_settings>`.

        """
        return AdvancedSettingsAPI(self._request_executor)

    @property
    def atp_policy(self):
        """
        The interface object for the :ref:`ZIA Advanced Threat Protection Policy interface <zia-atp_policy>`.

        """
        return ATPPolicyAPI(self._request_executor)

    @property
    def authentication_settings(self):
        """
        The interface object for the :ref:`ZIA Authentication Security Settings interface <zia-authentication_settings>`.

        """
        return AuthenticationSettingsAPI(self._request_executor)

    @property
    def cloudappcontrol(self):
        """
        The interface object for the :ref:`ZIA Cloud App Control <zia-cloudappcontrol>`.

        """
        return CloudAppControlAPI(self._request_executor)

    @property
    def cloud_applications(self):
        """
        The interface object for the :ref:`ZIA Cloud App Control <zia-cloud_applications>`.

        """
        return CloudApplicationsAPI(self._request_executor)
    
    @property
    def cloud_nss(self):
        """
        The interface object for the :ref:`ZIA Cloud NSS interface <zia-cloud_nss>`.

        """
        return CloudNSSAPI(self._request_executor)

    @property
    def cloud_firewall_dns(self):
        """
        The interface object for the :ref:`ZIA Firewall DNS Policies interface <zia-cloud_firewall_dns>`.

        """
        return FirewallDNSRulesAPI(self._request_executor)
    
    @property
    def cloud_firewall_ips(self):
        """
        The interface object for the :ref:`ZIA Firewall IPS Policies interface <zia-cloud_firewall_ips>`.

        """
        return FirewallIPSRulesAPI(self._request_executor)

    @property
    def cloud_firewall_rules(self):
        """
        The interface object for the :ref:`ZIA Firewall Policies interface <zia-cloud_firewall_rules>`.

        """
        return FirewallPolicyAPI(self._request_executor)

    @property
    def dlp_dictionary(self):
        """
        The interface object for the :ref:`ZIA DLP Dictionaries interface <zia-dlp_dictionary>`.

        """
        return DLPDictionaryAPI(self._request_executor)

    @property
    def dlp_engine(self):
        """
        The interface object for the :ref:`ZIA DLP Engine interface <zia-dlp_engine>`.

        """
        return DLPEngineAPI(self._request_executor)

    @property
    def dlp_web_rules(self):
        """
        The interface object for the :ref:`ZIA DLP Web Rules interface <zia-dlp_web_rules>`.

        """
        return DLPWebRuleAPI(self._request_executor)

    @property
    def dlp_templates(self):
        """
        The interface object for the :ref:`ZIA DLP Templates interface <zia-dlp_templates>`.

        """
        return DLPTemplates(self._request_executor)

    @property
    def dlp_resources(self):
        """
        The interface object for the :ref:`ZIA DLP Resources interface <zia-dlp_resources>`.

        """
        return DLPResourcesAPI(self._request_executor)

    @property
    def device_management(self):
        """
        The interface object for the :ref:`ZIA Device Management interface <zia-device_management>`.

        """
        return DeviceManagementAPI(self._request_executor)

    @property
    def end_user_notification(self):
        """
        The interface object for the :ref:`ZIA End user Notification interface <zia-end_user_notification>`.

        """
        return EndUserNotificationAPI(self._request_executor)
    
    @property
    def file_type_control_rule(self):
        """
        The interface object for the :ref:`ZIA File Type Control Rule interface <zia-file_type_control_rule>`.

        """
        return FileTypeControlRuleAPI(self._request_executor)

    @property
    def isolation_profile(self):
        """
        The interface object for the :ref:`ZIA Cloud Browser Isolation Profile <zia-isolation_profile>`.

        """
        return CBIProfileAPI(self._request_executor)
    
    @property
    def intermediate_certificates(self):
        """
        The interface object for the :ref:`ZIA Intermediate Certificate interface <zia-intermediate_certificates>`.

        """
        return IntermediateCertsAPI(self._request_executor)

    @property
    def forwarding_control(self):
        """
        The interface object for the :ref:`ZIA Forwarding Control Policies interface <zia-forwarding_control>`.

        """
        return ForwardingControlAPI(self._request_executor)

    @property
    def locations(self):
        """
        The interface object for the :ref:`ZIA Locations interface <zia-locations>`.

        """
        return LocationsAPI(self._request_executor)

    @property
    def malware_protection_policy(self):
        """
        The interface object for the :ref:`ZIA Malware Protection Policy interface <zia-malware_protection_policy>`.

        """
        return MalwareProtectionPolicyAPI(self._request_executor)
    
    @property
    def organization_information(self):
        """
        The interface object for the :ref:`ZIA Organization Information interface <zia-organization_information>`.

        """
        return OrganizationInformationAPI(self._request_executor)

    @property
    def pac_files(self):
        """
        The interface object for the :ref:`ZIA Pac Files interface <zia-pac_files>`.

        """
        return PacFilesAPI(self._request_executor)
    
    @property
    def remote_assistance(self):
        """
        The interface object for the :ref:`ZIA Remote Assistance interface <zia-remote_assistance>`.

        """
        return RemoteAssistanceAPI(self._request_executor)
    
    @property
    def rule_labels(self):
        """
        The interface object for the :ref:`ZIA Rule Labels interface <zia-rule_labels>`.

        """
        return RuleLabelsAPI(self._request_executor)

    @property
    def sandbox(self):
        """
        The interface object for the :ref:`ZIA Cloud Sandbox interface <zia-sandbox>`.

        """
        return CloudSandboxAPI(self._request_executor)

    @property
    def sandbox_rules(self):
        """
        The interface object for the :ref:`ZIA Sandbox Rules interface <zia-sandbox_rules>`.

        """
        return SandboxRulesAPI(self._request_executor)
    
    @property
    def security_policy_settings(self):
        """
        The interface object for the :ref:`ZIA Security Policy Settings interface <zia-security_policy_settings>`.

        """
        return SecurityPolicyAPI(self._request_executor)

    @property
    def traffic_gre_tunnel(self):
        """
        The interface object for the :ref:`ZIA Traffic Forwarding interface <zia-traffic_gre_tunnel>`.

        """
        return TrafficForwardingGRETunnelAPI(self._request_executor)

    @property
    def traffic_vpn_credentials(self):
        """
        The interface object for the :ref:`ZIA Traffic VPN Credential interface <zia-traffic_vpn_credentials>`.

        """
        return TrafficVPNCredentialAPI(self._request_executor)

    @property
    def traffic_static_ip(self):
        """
        The interface object for the :ref:`ZIA Traffic Static IP interface <zia-traffic_static_ip>`.

        """
        return TrafficStaticIPAPI(self._request_executor)

    @property
    def url_categories(self):
        """
        The interface object for the :ref:`ZIA URL Categories interface <zia-url_categories>`.

        """
        return URLCategoriesAPI(self._request_executor)

    @property
    def url_filtering(self):
        """
        The interface object for the :ref:`ZIA URL Filtering interface <zia-url_filtering>`.

        """
        return URLFilteringAPI(self._request_executor)

    @property
    def user_management(self):
        """
        The interface object for the :ref:`ZIA User Management interface <zia-user_management>`.

        """
        return UserManagementAPI(self._request_executor)

    @property
    def zpa_gateway(self):
        """
        The interface object for the :ref:`ZPA Gateway <zia-zpa_gateway>`.

        """
        return ZPAGatewayAPI(self._request_executor)

    @property
    def workload_groups(self):
        """
        The interface object for the :ref:`ZIA Workload Groups <zia-workload_groups>`.

        """
        return WorkloadGroupsAPI(self._request_executor)
