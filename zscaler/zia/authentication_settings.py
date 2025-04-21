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

        Examples:
            >>> urls, response, err = client.zia.authentication_settings.get_exempted_urls()
            >>> if not err:
            ...     print("Listed URLs:", urls)
        """

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings/exemptedUrls
        """
        )

        request, error = self._request_executor\
            .create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
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

        # Prepare request body and headers
        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, payload, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

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

        # Prepare request body and headers
        body = {}
        headers = {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, payload, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)

        if error:
            return (None, response, error)
        time.sleep(2) 
        return self.get_exempted_urls()

    def get_authentication_settings(self) -> tuple:
        """
        Retrieves the organization's default authentication settings information, including authentication profile and Kerberos authentication information.

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

        request, error = self._request_executor.\
            create_request(
            http_method, api_url
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)

        if error:
            return (None, response, error)

        try:
            auth_settings = AuthenticationSettings(response.get_body())
            return (auth_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_authentication_settings_lite(self) -> tuple:
        """
        Retrieves the organization's default authentication settings information, including authentication profile and Kerberos authentication information.

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

        request, error = self._request_executor.\
            create_request(
            http_method, api_url
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)

        if error:
            return (None, response, error)

        try:
            auth_settings = AuthenticationSettings(response.get_body())
            return (auth_settings, response, None)
        except Exception as ex:
            return (None, response, ex)
           
    def update_authentication_settings(self, settings: AuthenticationSettings) -> tuple:
        """
        Updates the organization's default authentication settings information.

        Args:
            settings (:obj:`AuthenticationSettings`): 
                An instance of `AuthenticationSettings` containing the updated configuration.

                Supported attributes:
                    **Authentication Settings:**
                    - **org_auth_type (str)**: User authentication type. Setting it to an LDAP-based authentication requires a complete LdapProperties configuration.
                    - **one_time_auth (str)**: When the orgAuthType is NONE, administrators must manually provide the password to new end users.
                    - **saml_enabled (bool)**: Whether or not to authenticate users using SAML Single Sign-On.            
                    - **kerberos_enabled (bool)**: Whether or not to authenticate users using Kerberos
                    - **kerberos_pwd (str)**: Read Only. Kerberos password can only be set through generateKerberosPassword api.
                    - **auth_frequency (str)**: How frequently the users are required to authenticate (i.e., cookie expiration duration after a user is first authenticated).                  
                    - **auth_custom_frequency (int)**: How frequently the users are required to authenticate. This field is customized to set the value in days. Valid range is 1-180.
                    - **password_strength (str)**: Password strength required for form-based authentication of hosted DB users. Supported values: NONE, MEDIUM, STRONG
                    - **password_expiry (str)**: Password expiration required for form-based authentication of hosted DB users. Supported values: NEVER, ONE_MONTH, THREE_MONTHS, SIX_MONTHS
                    - **last_sync_start_time (int)**: Timestamp (epoch time in seconds) corresponding to the start of the last LDAP sync.                   
                    - **last_sync_end_time (int)**: Timestamp (epoch time in seconds) corresponding to the end of the last LDAP sync.
                    - **mobile_admin_saml_idp_enabled (bool)**: Indicate the use of Mobile Admin as IdP
                    - **auto_provision (bool)**: Enable SAML Auto-Provisioning
                    - **directory_sync_migrate_to_scim_enabled (bool)**: Enable to disable directory synchronization for this user repository type so you can enable SCIM provisioning or SAML auto-provisioning.
                                                                                                                                            
        Returns:
            tuple: A tuple containing:
                - AuthenticationSettings: The updated authentication settings object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the update failed; otherwise, `None`.

        Examples:
            Update Authentication Settings by enabling saml_enabled and auth_frequency:

            >>> settings, response, err = client.zia.authentication_settings.update_authentication_settings()
            >>> if not err:
            ...     settings.saml_enabled = True
            ...     settings.auth_frequency = "DAILY_COOKIE"
            ...     updated_settings, response, err = client.zia.authentication_settings.update_authentication_settings(settings)
            ...     if not err:
            ...         print(f"Updated Saml Enabled: {updated_settings.saml_enabled}")
            ...     else:
            ...         print(f"Failed to update settings: {err}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /authSettings
            """
        )

        payload = settings.request_format()

        request, error = self._request_executor.\
            create_request(
            http_method, api_url, payload
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.\
            execute(request)

        if error:
            return (None, response, error)

        time.sleep(1)
        return self.get_authentication_settings()