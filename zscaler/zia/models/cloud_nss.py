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

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection
from zscaler.zia.models import location_management as location_management
from zscaler.zia.models import user_management as user_management
from zscaler.zia.models import traffic_vpn_credentials as vpn_credentials
from zscaler.zia.models import cloud_firewall_nw_service as nw_service
from zscaler.zia.models import dlp_dictionary as dlp_dictionary
from zscaler.zia.models import dlp_engine as dlp_engine


class NssFeeds(ZscalerObject):
    """
    A class for NssFeeds objects.
    """

    def __init__(self, config=None):
        """
        Initialize the NssFeeds model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.feed_status = config["feedStatus"] if "feedStatus" in config else None
            self.nss_log_type = config["nssLogType"] if "nssLogType" in config else None
            self.nss_feed_type = config["nssFeedType"] if "nssFeedType" in config else None
            self.feed_output_format = config["feedOutputFormat"] if "feedOutputFormat" in config else None
            self.user_obfuscation = config["userObfuscation"] if "userObfuscation" in config else None
            self.time_zone = config["timeZone"] if "timeZone" in config else None
            self.custom_escaped_character = ZscalerCollection.form_list(
                config["customEscapedCharacter"] if "customEscapedCharacter" in config else [], str
            )
            self.eps_rate_limit = config["epsRateLimit"] if "epsRateLimit" in config else None
            self.json_array_toggle = config["jsonArrayToggle"] if "jsonArrayToggle" in config else None
            self.siem_type = config["siemType"] if "siemType" in config else None
            self.max_batch_size = config["maxBatchSize"] if "maxBatchSize" in config else None
            self.connection_url = config["connectionURL"] if "connectionURL" in config else None
            self.authentication_token = config["authenticationToken"] if "authenticationToken" in config else None
            self.connection_headers = ZscalerCollection.form_list(
                config["connectionHeaders"] if "connectionHeaders" in config else [], str
            )
            self.last_success_full_test = config["lastSuccessFullTest"] if "lastSuccessFullTest" in config else None
            self.test_connectivity_code = config["testConnectivityCode"] if "testConnectivityCode" in config else None
            self.base64_encoded_certificate = (
                config["base64EncodedCertificate"] if "base64EncodedCertificate" in config else None
            )
            self.nss_type = config["nssType"] if "nssType" in config else None
            self.client_id = config["clientId"] if "clientId" in config else None
            self.client_secret = config["clientSecret"] if "clientSecret" in config else None
            self.authentication_url = config["authenticationUrl"] if "authenticationUrl" in config else None
            self.grant_type = config["grantType"] if "grantType" in config else None
            self.scope = config["scope"] if "scope" in config else None
            self.oauth_authentication = config["oauthAuthentication"] if "oauthAuthentication" in config else None
            self.server_ips = ZscalerCollection.form_list(config["serverIps"] if "serverIps" in config else [], str)
            self.client_ips = ZscalerCollection.form_list(config["clientIps"] if "clientIps" in config else [], str)
            self.domains = ZscalerCollection.form_list(config["domains"] if "domains" in config else [], str)
            self.dns_request_types = ZscalerCollection.form_list(
                config["dnsRequestTypes"] if "dnsRequestTypes" in config else [], str
            )
            self.dns_response_types = ZscalerCollection.form_list(
                config["dnsResponseTypes"] if "dnsResponseTypes" in config else [], str
            )
            self.dns_responses = ZscalerCollection.form_list(config["dnsResponses"] if "dnsResponses" in config else [], str)
            self.durations = ZscalerCollection.form_list(config["durations"] if "durations" in config else [], str)
            self.dns_actions = ZscalerCollection.form_list(config["dnsActions"] if "dnsActions" in config else [], str)
            self.firewall_logging_mode = config["firewallLoggingMode"] if "firewallLoggingMode" in config else None
            self.rules = ZscalerCollection.form_list(config["rules"] if "rules" in config else [], str)
            self.nw_services = ZscalerCollection.form_list(
                config["nwServices"] if "nwServices" in config else [], nw_service.NetworkServices
            )
            self.client_source_ips = ZscalerCollection.form_list(
                config["clientSourceIps"] if "clientSourceIps" in config else [], str
            )
            self.firewall_actions = ZscalerCollection.form_list(
                config["firewallActions"] if "firewallActions" in config else [], str
            )
            self.locations = ZscalerCollection.form_list(
                config["locations"] if "locations" in config else [], location_management.LocationManagement
            )
            self.countries = ZscalerCollection.form_list(config["countries"] if "countries" in config else [], str)
            self.server_source_ports = ZscalerCollection.form_list(
                config["serverSourcePorts"] if "serverSourcePorts" in config else [], str
            )
            self.client_source_ports = ZscalerCollection.form_list(
                config["clientSourcePorts"] if "clientSourcePorts" in config else [], str
            )
            self.action_filter = config["actionFilter"] if "actionFilter" in config else None
            self.email_dlp_policy_action = config["emailDlpPolicyAction"] if "emailDlpPolicyAction" in config else None
            self.direction = config["direction"] if "direction" in config else None
            self.event = config["event"] if "event" in config else None
            self.policy_reasons = ZscalerCollection.form_list(
                config["policyReasons"] if "policyReasons" in config else [], str
            )
            self.protocol_types = ZscalerCollection.form_list(
                config["protocolTypes"] if "protocolTypes" in config else [], str
            )
            self.user_agents = ZscalerCollection.form_list(config["userAgents"] if "userAgents" in config else [], str)
            self.request_methods = ZscalerCollection.form_list(
                config["requestMethods"] if "requestMethods" in config else [], str
            )
            self.casb_severity = ZscalerCollection.form_list(config["casbSeverity"] if "casbSeverity" in config else [], str)
            self.casb_policy_types = ZscalerCollection.form_list(
                config["casbPolicyTypes"] if "casbPolicyTypes" in config else [], str
            )
            self.casb_applications = ZscalerCollection.form_list(
                config["casbApplications"] if "casbApplications" in config else [], str
            )
            self.casb_action = ZscalerCollection.form_list(config["casbAction"] if "casbAction" in config else [], str)
            self.casb_tenant = ZscalerCollection.form_list(config["casbTenant"] if "casbTenant" in config else [], str)
            self.url_super_categories = ZscalerCollection.form_list(
                config["urlSuperCategories"] if "urlSuperCategories" in config else [], str
            )
            self.web_applications = ZscalerCollection.form_list(
                config["webApplications"] if "webApplications" in config else [], str
            )
            self.web_application_classes = ZscalerCollection.form_list(
                config["webApplicationClasses"] if "webApplicationClasses" in config else [], str
            )
            self.malware_names = ZscalerCollection.form_list(config["malwareNames"] if "malwareNames" in config else [], str)
            self.url_classes = ZscalerCollection.form_list(config["urlClasses"] if "urlClasses" in config else [], str)
            self.malware_classes = ZscalerCollection.form_list(
                config["malwareClasses"] if "malwareClasses" in config else [], str
            )
            self.advanced_threats = ZscalerCollection.form_list(
                config["advancedThreats"] if "advancedThreats" in config else [], str
            )
            self.response_codes = ZscalerCollection.form_list(
                config["responseCodes"] if "responseCodes" in config else [], str
            )
            self.nw_applications = ZscalerCollection.form_list(
                config["nwApplications"] if "nwApplications" in config else [], str
            )
            self.nat_actions = ZscalerCollection.form_list(config["natActions"] if "natActions" in config else [], str)
            self.traffic_forwards = ZscalerCollection.form_list(
                config["trafficForwards"] if "trafficForwards" in config else [], str
            )
            self.web_traffic_forwards = ZscalerCollection.form_list(
                config["webTrafficForwards"] if "webTrafficForwards" in config else [], str
            )
            self.tunnel_types = ZscalerCollection.form_list(config["tunnelTypes"] if "tunnelTypes" in config else [], str)
            self.alerts = ZscalerCollection.form_list(config["alerts"] if "alerts" in config else [], str)
            self.object_type = ZscalerCollection.form_list(config["objectType"] if "objectType" in config else [], str)
            self.activity = ZscalerCollection.form_list(config["activity"] if "activity" in config else [], str)
            self.object_type1 = ZscalerCollection.form_list(config["objectType1"] if "objectType1" in config else [], str)
            self.object_type2 = ZscalerCollection.form_list(config["objectType2"] if "objectType2" in config else [], str)
            self.end_point_dlp_log_type = ZscalerCollection.form_list(
                config["endPointDLPLogType"] if "endPointDLPLogType" in config else [], str
            )
            self.email_dlp_log_type = ZscalerCollection.form_list(
                config["emailDLPLogType"] if "emailDLPLogType" in config else [], str
            )
            self.file_type_super_categories = ZscalerCollection.form_list(
                config["fileTypeSuperCategories"] if "fileTypeSuperCategories" in config else [], str
            )
            self.file_type_categories = ZscalerCollection.form_list(
                config["fileTypeCategories"] if "fileTypeCategories" in config else [], str
            )
            self.casb_file_type = ZscalerCollection.form_list(config["casbFileType"] if "casbFileType" in config else [], str)
            self.casb_file_type_super_categories = ZscalerCollection.form_list(
                config["casbFileTypeSuperCategories"] if "casbFileTypeSuperCategories" in config else [], str
            )
            self.external_owners = ZscalerCollection.form_list(
                config["externalOwners"] if "externalOwners" in config else [], str
            )
            self.external_collaborators = ZscalerCollection.form_list(
                config["externalCollaborators"] if "externalCollaborators" in config else [], str
            )
            self.internal_collaborators = ZscalerCollection.form_list(
                config["internalCollaborators"] if "internalCollaborators" in config else [], str
            )
            self.itsm_object_type = ZscalerCollection.form_list(
                config["itsmObjectType"] if "itsmObjectType" in config else [], str
            )
            self.url_categories = ZscalerCollection.form_list(
                config["urlCategories"] if "urlCategories" in config else [], str
            )
            self.dlp_engines = ZscalerCollection.form_list(
                config["dlpEngines"] if "dlpEngines" in config else [], dlp_engine.DLPEngine
            )
            self.dlp_dictionaries = ZscalerCollection.form_list(
                config["dlpDictionaries"] if "dlpDictionaries" in config else [], dlp_dictionary.DLPDictionary
            )
            self.users = ZscalerCollection.form_list(
                config["users"] if "users" in config else [], user_management.UserManagement
            )
            self.departments = ZscalerCollection.form_list(
                config["departments"] if "departments" in config else [], user_management.Department
            )
            self.sender_name = ZscalerCollection.form_list(config["senderName"] if "senderName" in config else [], str)
            self.buckets = ZscalerCollection.form_list(config["buckets"] if "buckets" in config else [], str)
            self.vpn_credentials = ZscalerCollection.form_list(
                config["vpnCredentials"] if "vpnCredentials" in config else [], vpn_credentials.TrafficVPNCredentials
            )

            self.message_size = ZscalerCollection.form_list(config["messageSize"] if "messageSize" in config else [], str)
            self.file_sizes = ZscalerCollection.form_list(config["fileSizes"] if "fileSizes" in config else [], str)
            self.request_sizes = ZscalerCollection.form_list(config["requestSizes"] if "requestSizes" in config else [], str)
            self.response_sizes = ZscalerCollection.form_list(
                config["responseSizes"] if "responseSizes" in config else [], str
            )
            self.transaction_sizes = ZscalerCollection.form_list(
                config["transactionSizes"] if "transactionSizes" in config else [], str
            )
            self.inbound_bytes = ZscalerCollection.form_list(config["inBoundBytes"] if "inBoundBytes" in config else [], str)
            self.outbound_bytes = ZscalerCollection.form_list(
                config["outBoundBytes"] if "outBoundBytes" in config else [], str
            )
            self.download_time = ZscalerCollection.form_list(config["downloadTime"] if "downloadTime" in config else [], str)
            self.scan_time = ZscalerCollection.form_list(config["scanTime"] if "scanTime" in config else [], str)
            self.server_source_ips = ZscalerCollection.form_list(
                config["serverSourceIps"] if "serverSourceIps" in config else [], str
            )
            self.server_destination_ips = ZscalerCollection.form_list(
                config["serverDestinationIps"] if "serverDestinationIps" in config else [], str
            )
            self.tunnel_ips = ZscalerCollection.form_list(config["tunnelIps"] if "tunnelIps" in config else [], str)
            self.internal_ips = ZscalerCollection.form_list(config["internalIps"] if "internalIps" in config else [], str)
            self.tunnel_source_ips = ZscalerCollection.form_list(
                config["tunnelSourceIps"] if "tunnelSourceIps" in config else [], str
            )
            self.tunnel_dest_ips = ZscalerCollection.form_list(
                config["tunnelDestIps"] if "tunnelDestIps" in config else [], str
            )
            self.client_destination_ips = ZscalerCollection.form_list(
                config["clientDestinationIps"] if "clientDestinationIps" in config else [], str
            )
            self.audit_log_type = ZscalerCollection.form_list(config["auditLogType"] if "auditLogType" in config else [], str)
            self.project_name = ZscalerCollection.form_list(config["projectName"] if "projectName" in config else [], str)
            self.repo_name = ZscalerCollection.form_list(config["repoName"] if "repoName" in config else [], str)
            self.object_name = ZscalerCollection.form_list(config["objectName"] if "objectName" in config else [], str)
            self.channel_name = ZscalerCollection.form_list(config["channelName"] if "channelName" in config else [], str)
            self.file_source = ZscalerCollection.form_list(config["fileSource"] if "fileSource" in config else [], str)
            self.file_name = ZscalerCollection.form_list(config["fileName"] if "fileName" in config else [], str)
            self.session_counts = ZscalerCollection.form_list(
                config["sessionCounts"] if "sessionCounts" in config else [], str
            )
            self.adv_user_agents = ZscalerCollection.form_list(
                config["advUserAgents"] if "advUserAgents" in config else [], str
            )
            self.referer_urls = ZscalerCollection.form_list(config["refererUrls"] if "refererUrls" in config else [], str)
            self.host_names = ZscalerCollection.form_list(config["hostNames"] if "hostNames" in config else [], str)
            self.full_urls = ZscalerCollection.form_list(config["fullUrls"] if "fullUrls" in config else [], str)
            self.threat_names = ZscalerCollection.form_list(config["threatNames"] if "threatNames" in config else [], str)
            self.page_risk_indexes = ZscalerCollection.form_list(
                config["pageRiskIndexes"] if "pageRiskIndexes" in config else [], str
            )
            self.client_destination_ports = ZscalerCollection.form_list(
                config["clientDestinationPorts"] if "clientDestinationPorts" in config else [], str
            )
            self.tunnel_source_port = ZscalerCollection.form_list(
                config["tunnelSourcePort"] if "tunnelSourcePort" in config else [], str
            )
        else:
            self.id = None
            self.name = None
            self.feed_status = None
            self.nss_log_type = None
            self.nss_feed_type = None
            self.feed_output_format = None
            self.user_obfuscation = None
            self.time_zone = None
            self.custom_escaped_character = []
            self.eps_rate_limit = None
            self.json_array_toggle = None
            self.siem_type = None
            self.max_batch_size = None
            self.connection_url = None
            self.authentication_token = None
            self.connection_headers = []
            self.last_success_full_test = None
            self.test_connectivity_code = None
            self.base64_encoded_certificate = None
            self.nss_type = None
            self.client_id = None
            self.client_secret = None
            self.authentication_url = None
            self.grant_type = None
            self.scope = None
            self.oauth_authentication = None
            self.server_ips = []
            self.client_ips = []
            self.domains = []
            self.dns_request_types = []
            self.dns_response_types = []
            self.dns_responses = []
            self.durations = []
            self.dns_actions = []
            self.firewall_logging_mode = None
            self.rules = []
            self.nw_services = []
            self.client_source_ips = []
            self.firewall_actions = []
            self.locations = []
            self.countries = []
            self.server_source_ports = []
            self.client_source_ports = []
            self.action_filter = None
            self.email_dlp_policy_action = None
            self.direction = None
            self.event = None
            self.policy_reasons = []
            self.protocol_types = []
            self.user_agents = []
            self.request_methods = []
            self.casb_severity = []
            self.casb_policy_types = []
            self.casb_applications = []
            self.casb_action = []
            self.casb_tenant = []
            self.url_super_categories = []
            self.web_applications = []
            self.web_application_classes = []
            self.malware_names = []
            self.url_classes = []
            self.malware_classes = []
            self.advanced_threats = []
            self.response_codes = []
            self.nw_applications = []
            self.nat_actions = []
            self.traffic_forwards = []
            self.web_traffic_forwards = []
            self.tunnel_types = []
            self.alerts = []
            self.object_type = []
            self.activity = []
            self.object_type1 = []
            self.object_type2 = []
            self.end_point_dlp_log_type = []
            self.email_dlp_log_type = []
            self.file_type_super_categories = []
            self.file_type_categories = []
            self.casb_file_type = []
            self.casb_file_type_super_categories = []
            self.external_owners = []
            self.external_collaborators = []
            self.internal_collaborators = []
            self.itsm_object_type = []
            self.url_categories = []
            self.dlp_engines = []
            self.dlp_dictionaries = []
            self.users = []
            self.departments = []
            self.sender_name = []
            self.buckets = []
            self.vpn_credentials = []
            self.message_size = []
            self.file_sizes = []
            self.request_sizes = []
            self.response_sizes = []
            self.transaction_sizes = []
            self.inbound_bytes = []
            self.outbound_bytes = []
            self.download_time = []
            self.scan_time = []
            self.server_source_ips = []
            self.server_destination_ips = []
            self.tunnel_ips = []
            self.internal_ips = []
            self.tunnel_source_ips = []
            self.tunnel_dest_ips = []
            self.client_destination_ips = []
            self.audit_log_type = []
            self.project_name = []
            self.repo_name = []
            self.object_name = []
            self.channel_name = []
            self.file_source = []
            self.file_name = []
            self.session_counts = []
            self.adv_user_agents = []
            self.referer_urls = []
            self.host_names = []
            self.full_urls = []
            self.threat_names = []
            self.page_risk_indexes = []
            self.client_destination_ports = []
            self.tunnel_source_port = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "feedStatus": self.feed_status,
            "nssLogType": self.nss_log_type,
            "nssFeedType": self.nss_feed_type,
            "feedOutputFormat": self.feed_output_format,
            "userObfuscation": self.user_obfuscation,
            "timeZone": self.time_zone,
            "customEscapedCharacter": self.custom_escaped_character,
            "epsRateLimit": self.eps_rate_limit,
            "jsonArrayToggle": self.json_array_toggle,
            "siemType": self.siem_type,
            "maxBatchSize": self.max_batch_size,
            "connectionURL": self.connection_url,
            "authenticationToken": self.authentication_token,
            "connectionHeaders": self.connection_headers,
            "lastSuccessFullTest": self.last_success_full_test,
            "testConnectivityCode": self.test_connectivity_code,
            "base64EncodedCertificate": self.base64_encoded_certificate,
            "nssType": self.nss_type,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "authenticationUrl": self.authentication_url,
            "grantType": self.grant_type,
            "scope": self.scope,
            "oauthAuthentication": self.oauth_authentication,
            "serverIps": self.server_ips,
            "clientIps": self.client_ips,
            "domains": self.domains,
            "dnsRequestTypes": self.dns_request_types,
            "dnsResponseTypes": self.dns_response_types,
            "dnsResponses": self.dns_responses,
            "durations": self.durations,
            "dnsActions": self.dns_actions,
            "firewallLoggingMode": self.firewall_logging_mode,
            "rules": self.rules,
            "nwServices": self.nw_services,
            "clientSourceIps": self.client_source_ips,
            "firewallActions": self.firewall_actions,
            "locations": self.locations,
            "countries": self.countries,
            "serverSourcePorts": self.server_source_ports,
            "clientSourcePorts": self.client_source_ports,
            "actionFilter": self.action_filter,
            "emailDlpPolicyAction": self.email_dlp_policy_action,
            "direction": self.direction,
            "event": self.event,
            "policyReasons": self.policy_reasons,
            "protocolTypes": self.protocol_types,
            "userAgents": self.user_agents,
            "requestMethods": self.request_methods,
            "casbSeverity": self.casb_severity,
            "casbPolicyTypes": self.casb_policy_types,
            "casbApplications": self.casb_applications,
            "casbAction": self.casb_action,
            "casbTenant": self.casb_tenant,
            "urlSuperCategories": self.url_super_categories,
            "webApplications": self.web_applications,
            "webApplicationClasses": self.web_application_classes,
            "malwareNames": self.malware_names,
            "urlClasses": self.url_classes,
            "malwareClasses": self.malware_classes,
            "advancedThreats": self.advanced_threats,
            "responseCodes": self.response_codes,
            "nwApplications": self.nw_applications,
            "natActions": self.nat_actions,
            "trafficForwards": self.traffic_forwards,
            "webTrafficForwards": self.web_traffic_forwards,
            "tunnelTypes": self.tunnel_types,
            "alerts": self.alerts,
            "objectType": self.object_type,
            "activity": self.activity,
            "objectType1": self.object_type1,
            "objectType2": self.object_type2,
            "endPointDLPLogType": self.end_point_dlp_log_type,
            "emailDLPLogType": self.email_dlp_log_type,
            "fileTypeSuperCategories": self.file_type_super_categories,
            "fileTypeCategories": self.file_type_categories,
            "casbFileType": self.casb_file_type,
            "casbFileTypeSuperCategories": self.casb_file_type_super_categories,
            "externalOwners": self.external_owners,
            "externalCollaborators": self.external_collaborators,
            "internalCollaborators": self.internal_collaborators,
            "itsmObjectType": self.itsm_object_type,
            "urlCategories": self.url_categories,
            "dlpEngines": self.dlp_engines,
            "dlpDictionaries": self.dlp_dictionaries,
            "users": self.users,
            "departments": self.departments,
            "senderName": self.sender_name,
            "buckets": self.buckets,
            "vpnCredentials": self.vpn_credentials,
            "messageSize": self.message_size,
            "fileSizes": self.file_sizes,
            "requestSizes": self.request_sizes,
            "responseSizes": self.response_sizes,
            "transactionSizes": self.transaction_sizes,
            "inBoundBytes": self.inbound_bytes,
            "outBoundBytes": self.outbound_bytes,
            "downloadTime": self.download_time,
            "scanTime": self.scan_time,
            "serverSourceIps": self.server_source_ips,
            "serverDestinationIps": self.server_destination_ips,
            "tunnelIps": self.tunnel_ips,
            "internalIps": self.internal_ips,
            "tunnelSourceIps": self.tunnel_source_ips,
            "tunnelDestIps": self.tunnel_dest_ips,
            "clientDestinationIps": self.client_destination_ips,
            "auditLogType": self.audit_log_type,
            "projectName": self.project_name,
            "repoName": self.repo_name,
            "objectName": self.object_name,
            "channelName": self.channel_name,
            "fileSource": self.file_source,
            "fileName": self.file_name,
            "sessionCounts": self.session_counts,
            "advUserAgents": self.adv_user_agents,
            "refererUrls": self.referer_urls,
            "hostNames": self.host_names,
            "fullUrls": self.full_urls,
            "threatNames": self.threat_names,
            "pageRiskIndexes": self.page_risk_indexes,
            "clientDestinationPorts": self.client_destination_ports,
            "tunnelSourcePort": self.tunnel_source_port,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class NSSTestConnectivity(ZscalerObject):
    """
    A class for Nsstestconnectivity objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Nsstestconnectivity model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.siem_type = config["siemType"] if "siemType" in config else None
            self.max_batch_size = config["maxBatchSize"] if "maxBatchSize" in config else None
            self.connection_url = config["connectionURL"] if "connectionURL" in config else None
            self.authentication_token = config["authenticationToken"] if "authenticationToken" in config else None
            self.connection_headers = ZscalerCollection.form_list(
                config["connectionHeaders"] if "connectionHeaders" in config else [], str
            )
            self.last_success_full_test = config["lastSuccessFullTest"] if "lastSuccessFullTest" in config else None
            self.test_connectivity_status = config["testConnectivityStatus"] if "testConnectivityStatus" in config else None
            self.test_connectivity_code = config["testConnectivityCode"] if "testConnectivityCode" in config else None
            self.base64_encoded_certificate = (
                config["base64EncodedCertificate"] if "base64EncodedCertificate" in config else None
            )
            self.nss_type = config["nssType"] if "nssType" in config else None
            self.client_id = config["clientId"] if "clientId" in config else None
            self.client_secret = config["clientSecret"] if "clientSecret" in config else None
            self.authentication_url = config["authenticationUrl"] if "authenticationUrl" in config else None
            self.grant_type = config["grantType"] if "grantType" in config else None
            self.scope = config["scope"] if "scope" in config else None
            self.oauth_authentication = config["oauthAuthentication"] if "oauthAuthentication" in config else False
        else:
            self.siem_type = None
            self.max_batch_size = None
            self.connection_url = None
            self.authentication_token = None
            self.connection_headers = []
            self.last_success_full_test = None
            self.test_connectivity_status = None
            self.test_connectivity_code = None
            self.base64_encoded_certificate = None
            self.nss_type = None
            self.client_id = None
            self.client_secret = None
            self.authentication_url = None
            self.grant_type = None
            self.scope = None
            self.oauth_authentication = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "siemType": self.siem_type,
            "maxBatchSize": self.max_batch_size,
            "connectionURL": self.connection_url,
            "authenticationToken": self.authentication_token,
            "connectionHeaders": self.connection_headers,
            "lastSuccessFullTest": self.last_success_full_test,
            "testConnectivityStatus": self.test_connectivity_status,
            "testConnectivityCode": self.test_connectivity_code,
            "base64EncodedCertificate": self.base64_encoded_certificate,
            "nssType": self.nss_type,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "authenticationUrl": self.authentication_url,
            "grantType": self.grant_type,
            "scope": self.scope,
            "oauthAuthentication": self.oauth_authentication,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
