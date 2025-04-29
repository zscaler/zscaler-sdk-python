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
from zscaler.zia.models.alert_subscriptions import AlertSubscriptions
from zscaler.utils import format_url


class AlertSubscriptionsAPI(APIClient):
    """
    A Client object for the Alert Subscriptions resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_alert_subscriptions(self) -> tuple:
        """
        Retrieves a list of all alert subscriptions.

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
            /alertSubscriptions
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = AlertSubscriptions(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_alert_subscription(self, subscription_id: int) -> tuple:
        """
        Retrieves the alert subscription information based on the specified ID

        Args:
            subscription_id (int): The unique identifier for the Alert Subscription.

        Returns:
            tuple: A tuple containing (Alert Subscriptioninstance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions/{subscription_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertSubscriptions)
        if error:
            return (None, response, error)

        try:
            result = AlertSubscriptions(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_alert_subscription(self, **kwargs) -> tuple:
        """
        Adds a new alert subscription.

        Args:

        Returns:
            tuple: A tuple containing the newly added alert subscription, response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertSubscriptions)
        if error:
            return (None, response, error)

        try:
            result = AlertSubscriptions(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_alert_subscription(self, subscription_id: int, **kwargs) -> tuple:
        """
        Updates an existing alert subscription based on the specified ID

        Args:
            settings (:obj:`AlertSubscriptions`):
                An instance of `AlertSubscriptions` containing the updated configuration.

            Supported attributes:
                - block_apps_with_malicious_activity (bool): Blocks apps known to be malicious or hidden from users
                - block_apps_with_known_vulnerabilities (bool): Blocks apps with known vulnerabilities or insecure modules
                - block_apps_sending_unencrypted_user_credentials (bool): Blocks apps leaking user credentials unencrypted
                - block_apps_sending_location_info (bool): Blocks apps leaking device location unencrypted or unknown purpose
                - block_apps_sending_personally_identifiable_info (bool): Blocks apps leaking PII in unencrypted communications
                - block_apps_sending_device_identifier (bool): Blocks apps leaking device identifiers in unencrypted form
                - block_apps_communicating_with_ad_websites (bool): Blocks apps communicating with known ad websites
                - block_apps_communicating_with_remote_unknown_servers (bool): Blocks apps communicating with unknown servers

        Returns:
            tuple:
                - **MobileAdvancedThreatSettings**: The updated advanced settings object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Update mobile setting options:

            >>> malware_settings, _, err = client.zia.mobile_threat_settings.update_mobile_advanced_settings(
            ...     block_apps_with_malicious_activity = True,
            ...     block_apps_with_known_vulnerabilities = True,
            ...     block_apps_sending_unencrypted_user_credentials = True,
            ...     block_apps_sending_location_info = True,
            ...     block_apps_sending_personally_identifiable_info = True,
            ...     block_apps_sending_device_identifier = True,
            ...     block_apps_communicating_with_ad_websites = True,
            ...     block_apps_communicating_with_remote_unknown_servers = True
            ... )
            >>> if err:
            ...     print(f"Error fetching malware settings: {err}")
            ...     return
            ... print("Current malware settings fetched successfully.")
            ... print(malware_settings)
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions/{subscription_id}
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertSubscriptions)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = AlertSubscriptions(self.form_response_body(response.get_body()))
            else:
                result = AlertSubscriptions()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
