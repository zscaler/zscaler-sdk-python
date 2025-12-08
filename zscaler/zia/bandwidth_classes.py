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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.bandwidth_classes import BandwidthClasses
from zscaler.utils import format_url


class BandwidthClassesAPI(APIClient):
    """
    A Client object for the Bandwidth Classes resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_classes(self, query_params: Optional[dict] = None) -> List[BandwidthClasses]:
        """
        Retrieves a list of bandwidth classes for an organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:

        Examples:
            List Bandwidth Classes All:

            >>> classes_list, _, error = client.zia.bandwidth_classes.list_classes(
                query_params={'search': BWD_Classes01})
            >>> if error:
            ...     print(f"Error listing classes: {error}")
            ...     return
            ... print(f"Total Classes found: {len(classes_list)}")
            ... for bwd in classes_list:
            ...     print(bwd.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthClasses
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        response = self._request_executor.execute(request)
        results = []
        for item in response.get_results():
            results.append(BandwidthClasses(self.form_response_body(item)))
        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return results

    def list_classes_lite(self) -> List[BandwidthClasses]:
        """
        Fetches a specific bandwidth class lite by ID.

        Args:
            bwd_id (int): The unique identifier for the Bandwidth Class Lite.

        Returns:

        Examples:
            List Bandwidth Classes All:

            >>> classes_list, _, error = client.zia.bandwidth_classes.list_classes_lite(
                query_params={'search': BWD_Classes01})
            >>> if error:
            ...     print(f"Error listing classes: {error}")
            ...     return
            ... print(f"Total Classes found: {len(classes_list)}")
            ... for bwd in classes_list:
            ...     print(bwd.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthClasses/lite
        """
        )

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request, BandwidthClasses)
        result = []
        for item in response.get_results():
            result.append(BandwidthClasses(self.form_response_body(item)))
        return result

    def get_class(self, class_id: int) -> BandwidthClasses:
        """
        Fetches a specific bandwidth class by ID.

        Args:
            class_id (int): The unique identifier for the Bandwidth Class.

        Returns:

        Examples:
            List Bandwidth Classes All:

            >>> fetched_class, _, error = client.zia.bandwidth_classes.get_class(updated_class.id)
            >>>     if error:
            ...         print(f"Error fetching class by ID: {error}")
            ...         return
            ...     print(f"Fetched class by ID: {fetched_class.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthClasses/{class_id}
        """
        )

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request, BandwidthClasses)
        result = BandwidthClasses(self.form_response_body(response.get_body()))
        return result

    def add_class(self, **kwargs) -> BandwidthClasses:
        """
        Creates a new ZIA Bandwidth Class.

        Keyword Args:
            name (str): Name of the bandwidth class
            web_applications (:obj:`list` of :obj:`str`): The web conferencing applications included in the bandwidth class.
            urls (:obj:`list` of :obj:`str`): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            url_categories (:obj:`list` of :obj:`str`): The URL categories to add to the bandwidth class

        Returns:

        Examples:
            Create Bandwidth Classes:

            >>> added_class, _, error = client.zia.bandwidth_classes.add_class(
            ...     name=f"NewBDW_{random.randint(1000, 10000)}",
            ...     web_applications=["ACADEMICGPT", "AD_CREATIVES"],
            ...     urls=["chatgpt.com"],
            ...     url_categories=["ADULT_THEMES", "ADULT_SEX_EDUCATION"],
            ... )
            >>> if error:
            ...     print(f"Error adding class: {error}")
            ...     return
            ... print(f"Class added successfully: {added_class.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthClasses
        """
        )

        body = kwargs

        request = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response = self._request_executor.execute(request, BandwidthClasses)
        result = BandwidthClasses(self.form_response_body(response.get_body()))
        return result

    def update_class(self, class_id: int, **kwargs) -> BandwidthClasses:
        """
        Updates information for the specified ZIA Bandwidth Class.

        Args:
            class_id (int): The unique ID for the Bandwidth Class.

        Returns:

        Examples:
            Update Bandwidth Classes:

            >>> updated_class, _, error = client.zia.bandwidth_classes.update_class(
            ...     class_id='125245'
            ...     name=f"UpdateBDW_{random.randint(1000, 10000)}",
            ...     web_applications=["ACADEMICGPT", "AD_CREATIVES"],
            ...     urls=["chatgpt.com"],
            ...     url_categories=["ADULT_THEMES", "ADULT_SEX_EDUCATION"],
            ... )
            >>> if error:
            ...     print(f"Error adding class: {error}")
            ...     return
            ... print(f"Class added successfully: {updated_class.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthClasses/{class_id}
        """
        )
        body = {}

        body.update(kwargs)

        request = self._request_executor.create_request(http_method, api_url, body, {}, {})
        response = self._request_executor.execute(request, BandwidthClasses)
        result = BandwidthClasses(self.form_response_body(response.get_body()))
        return result

    def delete_class(self, class_id: int) -> None:
        """
        Deletes the specified Bandwidth Class.

        Args:
            class_id (int): The unique identifier of the Bandwidth Class.

        Returns:

        Examples:
            Delete a Bandwidth Classes:

            >>> _, _, error = client.zia.bandwidth_classes.delete_class('125454')
            >>>     if error:
            ...         print(f"Error deleting class: {error}")
            ...         return
            ...     print(f"Class with ID {'125454'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /bandwidthClasses/{class_id}
        """
        )

        params = {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
