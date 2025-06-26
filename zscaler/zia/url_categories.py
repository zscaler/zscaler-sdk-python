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
from zscaler.utils import chunker
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

    def list_categories(
        self,
        query_params=None,
    ) -> tuple:
        """
        Returns information on URL categories.

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results by rule name.
                ``[query_params.custom_only]`` {bool}: If set to true, gets information on custom URL categories only.
                ``[query_params.include_only_url_keyword_counts]`` {bool}: By default this parameter is set to false.

        Returns:
            tuple: A tuple containing (list of url categories instances, Response, error)

        Examples:
            >>> category_list, _, err = client.zia.url_categories.list_categories(
            ... query_params={'search': 'CategoryExample01')
            ... if err:
            ...     print(f"Error listing url categories: {err}")
            ...     return
            ... print(f"Total url categories found: {len(category_list)}")
            ... for url in category_list:
            ...     print(url.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(URLCategory(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.configured_name.lower() if r.configured_name else "")]

        return (results, response, None)

    def get_category(self, category_id: str) -> tuple:
        """
        Returns URL category information for the provided category.

        Args:
            category_id (str):
                The unique identifier for the category (e.g. 'MUSIC')

        Returns:
            :obj:`Tuple`: The resource record for the url category.

        Examples:
            >>> fetched_category, response, error = client.zia.url_categories.get_category('EDUCATION')
            ... if error:
            ...     print(f"Error fetching url category by ID: {error}")
            ...     return
            ... print(f"Fetched url category by ID: {fetched_category.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories/{category_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, URLCategory)

        if error:
            return (None, response, error)

        try:
            result = URLCategory(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_url_category(
        self,
        super_category: str,
        urls: list = None,
        configured_name: str = None,
        **kwargs
    ) -> tuple:
        """
        Adds a new custom URL category.

        Args:
            configured_name (str): Name of the URL category. This is only required for custom URL categories.
            super_category (str): This field is required when creating custom URL categories.
            urls (list): Custom URLs to add to a URL category.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            db_categorized_urls (list):
                URLs entered will be covered by policies that reference the parent category, in addition to this one.
            description (str):
                Description of the category.
            custom_category (bool):
                Set to true for custom URL category. Up to 48 custom URL categories can be added per organisation.
            ip_ranges (list):
                Custom IP addpress ranges associated to a URL category. This feature must be enabled on your tenancy.
            ip_ranges_retaining_parent_category (list):
                The retaining parent custom IP addess ranges associated to a URL category.
            keywords (list):
                Custom keywords associated to a URL category.
            keywords_retaining_parent_category (list):
                Retained custom keywords from the parent URL category that are associated with a URL category.
            ip_ranges (list):
                Custom IP address ranges associated to a URL category. Up to 2000 custom IP address ranges can be added
            ip_ranges_retaining_parent_category (list):
                The retaining parent custom IP address ranges associated to a URL category.
                Up to 2000 custom IP address ranges can be added

        Returns:
            :obj:`Tuple`: The newly configured custom URL category resource record.

        Examples:
            Add a new category for beers that don't taste good:

            >>> added_category, _, error = client.zia.url_categories.add_url_category(
            ...     configured_name=f"NewCategory_{random.randint(1000, 10000)}",
            ...     super_category="BUSINESS_AND_ECONOMY",
            ...     description="Google Finance",
            ...     urls=['finance.google.com'],
            ...     keywords=["microsoft"],
            ...     custom_category=True,
            ...     db_categorized_urls=[".creditkarma.com", ".youku.com"]
            ... )
            ... if error:
            ...     print(f"Error adding url category: {error}")
            ...     return
            ... print(f"url category added successfully: {added_category.as_dict()}")

            Add a new category with IP ranges:

            >>> added_category, _, error = client.zia.url_categories.add_url_category(
            ...     configured_name=f"NewCategory_{random.randint(1000, 10000)}",
            ...     super_category="BUSINESS_AND_ECONOMY",
            ...     description="Google Finance",
            ...     urls=['finance.google.com'],
            ...     keywords=["microsoft"],
            ...     custom_category=True,
            ...     db_categorized_urls=[".creditkarma.com", ".youku.com"]
            ...     ip_ranges=['10.0.0.0/24']
            ... )
            ... if error:
            ...     print(f"Error adding url category: {error}")
            ...     return
            ... print(f"url category added successfully: {added_category.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories
        """
        )

        custom_category = kwargs.pop("custom_category", False)

        payload = {
            "type": "URL_CATEGORY",
            "super_category": super_category,
            "urls": urls,
            "custom_category": custom_category,
            "configured_name": configured_name,
        }

        if custom_category:
            if not configured_name:
                raise ValueError("`configured_name` is required when `custom_category=True`.")
            payload["configured_name"] = configured_name

        payload.update(kwargs)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=payload,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, URLCategory)
        if error:
            return (None, response, error)

        try:
            result = URLCategory(self.form_response_body(response.get_body()))
        except Exception as parse_error:
            return (None, response, parse_error)

        return (result, response, None)

    def add_tld_category(self, configured_name: str, tlds: list, **kwargs) -> tuple:
        """
        Adds a new custom TLD category.

        Args:
            name (str):
                The name of the TLD category.
            tlds (list):
                A list of TLDs in the format '.tld'.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            description (str):
                Description of the category.

        Returns:
            :obj:`Tuple`: New TLD URL category resource record.

        Examples:
            Create a tld category:

            >>> added_category, _, error = client.zia.url_categories.add_tld_category(
            ...     configured_name=f"NewCategory_{random.randint(1000, 10000)}",
            ...     description="Google Finance",
            ...     tlds=['.co.uk'],
            ... )
            ... if error:
            ...     print(f"Error adding url category: {error}")
            ...     return
            ... print(f"url category added successfully: {added_category.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories
        """
        )

        if not configured_name:
            raise ValueError("`configured_name` is mandatory and cannot be empty.")
        if not tlds:
            raise ValueError("`tlds` is mandatory and cannot be empty.")

        payload = {
            "type": "TLD_CATEGORY",
            "superCategory": "USER_DEFINED",
            "configuredName": configured_name,
            "urls": tlds,
        }

        payload.update(kwargs)

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=payload,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, URLCategory)

        if error:
            return (None, response, error)

        try:
            result = URLCategory(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_url_category(self, category_id: str, action: str = None, **kwargs) -> tuple:
        """
        Updates a URL category.

        This method supports two update modes with different behaviors:

        1. **Full Update** (action=None): Replaces all URLs with the provided list

           - Any URLs not included in the request will be removed from the category
           - This is equivalent to completely replacing the URL list
           - Use this when you want to set the exact list of URLs for the category

        2. **Incremental Update** (action specified): Adds or removes specific URLs while preserving existing ones

           - `ADD_TO_LIST`: Adds new URLs to the existing list (preserves all current URLs)
           - `REMOVE_FROM_LIST`: Removes specified URLs from the existing list (preserves other URLs)
           - Use this when you want to modify the existing URL list without affecting other URLs

        **Note**: For incremental URL operations, you may also use the specialized functions:

        - :meth:`add_urls_to_category` - Convenience method for adding URLs (equivalent to action="ADD_TO_LIST")
        - :meth:`delete_urls_from_category` - Convenience method for removing URLs (equivalent to action="REMOVE_FROM_LIST")

        Args:
            category_id (str):
                The unique identifier of the URL category.
            action (str, optional):
                The action to perform for incremental updates.
                - `ADD_TO_LIST`: Add URLs to the category (preserves existing URLs)
                - `REMOVE_FROM_LIST`: Remove URLs from the category (preserves existing URLs)
                - None: Perform full update (replaces all URLs with provided list)
            **kwargs:
                Optional keyword args.

        Keyword Args:
            configured_name (str):
                The name of the URL category.
            urls (list):
                Custom URLs to add/remove/replace in the URL category.
                - For full updates: This list replaces all existing URLs
                - For incremental updates: This list is added to or removed from existing URLs
            db_categorized_urls (list):
                URLs entered will be covered by policies that reference the parent category, in addition to this one.
            description (str):
                Description of the category.
            ip_ranges (list):
                Custom IP address ranges associated to a URL category. This feature must be enabled on your tenancy.
            ip_ranges_retaining_parent_category (list):
                The retaining parent custom IP address ranges associated to a URL category.
            keywords (list):
                Custom keywords associated to a URL category.
            keywords_retaining_parent_category (list):
                Retained custom keywords from the parent URL category that are associated with a URL category.

        Returns:
            :obj:`Tuple`: The updated url category resource record.

        Examples:
            Full update - replace all URLs:

            >>> update_category, _, error = client.zia.url_categories.update_url_category(
            ...     category_id="EDUCATION",
            ...     configured_name="Updated Education Category",
            ...     description="University websites",
            ...     urls=['.edu', 'harvard.edu', 'mit.edu'],
            ... )
            >>> if error:
            ...     print(f"Error updating url category: {error}")
            ...     return
            ... print(f"url category updated successfully: {update_category.as_dict()}")

            Incremental update - add URLs to existing list:

            >>> update_category, _, error = client.zia.url_categories.update_url_category(
            ...     category_id="CUSTOM_01",
            ...     action="ADD_TO_LIST",
            ...     urls=['new-site1.com', 'new-site2.com'],
            ... )
            >>> if error:
            ...     print(f"Error adding URLs to category: {error}")
            ...     return
            ... print(f"URLs added successfully: {update_category.as_dict()}")

            Incremental update - remove URLs from existing list:

            >>> update_category, _, error = client.zia.url_categories.update_url_category(
            ...     category_id="CUSTOM_01",
            ...     action="REMOVE_FROM_LIST",
            ...     urls=['old-site1.com', 'old-site2.com'],
            ... )
            >>> if error:
            ...     print(f"Error removing URLs from category: {error}")
            ...     return
            ... print(f"URLs removed successfully: {update_category.as_dict()}")

            Alternative using specialized functions:

            Equivalent to action="ADD_TO_LIST"

            >>> update_category, _, error = client.zia.url_categories.add_urls_to_category(
            ...     category_id="CUSTOM_01",
            ...     urls=['new-site.com'],
            ... )

            Equivalent to action="REMOVE_FROM_LIST"

            >>> update_category, _, error = client.zia.url_categories.delete_urls_from_category(
            ...     category_id="CUSTOM_01",
            ...     urls=['old-site.com'],
            ... )
        """
        http_method = "put".upper()

        base_url = f"{self._zia_base_endpoint}/urlCategories/{category_id}"
        if action:
            if action not in ["ADD_TO_LIST", "REMOVE_FROM_LIST"]:
                raise ValueError("action must be either 'ADD_TO_LIST' or 'REMOVE_FROM_LIST'")
            api_url = format_url(f"{base_url}?action={action}")
        else:
            api_url = format_url(base_url)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, URLCategory)
        if error:
            return (None, response, error)

        try:
            result = URLCategory(self.form_response_body(response.get_body()))
        except Exception as parse_error:
            return (None, response, parse_error)

        return (result, response, None)

    def add_urls_to_category(self, category_id: str, **kwargs) -> tuple:
        """
        Adds URLS to a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to add to a URL category.

        Returns:
            :obj:`Tuple`: The urls added to a category record.

        Examples:
            >>> update_category, _, error = client.zia.url_categories.add_urls_to_category(
            ...     category_id='CUSTOM_01',
            ...     configured_name=f"NewCustomCategory{random.randint(1000, 10000)}",
            ...     urls=['finance1.google.com', 'finance2.google.com', 'finance3.google.com'],
            ... )
            ... if error:
            ...     print(f"Error updating url category: {error}")
            ...     return
            ... print(f"url category updated successfully: {update_category.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories/{category_id}?action=ADD_TO_LIST
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response, error = self._request_executor.execute(request, URLCategory)
        if error:
            return (None, response, error)

        try:
            result = URLCategory(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_urls_from_category(self, category_id: str, **kwargs) -> tuple:
        """
        Deletes URLS from a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to delete from a URL category.

        Returns:
            :obj:`Tuple`: The updated URL category resource record.

        Examples:

            Remove the URL finance1.google.com from the list

            >>> update_category, _, error = client.zia.url_categories.delete_urls_from_category(
            ...     category_id=added_category.id,
            ...     configured_name=added_category.configured_name,
            ...     urls=['finance2.google.com', 'finance3.google.com'],
            ... )
            ... if error:
            ...     print(f"Error updating url category: {error}")
            ...     return
            ... print(f"url category updated successfully: {update_category.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories/{category_id}?action=REMOVE_FROM_LIST
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response, error = self._request_executor.execute(request, URLCategory)
        if error:
            return (None, response, error)

        try:
            result = URLCategory(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_category(self, category_id: str) -> tuple:
        """
        Deletes the specified URL category.

        Args:
            category_id (str):
                The unique identifier for the category.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, _, err = client.zia.url_categories.delete_category(CUSTOM_01)
            ... if err:
            ...     print(f"Error deleting url category: {err}")
            ...     return
            ... print(f"url category with ID {CUSTOM_01} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories/{category_id}
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

    def lookup(self, urls: list) -> list:
        """
        Lookup the category for the provided URLs.

        Args:
            urls (list):
                The list of URLs to perform a category lookup on.

        Returns:
            :obj:`Tuple`: A list of URL category reports.

        Examples:
            >>> results, error = client.zia.url_categories.lookup(urls=["google.com, acme.com])
            >>> if error:
            ...     print(f"Error during URL lookup: {error}")
            ...     return
            ... print("URL Lookup Results:")
            ... for entry in results:
            ...     print(entry)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlLookup
        """
        )

        results = []
        for chunk in chunker(urls, 100):
            request, error = self._request_executor.create_request(http_method, api_url, chunk)
            if error:
                return None, error

            response, error = self._request_executor.execute(request)
            if error:
                return None, error

            results.extend(response.get_results())
            time.sleep(1)

        return results, None

    def review_domains_post(self, urls: list) -> list:
        """
        For the specified list of URLs, finds matching entries present in existing custom URL categories.

        Args:
            urls (str): The list of URLs that has a match in one or more existing custom URL categories
            domain_type: (str): The domain type of the URL. Supported Values: `WILDCARD`, `SUBDOMAIN`.
            matches  (list): Information about the list of categories where a URL match is found
                id: (str): The unique identifier assigned to the custom URL category
                name: (str): This attribute is populated with the name configured by the admin in the case of custom categories

        Returns:
            :obj:`Tuple`: The url matches in one or more existing custom URL categories

        Examples:
            >>> urls = ["acme.microsoft.com"]
            ... results = client.zia.url_categories.review_domains_post(urls)
            ... if not results:
            ...     print("No matches found in custom categories.")
            ...     return
            ... print("Matched results:")
            ... for item in results:
            ...     print(item)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories/review/domains
        """
        )

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

    def review_domains_put(self, urls: list) -> list:
        """
        For the specified list of URLs, finds matching entries present in existing custom URL categories.

        Args:
            urls (str): The list of URLs that has a match in one or more existing custom URL categories

        Returns:
            :obj:`Tuple`: The url matches in one or more existing custom URL categories

        Examples:
            >>> urls = ["acme.microsoft.com"]
            ... results = client.zia.url_categories.review_domains_put(urls)
            ... if not results:
            ...     print("No matches found in custom categories.")
            ...     return
            ... print("Matched results:")
            ... for item in results:
            ...     print(item)
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories/review/domains
        """
        )

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

    def get_quota(self) -> tuple:
        """
        Returns information on URL category quota usage.

        Returns:
            :obj:`Tuple`: The URL quota statistics.

        Examples:
            >>> quota = client.zia.url_categories.get_quota()
            ... print(quota)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /urlCategories/urlQuota
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            raise Exception(f"Error creating request: {error}")

        response, error = self._request_executor.execute(request)
        if error:
            raise Exception(f"Error executing request: {error}")

        return response.get_body()
