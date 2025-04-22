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
from zscaler.zia.models.organization_information import OrganizationInformation
from zscaler.zia.models.organization_information import OrganizationInformationLite
from zscaler.zia.models.organization_information import OrganizationSubscription
from zscaler.utils import format_url


class OrganizationInformationAPI(APIClient):
    """
    A Client object for the organization information resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_organization_information(self) -> tuple:
        """
        Retrieves the current organization information configured in the ZIA Admin Portal.

        This method makes a GET request to the ZIA Admin API and returns detailed organization information,
        including various bypass rules, DNS optimization configurations, and traffic control settings.

        Returns:
            tuple: A tuple containing:
                - OrganizationInformation: The current organization information object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current organization information:

            >>> settings, response, err = client.zia.organization_information.get_advanced_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /orgInformation
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = OrganizationInformation(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_org_info_lite(self) -> tuple:
        """
        Retrieves the current organization information configured in the ZIA Admin Portal.

        This method makes a GET request to the ZIA Admin API and returns detailed organization information,
        including various bypass rules, DNS optimization configurations, and traffic control settings.

        Returns:
            tuple: A tuple containing:
                - OrganizationInformation: The current organization information object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current organization information:

            >>> settings, response, err = client.zia.organization_information.get_advanced_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /orgInformation/lite
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = OrganizationInformationLite(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_subscriptions(self) -> tuple:
        """
        Retrieves the current organization information configured in the ZIA Admin Portal.

        This method makes a GET request to the ZIA Admin API and returns detailed organization information,
        including various bypass rules, DNS optimization configurations, and traffic control settings.

        Returns:
            tuple: A tuple containing:
                - OrganizationInformation: The current organization information object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current organization information:

            >>> settings, response, err = client.zia.organization_information.get_advanced_settings()
            >>> if err:
            ...     print(f"Error fetching settings: {err}")
            ... else:
            ...     print(f"Enable Office365: {settings.enable_office365}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /subscriptions
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            advanced_settings = OrganizationSubscription(response.get_body())
            return (advanced_settings, response, None)
        except Exception as ex:
            return (None, response, ex)
