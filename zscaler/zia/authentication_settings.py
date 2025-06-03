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
from zscaler.zia.models.authentication_settings import AuthenticationSettings
from zscaler.utils import format_url
import time


class AuthenticationSettingsAPI(APIClient):
    """
    A Client object for the Authentication Settings resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_exempted_urls(self) -> tuple:
        """
        Gets a list of URLs that were exempted from cookie authentication.

        Returns:
            tuple: A tuple containing:
                - list[str]: List of domains or URLs which are exempted from SSL Inspection
                - Response: The raw HTTP response from the API.
                - error: Error details if the request fails.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings/exemptedUrls
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, dict)
        if error:
            return (None, response, error)

        try:
            bypass_urls = response.get_body().get("urls", [])
            if not isinstance(bypass_urls, list):
                raise ValueError("Unexpected response format: Exempted should be a list.")
            return (bypass_urls, response, None)
        except Exception as ex:
            return (None, response, ex)

    def add_urls_to_exempt_list(self, url_list: list) -> tuple:
        """
        Adds the provided URLs to the exempt list.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs to be added.

        Returns:
            tuple: A tuple containing (updated AuthenticationSettings instance, Response, error)

        Examples:
            >>> exempted_urls, response, error = zia.authentication_settings.add_urls_to_exempt_list(["example.com"])
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings/exemptedUrls?action=ADD_TO_LIST
            """
        )

        payload = {"urls": url_list}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, payload, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        time.sleep(2)
        return self.get_exempted_urls()

    def delete_urls_from_exempt_list(self, url_list: list) -> tuple:
        """
        Deletes the provided URLs from the exemption list.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs to be removed.

        Returns:
            tuple: A tuple containing (updated AuthenticationSettings instance, Response, error)

        Examples:
            >>> exempted_urls, response, error = zia.authentication_settings.delete_urls_from_exempt_list(["example.com"])
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings/exemptedUrls?action=REMOVE_FROM_LIST
        """
        )

        payload = {"urls": url_list}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, payload, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        time.sleep(2)
        return self.get_exempted_urls()

    def get_authentication_settings(self) -> tuple:
        """
        Retrieves the organization's default authentication settings.

        Returns:
            tuple: A tuple containing:
                - AuthenticationSettings: The current authentication settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current authentication settings:

            >>> settings, response, err = client.zia.authentication_settings.get_authentication_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Saml Enabled: {settings.saml_enabled}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            auth_settings = AuthenticationSettings(response.get_body())
            return (auth_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_authentication_settings_lite(self) -> tuple:
        """
        Retrieves the organization's default authentication settings information.

        Returns:
            tuple: A tuple containing:
                - AuthenticationSettings: The current authentication settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current authentication settings:

            >>> settings, response, err = client.zia.authentication_settings.get_authentication_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Saml Enabled: {settings.saml_enabled}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings/lite
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            auth_settings = AuthenticationSettings(response.get_body())
            return (auth_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def update_authentication_settings(self, **kwargs) -> tuple:
        """
        Updates the organization's default authentication settings information.

        Args:
            settings (:obj:`AuthenticationSettings`): An instance of `AuthenticationSettings`
            containing the updated configuration.

        Supported attributes:
            - org_auth_type (str): User authentication type. Setting this to an LDAP-based authentication
              requires a complete LdapProperties configuration.
            - one_time_auth (str): When the org_auth_type is NONE, administrators must manually
              provide the password to new end users.
            - saml_enabled (bool): Whether or not to authenticate users using SAML Single Sign-On.
            - kerberos_enabled (bool): Whether or not to authenticate users using Kerberos.
            - kerberos_pwd (str): Read-only. Can only be set through the generate KerberosPassword API.
            - auth_frequency (str): How frequently users are required to authenticate (e.g., cookie
              expiration duration).
            - auth_custom_frequency (int): Custom frequency in days for authentication. Valid range: 1-180.
            - password_strength (str): Password strength for form-based authentication.
              Supported values: NONE, MEDIUM, STRONG.
            - password_expiry (str): Password expiration for hosted DB users.
              Supported values: NEVER, ONE_MONTH, THREE_MONTHS, SIX_MONTHS.
            - last_sync_start_time (int): Epoch timestamp representing start of last LDAP sync.
            - last_sync_end_time (int): Epoch timestamp representing end of last LDAP sync.
            - mobile_admin_saml_idp_enabled (bool): Indicates use of Mobile Admin as an IdP.
            - auto_provision (bool): Enables SAML Auto-Provisioning.
            - directory_sync_migrate_to_scim_enabled (bool): Enables migration to SCIM by disabling legacy sync.

        Returns:
            tuple: A tuple containing:
                - AuthenticationSettings: The updated authentication settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, `None`.

        Examples:
            Update authentication settings:

            >>> settings, _, error = client.zia.authentication_settings.update_authentication_settings(
            ...     org_auth_type='ANY',
            ...     auth_frequency='DAILY_COOKIE',
            ... )
            >>> if error:
            ...     print(f"Error updating authentication settings: {error}")
            ... else:
            ...     print(f"Settings updated: {settings.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings
            """
        )

        body = {}
        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = AuthenticationSettings(self.form_response_body(response.get_body()))
            else:
                result = AuthenticationSettings()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
