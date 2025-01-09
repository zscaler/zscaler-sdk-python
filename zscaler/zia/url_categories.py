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

import time

from zscaler.request_executor import RequestExecutor
from zscaler.utils import chunker, convert_keys, snake_to_camel
from zscaler.api_client import APIClient
from zscaler.zia.models.urlcategory import URLCategory
from zscaler.utils import format_url

class URLCategoriesAPI(APIClient):
    """
    A Client object for the URL Categories resources.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def lookup(self, urls: list) -> list:
        """
        Lookup the category for the provided URLs.
        
        Args:
            urls (list):
                The list of URLs to perform a category lookup on.

        Returns:
            :obj:`BoxList`: A list of URL category reports.

        Examples:
            >>> zia.url_categories.lookup(['example.com', 'test.com'])
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlLookup
        """)

        results = []
        for chunk in chunker(urls, 100):
            request, error = self._request_executor.create_request(http_method, api_url, chunk, {}, {})
            if error:
                continue

            response, error = self._request_executor.execute(request)
            if error:
                continue

            results.extend(response.get_results())
            time.sleep(1)

        return results

    def review_domains_post(self, urls: list) -> list:
        """
        For the specified list of URLs, finds matching entries present in existing custom URL categories.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlCategories/review/domains
        """)

        results = []
        for chunk in chunker(urls, 100):
            request, error = self._request_executor\
                .create_request(http_method, api_url, chunk, {}, {})
            if error:
                continue

            response, error = self._request_executor\
                .execute(request)
            if error:
                continue

            results.extend(response.get_results())
            time.sleep(1)

        return results

    def review_domains_put(self, urls: list) -> list:
        """
        Adds the list of matching URLs fetched by POST via the review_domains_post method.
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlCategories/review/domains
        """)

        results = []
        for chunk in chunker(urls, 100):
            request, error = self._request_executor\
                .create_request(http_method, api_url, chunk, {}, {})
            if error:
                continue

            response, error = self._request_executor\
                .execute(request)
            if error:
                continue

            results.extend(response.get_results())
            time.sleep(1)

        return results

    def list_categories(self, custom_only: bool = False, only_counts: bool = False) -> tuple:
        """
        Returns information on URL categories.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlCategories
        """)

        params = {
            "customOnly": custom_only,
            "includeOnlyUrlKeywordCounts": only_counts,
        }

        request, error = self._request_executor\
            .create_request(http_method, api_url, {}, {}, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(URLCategory(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_quota(self) -> tuple:
        """
        Returns information on URL category quota usage.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlCategories/urlQuota
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)
        return (response.get_body(), response, None)

    def get_category(self, category_id: str) -> tuple:
        """
        Returns URL category information for the provided category.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlCategories/{category_id}
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        return (response.get_body(), response, None)

    def add_url_category(self, configured_name: str, super_category: str, urls: list, **kwargs) -> tuple:
        """
        Adds a new custom URL category.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /urlCategories
        """)

        payload = {
            "type": "URL_CATEGORY",
            "superCategory": super_category,
            "configuredName": configured_name,
            "urls": urls,
        }

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        request, error = self._request_executor\
            .create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, URLCategory)
        if error:
            return (None, response, error)

        try:
            result = URLCategory(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_tld_category(self, name: str, tlds: list, **kwargs) -> tuple:
        """
        Adds a new custom TLD category.
        """
        http_method = "post".upper()
        api_url = f"{self._zia_base_endpoint}/urlCategories"

        payload = {
            "type": "TLD_CATEGORY",
            "superCategory": "USER_DEFINED",
            "configuredName": name,
            "urls": tlds,
        }

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.get_body(), response, None)

    def update_url_category(self, category_id: str, **kwargs) -> tuple:
        """
        Updates a URL category.
        """
        http_method = "put".upper()
        api_url = f"{self._zia_base_endpoint}/urlCategories/{category_id}"

        payload = convert_keys(self.get_category(category_id))

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.get_body(), response, None)

    def add_urls_to_category(self, category_id: str, urls: list) -> tuple:
        """
        Adds URLs to a URL category.
        """
        http_method = "put".upper()
        api_url = f"{self._zia_base_endpoint}/urlCategories/{category_id}?action=ADD_TO_LIST"

        payload = convert_keys(self.get_category(category_id))
        payload["urls"] = urls

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.get_body(), response, None)

    def delete_urls_from_category(self, category_id: str, urls: list) -> tuple:
        """
        Deletes URLs from a URL category.
        """
        http_method = "put".upper()
        api_url = f"{self._zia_base_endpoint}/urlCategories/{category_id}?action=REMOVE_FROM_LIST"

        current_config = self.get_category(category_id)
        payload = {
            "configuredName": current_config["configured_name"],
            "urls": urls,
        }

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.get_status(), response, None)

    def delete_from_category(self, category_id: str, **kwargs) -> tuple:
        """
        Deletes the specified items from a URL category.
        """
        http_method = "put".upper()
        api_url = f"{self._zia_base_endpoint}/urlCategories/{category_id}?action=REMOVE_FROM_LIST"

        current_config = self.get_category(category_id)
        payload = {
            "configured_name": current_config["configured_name"],
        }

        for key, value in kwargs.items():
            payload[key] = value

        payload = convert_keys(payload)

        request, error = self._request_executor.create_request(http_method, api_url, payload, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.get_status(), response, None)

    def delete_category(self, category_id: str) -> tuple:
        """
        Deletes the specified URL category.
        """
        http_method = "delete".upper()
        api_url = f"{self._zia_base_endpoint}/urlCategories/{category_id}"

        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (response.get_status(), response, None)
