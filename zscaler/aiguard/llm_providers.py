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

from typing import List, Optional

from zscaler.aiguard.models.llm_providers import LlmProviders
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url


class LLMProvidersAPI(APIClient):
    """
    A Client object for the AI Guard LLM Providers resource.
    """

    _aiguard_base_endpoint = "/aiguard/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_providers(self, query_params: Optional[dict] = None) -> APIResult[List[LlmProviders]]:
        """
        Lists the LLM providers configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of LlmProviders instances, Response, error)

        Examples:
            List LLM providers:

            >>> provider_list, _, error = client.aiguard.llm_providers.list_providers()
            >>> if error:
            ...     print(f"Error listing LLM providers: {error}")
            ...     return
            ... print(f"Total LLM providers found: {len(provider_list)}")
            ... for provider in provider_list:
            ...     print(provider.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-providers
        """)

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
                result.append(LlmProviders(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_provider(self, provider_id: int) -> APIResult[LlmProviders]:
        """
        Fetches a specific LLM provider by ID.

        Args:
            provider_id (int): The unique identifier for the LLM provider.

        Returns:
            tuple: A tuple containing (LlmProviders instance, Response, error).

        Examples:
            Print a specific LLM provider:

            >>> fetched_provider, _, error = client.aiguard.llm_providers.get_provider(1013)
            >>> if error:
            ...     print(f"Error fetching LLM provider by ID: {error}")
            ...     return
            ... print(f"Fetched LLM provider by ID: {fetched_provider.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-providers/{provider_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviders)
        if error:
            return (None, response, error)

        try:
            result = LlmProviders(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_provider_by_name(self, name: str) -> APIResult[LlmProviders]:
        """
        Fetches a specific LLM provider by name.

        Args:
            name (str): The name of the LLM provider.

        Returns:
            tuple: A tuple containing (LlmProviders instance, Response, error).

        Examples:
            Print a specific LLM provider by name:

            >>> fetched_provider, _, error = client.aiguard.llm_providers.get_provider_by_name('Provider01')
            >>> if error:
            ...     print(f"Error fetching LLM provider by name: {error}")
            ...     return
            ... print(f"Fetched LLM provider by name: {fetched_provider.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-providers/name/{name}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviders)
        if error:
            return (None, response, error)

        try:
            result = LlmProviders(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    # NOTE: The referential-check endpoint is currently returning HTTP 404 for every
    # resource type, including via Postman with a known-good id. The method is
    # commented out until the API supports it; re-enable once the endpoint is live.
    # def referential_check(self, provider_id: int) -> APIResult[dict]:
    #     """
    #     Performs a referential check for the specified LLM provider, returning the resources that reference it (e.g. credentials, applications, rules).
    #
    #     Args:
    #         provider_id (int): The unique identifier for the LLM provider.
    #
    #     Returns:
    #         tuple: A tuple containing (the raw response value, Response, error).
    #
    #     Examples:
    #         >>> result, _, error = client.aiguard.llm_providers.referential_check(1013)
    #         >>> if error:
    #         ...     print(f"Error calling referential_check: {error}")
    #         ...     return
    #         ... print(f"Result: {result}")
    #     """
    #     http_method = "get".upper()
    #     api_url = format_url(f"""
    #         {self._aiguard_base_endpoint}
    #         /llm-providers/{provider_id}/referential-check
    #     """)
    #
    #     body = {}
    #     headers = {}
    #
    #     request, error = self._request_executor.create_request(http_method, api_url, body, headers)
    #
    #     if error:
    #         return (None, None, error)
    #
    #     response, error = self._request_executor.execute(request)
    #     if error:
    #         return (None, response, error)
    #
    #     try:
    #         result = self.form_response_body(response.get_body())
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)

    def list_provider_types(self, query_params: Optional[dict] = None) -> APIResult[list]:
        """
        Lists the LLM provider types supported by AI Guard.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of LLM providers, Response, error)

        Examples:
            List LLM providers:

            >>> provider_list, _, error = client.aiguard.llm_providers.list_provider_types()
            >>> if error:
            ...     print(f"Error listing LLM providers: {error}")
            ...     return
            ... print(f"Total LLM providers found: {len(provider_list)}")
            ... for provider in provider_list:
            ...     print(provider.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-types
        """)

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
            result = response.get_results()
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_provider_type(self, provider_type: str) -> APIResult[dict]:
        """
        Fetches details for a specific LLM provider type.

        Args:
            provider_type (str): The LLM provider type (e.g. ``OPENAI``).

        Returns:
            tuple: A tuple containing (the raw response value, Response, error).

        Examples:
            >>> result, _, error = client.aiguard.llm_providers.get_provider_type('OPENAI')
            >>> if error:
            ...     print(f"Error calling get_provider_type: {error}")
            ...     return
            ... print(f"Result: {result}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-types/{provider_type}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_provider(self, **kwargs) -> APIResult[LlmProviders]:
        """
        Creates a new LLM provider.

        Args:
            name (str): The name of the LLM provider.
            **kwargs: Optional keyword args.

        Keyword Args:
            type (str): The type for this LLM provider.
            public (str): The public for this LLM provider.

        Returns:
            tuple: A tuple containing the newly added LlmProviders instance, response, and error.

        Examples:
            Add a new public LLM provider:

            >>> added_provider, _, error = client.aiguard.llm_providers.add_provider(
            ...     name="BDAnthropic",
            ...     type="xai",
            ...     public=True,
            ... )
            >>> if error:
            ...     print(f"Error adding LLM provider: {error}")
            ...     return
            ... print(f"LLM provider added successfully: {added_provider.as_dict()}")

            Note:
                A private provider (``public=False``) additionally requires a ``servers``
                payload. Use :meth:`list_provider_types` to discover the supported values
                for ``type``.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-providers
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviders)
        if error:
            return (None, response, error)

        try:
            result = LlmProviders(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_provider(self, provider_id: int, **kwargs) -> APIResult[LlmProviders]:
        """
        Updates information for the specified LLM provider.

        Args:
            provider_id (int): The unique identifier for the LLM provider.

        Keyword Args:
            name (str): The name of the LLM provider.
            type (str): The type for this LLM provider.
            public (str): The public for this LLM provider.

        Returns:
            tuple: A tuple containing the updated LlmProviders instance, response, and error.

        Examples:
            Update an existing LLM provider:

            >>> updated_provider, _, error = client.aiguard.llm_providers.update_provider(
            ...     provider_id=29103,
            ...     name="BDAnthropic_Updated",
            ...     type="xai",
            ...     public=False,
            ... )
            >>> if error:
            ...     print(f"Error updating LLM provider: {error}")
            ...     return
            ... print(f"LLM provider updated successfully: {updated_provider.as_dict()}")

            Note:
                Public providers are not editable -- the API rejects the update with
                "A public provider is not editable."
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-providers/{provider_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviders)
        if error:
            return (None, response, error)

        try:
            result = LlmProviders(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_provider(self, provider_id: int) -> APIResult[None]:
        """
        Deletes the specified LLM provider.

        Args:
            provider_id (int): The unique identifier for the LLM provider.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a LLM provider:

            >>> _, _, error = client.aiguard.llm_providers.delete_provider(1013)
            >>> if error:
            ...     print(f"Error deleting LLM provider: {error}")
            ...     return
            ... print(f"Llm provider deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-providers/{provider_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
