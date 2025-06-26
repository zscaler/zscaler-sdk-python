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

from zscaler.request_executor import RequestExecutor
from zscaler.zia.activate import ActivationAPI
from zscaler.zia.advanced_settings import AdvancedSettingsAPI
from zscaler.zia.atp_policy import ATPPolicyAPI
from zscaler.zia.admin_roles import AdminRolesAPI
from zscaler.zia.admin_users import AdminUsersAPI
from zscaler.zia.apptotal import AppTotalAPI
from zscaler.zia.audit_logs import AuditLogsAPI
from zscaler.zia.authentication_settings import AuthenticationSettingsAPI
from zscaler.zia.bandwidth_classes import BandwidthClassesAPI
from zscaler.zia.bandwidth_control_rules import BandwidthControlRulesAPI
from zscaler.zia.browser_control_settings import BrowserControlSettingsPI
from zscaler.zia.shadow_it_report import ShadowITAPI
from zscaler.zia.cloudappcontrol import CloudAppControlAPI
from zscaler.zia.casb_dlp_rules import CasbdDlpRulesAPI
from zscaler.zia.casb_malware_rules import CasbMalwareRulesAPI
from zscaler.zia.cloud_applications import CloudApplicationsAPI
from zscaler.zia.cloud_app_instances import CloudApplicationInstancesAPI
from zscaler.zia.cloud_nss import CloudNSSAPI
from zscaler.zia.cloud_browser_isolation import CBIProfileAPI
from zscaler.zia.sandbox import CloudSandboxAPI
from zscaler.zia.dlp_dictionary import DLPDictionaryAPI
from zscaler.zia.dlp_engine import DLPEngineAPI
from zscaler.zia.dlp_web_rules import DLPWebRuleAPI
from zscaler.zia.dlp_templates import DLPTemplatesAPI
from zscaler.zia.dlp_resources import DLPResourcesAPI
from zscaler.zia.device_management import DeviceManagementAPI
from zscaler.zia.end_user_notification import EndUserNotificationAPI
from zscaler.zia.file_type_control_rule import FileTypeControlRuleAPI
from zscaler.zia.cloud_firewall_dns import FirewallDNSRulesAPI
from zscaler.zia.cloud_firewall_ips import FirewallIPSRulesAPI
from zscaler.zia.cloud_firewall_rules import FirewallPolicyAPI
from zscaler.zia.cloud_firewall import FirewallResourcesAPI
from zscaler.zia.forwarding_control import ForwardingControlAPI
from zscaler.zia.ftp_control_policy import FTPControlPolicyAPI
from zscaler.zia.ipv6_config import TrafficIPV6ConfigAPI
from zscaler.zia.malware_protection_policy import MalwareProtectionPolicyAPI
from zscaler.zia.locations import LocationsAPI
from zscaler.zia.organization_information import OrganizationInformationAPI
from zscaler.zia.pac_files import PacFilesAPI
from zscaler.zia.policy_export import PolicyExportAPI
from zscaler.zia.proxies import ProxiesAPI
from zscaler.zia.risk_profiles import RiskProfilesAPI
from zscaler.zia.remote_assistance import RemoteAssistanceAPI
from zscaler.zia.rule_labels import RuleLabelsAPI
from zscaler.zia.sandbox_rules import SandboxRulesAPI
from zscaler.zia.security_policy_settings import SecurityPolicyAPI
from zscaler.zia.ssl_inspection_rules import SSLInspectionAPI
from zscaler.zia.intermediate_certificates import IntermediateCertsAPI
from zscaler.zia.traffic_extranet import TrafficExtranetAPI
from zscaler.zia.gre_tunnel import TrafficForwardingGRETunnelAPI
from zscaler.zia.traffic_vpn_credentials import TrafficVPNCredentialAPI
from zscaler.zia.traffic_static_ip import TrafficStaticIPAPI
from zscaler.zia.url_categories import URLCategoriesAPI
from zscaler.zia.url_filtering import URLFilteringAPI
from zscaler.zia.user_management import UserManagementAPI
from zscaler.zia.workload_groups import WorkloadGroupsAPI
from zscaler.zia.zpa_gateway import ZPAGatewayAPI
from zscaler.zia.sub_clouds import SubCloudsAPI
from zscaler.zia.system_audit import SystemAuditReportAPI
from zscaler.zia.iot_report import IOTReportAPI
from zscaler.zia.mobile_threat_settings import MobileAdvancedSettingsAPI
from zscaler.zia.dns_gatways import DNSGatewayAPI
from zscaler.zia.alert_subscriptions import AlertSubscriptionsAPI
from zscaler.zia.tenancy_restriction_profile import TenancyRestrictionProfileAPI
from zscaler.zia.time_intervals import TimeIntervalsAPI
from zscaler.zia.dedicated_ip_gateways import DedicatedIPGatewaysAPI
from zscaler.zia.traffic_datacenters import TrafficDatacentersAPI
from zscaler.zia.nss_servers import NssServersAPI
from zscaler.zia.nat_control_policy import NatControlPolicyAPI
from zscaler.zia.vzen_clusters import VZENClustersAPI
from zscaler.zia.saas_security_api import SaaSSecurityAPI


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
        return ActivationAPI(self._request_executor)

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
    def casb_dlp_rules(self):
        """
        The interface object for the :ref:`ZIA Casb DLP Rules interface <zia-casb_dlp_rules>`.

        """

        return CasbdDlpRulesAPI(self._request_executor)

    @property
    def casb_malware_rules(self):
        """
        The interface object for the :ref:`ZIA Casb Malware Rules interface <zia-casb_malware_rules>`.

        """

        return CasbMalwareRulesAPI(self._request_executor)

    @property
    def cloud_applications(self):
        """
        The interface object for the :ref:`ZIA Cloud App Control <zia-cloud_applications>`.

        """
        return CloudApplicationsAPI(self._request_executor)

    @property
    def shadow_it_report(self):
        """
        The interface object for the :ref:`ZIA Shadow IT Report <zia-shadow_it_report>`.

        """
        return ShadowITAPI(self._request_executor)

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
    def cloud_firewall(self):
        """
        The interface object for the :ref:`ZIA Cloud Firewall resources interface <zia-cloud_firewall>`.

        """

        return FirewallResourcesAPI(self._request_executor)

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
        return DLPTemplatesAPI(self._request_executor)

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
    def ipv6_config(self):
        """
        The interface object for the :ref:`ZIA Traffic IPV6 Configuration <zia-ipv6_config>`.

        """
        return TrafficIPV6ConfigAPI(self._request_executor)

    @property
    def cloud_browser_isolation(self):
        """
        The interface object for the :ref:`ZIA Cloud Browser Isolation Profile <zia-cloud_browser_isolation>`.

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
    def policy_export(self):
        """
        The interface object for the :ref:`ZIA Policy Export interface <zia-policy_export>`.

        """
        return PolicyExportAPI(self._request_executor)

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
    def ssl_inspection_rules(self):
        """
        The interface object for the :ref:`ZIA SSL Inspection Rules interface <zia-ssl_inspection_rules>`.

        """
        return SSLInspectionAPI(self._request_executor)

    @property
    def traffic_extranet(self):
        """
        The interface object for the :ref:`ZIA Extranet interface <zia-traffic_extranet>`.

        """
        return TrafficExtranetAPI(self._request_executor)

    @property
    def gre_tunnel(self):
        """
        The interface object for the :ref:`ZIA Traffic GRE Tunnel interface <zia-gre_tunnel>`.

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

    @property
    def sub_clouds(self):
        """
        The interface object for the :ref:`ZIA Workload Groups <zia-sub_clouds>`.

        """

        return SubCloudsAPI(self._request_executor)

    @property
    def system_audit(self):
        """
        The interface object for the :ref:`ZIA System Audit Report <zia-system_audit>`.

        """

        return SystemAuditReportAPI(self._request_executor)

    @property
    def iot_report(self):
        """
        The interface object for the :ref:`ZIA IOT Report interface <zia-iot_report>`.

        """

        return IOTReportAPI(self._request_executor)

    @property
    def mobile_threat_settings(self):
        """
        The interface object for the :ref:`ZIA Mobile Threat Settings interface <zia-mobile_threat_settings>`.

        """

        return MobileAdvancedSettingsAPI(self._request_executor)

    @property
    def dns_gatways(self):
        """
        The interface object for the :ref:`ZIA DNS Gateway interface <zia-dns_gatways>`.

        """

        return DNSGatewayAPI(self._request_executor)

    @property
    def alert_subscriptions(self):
        """
        The interface object for the :ref:`ZIA Alert Subscriptions interface <zia-alert_subscriptions>`.

        """

        return AlertSubscriptionsAPI(self._request_executor)

    @property
    def bandwidth_classes(self):
        """
        The interface object for the :ref:`ZIA Bandwidth Classes interface <zia-bandwidth_classes>`.

        """

        return BandwidthClassesAPI(self._request_executor)

    @property
    def bandwidth_control_rules(self):
        """
        The interface object for the :ref:`ZIA Bandwidth Control Rule interface <zia-bandwidth_control_rules>`.

        """

        return BandwidthControlRulesAPI(self._request_executor)

    @property
    def risk_profiles(self):
        """
        The interface object for the :ref:`ZIA Risk Profiles interface <zia-risk_profiles>`.

        """

        return RiskProfilesAPI(self._request_executor)

    @property
    def cloud_app_instances(self):
        """
        The interface object for the :ref:`ZIA Cloud Application Instances interface <zia-cloud_app_instances>`.

        """

        return CloudApplicationInstancesAPI(self._request_executor)

    @property
    def tenancy_restriction_profile(self):
        """
        The interface object for the :ref:`ZIA Tenant Restriction Profile interface <zia-tenancy_restriction_profile>`.

        """

        return TenancyRestrictionProfileAPI(self._request_executor)

    @property
    def time_intervals(self):
        """
        The interface object for the :ref:`ZIA Time Intervals interface <zia-time_intervals>`.

        """

        return TimeIntervalsAPI(self._request_executor)

    @property
    def ftp_control_policy(self):
        """
        The interface object for the :ref:`ZIA FTP Control Policy interface <zia-ftp_control_policy>`.

        """

        return FTPControlPolicyAPI(self._request_executor)

    @property
    def proxies(self):
        """
        The interface object for the :ref:`ZIA Proxies interface <zia-proxies>`.

        """

        return ProxiesAPI(self._request_executor)

    @property
    def dedicated_ip_gateways(self):
        """
        The interface object for the :ref:`ZIA Dedicated IP Gateways interface <zia-dedicated_ip_gateways>`.

        """

        return DedicatedIPGatewaysAPI(self._request_executor)

    @property
    def traffic_datacenters(self):
        """
        The interface object for the :ref:`ZIA Traffic Datacenters interface <zia-traffic_datacenters>`.

        """

        return TrafficDatacentersAPI(self._request_executor)

    @property
    def nss_servers(self):
        """
        The interface object for the :ref:`ZIA NSS Servers interface <zia-nss_servers>`.

        """

        return NssServersAPI(self._request_executor)

    @property
    def nat_control_policy(self):
        """
        The interface object for the :ref:`ZIA NAT Control Policy interface <zia-nat_control_policy>`.

        """

        return NatControlPolicyAPI(self._request_executor)

    @property
    def vzen_clusters(self):
        """
        The interface object for the :ref:`Virtual ZEN Clusters interface <zia-vzen_clusters>`.

        """

        return VZENClustersAPI(self._request_executor)

    @property
    def browser_control_settings(self):
        """
        The interface object for the :ref:`Browser Control Settings interface <zia-browser_control_settings>`.

        """

        return BrowserControlSettingsPI(self._request_executor)

    @property
    def saas_security_api(self):
        """
        The interface object for the :ref:`ZIA SaaS Security API interface <zia-saas_security_api>`.

        """

        return SaaSSecurityAPI(self._request_executor)
