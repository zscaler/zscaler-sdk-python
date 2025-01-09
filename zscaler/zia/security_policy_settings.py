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
from zscaler.zia.models.security_policy_settings import SecurityPolicySettings
from zscaler.utils import format_url


class SecurityPolicyAPI(APIClient):
    """
    A Client object for the Security Policy Settings resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def get_whitelist(self) -> tuple:
        """
        Returns a list of whitelisted URLs.

        Returns:
            tuple: A tuple containing (SecurityPolicySettings instance, Response, error)

        Examples:
            >>> whitelist, response, error = zia.security.get_whitelist()
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/security")

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SecurityPolicySettings)
        if error:
            return (None, response, error)

        try:
            result = SecurityPolicySettings(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_blacklist(self) -> tuple:
        """
        Returns a list of blacklisted URLs.

        Returns:
            tuple: A tuple containing (SecurityPolicySettings instance, Response, error)

        Examples:
            >>> blacklist, response, error = zia.security.get_blacklist()
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/security/advanced")

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SecurityPolicySettings)
        if error:
            return (None, response, error)

        try:
            result = SecurityPolicySettings(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def replace_whitelist(self, url_list: list) -> tuple:
        """
        Replaces the existing whitelist with the URLs provided.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs for the new whitelist.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> whitelist, response, error = zia.security.replace_whitelist(['example.com'])
        """
        http_method = "put".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/security")

        payload = {"whitelistUrls": url_list}

        request, error = self._request_executor.create_request(http_method, api_url, payload)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SecurityPolicySettings)
        if error:
            return (None, response, error)

        return self.get_whitelist()

    def add_urls_to_whitelist(self, url_list: list) -> tuple:
        """
        Adds the provided URLs to the whitelist.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs to be added.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> whitelist, response, error = zia.security.add_urls_to_whitelist(['example.com'])
        """
        whitelist, _, _ = self.get_whitelist()
        whitelist.whitelist_urls.extend(url for url in url_list if url not in whitelist.whitelist_urls)

        return self.replace_whitelist(whitelist.whitelist_urls)

    def delete_urls_from_whitelist(self, url_list: list) -> tuple:
        """
        Deletes the provided URLs from the whitelist.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs to be deleted.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> whitelist, response, error = zia.security.delete_urls_from_whitelist(['example.com'])
        """
        whitelist, _, _ = self.get_whitelist()
        whitelist.whitelist_urls = [url for url in whitelist.whitelist_urls if url not in url_list]

        return self.replace_whitelist(whitelist.whitelist_urls)

    def add_urls_to_blacklist(self, url_list: list) -> tuple:
        """
        Adds the provided URLs to the blacklist.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs to be added.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> blacklist, response, error = zia.security.add_urls_to_blacklist(['example.com'])
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/security/advanced/blacklistUrls")
        params = {"action": "ADD_TO_LIST"}
        payload = {"blacklistUrls": url_list}

        request, error = self._request_executor.create_request(http_method, api_url, payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SecurityPolicySettings)
        if error:
            return (None, response, error)

        return self.get_blacklist()

    def delete_urls_from_blacklist(self, url_list: list) -> tuple:
        """
        Deletes the provided URLs from the blacklist.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs to be deleted.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> blacklist, response, error = zia.security.delete_urls_from_blacklist(['example.com'])
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/security/advanced/blacklistUrls")
        params = {"action": "REMOVE_FROM_LIST"}
        payload = {"blacklistUrls": url_list}

        request, error = self._request_executor.create_request(http_method, api_url, payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SecurityPolicySettings)
        if error:
            return (None, response, error)

        return self.get_blacklist()

    def replace_blacklist(self, url_list: list) -> tuple:
        """
        Replaces the existing blacklist with the URLs provided.

        Args:
            url_list (:obj:`list` of :obj:`str`): The list of URLs for the new blacklist.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> blacklist, response, error = zia.security.replace_blacklist(['example.com'])
        """
        http_method = "put".upper()
        api_url = format_url(f"{self._zia_base_endpoint}/security/advanced")

        payload = {"blacklistUrls": url_list}

        request, error = self._request_executor.create_request(http_method, api_url, payload)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SecurityPolicySettings)
        if error:
            return (None, response, error)

        return self.get_blacklist()

    def erase_blacklist(self) -> tuple:
        """
        Erases all URLs in the blacklist.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> blacklist, response, error = zia.security.erase_blacklist()
        """
        return self.replace_blacklist([])

    def erase_whitelist(self) -> tuple:
        """
        Erases all URLs in the whitelist.

        Returns:
            tuple: A tuple containing (updated SecurityPolicySettings instance, Response, error)

        Examples:
            >>> whitelist, response, error = zia.security.erase_whitelist()
        """
        return self.replace_whitelist([])
