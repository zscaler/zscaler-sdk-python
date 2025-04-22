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
from zscaler.zia.models.endusernotification import EndUserNotification
from zscaler.utils import format_url


class EndUserNotificationAPI(APIClient):
    """
    A Client object for the Advanced Threat Protection Policy resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_eun_settings(self) -> tuple:
        """
        Retrieves the current End User Notification configured in the ZIA Admin Portal.

        This method makes a GET request to the ZIA Admin API and returns detailed End User Notification settings,

        Returns:
            tuple: A tuple containing:
                - EndUserNotification: The current end user notification settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Example:
            Fetch and print the current EUN settings:

            >>> settings, response, err = client.zia.end_user_notification.get_eun_settings()
            >>> if not err:
            ...     print(f"Notification Type: {settings['notification_type']}")
            ...     print(f"Support Email: {settings['support_email']}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /eun
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = EndUserNotification(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_eun_settings(self, **kwargs) -> tuple:
        """
        Updates advanced threat protection settings in the ZIA Admin Portal.

        This method pushes updated advanced threat protection policy settings.

        Args:
            settings (:obj:`EndUserNotification`):
                An instance of `EndUserNotification` containing the updated configuration.

                Supported attributes:
                    - aup_frequency (str): How often AUP is shown.
                        Values: NEVER, SESSION, DAILY, WEEKLY, ONLOGIN, CUSTOM, ON_DATE, ON_WEEKDAY
                    - aup_custom_frequency (int): Custom frequency (in days) to show AUP. Range: 1 to 180
                    - aup_day_offset (int): Day of week or month to show AUP. Range: 1 to 31
                    - aup_message (str): The acceptable use message shown in the AUP
                    - notification_type (str): EUN type. Values: DEFAULT, CUSTOM
                    - display_reason (bool): Show reason for blocking/cautioning access to a site, file, or app
                    - display_comp_name (bool): Show organization's name in the EUN
                    - display_comp_logo (bool): Show organization's logo in the EUN
                    - custom_text (str): Custom EUN message shown to users
                    - url_cat_review_enabled (bool): Enable/disable URL Categorization review notification
                    - url_cat_review_submit_to_security_cloud (bool): Submit URL review requests to Zscaler
                    - url_cat_review_custom_location (str): URL to send review requests for blocked URLs
                    - url_cat_review_text (str): Message shown in URL Categorization notification
                    - security_review_enabled (bool): Enable/disable Security Violation review notification
                    - security_review_submit_to_security_cloud (bool): Submit Security Violation reviews to Zscaler
                    - security_review_custom_location (str): URL to send review requests for misclassified URLs
                    - security_review_text (str): Message shown in Security Violation notification
                    - web_dlp_review_enabled (bool): Enable/disable Web DLP Violation notification
                    - web_dlp_review_submit_to_security_cloud (bool): Submit Web DLP reviews to Zscaler
                    - web_dlp_review_custom_location (str): URL to send Web DLP policy violation review requests
                    - web_dlp_review_text (str): Message shown in Web DLP Violation notification
                    - redirect_url (str): Redirect URL used with custom notification type
                    - support_email (str): IT support contact email
                    - support_phone (str): IT support contact phone number
                    - org_policy_link (str): URL to org's policy page. Required for default notification type
                    - caution_again_after (int): Time interval to repeat caution notification
                    - caution_per_domain (bool): Show caution per domain for unknown or misc. categories
                    - caution_custom_text (str): Custom message in the caution notification
                    - idp_proxy_notification_text (str): Message shown in IdP Proxy notification
                    - quarantine_custom_notification_text (str): Message shown in quarantine notification
        Returns:
            tuple: A tuple containing:
                - EndUserNotification: The updated end user notification settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, `None`.

        Example:
            Update and apply EUN settings:

            >>> eun_settings, response, err = client.zia.end_user_notification.get_eun_settings()
            >>> if not err:
            ...     eun_settings['notification_type'] = "CUSTOM"
            ...     eun_settings['support_email'] = "support@example.com"
            ...     updated_settings, response, err = client.zia.end_user_notification.update_eun_settings(eun_settings)
            ...     if not err:
            ...         print("EUN settings updated successfully.")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /eun
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EndUserNotification)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = EndUserNotification(self.form_response_body(response.get_body()))
            else:
                result = EndUserNotification()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
