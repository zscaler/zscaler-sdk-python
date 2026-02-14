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
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.api_client import APIClient
from zscaler.zia.models.custom_file_types import CustomFileTypes
from zscaler.types import APIResult


class CustomFileTypesAPI(APIClient):

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_custom_file_types(
        self,
        query_params: Optional[dict] = None,
    ) -> APIResult[List[CustomFileTypes]]:
        """
        Retrieves the list of Custom file types can be configured as rule conditions in different ZIA policies.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.page]`` {int}: Specifies the page offset
                ``[query_params.page_size]`` {int}: Specifies the page size. Default value: 250

        Returns:
            tuple: A tuple containing (list of custom file types instances, Response, error).

        Example:
            List all custom file types with a specific page size:

            >>> files_list, response, error = zia.custom_file_types.list_custom_file_types(
            ...    query_params={"page_size": 50}
            ... )
            >>> for file in files_list:
            ...    print(file.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /customFileTypes
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CustomFileTypes(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_custom_file_tytpe(
        self,
        file_id: int,
    ) -> APIResult[dict]:
        """
        Retrieves information about a custom file type based on the specified ID

        Args:
            file_id (str): The unique identifier for the custom file types filter.

        Returns:
            tuple: A tuple containing (custom file types instance, Response, error).

        Example:
            Retrieve a custom file types by its ID:

            >>> file, response, error = zia.custom_file_types.get_custom_file_tytpe(file_id=123456)
            >>> if not error:
            ...    print(file.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /customFileTypes/{file_id}
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CustomFileTypes)

        if error:
            return (None, response, error)

        try:
            result = CustomFileTypes(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_custom_file_type(
        self,
        **kwargs,
    ) -> APIResult[dict]:
        """
        Adds a new custom file type.

        Args:
            name (str): Custom file type name

        Keyword Args:
            name (str): Custom file type name
            description (str): Additional information about the custom file type, if any.

            extension (str): Specifies the file type extension.
                The maximum extension length is 10 characters.
                Existing Zscaler extensions cannot be added to custom file types.

            file_type_id (int): File type ID.
                This ID is assigned and maintained for all file types including predefined and custom file types
                and this value is different from the custom file type ID.

        Returns:
            tuple: new custom file type resource record.

        Example:
            add an a new custom file type:

            >>> zia.custom_file_types.add_custom_file_type(
            ...    name='FileType02',
            ...    description='FileType02',
            ...    extension='tf'
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /customFileTypes
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

        response, error = self._request_executor.execute(request, CustomFileTypes)
        if error:
            return (None, response, error)

        try:
            result = CustomFileTypes(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_custom_file_type(self, file_id: int, **kwargs) -> APIResult[dict]:
        """
        Updates information for a custom file type based on the specified ID

        Args:
            file_id (int): The unique ID for the custom file type that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): Custom file type name
            description (str): Additional information about the custom file type, if any.

            extension (str): Specifies the file type extension.
                The maximum extension length is 10 characters.
                Existing Zscaler extensions cannot be added to custom file types.

            file_type_id (int): File type ID.
                This ID is assigned and maintained for all file types including predefined and custom file types
                and this value is different from the custom file type ID.

        Returns:
            tuple: update an existing custom file type resource record.

        Example:
            Update an existing custom file type to change its name and action:

            >>> zia.custom_file_types.update_custom_file_type(
            ...    file_id=123456,
            ...    name='FileType02',
            ...    description='FileType02',
            ...    extension='tf'
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /customFileTypes/{file_id}
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

        response, error = self._request_executor.execute(request, CustomFileTypes)
        if error:
            return (None, response, error)

        try:
            result = CustomFileTypes(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_custom_file_type(self, file_id: int) -> APIResult[dict]:
        """
        Deletes a custom file type based on the specified ID

        Args:
            file_id (int): The unique identifier for the custom file types

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.custom_file_types.delete_custom_file_type('278454')

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /customFileTypes/{file_id}
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

    def get_custom_file_type_count(self) -> APIResult[int]:
        """
        Retrieves the count of custom file types available.
        The API returns a scalar (e.g. 1); this method returns it as an int.

        Returns:
            tuple: A tuple containing (count of custom file types as int, Response, error).

        Examples:
            Retrieve the custom file type count (returns int)::

                >>> count, response, error = zia.custom_file_types.get_custom_file_type_count()
                >>> if not error:
                ...     print(f"Custom file types count: {count}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /customFileTypes/count
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            body = response.get_body()
            if isinstance(body, dict) and "count" in body:
                result = int(body["count"])
            elif isinstance(body, (int, float)):
                result = int(body)
            elif isinstance(body, str):
                result = int(body)
            else:
                result = int(body) if body is not None else 0
        except (TypeError, ValueError) as err:
            return (None, response, err)
        return (result, response, None)
