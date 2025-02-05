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

        request, error = self._request_executor\
            .create_request(
            http_method, api_url
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = EndUserNotification(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_eun_settings(self, settings: EndUserNotification) -> tuple:
        """
        Updates advanced threat protection settings in the ZIA Admin Portal.

        This method pushes updated advanced threat protection policy settings.

        Args:
            settings (:obj:`AdvancedThreatProtectionSettings`): 
                An instance of `AdvancedThreatProtectionSettings` containing the updated configuration.

                Supported attributes:
                    - aup_frequency (str): The frequency at which the Acceptable Use Policy (AUP) is shown to the end users
                        Supported values: NEVER, SESSION, DAILY, WEEKLY, ONLOGIN, CUSTOM, ON_DATE, ON_WEEKDAY
                    - aup_custom_frequency (int): The custom frequency (in days) for showing the AUP to the end users. Valid range is 1 to 180.
                    - aup_day_offset (int): Specifies which day of the week or month the AUP is shown for users when aupFrequency is set. Valid range is 1 to 31.
                    - aup_message: (str): The acceptable use statement that is shown in the AUP
                    - notification_type: (str): The type of EUN as default or custom. Supported vlues: DEFAULT, CUSTOM
                    - display_reason: (bool): Whether or not the reason for cautioning or blocking access to a site, file, or application is shown when triggered
                    - display_comp_name: (bool): Whether the organization's name appears in the EUN or not
                    - display_comp_logo: (bool): Whether your organization's logo appears in the EUN or not
                    - custom_text: (str): The custom text shown in the EUN
                    - url_cat_review_enabled: (bool): Whether the URL Categorization notification is enabled or disabled
                    - url_cat_review_submit_to_security_cloud: (bool): Whether users' review requests for possibly misclassified URLs are submitted to the Zscaler service
                    - url_cat_review_custom_location: (str): A custom URL location where users' review requests for blocked URLs are sent
                    - url_cat_review_text: (str): The message that appears in the URL Categorization notification
                    - security_review_enabled: (bool): Whether the Security Violation notification is enabled or disabled
                    - security_review_submit_to_security_cloud: (bool): Whether users' review requests for blocked URLs are submitted to the Zscaler service
                    - security_review_custom_location: (str): A custom URL location where users' review requests for possible misclassified URLs are sent
                    - security_review_text: (str): The message that appears in the Security Violation notification
                    - web_dlp_review_enabled: (bool): Whether the Web DLP Violation notification is enabled or disabled    
                    - web_dlp_review_submit_to_security_cloud: (bool): Whether users' review requests for web DLP policy violation are submitted to the Zscaler service
                    - web_dlp_review_custom_location: (str): A custom URL location where users' review requests for the web DLP policy violation are sent              
                    - web_dlp_review_text: (str): The message that appears in the Web DLP Violation notification
                    - redirect_url: (str): The redirect URL for the external site hosting the EUN specified when the custom notification type is selected
                    - support_email: (str): The email address for writing to IT Support
                    - support_phone: (str): The phone number for contacting IT Support
                    - org_policy_link: (str): The URL of the organization's policy page. This field is required for the default notification type.
                    - caution_gain_after: (int): The time interval at which the caution notification is shown when users continue browsing a restricted site.
                    - caution_per_domain: (bool): Specifies whether to display the caution notification at a specific time interval for URLs in the Miscellaneous or Unknown category.                
                    - caution_custom_text: (str): The custom message that appears in the caution notification
                    - idp_proxy_notification_text: (str): The message that appears in the IdP Proxy notification
                    - quarantine_custom_notification_text: (str): The message that appears in the quarantine notification                                                                                                                                                
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

        payload = settings.request_format()

        request, error = self._request_executor\
            .create_request(
            http_method, api_url, payload
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)

        # Fetch updated settings from API after successful update
        return self.get_eun_settings()
