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
from zscaler.zia.models.cloud_nss import NSSTestConnectivity
from zscaler.zia.models.cloud_nss import NssFeeds
from zscaler.utils import format_url


class CloudNSSAPI(APIClient):
    """
    A Client object for the Cloud NSS resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_nss_feed(self, query_params=None) -> tuple:
        """
        Retrieves the cloud NSS feeds configured in the ZIA Admin Portal

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.feed_type]`` {str}: The cloud NSS feed type

        Returns:
            tuple: A tuple containing (Retries the cloud nss feed instances, Response, error)


        Examples:
            Get the cloud nss feed:
            >>> nss = zia.cloud_nss.list_nss_feed()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds
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
                result.append(NssFeeds(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_nss_feed(
        self,
        feed_id: int,
    ) -> tuple:
        """
        Retrieves information about cloud NSS feed based on the specified ID

        Args:
            feed_id (str): The unique identifier for the cloud cloud NSS feed.

        Returns:
            tuple: A tuple containing (cloud NSS feed instance, Response, error).

        Example:
            Retrieve a cloud NSS feed by its feed_id:

            >>> feed, response, error = zia.cloud_nss.get_nss_feed(feed_id=123456)
            >>> if not error:
            ...    print(feed.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds/{feed_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NssFeeds)

        if error:
            return (None, response, error)

        try:
            result = NssFeeds(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_nss_feed(
        self,
        **kwargs,
    ) -> tuple:
        """
        Adds a new cloud NSS feed.

        Args:
            name (str): he name of the cloud NSS feed.

        Keyword Args:
            feed_status (str): The status of the feed.
            nss_log_type (str): The type of NSS logs that are streamed (e.g., Web, Firewall, DNS, Alert).
            nss_feed_type (str): NSS feed format type (e.g., CSV, syslog, Splunk Common Information Model).
            feed_output_format (str): Output format used for the feed.
            user_obfuscation (str): Specifies whether user obfuscation is enabled or disabled.
            time_zone (str): Specifies the time zone used in the output file.
            custom_escaped_character (list[str]): Characters to be encoded using hex when they appear in URL, Host, or Referrer
            eps_rate_limit (int): Event per second limit.
            json_array_toggle (bool): Enables or disables streaming logs in JSON array format.
            siem_type (str): Cloud NSS SIEM type.
            max_batch_size (int): The maximum batch size in KB.
            connection_url (str): The HTTPS URL of the SIEM log collection API endpoint.
            authentication_token (str): The authentication token value.
            connection_headers (list[str]): The HTTP connection headers.
            last_successful_test (int): The timestamp of the last successful test in Unix time.
            test_connectivity_code (int): The code from the last test.
            base64_encoded_certificate (str): Base64-encoded certificate.
            nss_type (str): NSS type.
            client_id (str): Client ID applicable when SIEM type is set to S3 or Azure Sentinel.
            client_secret (str): Client secret applicable when SIEM type is set to S3 or Azure Sentinel.
            authentication_url (str): Authentication URL applicable when SIEM type is set to Azure Sentinel.
            grant_type (str): Grant type applicable when SIEM type is set to Azure Sentinel.
            scope (str): Scope applicable when SIEM type is set to Azure Sentinel.
            oauth_authentication (bool): Indicates whether OAuth 2.0 authentication is enabled.
            server_ips (list): Filter to limit the logs based on the server's IPv4 addresses
            client_ips (list): Filter to limit the logs based on a client's public IPv4 addresses
            domains (list): Filter to limit the logs to sessions associated with specific domains
            dns_request_types (list): DNS request types filter
            dns_response_types (list): DNS response types filter
            dns_responses (list): DNS responses filter
            durations (list): Filter based on time durations
            dns_actions (list): DNS Control policy action filter
            firewall_logging_mode (str): Firewall Filtering policy logging mode. Supported values: SESSION, AGGREGATE, ALL
            rules (list): Policy rules filter (e.g., Firewall Filtering or DNS Control rule filter)
            nw_services (list): Firewall network services filter
            client_source_ips (list): Filter based on a client's source IPv4 address in the Firewall policy
            firewall_actions (list): Firewall and IPS Control policy actions filter
            locations (list): Location filter
            countries (list): Countries filter in the Firewall policy
            server_source_ports (list): Firewall log filter based on the traffic destination name
            client_source_ports (list): Firewall log filter based on a client's source ports
            action_filter (str): Policy action filter. Supported values: ALLOWED, BLOCKED
            email_dlp_policy_action (str): Action filter for Email DLP log type.
                Supported values: ALLOW, CUSTOMHEADERINSERTION, BLOCK
            direction (str): Traffic direction filter specifying inbound or outbound.
                Supported values: INBOUND, OUTBOUND
            event (str): CASB event filter. Supported values: SCAN, VIOLATION, INCIDENT
            policy_reasons (list): Policy reason filter
            protocol_types (list): Protocol types filter
            user_agents (list): Predefined user agents filter
            request_methods (list): Request methods filter
            casb_severity (list): Zscaler's Cloud Access Security Broker (CASB) severity filter.
                Supported values: RULE_SEVERITY_HIGH, RULE_SEVERITY_MEDIUM, RULE_SEVERITY_LOW, RULE_SEVERITY_INFO
            casb_policy_types (list): CASB policy type filter.
                Supported values: MALWARE, DLP, ALL_INCIDENT
            casb_applications (list): CASB application filter
            casb_action (list): CASB policy action filter
            casb_tenant (list): CASB tenant filter
            url_super_categories (list): URL supercategory filter
            web_applications (list): Cloud applications filter
            web_application_classes (list): Cloud application categories Filter
            malware_names (list): Filter based on malware names
            url_classes (list): URL category filter
            advanced_threats (list): Advanced threats filter
            response_codes (list): Response codes filter
            nw_applications (list): Firewall network applications filter
            nat_actions (list): NAT Control policy actions filter. Supported values: NONE, DNAT
            traffic_forwards (list): Filter based on the firewall traffic forwarding method
            web_traffic_forwards (list): Filter based on the web traffic forwarding method
            tunnel_types (list): Tunnel type filter. Supported values: GRE, IPSEC_IKEV1, IPSEC_IKEV2, SVPN, EXTRANET, ZUB, ZCB
            alerts (list): Alert filter. Supported values: CRITICAL, WARN
            object_type (list): CRM object type filter
            activity (list): CASB activity filter
            object_type1 (list): CASB activity object type filter
            object_type2 (list): CASB activity object type filter if applicable
            end_point_dlp_log_type (list): Endpoint DLP log type filter.
                Supported values: EPDLP_SCAN_AGGREGATE, EPDLP_SENSITIVE_ACTIVITY, EPDLP_DLP_INCIDENT
            email_dlp_log_type (list): Email DLP record type filter.
                Supported values: EMAILDLP_SCAN, EMAILDLP_SENSITIVE_ACTIVITY, EMAILDLP_DLP_INCIDENT
            file_type_super_categories (list): Filter based on the category of file type in download
            file_type_categories (list): Filter based on the file type in download
            casb_file_type (list): Endpoint DLP file type filter
            casb_file_type_super_categories (list): Endpoint DLP file type category filer
            external_owners (list): Filter logs associated with file owners
            external_collaborators (list): Filter logs to specific recipients outside your organization
            internal_collaborators (list): Filter logs to specific recipients within your organization
            itsm_object_type (list): ITSM object type filter
            url_categories (list): URL category filter
            dlp_engines (list): DLP engine filter
            dlp_dictionaries (list): DLP dictionary filter
            users (list): User filter
            departments (list): Department filter
            sender_name (list): Filter based on sender or owner name
            buckets (list): Filter based on public cloud storage buckets
            vpn_credentials (list): Filter based on specific VPN credentials
            message_size (list): Message size filter
            file_sizes (list): File size filter
            request_sizes (list): Request size filter
            response_sizes (list): Response size filter
            transaction_sizes (list): Transaction size filter
            inbound_bytes (list): Filter based on inbound bytes
            outbound_bytes (list): Filter based on outbound bytes
            download_time (list): Download time filter
            scan_time (list): Scan time filter
            server_source_ips (list): Filter based on the server's source IPv4 addresses in Firewall policy
            server_destination_ips (list): Filter based on the server's destination IPv4 addresses in Firewall policy
            tunnel_ips (list): Filter based on tunnel IPv4 addresses in Firewall policy
            internal_ips (list): Filter based on internal IPv4 addresses
            tunnel_source_ips (list): Source IPv4 addresses of tunnels
            tunnel_dest_ips (list): Destination IPv4 addresses of tunnels
            client_destination_ips (list): Client's destination IPv4 addresses in Firewall policy
            audit_log_type (list): Audit log type filter
            project_name (list): Repository project name filter
            repo_name (list): Repository name filter
            object_name (list): CRM object name filter
            channel_name (list): Collaboration channel name filter
            file_source (list): Filter based on the file source
            file_name (list): Filter based on the file name
            session_counts (list): Firewall logs filter based on the number of sessions
            adv_user_agents (list): Filter based on custom user agent strings
            referer_urls (list): Referrer URL filter
            hostnames (list): Filter to limit the logs based on specific hostnames
            full_urls (list): Filter to limit the logs based on specific full URLs
            threat_names (list): Filter based on threat names
            page_risk_indexes (list): Page Risk Index filter
            client_destination_ports (list): Firewall logs filter based on a client's destination
            tunnel_source_port (list): Filter based on the tunnel source port

        Returns:
            tuple: Add a new NSS feed.

        Example:
            Add a new NSS feed.:

            >>> added_feed, _, error = client.zia.cloud_nss.add_nss_feed(
            ...     name=f"NSSFeed_{random.randint(1000, 10000)}",
            ...     feed_status="ENABLED",
            ...     nss_type='NSS_FOR_WEB',
            ...     nss_log_type="WEBLOG",
            ...     nss_feed_type="JSON",
            ...     siem_type="SPLUNK",
            ...     feed_output_format=""\\{ \"sourcetype\" : \"zscalernss-web\", \"event\"-",
            ...     user_obfuscation="DISABLED",
            ...     time_zone="GMT",
            ...     custom_escaped_character= ["ASCII_44", "ASCII_92", "ASCII_34"],
            ...     eps_rateLimit = 0,
            ...     duplicate_logs = 0,
            ...     cloud_nss=True,
            ...     json_array_toggle=False,
            ...     max_batch_size=512,
            ...     connection_url="http://15.222.242.150:10000/services/collector?auto_extract_timestamp=true",
            ...     connection_headers=[
            ...             "Authorization:Splunk 34de02bc-e1fa-4c24-b025-a6c8f1214991"
            ... ],
            ...     test_connectivity_display="Validation pending. Click icon to test the connectivity."
            ... )
            ... if error:
            ...     print(f"Error adding NSS Feed: {error}")
            ...     return
            ... print(f"NSS Feed added successfully: {added_feed.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds
        """
        )

        body = kwargs

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, NssFeeds)
        if error:
            return (None, response, error)

        try:
            result = NssFeeds(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_nss_feed(self, feed_id: int, **kwargs) -> tuple:
        """
        Updates cloud NSS feed configuration based on the specified ID

        Args:
            feed_id (str): The unique identifier of the cloud NSS feed
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the cloud NSS feed
            feed_status (str): The status of the feed.
            nss_log_type (str): The type of NSS logs that are streamed (e.g., Web, Firewall, DNS, Alert).
            nss_feed_type (str): NSS feed format type (e.g., CSV, syslog, Splunk Common Information Model).
            feed_output_format (str): Output format used for the feed.
            user_obfuscation (str): Specifies whether user obfuscation is enabled or disabled.
            time_zone (str): Specifies the time zone used in the output file.
            custom_escaped_character (list[str]): Characters to be encoded using hex when they appear in URL, Host, or Referrer
            eps_rate_limit (int): Event per second limit
            json_array_toggle (bool): Enables or disables streaming logs in JSON array format
            siem_type (str): Cloud NSS SIEM type.
            max_batch_size (int): The maximum batch size in KB.
            connection_url (str): The HTTPS URL of the SIEM log collection API endpoint.
            authentication_token (str): The authentication token value.
            connection_headers (list[str]): The HTTP connection headers.
            last_successful_test (int): The timestamp of the last successful test in Unix time.
            test_connectivity_code (int): The code from the last test.
            base64_encoded_certificate (str): Base64-encoded certificate.
            nss_type (str): NSS type.
            client_id (str): Client ID applicable when SIEM type is set to S3 or Azure Sentinel.
            client_secret (str): Client secret applicable when SIEM type is set to S3 or Azure Sentinel.
            authentication_url (str): Authentication URL applicable when SIEM type is set to Azure Sentinel.
            grant_type (str): Grant type applicable when SIEM type is set to Azure Sentinel.
            scope (str): Scope applicable when SIEM type is set to Azure Sentinel.
            oauth_authentication (bool): Indicates whether OAuth 2.0 authentication is enabled.
            server_ips (list): Filter to limit the logs based on the server's IPv4 addresses
            client_ips (list): Filter to limit the logs based on a client's public IPv4 addresses
            domains (list): Filter to limit the logs to sessions associated with specific domains
            dns_request_types (list): DNS request types filter
            dns_response_types (list): DNS response types filter
            dns_responses (list): DNS responses filter
            durations (list): Filter based on time durations
            dns_actions (list): DNS Control policy action filter
            firewall_logging_mode (str): Filter based on the Firewall Filtering policy logging mode.
                Supported values: SESSION, AGGREGATE, ALL
            rules (list): Policy rules filter (e.g., Firewall Filtering or DNS Control rule filter)
            nw_services (list): Firewall network services filter
            client_source_ips (list): Filter based on a client's source IPv4 address in the Firewall policy
            firewall_actions (list): Firewall and IPS Control policy actions filter
            locations (list): Location filter
            countries (list): Countries filter in the Firewall policy
            server_source_ports (list): Firewall log filter based on the traffic destination name
            client_source_ports (list): Firewall log filter based on a client's source ports
            action_filter (str): Policy action filter. Supported values: ALLOWED, BLOCKED
            email_dlp_policy_action (str): Action filter for Email DLP log type.
                Supported values: ALLOW, CUSTOMHEADERINSERTION, BLOCK
            direction (str): Traffic direction filter specifying inbound or outbound.
                Supported values: INBOUND, OUTBOUND
            event (str): CASB event filter. Supported values: SCAN, VIOLATION, INCIDENT
            policy_reasons (list): Policy reason filter
            protocol_types (list): Protocol types filter
            user_agents (list): Predefined user agents filter
            request_methods (list): Request methods filter
            casb_severity (list): Zscaler's Cloud Access Security Broker (CASB) severity filter.
                Supported values: RULE_SEVERITY_HIGH, RULE_SEVERITY_MEDIUM, RULE_SEVERITY_LOW, RULE_SEVERITY_INFO
            casb_policy_types (list): CASB policy type filter.
                Supported values: MALWARE, DLP, ALL_INCIDENT
            casb_applications (list): CASB application filter
            casb_action (list): CASB policy action filter
            casb_tenant (list): CASB tenant filter
            url_super_categories (list): URL supercategory filter
            web_applications (list): Cloud applications filter
            web_application_classes (list): Cloud application categories Filter
            malware_names (list): Filter based on malware names
            url_classes (list): URL category filter
            advanced_threats (list): Advanced threats filter
            response_codes (list): Response codes filter
            nw_applications (list): Firewall network applications filter
            nat_actions (list): NAT Control policy actions filter. Supported values: NONE, DNAT
            traffic_forwards (list): Filter based on the firewall traffic forwarding method
            web_traffic_forwards (list): Filter based on the web traffic forwarding method
            tunnel_types (list): Tunnel type filter. Supported values: GRE, IPSEC_IKEV1, IPSEC_IKEV2, SVPN, EXTRANET, ZUB, ZCB
            alerts (list): Alert filter. Supported values: CRITICAL, WARN
            object_type (list): CRM object type filter
            activity (list): CASB activity filter
            object_type1 (list): CASB activity object type filter
            object_type2 (list): CASB activity object type filter if applicable
            end_point_dlp_log_type (list): Endpoint DLP log type filter.
                Supported values: EPDLP_SCAN_AGGREGATE, EPDLP_SENSITIVE_ACTIVITY, EPDLP_DLP_INCIDENT
            email_dlp_log_type (list): Email DLP record type filter.
                Supported values: EMAILDLP_SCAN, EMAILDLP_SENSITIVE_ACTIVITY, EMAILDLP_DLP_INCIDENT
            file_type_super_categories (list): Filter based on the category of file type in download
            file_type_categories (list): Filter based on the file type in download
            casb_file_type (list): Endpoint DLP file type filter
            casb_file_type_super_categories (list): Endpoint DLP file type category filer
            external_owners (list): Filter logs associated with file owners
            external_collaborators (list): Filter logs to specific recipients outside your organization
            internal_collaborators (list): Filter logs to specific recipients within your organization
            itsm_object_type (list): ITSM object type filter
            url_categories (list): URL category filter
            dlp_engines (list): DLP engine filter
            dlp_dictionaries (list): DLP dictionary filter
            users (list): User filter
            departments (list): Department filter
            sender_name (list): Filter based on sender or owner name
            buckets (list): Filter based on public cloud storage buckets
            vpn_credentials (list): Filter based on specific VPN credentials
            message_size (list): Message size filter
            file_sizes (list): File size filter
            request_sizes (list): Request size filter
            response_sizes (list): Response size filter
            transaction_sizes (list): Transaction size filter
            inbound_bytes (list): Filter based on inbound bytes
            outbound_bytes (list): Filter based on outbound bytes
            download_time (list): Download time filter
            scan_time (list): Scan time filter
            server_source_ips (list): Filter based on the server's source IPv4 addresses in Firewall policy
            server_destination_ips (list): Filter based on the server's destination IPv4 addresses in Firewall policy
            tunnel_ips (list): Filter based on tunnel IPv4 addresses in Firewall policy
            internal_ips (list): Filter based on internal IPv4 addresses
            tunnel_source_ips (list): Source IPv4 addresses of tunnels
            tunnel_dest_ips (list): Destination IPv4 addresses of tunnels
            client_destination_ips (list): Client's destination IPv4 addresses in Firewall policy
            audit_log_type (list): Audit log type filter
            project_name (list): Repository project name filter
            repo_name (list): Repository name filter
            object_name (list): CRM object name filter
            channel_name (list): Collaboration channel name filter
            file_source (list): Filter based on the file source
            file_name (list): Filter based on the file name
            session_counts (list): Firewall logs filter based on the number of sessions
            adv_user_agents (list): Filter based on custom user agent strings
            referer_urls (list): Referrer URL filter
            hostnames (list): Filter to limit the logs based on specific hostnames
            full_urls (list): Filter to limit the logs based on specific full URLs
            threat_names (list): Filter based on threat names
            page_risk_indexes (list): Page Risk Index filter
            client_destination_ports (list): Firewall logs filter based on a client's destination
            tunnel_source_port (list): Filter based on the tunnel source port

        Returns:
            tuple: Updated cloud NSS feed resource record.

        Example:
            Update an existing rule to change its name and action:

            >>> zia.cloud_nss.update_nss_feed(
            ...    feed_id=123456,
            ...    name='New_Cloud_NSS_Feed_WebLog',
            ...    nss_log_type='WEBLOG',
            ...    user_obfuscation='ENABLED'
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds/{feed_id}
        """
        )

        body = kwargs

        # Create the request
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, NssFeeds)
        if error:
            return (None, response, error)

        try:
            result = NssFeeds(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_feed(self, feed_id: int) -> tuple:
        """
        Deletes cloud NSS feed configuration based on the specified ID

        Args:
            feed_id (str): The unique identifier for the cloud NSS feed.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.cloud_nss.delete_feed('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds/{feed_id}
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

    def list_feed_output(self, query_params=None) -> tuple:
        """
        Retrieves the default cloud NSS feed output format for different log types

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.type]`` {str}: The type of logs that you are streaming

               ``[query_params.multi_feed_type]`` {str}: This field is used to set the multi-feed type to Tunnel

                ``[query_params.field_format]`` {str}: The feed output type of your SIEM

        Returns:
            tuple: A tuple containing (Retrieve the default cloud NSS feed output format, Response, error)


        Examples:
            Get a list of all cloud application policies:
            >>> nss = zia.cloud_nss.list_feed_output()

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds/feedOutputDefaults
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
            result = response.get_results()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def test_connectivity(
        self,
        feed_id: int,
    ) -> tuple:
        """
        Tests the connectivity of cloud NSS feed based on the specified ID

        Args:
            feed_id (int): Unique identifier for the cloud NSS feed

        Returns:
            tuple: A tuple containing (Cloud NSS Connectivity Feed instance, Response, error).

        Example:
            Retrieve a Cloud NSS Connectivity Feed by its feed ID:

            >>> feed, response, error = zia.cloud_nss.test_connectivity(feed_id=123456)
            >>> if not error:
            ...    print(feed.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds/testConnectivity/{feed_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, NSSTestConnectivity)

        if error:
            return (None, response, error)

        try:
            result = NSSTestConnectivity(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def validate_feed_format(self, feed_type: str = None) -> tuple:
        """
        Validates the cloud NSS feed format and returns the validation result.

        Args:
            feed_type (str, optional): The type of log feed to validate (e.g., WEBLOG, FWLOG, CASB_FILELOG etc).

        Returns:
            tuple: A tuple containing the validated cloud NSS feed format, response, and error.

        Example:
            >>> validation_result, response, error = zia.cloud_nss.validate_feed_format(feed_type="WEBLOG")
            >>> if not error:
            ...    print(validation_result)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /nssFeeds/validateFeedFormat
            """
        )

        query_params = {"type": feed_type} if feed_type else {}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            params=query_params,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
