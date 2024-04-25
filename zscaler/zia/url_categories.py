# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import time

from box import Box, BoxList
from requests import Response

from zscaler.utils import chunker, convert_keys, snake_to_camel
from zscaler.zia import ZIAClient


class URLCategoriesAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def lookup(self, urls: list) -> BoxList:
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

        if len(urls) > 100:
            results = BoxList()
            for chunk in chunker(urls, 100):
                results.extend(self._post("urlLookup", json=chunk))
                time.sleep(1)
            return results

        else:
            payload = urls
            return self.rest.post("urlLookup", json=payload)

    def list_categories(self, custom_only: bool = False, only_counts: bool = False) -> BoxList:
        """
        Returns information on URL categories.

        Args:
            custom_only (bool):
                Returns only custom categories if True.
            only_counts (bool):
                Returns only URL and keyword counts if True.

        Returns:
            :obj:`BoxList`: A list of information for all or custom URL categories.

        Examples:
            List all URL categories:

            >>> zia.url_categories.list_categories()

            List only custom URL categories:

            >>> zia.url_categories.list_categories(custom_only=True)

        """
        payload = {
            "customOnly": custom_only,
            "includeOnlyUrlKeywordCounts": only_counts,
        }

        return self.rest.get("urlCategories", params=payload)

    def get_category_by_name(self, name):
        categories = self.list_categories()
        for category in categories:
            if category.get("configured_name") == name:
                return category
        return None

    def get_quota(self) -> Box:
        """
        Returns information on URL category quota usage.

        Returns:
            :obj:`Box`: The URL quota statistics.

        Examples:
            >>> zia.url_categories.get_quota()

        """

        return self.rest.get("urlCategories/urlQuota")

    def get_category(self, category_id: str) -> Box:
        """
        Returns URL category information for the provided category.

        Args:
            category_id (str):
                The unique identifier for the category (e.g. 'MUSIC')

        Returns:
            :obj:`Box`: The resource record for the category.

        Examples:
            >>> zia.url_categories.get_category('ALCOHOL_TOBACCO')

        """
        return self.rest.get(f"urlCategories/{category_id}")

    def add_url_category(self, configured_name: str, super_category: str, urls: list, **kwargs) -> Box:
        """
        Adds a new custom URL category.

        Args:
            name (str):
                Name of the URL category.
            super_category (str):
                The name of the parent category.
            urls (list):
                Custom URLs to add to a URL category.
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

        Returns:
            :obj:`Box`: The newly configured custom URL category resource record.

        Examples:
            Add a new category for beers that don't taste good:

            >>> zia.url_categories.add_url_category(name='Beer',
            ...    super_category='ALCOHOL_TOBACCO',
            ...    urls=['xxxx.com.au', 'carltondraught.com.au'],
            ...    description="Beers that don't taste good.")

            Add a new category with IP ranges:

            >>> zia.url_categories.add_url_category(name='Beer',
            ...    super_category='FINANCE',
            ...    urls=['finance.google.com'],
            ...    description="Google Finance.",
            ...    ip_ranges=['10.0.0.0/24'])

        """

        payload = {
            "type": "URL_CATEGORY",
            "superCategory": super_category,
            "configuredName": configured_name,
            "urls": urls,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("urlCategories", json=payload)
        if isinstance(response, Response):
            # Handle error response
            status_code = response.status_code
            if status_code != 200:
                raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def add_tld_category(self, name: str, tlds: list, **kwargs) -> Box:
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
            :obj:`Box`: The newly configured custom TLD category resource record.

        Examples:
            Create a category for all 'developer' sites:

            >>> zia.url_categories.add_tld_category(name='Developer Sites',
            ...    urls=['.dev'],
            ...    description="Sites that are likely run by developers.")

        """

        payload = {
            "type": "TLD_CATEGORY",
            "superCategory": "USER_DEFINED",  # TLDs can only be added in USER_DEFINED category
            "configuredName": name,
            "urls": tlds,  # ZIA API reuses the 'urls' key for tlds
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("urlCategories", json=payload)
        if isinstance(response, Response):
            # Handle error response
            status_code = response.status_code
            if status_code != 200:
                raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_url_category(self, category_id: str, **kwargs) -> Box:
        """
        Updates a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            name (str):
                The name of the URL category.
            urls (list):
                Custom URLs to add to a URL category.
            db_categorized_urls (list):
                URLs entered will be covered by policies that reference the parent category, in addition to this one.
            description (str):
                Description of the category.
            ip_ranges (list):
                Custom IP addpress ranges associated to a URL category. This feature must be enabled on your tenancy.
            ip_ranges_retaining_parent_category (list):
                The retaining parent custom IP addess ranges associated to a URL category.
            keywords (list):
                Custom keywords associated to a URL category.
            keywords_retaining_parent_category (list):
                Retained custom keywords from the parent URL category that are associated with a URL category.

        Returns:
            :obj:`Box`: The updated URL category resource record.

        Examples:
            Update the name of a category:

            >>> zia.url_categories.update_url_category('CUSTOM_01',
            ...    name="Wines that don't taste good.")

            Update the urls of a category:

            >>> zia.url_categories.update_url_category('CUSTOM_01',
            ...    urls=['www.yellowtailwine.com'])

        """

        payload = convert_keys(self.get_category(category_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.put(f"urlCategories/{category_id}", json=payload)
        if isinstance(response, Response) and not response.ok:
            # Handle error response
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

        # Return the updated object
        return self.get_category(category_id)

    def add_urls_to_category(self, category_id: str, urls: list) -> Box:
        """
        Adds URLS to a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to add to a URL category.

        Returns:
            :obj:`Box`: The updated URL category resource record.

        Examples:
            >>> zia.url_categories.add_urls_to_category('CUSTOM_01',
            ...    urls=['example.com'])

        """

        payload = convert_keys(self.get_category(category_id))
        payload["urls"] = urls

        response = self.rest.put(f"urlCategories/{category_id}?action=ADD_TO_LIST", json=payload)
        if isinstance(response, Response) and not response.ok:
            # Handle error response
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def delete_urls_from_category(self, category_id: str, urls: list) -> Box:
        """
        Deletes URLS from a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to delete from a URL category.

        Returns:
            :obj:`Box`: The updated URL category resource record.

        Examples:
            >>> zia.url_categories.delete_urls_from_category('CUSTOM_01',
            ...    urls=['example.com'])

        """
        current_config = self.get_category(category_id)
        payload = {
            "configuredName": current_config["configured_name"],
            "urls": urls,
        }  # Required for successful call

        return self.rest.put(f"urlCategories/{category_id}?action=REMOVE_FROM_LIST", json=payload)

    def delete_from_category(self, category_id: str, **kwargs):
        """
        Deletes the specified items from a URL category.

        Args:
            category_id (str):
                The unique id for the URL category.
            **kwargs:
                Optional parameters.

        Keyword Args:
            keywords (list):
                A list of keywords that will be deleted.
            keywords_retaining_parent_category (list):
                A list of keywords retaining their parent category that will be deleted.
            urls (list):
                A list of URLs that will be deleted.
            db_categorized_urls (list):
                A list of URLs retaining their parent category that will be deleted

        Returns:
            :obj:`Box`: The updated URL category resource record.

        Examples:
            Delete URLs retaining parent category from a custom category:

            >>> zia.url_categories.delete_from_category(
            ...    category_id="CUSTOM_01",
            ...    db_categorized_urls=['twitter.com'])

            Delete URLs and URLs retaining parent category from a custom category:

            >>> zia.url_categories.delete_from_category(
            ...    category_id="CUSTOM_01",
            ...    urls=['news.com', 'cnn.com'],
            ...    db_categorized_urls=['google.com, bing.com'])

        """
        current_config = self.get_category(category_id)

        payload = {
            "configured_name": current_config["configured_name"],  # Required for successful call
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self.rest.put(f"urlCategories/{category_id}?action=REMOVE_FROM_LIST", json=payload)

    def delete_category(self, category_id: str) -> int:
        """
        Deletes the specified URL category.

        Args:
            category_id (str):
                The unique identifier for the category.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.url_categories.delete_category('CUSTOM_01')

        """
        return self.rest.delete(f"urlCategories/{category_id}").status_code
