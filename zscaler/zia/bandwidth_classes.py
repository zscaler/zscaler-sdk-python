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
from zscaler.zia.models.bandwidth_classes import BandwidthClasses
from zscaler.utils import format_url


class BandwidthClassesAPI(APIClient):
    """
    A Client object for the Bandwidth Classes resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_classes(self, query_params=None) -> tuple:
        """
        Retrieves a list of bandwidth classes for an organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of Bandwidth Classs instances, Response, error)

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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            results = []
            for item in response.get_results():
                results.append(BandwidthClasses(self.form_response_body(item)))
        except Exception as exc:
            return (None, response, exc)

        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return (results, response, None)

    def list_classes_lite(self) -> tuple:
        """
        Fetches a specific bandwidth class lite by ID.

        Args:
            bwd_id (int): The unique identifier for the Bandwidth Class Lite.

        Returns:
            tuple: A tuple containing (Bandwidth Class instance, Response, error).

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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthClasses)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(BandwidthClasses(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_class(self, class_id: int) -> tuple:
        """
        Fetches a specific bandwidth class by ID.

        Args:
            class_id (int): The unique identifier for the Bandwidth Class.

        Returns:
            tuple: A tuple containing (Bandwidth Class instance, Response, error).

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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthClasses)
        if error:
            return (None, response, error)

        try:
            result = BandwidthClasses(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_class(self, **kwargs) -> tuple:
        """
        Creates a new ZIA Bandwidth Class.

        Keyword Args:
            name (str): Name of the bandwidth class
            web_applications (:obj:`list` of :obj:`str`): The web conferencing applications included in the bandwidth class.
            urls (:obj:`list` of :obj:`str`): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            url_categories (:obj:`list` of :obj:`str`): The URL categories to add to the bandwidth class

        Returns:
            tuple: A tuple containing the newly added Bandwidth Class, response, and error.

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

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthClasses)
        if error:
            return (None, response, error)

        try:
            result = BandwidthClasses(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_class(self, class_id: int, **kwargs) -> tuple:
        """
        Updates information for the specified ZIA Bandwidth Class.

        Args:
            class_id (int): The unique ID for the Bandwidth Class.

        Returns:
            tuple: A tuple containing the updated Bandwidth Class, response, and error.

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

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, BandwidthClasses)
        if error:
            return (None, response, error)

        try:
            result = BandwidthClasses(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_class(self, class_id: int) -> tuple:
        """
        Deletes the specified Bandwidth Class.

        Args:
            class_id (int): The unique identifier of the Bandwidth Class.

        Returns:
            tuple: A tuple containing the response object and error (if any).

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

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
