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

from zscaler.aiguard.models.llm_provider_credentials import LlmProviderCredentials
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url


class LLMProviderCredentialsAPI(APIClient):
    """
    A Client object for the AI Guard LLM Provider Credentials resource.
    """

    _aiguard_base_endpoint = "/aiguard/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_credentials(self, query_params: Optional[dict] = None) -> APIResult[List[LlmProviderCredentials]]:
        """
        Lists the LLM provider credentials configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of LlmProviderCredentials instances, Response, error)

        Examples:
            List LLM provider credentials:

            >>> credential_list, _, error = client.aiguard.llm_provider_credentials.list_credentials()
            >>> if error:
            ...     print(f"Error listing LLM provider credentials: {error}")
            ...     return
            ... print(f"Total LLM provider credentials found: {len(credential_list)}")
            ... for credential in credential_list:
            ...     print(credential.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-credentials
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
                result.append(LlmProviderCredentials(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_credential(self, credential_id: int) -> APIResult[LlmProviderCredentials]:
        """
        Fetches a specific LLM provider credential by ID.

        Args:
            credential_id (int): The unique identifier for the LLM provider credential.

        Returns:
            tuple: A tuple containing (LlmProviderCredentials instance, Response, error).

        Examples:
            Print a specific LLM provider credential:

            >>> fetched_credential, _, error = client.aiguard.llm_provider_credentials.get_credential(1013)
            >>> if error:
            ...     print(f"Error fetching LLM provider credential by ID: {error}")
            ...     return
            ... print(f"Fetched LLM provider credential by ID: {fetched_credential.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-credentials/{credential_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviderCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmProviderCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_credential_by_name(self, name: str) -> APIResult[LlmProviderCredentials]:
        """
        Fetches a specific LLM provider credential by name.

        Args:
            name (str): The name of the LLM provider credential.

        Returns:
            tuple: A tuple containing (LlmProviderCredentials instance, Response, error).

        Examples:
            Print a specific LLM provider credential by name:

            >>> fetched_credential, _, error = client.aiguard.llm_provider_credentials.get_credential_by_name('Credential01')
            >>> if error:
            ...     print(f"Error fetching LLM provider credential by name: {error}")
            ...     return
            ... print(f"Fetched LLM provider credential by name: {fetched_credential.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-credentials/name/{name}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviderCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmProviderCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    # NOTE: The referential-check endpoint is currently returning HTTP 404 for every
    # resource type, including via Postman with a known-good id. The method is
    # commented out until the API supports it; re-enable once the endpoint is live.
    # def referential_check(self, credential_id: int) -> APIResult[dict]:
    #     """
    #     Performs a referential check for the specified LLM provider credential, returning the resources that reference it.
    #
    #     Args:
    #         credential_id (int): The unique identifier for the LLM provider credential.
    #
    #     Returns:
    #         tuple: A tuple containing (the raw response value, Response, error).
    #
    #     Examples:
    #         >>> result, _, error = client.aiguard.llm_provider_credentials.referential_check(1013)
    #         >>> if error:
    #         ...     print(f"Error calling referential_check: {error}")
    #         ...     return
    #         ... print(f"Result: {result}")
    #     """
    #     http_method = "get".upper()
    #     api_url = format_url(f"""
    #         {self._aiguard_base_endpoint}
    #         /llm-provider-credentials/{credential_id}/referential-check
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

    def add_credential(self, **kwargs) -> APIResult[LlmProviderCredentials]:
        """
        Creates a new LLM provider credential.

        Args:
            name (str): The name of the LLM provider credential.
            **kwargs: Optional keyword args.

        Keyword Args:
            provider_id (str): The provider id for this LLM provider credential.
            expire_time_millis (str): The expire time millis for this LLM provider credential.
            api_credentials (str): The api credentials for this LLM provider credential.

        Returns:
            tuple: A tuple containing the newly added LlmProviderCredentials instance, response, and error.

        Examples:
            Add a new LLM provider credential. ``providerId`` must reference an existing
            provider -- resolve it with :meth:`~zscaler.aiguard.llm_providers.LlmProvidersAPI.get_provider_by_name`:

            >>> provider, _, error = client.aiguard.llm_providers.get_provider_by_name("Default Anthropic Provider")
            >>> added_credential, _, error = client.aiguard.llm_provider_credentials.add_credential(
            ...     name="Anthropic_API02",
            ...     providerId=provider.id,
            ...     apiCredentials={"type": "API_KEY", "key": "<provider api key>"},
            ... )
            >>> if error:
            ...     print(f"Error adding LLM provider credential: {error}")
            ...     return
            ... print(f"LLM provider credential added successfully: {added_credential.as_dict()}")

            Note:
                ``apiCredentials`` is write-only and is never returned in responses. Valid
                ``type`` values are API_KEY, BEARER, CROSS_ACCOUNT_ROLE, ACCESS_KEY and
                TRANSPARENT. ``expireTimeMillis`` is optional -- omit it for credentials
                that do not expire.
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-credentials
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviderCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmProviderCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_credential(self, credential_id: int, **kwargs) -> APIResult[LlmProviderCredentials]:
        """
        Updates information for the specified LLM provider credential.

        Args:
            credential_id (int): The unique identifier for the LLM provider credential.

        Keyword Args:
            name (str): The name of the LLM provider credential.
            provider_id (str): The provider id for this LLM provider credential.
            expire_time_millis (str): The expire time millis for this LLM provider credential.
            api_credentials (str): The api credentials for this LLM provider credential.

        Returns:
            tuple: A tuple containing the updated LlmProviderCredentials instance, response, and error.

        Examples:
            Update an existing LLM provider credential:

            >>> updated_credential, _, error = client.aiguard.llm_provider_credentials.update_credential(
            ...     credential_id=739,
            ...     name="Anthropic_API02_Updated",
            ...     providerId=6099,
            ...     apiCredentials={"type": "API_KEY", "key": "<provider api key>"},
            ... )
            >>> if error:
            ...     print(f"Error updating LLM provider credential: {error}")
            ...     return
            ... print(f"LLM provider credential updated successfully: {updated_credential.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-credentials/{credential_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LlmProviderCredentials)
        if error:
            return (None, response, error)

        try:
            result = LlmProviderCredentials(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_credential(self, credential_id: int) -> APIResult[None]:
        """
        Deletes the specified LLM provider credential.

        Args:
            credential_id (int): The unique identifier for the LLM provider credential.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a LLM provider credential:

            >>> _, _, error = client.aiguard.llm_provider_credentials.delete_credential(1013)
            >>> if error:
            ...     print(f"Error deleting LLM provider credential: {error}")
            ...     return
            ... print(f"Llm provider credential deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /llm-provider-credentials/{credential_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
